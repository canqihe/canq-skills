---
name: pokieticker
description: 分析美股和加密货币涨跌原因，查询 PokieTicker SQLite 数据库获取价格和新闻数据
---

# PokieTicker - 股票 & 加密货币涨跌原因分析

**何时使用此 skill**：
- 用户询问："为什么 [股票/加密货币代码] 在 [日期] 跌了/涨了？"
- 用户询问："[股票/加密货币代码] [日期] 发生了什么？"
- 用户询问："分析 [股票/加密货币代码] 某天的价格变动原因"
- 用户询问："解释 [股票/加密货币代码] 最近的表现"
- 用户请求："更新数据"/"更新股票数据"/"获取最新数据"

**不使用此 skill**：
- 用户询问实时价格（此 skill 使用历史数据库）
- 用户询问金融建议（声明：仅供参考）
- 用户询问 A 股/港股（数据库仅包含美股）

**支持的数据类型**：
- **股票**：AAPL, NVDA, TSLA 等（约 113 只）
- **加密货币**：X:BTCUSD, X:ETHUSD, X:SOLUSD, X:XRPUSD, X:BNBUSD（5 种）

---

## 📁 数据库架构

**双数据库设计**：

| 数据库 | 文件 | 用途 | Symbol 格式 |
|--------|------|------|-------------|
| **股票数据库** | `pokieticker.db` | 美股、ETF | AAPL, NVDA, GLD 等 |
| **加密货币数据库** | `crypto.db` | 加密货币 | X:BTCUSD, X:ETHUSD 等 |

**自动路由规则**：
- Symbol 以 `X:` 开头 → 加密货币数据库
- 其他格式 → 股票数据库

---

## 工作流程

### STEP 1: 解析用户输入

从用户问题中提取：
- **代码** (symbol):
  - 股票：AAPL, NVDA, TSLA 等
  - 加密货币：X:BTCUSD, X:ETHUSD 等
- **日期** (date): 可以是相对时间（昨天、上周五）或具体日期（2024-03-15）
- **变动方向** (direction): 跌/涨/变动

### STEP 2: 查询数据库确认价格变动

⚠️ **⚠️⚠️ 强制规则：涨跌幅计算 ⚠️⚠️⚠️**

**每次计算涨跌幅时，你必须使用以下方法：**

✅ **正确方法**（包含跳空的真实涨跌幅）：

**股票**（使用 `pokieticker.db`）：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
WITH daily_change AS (
    SELECT
        symbol,
        date,
        open,
        high,
        low,
        close,
        volume,
        LAG(close) OVER (PARTITION BY symbol ORDER BY date) as prev_close
    FROM ohlc
    WHERE date >= DATE('$DATE', '-1 day')
)
SELECT
    date,
    open,
    close,
    prev_close,
    ROUND((close - prev_close) / prev_close * 100, 2) as change_pct,
    volume
FROM daily_change
WHERE symbol = '$SYMBOL' AND date = '$DATE' AND prev_close IS NOT NULL;
EOF
```

**加密货币**（使用 `crypto.db`）：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/crypto.db <<EOF
WITH daily_change AS (
    SELECT
        symbol,
        date,
        open,
        high,
        low,
        close,
        volume,
        LAG(close) OVER (PARTITION BY symbol ORDER BY date) as prev_close
    FROM ohlc
    WHERE date >= DATE('$DATE', '-1 day')
)
SELECT
    date,
    open,
    close,
    prev_close,
    ROUND((close - prev_close) / prev_close * 100, 2) as change_pct,
    volume
FROM daily_change
WHERE symbol = '$SYMBOL' AND date = '$DATE' AND prev_close IS NOT NULL;
EOF
```

❌ **绝对禁止使用**：
```sql
-- 错误：只看日内变化，忽略跳空
(close - open) / open * 100
```

**原因**：跳空是重要的市场信号，忽略它会导致严重错误。

**真实案例**（SMCI, 2026-03-20）：
- 错误方法（日内）：-8.84%
- 正确方法（包含跳空）：-33.32%
- **差异：24.48%** ← 这是重大利空信号！

---

如果具体日期没有数据，查询最接近的日期。

### STEP 3: 查询相关新闻

