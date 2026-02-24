#!/usr/bin/env python3
"""
美股盘前专业分析报告 v2.1
基于用户Role.md的专业要求
新增: 重要财经新闻 + 完整财经日历
"""
import yfinance as yf
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
import subprocess
import os
import json
from urllib.parse import quote

class ProfessionalReportGenerator:
    def __init__(self):
        self.holdings_stocks = ['TSLA', 'NVDA', 'GOOGL', 'MU', 'HOOD', 'RKLB', 'CRWD']
        self.holdings_crypto = ['BTC-USD', 'ETH-USD']
        self.today = datetime.now(pytz.UTC)

    def get_market_sentiment(self):
        """第一步：市场情绪雷达"""
        print("1️⃣ 市场情绪雷达")
        sentiment = {}

        # VIX
        vix_data = yf.Ticker('^VIX').history(period="1d")
        sentiment['vix'] = vix_data['Close'].iloc[-1] if not vix_data.empty else 20

        # 加密恐惧贪婪
        try:
            fg_req = requests.get("https://api.alternative.me/fng/", timeout=10)
            sentiment['crypto_fg'] = int(fg_req.json()['data'][0]['value'])
        except:
            sentiment['crypto_fg'] = 50

        # 10年期美债收益率
        try:
            tnx_data = yf.Ticker('^TNX').history(period="5d")
            if not tnx_data.empty:
                sentiment['treasury_10y'] = tnx_data['Close'].iloc[-1]
            else:
                sentiment['treasury_10y'] = 4.0
        except:
            sentiment['treasury_10y'] = 4.0

        # 综合评分
        score = (sentiment['crypto_fg'] + (100 - sentiment['vix'] * 2)) / 2
        sentiment['composite'] = int(score)

        if score < 40:
            sentiment['outlook'] = "恐惧"
        elif score < 60:
            sentiment['outlook'] = "中性"
        else:
            sentiment['outlook'] = "贪婪"

        print(f"   VIX: {sentiment['vix']:.2f}")
        print(f"   加密恐惧贪婪: {sentiment['crypto_fg']}")
        print(f"   美债收益率: {sentiment['treasury_10y']:.2f}%")
        print(f"   综合情绪: {sentiment['composite']}/100 ({sentiment['outlook']})")

        return sentiment

    def get_major_indices(self):
        """获取主要指数"""
        print("\n2️⃣ 主要市场指数")
        indices = {}

        for ticker, name in [('^GSPC', '标普500'), ('^IXIC', '纳斯达克'), ('^DJI', '道琼斯')]:
            data = yf.Ticker(ticker).history(period="1d")
            if not data.empty:
                price = data['Close'].iloc[-1]
                change_pct = ((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100
                indices[name] = {'price': round(price, 2), 'change_pct': round(change_pct, 2)}
                symbol = "📈" if change_pct >= 0 else "📉"
                print(f"   {name}: {price:.2f} ({change_pct:+.2f}%) {symbol}")

        return indices

    def get_crypto_data(self):
        """获取加密货币数据"""
        print("\n加密货币:")
        crypto = {}

        for ticker in self.holdings_crypto:
            try:
                data = yf.Ticker(ticker).history(period="1d")
                if not data.empty:
                    price = data['Close'].iloc[-1]
                    change_pct = ((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100
                    name = ticker.replace('-USD', '')
                    crypto[name] = {'price': round(price, 2), 'change_pct': round(change_pct, 2)}
                    symbol = "📈" if change_pct >= 0 else "📉"
                    print(f"   {name}: ${price:.2f} ({change_pct:+.2f}%) {symbol}")
            except:
                pass

        return crypto

    def get_important_news(self):
        """第二步：专业信源采集 - 从Google News RSS获取重要财经新闻"""
        print("\n3️⃣ 重要财经新闻采集")

        # 构建搜索查询 - 需要URL编码
        query = quote(' OR '.join(self.holdings_stocks))
        rss_url = f"https://news.google.com/rss/search?q={query}+stock&hl=en-US&gl=US&ceid=US:en"

        news_items = []

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(rss_url, headers=headers, timeout=10)

            if response.status_code != 200:
                print(f"   新闻获取失败: HTTP {response.status_code}")
                return []

            # 解析XML
            root = ET.fromstring(response.content)

            now = datetime.now(pytz.UTC)

            # 遍历所有item
            for item in root.findall('.//item'):
                try:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    pub_date_elem = item.find('pubDate')
                    source_elem = item.find('source')

                    if title_elem is None or title_elem.text is None:
                        continue

                    title = title_elem.text
                    link = link_elem.text if link_elem is not None else ''

                    # 解析发布时间
                    if pub_date_elem is not None and pub_date_elem.text:
                        try:
                            pub_date = datetime.strptime(pub_date_elem.text, '%a, %d %b %Y %H:%M:%S %Z')
                            pub_date = pub_date.replace(tzinfo=pytz.UTC)
                        except:
                            pub_date = now - timedelta(hours=1)
                    else:
                        pub_date = now - timedelta(hours=1)

                    hours_ago = int((now - pub_date).total_seconds() / 3600)

                    # 只显示最近48小时的新闻
                    if hours_ago > 48:
                        continue

                    # 确定相关股票
                    related_stocks = []
                    title_upper = title.upper()
                    for stock in self.holdings_stocks:
                        if stock in title_upper:
                            related_stocks.append(stock)

                    if not related_stocks:
                        continue

                    # 判断影响程度
                    high_keywords = ['earnings', 'revenue', 'profit', 'loss', 'guidance', 'layoff',
                                   'acquisition', 'merger', 'sec', 'investigation', 'lawsuit',
                                   '财报', '营收', '利润', '收购', '裁员', '调查']
                    medium_keywords = ['launch', 'product', 'partnership', 'deal', 'analyst',
                                     'upgrade', 'downgrade', 'target', 'forecast',
                                     '发布', '合作', '分析师', '评级', '目标价']

                    title_lower = title.lower()
                    if any(k in title_lower for k in high_keywords):
                        impact = "高"
                    elif any(k in title_lower for k in medium_keywords):
                        impact = "中"
                    else:
                        impact = "低"

                    # 提取来源
                    if source_elem is not None and source_elem.text:
                        publisher = source_elem.text
                    else:
                        # 从link中提取域名
                        if 'reuters.com' in link:
                            publisher = 'Reuters'
                        elif 'bloomberg.com' in link:
                            publisher = 'Bloomberg'
                        elif 'wsj.com' in link:
                            publisher = 'WSJ'
                        elif 'cnbc.com' in link:
                            publisher = 'CNBC'
                        elif 'seekingalpha.com' in link:
                            publisher = 'Seeking Alpha'
                        elif 'yahoo.com' in link:
                            publisher = 'Yahoo Finance'
                        else:
                            publisher = 'News'

                    news_items.append({
                        'ticker': related_stocks[0],  # 主相关股票
                        'title': title,
                        'publisher': publisher,
                        'link': link,
                        'impact': impact,
                        'related': related_stocks,
                        'hours_ago': hours_ago,
                        'time': f"{hours_ago}小时前" if hours_ago > 0 else "刚刚"
                    })

                except Exception as e:
                    continue

            # 按影响程度和时间排序
            impact_order = {'高': 0, '中': 1, '低': 2}
            news_items.sort(key=lambda x: (impact_order.get(x['impact'], 3), x['hours_ago']))

            print(f"   采集到 {len(news_items)} 条相关新闻")
            for item in news_items[:5]:
                print(f"   [{item['impact']}] {item['time']} - {item['title'][:50]}...")

            return news_items

        except Exception as e:
            print(f"   新闻获取失败: {e}")
            return []

    def get_economic_calendar(self):
        """第二步：完整财经日历
        包括FOMC会议、重要经济数据发布等
        """
        print("\n4️⃣ 财经日历")
        events = []

        # 已知的重要财经事件（根据2026年日历）
        known_events = [
            {
                'date': '2026-02-25',
                'event': 'NVDA财报',
                'impact': '高',
                'related': ['NVDA']
            },
            {
                'date': '2026-02-26',
                'event': 'RKLB财报',
                'impact': '中',
                'related': ['RKLB']
            },
            {
                'date': '2026-02-28',
                'event': '美联储主席鲍威尔讲话',
                'impact': '高',
                'related': ['ALL']
            },
            {
                'date': '2026-03-03',
                'event': 'CRWD财报',
                'impact': '中',
                'related': ['CRWD']
            },
            {
                'date': '2026-03-05',
                'event': '非农就业数据',
                'impact': '高',
                'related': ['ALL']
            },
            {
                'date': '2026-03-12',
                'event': 'CPI通胀数据',
                'impact': '高',
                'related': ['ALL']
            },
            {
                'date': '2026-03-18',
                'event': 'FOMC利率决议',
                'impact': '高',
                'related': ['ALL']
            }
        ]

        for event in known_events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').replace(tzinfo=pytz.UTC)
            days_until = (event_date - self.today).days

            if 0 <= days_until <= 30:
                events.append({
                    'date': event['date'],
                    'event': event['event'],
                    'impact': event['impact'],
                    'days_until': days_until,
                    'related': event['related']
                })

        # 按日期排序
        events.sort(key=lambda x: x['days_until'])

        print(f"   未来30天有 {len(events)} 个重要事件")
        for event in events[:5]:
            print(f"   {event['date']}: {event['event']} (还有{event['days_until']}天)")

        return events

    def analyze_stocks(self):
        """第三步：个股深度扫描"""
        print("\n5️⃣ 持仓个股分析")
        analyses = {}
        earnings_calendar = []

        for ticker in self.holdings_stocks:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period="1y")

                if hist.empty:
                    continue

                price = hist['Close'].iloc[-1]
                change = price - hist['Close'].iloc[-2]
                change_pct = (change / hist['Close'].iloc[-2]) * 100

                # 200日均线
                ma200 = hist['Close'].rolling(200).mean().iloc[-1]
                above_ma200 = price > ma200

                # 52周位置
                week_52_high = info.get('fiftyTwoWeekHigh', 0)
                week_52_low = info.get('fiftyTwoWeekLow', 0)
                if week_52_high > week_52_low:
                    position_52w = ((price - week_52_low) / (week_52_high - week_52_low)) * 100
                else:
                    position_52w = 50

                # 成交量
                volume = int(hist['Volume'].iloc[-1])
                avg_volume = info.get('averageVolume', volume)
                volume_ratio = volume / avg_volume if avg_volume > 0 else 1

                # 分析师评级
                rec = info.get('recommendationKey', 'N/A')
                target_price = info.get('targetMeanPrice', 0)

                # PE
                pe = info.get('trailingPE', 0)

                # 财报
                earnings_ts = info.get('earningsTimestamp')
                if earnings_ts:
                    earnings_date = datetime.fromtimestamp(int(earnings_ts), tz=pytz.UTC)
                    days_until = (earnings_date - self.today).days
                    if 0 <= days_until <= 30:
                        earnings_calendar.append({
                            'ticker': ticker,
                            'date': earnings_date.strftime('%Y-%m-%d'),
                            'days': days_until
                        })

                analyses[ticker] = {
                    'price': round(price, 2),
                    'change': round(change, 2),
                    'change_pct': round(change_pct, 2),
                    'ma200': round(ma200, 2) if not ma200 != ma200 else 0,
                    'above_ma200': above_ma200,
                    'position_52w': round(position_52w, 1),
                    'volume': volume,
                    'volume_ratio': round(volume_ratio, 2),
                    'pe': round(pe, 2) if pe else 0,
                    'rec': rec,
                    'target': round(target_price, 2) if target_price else 0
                }

                # 输出
                symbol = "🟢" if change_pct >= 0 else "🔴"
                ma_status = "高于" if above_ma200 else "低于"
                vol_status = "放量" if volume_ratio > 1.3 else ("缩量" if volume_ratio < 0.7 else "正常")

                print(f"   {ticker}: ${price:.2f} ({change_pct:+.2f}%) {symbol}")
                print(f"      200日均线: {ma_status} | 52周位置: {position_52w:.1f}% | PE: {pe:.1f}")
                print(f"      成交量: {vol_status}({volume_ratio:.2f}x) | 评级: {rec}")

            except Exception as e:
                print(f"   {ticker}: 数据获取失败 - {e}")

        return analyses, earnings_calendar

    def generate_recommendations(self, sentiment, analyses, earnings, news, economic_events):
        """第四步：操作建议逻辑（考虑新闻和事件）"""
        print("\n6️⃣ 每日操作策略")

        # 环境判断
        print("\n   环境判断:")
        if sentiment['composite'] < 40:
            env = "偏空，适度控制仓位"
            position = "30-50%"
        elif sentiment['composite'] < 60:
            env = "中性，正常参与"
            position = "50-70%"
        else:
            env = "偏多，警惕回调"
            position = "40-60%"

        print(f"   宏观环境: {env}")
        print(f"   建议仓位: {position}")

        # 个股建议
        print("\n   个股操作建议:")
        recommendations = {}

        for ticker, data in analyses.items():
            # 检查是否有即将到来的财报
            upcoming_earnings = [e for e in earnings if e['ticker'] == ticker and e['days'] <= 7]

            # 检查相关新闻
            ticker_news = [n for n in news if n['ticker'] == ticker or ticker in n.get('related', [])]
            high_impact_news = [n for n in ticker_news if n['impact'] == '高']

            # 检查相关经济事件
            related_events = [e for e in economic_events if ticker in e.get('related', ['ALL']) and e['days_until'] <= 7]

            # CoT推理
            if high_impact_news:
                action = "关注新闻"
                reason = f"有重要新闻: {high_impact_news[0]['title'][:40]}..."
                risk = "高"
            elif upcoming_earnings:
                action = "财报前谨慎"
                reason = f"未来{upcoming_earnings[0]['days']}天有财报，注意波动"
                risk = "高"
            elif related_events:
                action = "注意风险"
                reason = f"临近{related_events[0]['event']}，市场波动可能加大"
                risk = "中"
            elif not data['above_ma200'] and data['change_pct'] < -3:
                action = "关注支撑"
                reason = "跌破200日均线且跌幅较大，等待企稳"
                risk = "中"
            elif data['position_52w'] > 85 and data['change_pct'] > 3:
                action = "考虑减仓"
                reason = "接近52周高位且大涨，注意回调风险"
                risk = "中"
            elif data['change_pct'] > 5:
                action = "持有观望"
                reason = "涨幅较大，不建议追高"
                risk = "低"
            elif data['change_pct'] < -5:
                action = "关注反弹"
                reason = "跌幅较大，可能超跌，等待企稳信号"
                risk = "中"
            else:
                action = "继续持有"
                reason = "波动正常，继续观察"
                risk = "低"

            recommendations[ticker] = {
                'action': action,
                'reason': reason,
                'risk': risk
            }

            risk_emoji = "🔴" if risk == "高" else "🟡" if risk == "中" else "🟢"
            print(f"   {ticker}: {action} {risk_emoji}")
            print(f"      理由: {reason}")

        return recommendations

    def generate_html_report(self, sentiment, indices, crypto, analyses, earnings, recommendations, news, economic_events):
        """生成HTML报告（v2.1 - 包含新闻和完整日历）"""
        report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>美股盘前专业分析报告 v2.2</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #e0e0e0;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 2px solid rgba(255,255,255,0.1);
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.8em;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        .section {{
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }}
        .section-title {{
            font-size: 1.8em;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .sentiment-box {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .sentiment-item {{
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        .sentiment-value {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }}
        .card {{
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }}
        .positive {{ color: #2ed573; }}
        .negative {{ color: #ff4757; }}
        .stock-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 20px; }}
        .stock-card {{
            background: rgba(0,0,0,0.2);
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid #00d2ff;
        }}
        .stock-card.warning {{ border-left-color: #ff6b6b; }}
        .stock-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
        .stock-ticker {{ font-size: 1.5em; font-weight: bold; }}
        .stock-price {{ font-size: 2em; font-weight: bold; color: #00d2ff; }}
        .stock-metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 15px 0; font-size: 0.9em; color: #aaa; }}
        .news-item {{
            background: rgba(0,0,0,0.2);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 12px;
            border-left: 3px solid #00d2ff;
        }}
        .news-item.high-impact {{ border-left-color: #ff6b6b; }}
        .news-item.medium-impact {{ border-left-color: #ffd93d; }}
        .news-header {{ display: flex; justify-content: space-between; margin-bottom: 8px; }}
        .news-impact {{ padding: 3px 10px; border-radius: 12px; font-size: 0.8em; }}
        .impact-high {{ background: rgba(255,107,107,0.3); color: #ff6b6b; }}
        .impact-medium {{ background: rgba(255,217,61,0.3); color: #ffd93d; }}
        .impact-low {{ background: rgba(46,213,115,0.3); color: #6bcb77; }}
        .news-title {{ color: #e0e0e0; margin-bottom: 5px; }}
        .news-source {{ font-size: 0.85em; color: #888; }}
        .earnings-alert {{
            background: rgba(255,107,107,0.1);
            border: 2px solid #ff6b6b;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .earnings-item {{ padding: 12px; background: rgba(0,0,0,0.2); border-radius: 8px; margin-bottom: 8px; }}
        .economic-item {{ padding: 15px; background: rgba(0,0,0,0.2); border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #ffd93d; }}
        .action-item {{
            background: rgba(0,210,255,0.1);
            border: 2px solid #00d2ff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        .action-item.sell {{ border-color: #ff6b6b; background: rgba(255,107,107,0.1); }}
        .risk-high {{ color: #ff6b6b; }}
        .risk-medium {{ color: #ffd93d; }}
        .risk-low {{ color: #6bcb77; }}
        .footer {{ text-align: center; padding: 30px; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 美股盘前专业分析报告 v2.1</h1>
            <p style="color: #888;">{report_date}</p>
        </div>

        <!-- 市场情绪 -->
        <div class="section">
            <div class="section-title">🎯 市场情绪总览</div>
            <div class="sentiment-box">
                <div class="sentiment-item">
                    <h3>VIX波动率</h3>
                    <div class="sentiment-value">{sentiment['vix']:.2f}</div>
                    <div style="font-size: 0.9em; color: #888;">{'正常' if sentiment['vix'] < 20 else '偏高' if sentiment['vix'] < 30 else '高'}</div>
                </div>
                <div class="sentiment-item">
                    <h3>加密恐惧贪婪</h3>
                    <div class="sentiment-value">{sentiment['crypto_fg']}</div>
                    <div style="font-size: 0.9em; color: #888;">{'极度恐惧' if sentiment['crypto_fg'] < 20 else '恐惧' if sentiment['crypto_fg'] < 40 else '中性' if sentiment['crypto_fg'] < 60 else '贪婪'}</div>
                </div>
                <div class="sentiment-item">
                    <h3>美债收益率</h3>
                    <div class="sentiment-value">{sentiment['treasury_10y']:.2f}%</div>
                    <div style="font-size: 0.9em; color: #888;">影响科技股估值</div>
                </div>
                <div class="sentiment-item">
                    <h3>综合情绪</h3>
                    <div class="sentiment-value">{sentiment['composite']}</div>
                    <div style="font-size: 0.9em; color: #888;">{sentiment['outlook']}</div>
                </div>
            </div>
        </div>

        <!-- 主要指数 -->
        <div class="section">
            <div class="section-title">📈 主要市场指数</div>
            <div class="grid">
"""

        for name, idx in indices.items():
            change_class = 'positive' if idx['change_pct'] >= 0 else 'negative'
            html += f"""                <div class="card">
                    <h3>{name}</h3>
                    <div style="font-size: 1.8em; font-weight: bold; margin: 15px 0;">{idx['price']}</div>
                    <div class="{change_class}">{idx['change_pct']:+.2f}%</div>
                </div>
"""

        html += """            </div>
        </div>

        <!-- 加密货币 -->
        <div class="section">
            <div class="section-title">₿ 加密货币持仓</div>
            <div class="grid">
"""

        for name, data in crypto.items():
            change_class = 'positive' if data['change_pct'] >= 0 else 'negative'
            html += f"""                <div class="card">
                    <h3>{name}</h3>
                    <div style="font-size: 1.5em; font-weight: bold; margin: 15px 0;">${data['price']:.2f}</div>
                    <div class="{change_class}">{data['change_pct']:+.2f}%</div>
                </div>
"""

        html += """            </div>
        </div>

        <!-- 重要财经新闻 -->
        <div class="section">
            <div class="section-title">📰 重要财经新闻</div>
"""

        if news:
            for item in news[:10]:
                impact_class = 'high-impact' if item['impact'] == '高' else 'medium-impact' if item['impact'] == '中' else ''
                impact_label = 'impact-high' if item['impact'] == '高' else 'impact-medium' if item['impact'] == '中' else 'impact-low'
                html += f"""            <div class="news-item {impact_class}">
                <div class="news-header">
                    <span class="news-impact {impact_label}">{item['impact']}影响</span>
                    <span style="color: #888; font-size: 0.85em;">{item['time']}</span>
                </div>
                <div class="news-title">{item['title']}</div>
                <div class="news-source">📌 {item['ticker']} | {item['publisher']}</div>
            </div>
"""
        else:
            html += """            <p style="color: #888;">暂无最新新闻</p>
"""

        html += """        </div>

        <!-- 财经日历 -->
        <div class="section">
            <div class="section-title">📅 完整财经日历</div>
"""

        if economic_events:
            html += """            <div class="earnings-alert">
                <h3 style="margin-bottom: 15px;">未来30天重要事件</h3>
"""
            for event in economic_events:
                html += f"""                <div class="economic-item">
                    <strong>{event['date']}</strong> - {event['event']}
                    <span style="color: #888; float: right;">还有{event['days_until']}天</span>
                </div>
"""
            html += """            </div>
"""
        else:
            html += """            <p style="color: #888;">未来30天无重要事件</p>
"""

        html += """        </div>

        <!-- 财报提醒 -->
        <div class="section">
            <div class="section-title">⚠️ 近期财报提醒</div>
"""

        if earnings:
            html += """            <div class="earnings-alert">
                <h3 style="margin-bottom: 15px;">📅 财报日历</h3>
"""
            for e in earnings:
                html += f"""                <div class="earnings-item"><strong>{e['ticker']}</strong> - {e['date']} (还有{e['days']}天)</div>
"""
            html += """            </div>
"""
        else:
            html += """            <p style="color: #888;">未来30天无财报</p>
"""

        html += """        </div>

        <!-- 个股分析 -->
        <div class="section">
            <div class="section-title">🎯 持仓个股深度分析</div>
            <div class="stock-grid">
"""

        for ticker, data in analyses.items():
            change_class = 'positive' if data['change_pct'] >= 0 else 'negative'
            is_warning = data['change_pct'] < -5 or not data['above_ma200']
            ma_status = "高于" if data['above_ma200'] else "低于"

            # 获取操作建议
            rec = recommendations.get(ticker, {})
            action = rec.get('action', '观察')
            reason = rec.get('reason', '')
            risk = rec.get('risk', '低')

            risk_class = 'risk-high' if risk == '高' else 'risk-medium' if risk == '中' else 'risk-low'
            risk_color = '#ff6b6b' if risk == '高' else '#ffd93d' if risk == '中' else '#6bcb77'

            html += f"""                <div class="stock-card {'warning' if is_warning else ''}">
                    <div class="stock-header">
                        <span class="stock-ticker">{ticker}</span>
                        <span style="font-size: 0.9em; color: #888;">52周: {data['position_52w']}%</span>
                    </div>
                    <div class="stock-price">${data['price']}</div>
                    <div class="{change_class}" style="font-size: 1.3em; margin: 10px 0;">{data['change_pct']:+.2f}%</div>
                    <div class="stock-metrics">
                        <div>200日均线: {ma_status}</div>
                        <div>PE: {data['pe']:.1f}</div>
                        <div>成交量: {data['volume_ratio']:.1f}x</div>
                    </div>
                    {f"<div style='font-size: 0.85em; color: #888; margin: 10px 0;'>评级: {data['rec']} | 目标: ${data['target']}</div>" if data['target'] > 0 else ""}
                    <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                            <span class="{risk_class}" style="font-weight: bold;">{action}</span>
                            <span style="font-size: 0.8em; color: #888;">{reason}</span>
                        </div>
                    </div>
                </div>
"""

        html += """            </div>
        </div>

        <div class="footer">
            <p>⚠️ 本报告仅供参考，不构成投资建议。投资有风险，决策需谨慎。</p>
            <p style="margin-top: 10px;">数据来源: Yahoo Finance, Alternative.me, Google News | 生成时间: {report_date}</p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def generate(self):
        """生成完整报告"""
        print("=" * 70)
        print("📊 美股盘前专业分析报告 v2.2")
        print("=" * 70)

        # 收集数据
        sentiment = self.get_market_sentiment()
        indices = self.get_major_indices()
        crypto = self.get_crypto_data()
        news = self.get_important_news()
        economic_events = self.get_economic_calendar()
        analyses, earnings = self.analyze_stocks()
        recommendations = self.generate_recommendations(sentiment, analyses, earnings, news, economic_events)

        # 生成HTML
        print("\n📝 生成HTML报告...")
        html = self.generate_html_report(sentiment, indices, crypto, analyses, earnings, recommendations, news, economic_events)

        # 保存
        reports_dir = os.path.expanduser('~/Desktop/reports')
        os.makedirs(reports_dir, exist_ok=True)
        filename = f"professional_report_v2.2_{datetime.now().strftime('%Y-%m-%d')}.html"
        filepath = os.path.join(reports_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n✅ 报告已保存: {filepath}")

        # 打开
        subprocess.run(['open', filepath])

        print("\n" + "=" * 70)
        print("📊 v2.2 新增功能:")
        print("   ✓ 重要财经新闻采集 (Google News RSS)")
        print("   ✓ 完整财经日历(FOMC/CPI/非农等)")
        print("   ✓ 新闻与事件关联持仓分析")
        print("   ✓ 操作建议合并到个股卡片 (更紧凑)")
        print("=" * 70)

        return filepath

if __name__ == "__main__":
    generator = ProfessionalReportGenerator()
    generator.generate()
