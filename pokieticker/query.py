#!/usr/bin/env python3
"""
PokieTicker 数据库查询工具

用法:
    python query.py AAPL 2026-03-03
    python query.py NVDA "yesterday"
    python query.py TSLA "last Friday"
"""

import sys
import sqlite3
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 数据库路径
DB_PATH = Path("/Users/colin/Desktop/File/PokieTicker-main/pokieticker.db")


def parse_relative_date(date_str: str) -> str:
    """解析相对日期为 YYYY-MM-DD 格式"""
    date_str = date_str.lower().strip()

    today = datetime.now().date()

    if "yesterday" in date_str or "昨天" in date_str:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "today" in date_str or "今天" in date_str:
        return today.strftime("%Y-%m-%d")
    elif "tomorrow" in date_str or "明天" in date_str:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    # 简单的 "last Friday" 之类处理
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(weekdays):
        if day in date_str:
            # 找到最近的那个工作日
            target_weekday = i
            days_ago = (today.weekday() - target_weekday) % 7
            if days_ago == 0:
                days_ago = 7  # 如果是今天，找上周的
            return (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")

    # 尝试解析为具体日期
    try:
        # 支持 2026-03-03, 2026/03/03, Mar 3 等格式
        for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%b %d", "%B %d", "%m-%d"]:
            try:
                parsed = datetime.strptime(date_str, fmt)
                if fmt in ["%b %d", "%B %d", "%m-%d"]:
                    # 没有年份，使用当年
                    parsed = parsed.replace(year=today.year)
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                continue
    except Exception:
        pass

    return date_str  # 返回原样，让数据库处理


def get_stock_data(conn: sqlite3.Connection, symbol: str, date: str) -> dict:
    """获取指定日期的 OHLC 数据"""
    cursor = conn.cursor()

    # 先查询精确匹配
    cursor.execute(
        """
        SELECT date, open, high, low, close, volume
        FROM ohlc
        WHERE symbol = ? AND date = ?
    """,
        (symbol.upper(), date),
    )
    row = cursor.fetchone()

    # 如果没有，查询最接近的日期
    if not row:
        cursor.execute(
            """
            SELECT date, open, high, low, close, volume
            FROM ohlc
            WHERE symbol = ?
            ORDER BY ABS(julianday(date) - julianday(?))
            LIMIT 1
        """,
            (symbol.upper(), date),
        )
        row = cursor.fetchone()

    if row:
        return {
            "date": row[0],
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
            "volume": row[5],
            "change_pct": ((row[4] - row[1]) / row[1] * 100) if row[1] else 0,
        }
    return None


def get_news_for_date(
    conn: sqlite3.Connection, symbol: str, date: str, days_range: int = 3
) -> list:
    """获取指定日期前后的新闻"""
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            nr.title,
            nr.description,
            nr.publisher,
            nr.published_utc,
            l1.sentiment,
            l1.reason_growth,
            l1.reason_decrease,
            l1.key_discussion
        FROM news_aligned na
        JOIN news_raw nr ON na.news_id = nr.id
        LEFT JOIN layer1_results l1 ON na.news_id = l1.news_id AND na.symbol = l1.symbol
        WHERE na.symbol = ?
          AND na.trade_date BETWEEN DATE(?, '-{} days') AND DATE(?, '+{} days')
        ORDER BY na.published_utc
    """.format(
            days_range, days_range
        ),
        (symbol.upper(), date, date),
    )

    news = []
    for row in cursor.fetchall():
        news.append(
            {
                "title": row[0],
                "description": row[1],
                "publisher": row[2],
                "published_utc": row[3],
                "sentiment": row[4],
                "reason_growth": row[5],
                "reason_decrease": row[6],
                "key_discussion": row[7],
            }
        )
    return news


def list_available_symbols(conn: sqlite3.Connection, search: str = "") -> list:
    """列出可用的股票代码"""
    cursor = conn.cursor()
    if search:
        cursor.execute(
            "SELECT symbol, name FROM tickers WHERE symbol LIKE ? OR name LIKE ? LIMIT 10",
            (f"%{search}%", f"%{search}%"),
        )
    else:
        cursor.execute("SELECT symbol, name FROM tickers LIMIT 20")
    return [{"symbol": row[0], "name": row[1]} for row in cursor.fetchall()]


def format_analysis(symbol: str, stock_data: dict, news: list) -> str:
    """格式化分析结果"""
    if not stock_data:
        return f"❌ 未找到 {symbol} 的数据"

    output = []
    output.append(f"## 📊 {symbol} - {stock_data['date']} 价格变动分析\n")
    output.append("### 价格表现")
    output.append(f"- 日期: {stock_data['date']}")
    output.append(f"- 开盘: ${stock_data['open']:.2f}")
    output.append(f"- 最高: ${stock_data['high']:.2f}")
    output.append(f"- 最低: ${stock_data['low']:.2f}")
    output.append(f"- 收盘: ${stock_data['close']:.2f}")
    output.append(f"- 涨跌幅: {stock_data['change_pct']:+.2f}%")
    output.append(f"- 成交量: {stock_data['volume']:,.0f}\n")

    if news:
        # 分类新闻
        positive = [n for n in news if n["sentiment"] == "positive"]
        negative = [n for n in news if n["sentiment"] == "negative"]
        neutral = [n for n in news if n["sentiment"] == "neutral"]

        output.append(f"### 📰 相关新闻 ({len(news)} 条)\n")

        if negative:
            output.append("**负面/利空因素**")
            for n in negative[:5]:
                reason = n["reason_decrease"] or "暂无分析"
                output.append(f"- [{n['publisher']}] {n['title']}")
                output.append(f"  理由: {reason[:100]}...")
            output.append("")

        if positive:
            output.append("**正面/利多因素**")
            for n in positive[:5]:
                reason = n["reason_growth"] or "暂无分析"
                output.append(f"- [{n['publisher']}] {n['title']}")
                output.append(f"  理由: {reason[:100]}...")
            output.append("")

        if neutral:
            output.append("**中性/其他**")
            for n in neutral[:3]:
                output.append(f"- [{n['publisher']}] {n['title']}")
            output.append("")

        # 主要原因总结
        output.append("### 💡 主要原因总结")
        if stock_data["change_pct"] < -2:
            output.append(f"当日 {symbol} 下跌 {abs(stock_data['change_pct']):.2f}%，主要因素：")
        elif stock_data["change_pct"] > 2:
            output.append(f"当日 {symbol} 上涨 {stock_data['change_pct']:.2f}%，主要因素：")
        else:
            output.append(f"当日 {symbol} 价格小幅波动 {stock_data['change_pct']:.2f}%，主要因素：")

        # 统计情感
        sentiment_counts = {"positive": len(positive), "negative": len(negative), "neutral": len(neutral)}
        dominant = max(sentiment_counts.items(), key=lambda x: x[1])[0]

        if dominant == "negative" and len(negative) > 0:
            output.append(f"- 利空消息占主导（{len(negative)}条负面新闻）")
            if negative[0]["reason_decrease"]:
                output.append(f"- 主要担忧: {negative[0]['reason_decrease'][:80]}...")
        elif dominant == "positive" and len(positive) > 0:
            output.append(f"- 利好消息占主导（{len(positive)}条正面新闻）")
            if positive[0]["reason_growth"]:
                output.append(f"- 主要利好: {positive[0]['reason_growth'][:80]}...")
        else:
            output.append("- 当天新闻情感偏中性，价格波动可能受技术面或大盘影响")

    else:
        output.append("### 📰 相关新闻")
        output.append(f"未找到 {stock_data['date']} 前后的相关新闻")
        output.append("可能原因：")
        output.append("- 该日期为非交易日或周末")
        output.append("- 数据库中暂无该时期的新闻数据")

    output.append("\n---")
    output.append("数据来源: PokieTicker 数据库 (Polygon.io + Claude AI 分析)")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="查询 PokieTicker 股票数据")
    parser.add_argument("symbol", help="股票代码 (如: AAPL, NVDA)")
    parser.add_argument("date", help="日期 (如: 2026-03-03, yesterday, last Friday)")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用股票")
    parser.add_argument("--search", "-s", help="搜索股票代码")

    args = parser.parse_args()

    if not DB_PATH.exists():
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        print("请先启动 PokieTicker 服务并确保数据库已初始化")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        if args.list or args.search:
            symbols = list_available_symbols(conn, args.search or "")
            print("可用股票代码:")
            for s in symbols:
                print(f"  {s['symbol']}: {s['name']}")
            return

        # 解析日期
        date = parse_relative_date(args.date)
        print(f"🔍 查询 {args.symbol.upper()} 在 {date} 的数据...\n")

        # 获取数据
        stock_data = get_stock_data(conn, args.symbol, date)
        news = get_news_for_date(conn, args.symbol, date)

        # 输出分析
        print(format_analysis(args.symbol.upper(), stock_data, news))

    finally:
        conn.close()


if __name__ == "__main__":
    main()