⚠️ **⚠️⚠️ 重要：新闻查询必须同时使用两种方式 ⚠️⚠️⚠️**

**问题**：`news_aligned.trade_date` 和 `news_raw.published_utc` 可能不一致
- **真实案例**（SMCI, 2026-03-20）：
  - 仅用 `trade_date` 查询 → 找到 1 条新闻（遗漏关键利空）
  - 仅用 `published_utc` 查询 → 找到 5 条新闻（包含调查警报）
  - **差异：漏掉 80% 的新闻！**

✅ **正确做法：同时查询两种方式**

**方式 1：按对齐日期查询**（`news_aligned.trade_date`）：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
SELECT
    nr.title,
    nr.description,
    nr.publisher,
    nr.published_utc,
    na.trade_date,
    l1.sentiment,
    l1.reason_growth,
    l1.reason_decrease,
    l1.key_discussion
FROM news_aligned na
JOIN news_raw nr ON na.news_id = nr.id
LEFT JOIN layer1_results l1 ON na.news_id = l1.news_id AND na.symbol = l1.symbol
WHERE na.symbol = '$SYMBOL'
  AND na.trade_date BETWEEN DATE('$DATE', '-3 days') AND DATE('$DATE', '+3 days')
ORDER BY na.published_utc;
EOF
```

**方式 2：按发布时间查询**（`news_raw.published_utc`）：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
SELECT
    nr.title,
    nr.description,
    nr.publisher,
    nr.published_utc,
    DATE(nr.published_utc) as '发布日期',
    l1.sentiment,
    l1.reason_growth,
    l1.reason_decrease,
    l1.key_discussion
FROM news_raw nr
JOIN news_ticker nt ON nr.id = nt.news_id
LEFT JOIN layer1_results l1 ON nr.id = l1.news_id AND nt.symbol = l1.symbol
WHERE nt.symbol = '$SYMBOL'
  AND DATE(nr.published_utc) BETWEEN DATE('$DATE', '-3 days') AND DATE('$DATE', '+3 days')
ORDER BY nr.published_utc;
EOF
```

**方式 3：统计每日新闻数**（验证完整性）：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
SELECT
    DATE(nr.published_utc) as '日期',
    COUNT(*) as '新闻数'
FROM news_ticker nt
JOIN news_raw nr ON nt.news_id = nr.id
WHERE nt.symbol = '$SYMBOL'
  AND DATE(nr.published_utc) >= DATE('$DATE', '-5 days')
GROUP BY DATE(nr.published_utc)
ORDER BY DATE(nr.published_utc) DESC;
EOF
```

**加密货币**：目前加密货币数据库暂无新闻数据。

### STEP 4: 分析总结

基于查询结果，提供以下分析：

1. **价格变动摘要**
   - 日期、开盘价、收盘价、涨跌幅
   - 成交量变化（如果有）

2. **相关新闻汇总**
   - 按情感分类（positive/negative/neutral）
   - 列出主要影响因素

3. **主要原因分析**
   - 如果有 layer1 分析结果，引用 reason_growth 或 reason_decrease
   - 总结影响该资产的主要事件

4. **历史背景（可选）**
   - 如果用户想了解更多，提供前后几天的对比

---

## 输出格式

```
## 📊 [SYMBOL] - [DATE] 价格变动分析

### 价格表现
- 日期: [DATE]
- 前收盘: $[PREV_CLOSE]
- 开盘: $[OPEN]
- 收盘: $[CLOSE]
- **真实涨跌幅**: [CHANGE]%
- 成交量: [VOLUME]

### 📰 相关新闻 ([N] 条)

**负面/利空因素**
- [Publisher] [Date]: [Title]
  理由: [reason_decrease]

**正面/利多因素**
- [Publisher] [Date]: [Title]
  理由: [reason_growth]

**中性/其他**
- [Publisher] [Date]: [Title]

### 💡 主要原因总结

[基于新闻情感和 layer1 分析，总结 1-3 条主要原因]

---

