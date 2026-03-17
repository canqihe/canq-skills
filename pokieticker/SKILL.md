---
name: pokieticker
description: 分析美股涨跌原因，查询 PokieTicker SQLite 数据库获取价格和新闻数据
---

# PokieTicker - 股票涨跌原因分析

**何时使用此 skill**：
- 用户询问："为什么 [股票代码] 在 [日期] 跌了/涨了？"
- 用户询问："[股票代码] [日期] 发生了什么？"
- 用户询问："分析 [股票代码] 某天的价格变动原因"
- 用户询问："解释 [股票代码] 最近的表现"

**不使用此 skill**：
- 用户询问实时股价（此 skill 使用历史数据库）
- 用户询问金融建议（声明：仅供参考）
- 用户询问 A 股/港股（数据库仅包含美股）

---

## 工作流程

### STEP 1: 解析用户输入

从用户问题中提取：
- **股票代码** (symbol): AAPL, NVDA, TSLA 等
- **日期** (date): 可以是相对时间（昨天、上周五）或具体日期（2024-03-15）
- **变动方向** (direction): 跌/涨/变动

### STEP 2: 查询数据库确认价格变动

使用以下 SQL 查询获取 OHLC 数据：

```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
SELECT date, open, high, low, close, volume
FROM ohlc
WHERE symbol = '$SYMBOL' AND date = '$DATE'
ORDER BY date DESC
LIMIT 5;
EOF
```

如果具体日期没有数据，查询最接近的日期。

计算价格变动：
```
涨跌幅 = (close - open) / open * 100%
```

### STEP 3: 查询相关新闻

查询该日期前后（±3天）的新闻：

```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
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
WHERE na.symbol = '$SYMBOL'
  AND na.trade_date BETWEEN DATE('$DATE', '-3 days') AND DATE('$DATE', '+3 days')
ORDER BY na.published_utc;
EOF
```

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
   - 总结影响该股票的主要事件

4. **历史背景（可选）**
   - 如果用户想了解更多，提供前后几天的对比

---

## 输出格式

```
## 📊 [SYMBOL] - [DATE] 价格变动分析

### 价格表现
- 日期: [DATE]
- 开盘: $[OPEN]
- 收盘: $[CLOSE]
- 涨跌幅: [CHANGE]%
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
```

---

## 技巧

### 日期解析

- "昨天" → `date -v-1d +%Y-%m-%d` (macOS) 或 `date -d "yesterday" +%Y-%m-%d` (Linux)
- "上周五" → 计算上周五日期
- "3月15日" → 补充年份（当年）
- "2024-03-15" → 直接使用

### 股票代码验证

```bash
sqlite3 /Users/colin/Desktop/File/PokieTicker-main/pokieticker.db <<EOF
SELECT DISTINCT symbol FROM tickers WHERE symbol LIKE '%$SYMBOL%' LIMIT 10;
EOF
```

### 数据库路径

- 生产环境: `/Users/colin/Desktop/File/PokieTicker-main/pokieticker.db`
- 检查服务状态: `curl -s http://localhost:8000/api/health`

---

## 错误处理

1. **服务未启动** → 提醒用户启动服务
2. **股票代码不存在** → 列出可用股票
3. **日期无数据** → 查询最接近的日期
4. **该日期无新闻** → 说明可能原因

---

## 依赖

- PokieTicker 数据库 (`pokieticker.db`)
- FastAPI 后端服务 (可选，也可直接查询 SQLite)
- Bash 和 SQLite3 命令行工具