数据来源: PokieTicker 数据库 (Polygon.io + Claude AI 分析)
注：涨跌幅计算包含跳空 (当天收盘 vs 前一天收盘)
```

---

## 技巧

### 日期解析

- "昨天" → `date -v-1d +%Y-%m-%d` (macOS) 或 `date -d "yesterday" +%Y-%m-%d` (Linux)
- "上周五" → 计算上周五日期
- "3月15日" → 补充年份（当年）
- "2024-03-15" → 直接使用

### 代码验证

**验证股票代码**：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
SELECT DISTINCT symbol FROM tickers WHERE symbol LIKE '%$SYMBOL%' LIMIT 10;
EOF
```

**验证加密货币代码**：
```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/crypto.db <<EOF
SELECT DISTINCT symbol FROM tickers WHERE symbol LIKE '%$SYMBOL%' LIMIT 10;
EOF
```

### 新闻查询最佳实践 ⚠️ **新增**

**问题根源**：
- `news_aligned.trade_date`：新闻对齐到的交易日（可能不等于发布日期）
- `news_raw.published_utc`：新闻实际发布时间（UTC）

**典型场景**：
- 3/19 22:00 发布的利空新闻 → `trade_date` 可能是 3/20（对齐到下一个交易日）
- 3/20 23:00 发布的调查新闻 → 查询 3/20 的 `trade_date` 可能找不到

**正确流程**：
```bash
# Step 1: 按 trade_date 查询（已对齐的新闻）
sqlite3 ... "WHERE na.trade_date BETWEEN ..."

# Step 2: 按 published_utc 查询（原始发布时间）
sqlite3 ... "WHERE DATE(nr.published_utc) BETWEEN ..."

# Step 3: 对比结果，如果数量差异大 → 需要进一步调查
# Step 4: 列出所有相关新闻的详情，避免遗漏
```

**教训总结**（SMCI 2026-03-20 案例）：
- ❌ 仅用 `trade_date` 查询：找到 1 条 → 结论"新闻数据不足"
- ✅ 同时用 `published_utc` 查询：找到 5 条 → 发现关键调查新闻
- **差异：漏掉 80% 新闻，导致分析错误**

### 数据库路径

- **股票数据库**: `/Users/colin/Desktop/File/PokieTicker-main/pokieticker.db`
- **加密货币数据库**: `/Users/colin/Desktop/File/PokieTicker-main/crypto.db`
- 检查服务状态: `curl -s http://localhost:8000/api/health`

---

## 错误处理

1. **服务未启动** → 提醒用户启动服务
2. **代码不存在** → 列出可用资产
3. **日期无数据** → 查询最接近的日期
4. **该日期无新闻** → 说明可能原因（加密货币暂无新闻数据）

---

## 常见错误与教训 ⚠️ **新增**

### 错误 1：新闻查询不完整导致遗漏关键信息

**场景**：SMCI 2026-03-20 暴跌 33% 分析

**错误做法**：
```sql
-- ❌ 仅使用 trade_date 查询
WHERE na.trade_date BETWEEN DATE('2026-03-20', '-3 days') AND DATE('2026-03-20', '+3 days')
-- 结果：找到 1 条新闻 → 结论"数据库新闻缺失"
```

**正确做法**：
```sql
-- ✅ 同时使用 trade_date 和 published_utc 查询
-- 方式1: WHERE na.trade_date BETWEEN ...
-- 方式2: WHERE DATE(nr.published_utc) BETWEEN ...
-- 结果：找到 5 条新闻 → 发现关键调查新闻
```

**真实影响**：
- 遗漏新闻：3/19 宣布联合创始人被捕，3 人被起诉
- 错误结论："数据库新闻不足"
- 实际原因：向中国走私 $25 亿 AI 服务器，违反出口管制

**教训**：
1. **永远不要依赖单一查询方式** - 必须同时使用 `trade_date` 和 `published_utc`
2. **不要过早下结论** - 说"数据缺失"前先验证查询方式
3. **交叉验证结果** - 对比不同查询方式的结果数量
4. **统计每日新闻数** - 确认数据完整性后再分析

---

### 错误 2：涨跌幅计算忽略跳空

**场景**：任何有跳空的交易日

**错误做法**：
```sql
-- ❌ 只计算日内变化
(close - open) / open * 100
-- SMCI 2026-03-20: -8.84%（严重错误）
```

**正确做法**：
```sql
-- ✅ 计算包含跳空的真实涨跌幅
(close - LAG(close) OVER (...)) / LAG(close) OVER (...) * 100
-- SMCI 2026-03-20: -33.32%（正确）
```

**教训**：
- 跳空是重要的市场信号，不能忽略
- 盘后重大利空会导致第二天跳空
- 真实涨跌幅 = (当天收盘 - 前一天收盘) / 前一天收盘

---

## 数据更新流程

### 当用户请求更新数据时

**用户说**：
- "更新数据"
- "更新股票数据"
- "获取最新数据"
- "pokieticker 更新"

### STEP 1: 检查当前数据状态

```bash
# 检查股票数据库最新 OHLC 日期
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db "SELECT MAX(date) as latest_ohlc FROM ohlc;"

# 检查加密货币数据库最新 OHLC 日期
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/crypto.db "SELECT MAX(date) as latest_ohlc FROM ohlc;"

# 检查股票数据库最新新闻日期
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db "SELECT MAX(published_utc) as latest_news FROM news_raw;"

# 获取今天日期
date +%Y-%m-%d
```

### STEP 2: 判断更新范围

**重要规则**：
- ✅ 只更新到**昨天**（最近的完整交易日）
- ❌ **不要**尝试获取今天的数据（Polygon 免费版不支持，会返回 403）

**判断逻辑**：
```python
# 如果数据库最新日期是 2026-03-16，今天是 2026-03-18
# 更新范围: 2026-03-17 → 2026-03-17（昨天）
```

### STEP 3: 执行更新

**默认方式：完整更新（所有股票）**
```bash
cd /Users/colin/Desktop/File/PokieTicker-main
source venv/bin/activate
python3 -m backend.weekly_update
```

**可选方式：快速更新（仅热门股票，适合快速测试）**
```bash
cd /Users/colin/Desktop/File/PokieTicker-main
source venv/bin/activate

python3 << 'EOF'
from datetime import datetime, timedelta, timezone
from backend.database import get_conn_for_symbol
from backend.polygon.client import fetch_ohlc, fetch_news
from backend.pipeline.alignment import align_news_for_symbol
from backend.pipeline.layer0 import run_layer0
import json

# 计算昨天日期（避免403错误）
YESTERDAY = (datetime.now(timezone.utc) - timedelta(days=1)).date().isoformat()
SYMBOLS = ["NVDA", "AAPL", "TSLA", "META", "GOOGL", "MSFT", "AMZN"]

print(f"=== 更新热门股票: {YESTERDAY} ===\n")

for symbol in SYMBOLS:
    print(f"📈 {symbol}")

    # 使用自动路由获取正确的数据库连接
    conn = get_conn_for_symbol(symbol)
    result = conn.execute(
        "SELECT last_ohlc_fetch, last_news_fetch FROM tickers WHERE symbol = ?",
        (symbol,)
    ).fetchone()
    conn.close()

    if not result:
        print(f"  ❌ 股票不在数据库中\n")
        continue

    ohlc_fetch = result["last_ohlc_fetch"] or "2024-01-01"
    news_fetch = result["last_news_fetch"] or ohlc_fetch

    # 更新 OHLC
    start_date = (datetime.fromisoformat(ohlc_fetch) + timedelta(days=1)).date().isoformat()
    if start_date <= YESTERDAY:
        try:
            rows = fetch_ohlc(symbol, start_date, YESTERDAY)
            if rows:
                conn = get_conn_for_symbol(symbol)
                for row in rows:
                    conn.execute(
                        """INSERT OR IGNORE INTO ohlc
                           (symbol, date, open, high, low, close, volume, vwap, transactions)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (symbol, row["date"], row["open"], row["high"], row["low"],
                         row["close"], row["volume"], row["vwap"], row["transactions"]),
                    )
                conn.execute("UPDATE tickers SET last_ohlc_fetch = ? WHERE symbol = ?", (YESTERDAY, symbol))
                conn.commit()
                conn.close()
                print(f"  ✅ OHLC: +{len(rows)} 天")
            else:
                print(f"  ℹ️  OHLC: 无新数据")
        except Exception as e:
            print(f"  ❌ OHLC 错误: {e}")

    # 更新新闻
    start_date = (datetime.fromisoformat(news_fetch) + timedelta(days=1)).date().isoformat()
    if start_date <= YESTERDAY:
        try:
            articles = fetch_news(symbol, start_date, YESTERDAY)
            if articles:
                conn = get_conn_for_symbol(symbol)
                count = 0
                for art in articles:
                    news_id = art.get("id")
                    if not news_id:
                        continue
                    tickers = art.get("tickers") or []
                    conn.execute(
                        """INSERT OR IGNORE INTO news_raw
                           (id, title, description, publisher, author,
                            published_utc, article_url, amp_url, tickers_json, insights_json)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (news_id, art.get("title"), art.get("description"),
                         art.get("publisher"), art.get("author"), art.get("published_utc"),
                         art.get("article_url"), art.get("amp_url"),
                         json.dumps(tickers), json.dumps(art.get("insights"))),
                    )
                    for tk in tickers:
                        conn.execute("INSERT OR IGNORE INTO news_ticker (news_id, symbol) VALUES (?, ?)", (news_id, tk))
                    count += 1
                conn.execute("UPDATE tickers SET last_news_fetch = ? WHERE symbol = ?", (YESTERDAY, symbol))
                conn.commit()
                conn.close()
                print(f"  ✅ News: +{count} 篇")

                # 运行 Layer 0 过滤
                align_news_for_symbol(symbol)
                l0 = run_layer0(symbol)
                print(f"  🔍 Layer0: {l0.get('passed', 0)}/{l0.get('total', 0)} 通过")
            else:
                print(f"  ℹ️  News: 无新文章")
        except Exception as e:
            print(f"  ❌ News 错误: {e}")

    print()

print("=== 更新完成 ===")
EOF
```

### STEP 4: 验证更新结果

```bash
# 确认股票数据库最新日期
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db "SELECT MAX(date) as latest_ohlc FROM ohlc;"

# 确认加密货币数据库最新日期
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/crypto.db "SELECT MAX(date) as latest_ohlc FROM ohlc;"
```

### 更新策略

| 场景 | 操作 | 原因 |
|------|------|------|
| 数据库最新日期 < 昨天 | 更新到昨天 | 有新数据可获取 |
| 数据库最新日期 = 昨天 | 无需更新 | 已是最新 |
| 尝试获取今天数据 | ❌ 跳过 | Polygon 免费版不支持（403） |

### 常见错误处理

**错误 1: 403 NOT_AUTHORIZED**
```
原因: 尝试获取今天的数据
解决: 只更新到昨天（YESTERDAY = 今天 - 1天）
```

**错误 2: 无新数据**
```
原因: 市场休日（周末/假日）或已是最新
解决: 正常情况，无需处理
```

---

## 输出验证清单（强制执行）

⚠️ **在输出任何分析答案之前，你必须确认以下所有项：**

- [ ] **使用了正确的数据库？**
  - 股票代码使用 `pokieticker.db`
  - 加密货币代码（X:开头）使用 `crypto.db`

- [ ] **涨跌幅计算使用了 `LAG(close)` 方法？**
  - SQL 中包含 `LAG(close) OVER (PARTITION BY symbol ORDER BY date)`
  - 计算公式是 `(close - prev_close) / prev_close * 100`

- [ ] **没有使用错误的 `(close - open) / open` 方法？**
  - SQL 中没有基于 open 计算涨跌幅

- [ ] **SQL 查询包含 `prev_close` 字段？**
  - 结果中显示前一天收盘价用于验证

- [ ] **新闻查询使用了多种方式？** ⚠️ **新增**
  - 同时使用 `trade_date` 和 `published_utc` 查询
  - 统计每日新闻数验证完整性
  - 对比两种查询结果，确保不遗漏

**如果任何一项为"否" → 立即重新计算！**

**如果发现已经输出了错误答案 → 主动承认错误并重新提供正确数据**

---

## 依赖

- **股票数据库**: `/Users/colin/Desktop/File/PokieTicker-main/pokieticker.db`
- **加密货币数据库**: `/Users/colin/Desktop/File/PokieTicker-main/crypto.db`
- FastAPI 后端服务 (可选，也可直接查询 SQLite)
- Bash 和 SQLite3 命令行工具
