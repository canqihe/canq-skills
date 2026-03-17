# PokieTicker Skill

分析股票价格变动原因 - 基于 PokieTicker 数据库的智能问答系统。

## 功能

当你问"某只股票某天为什么跌了/涨了"时，这个 skill 会：
1. 从数据库查询该日的价格数据
2. 获取当天前后的相关新闻
3. 分析 Claude AI 的情感分析结果
4. 总结主要原因

## 使用示例

```
"为什么 AAPL 昨天跌了？"
"NVDA 2026-03-03 发生了什么？"
"TSLA 上周五为什么大涨？"
```

## 文件结构

```
pokieticker/
├── skill.md      # Skill 主逻辑（Claude Code 会自动读取）
├── query.py      # 数据库查询辅助脚本
└── README.md     # 本文件
```

## 直接使用脚本

你也可以直接使用 Python 脚本查询：

```bash
# 查询特定日期
python /Users/colin/.claude/skills/pokieticker/query.py AAPL 2026-03-03

# 使用相对日期
python /Users/colin/.claude/skills/pokieticker/query.py NVDA yesterday

# 列出可用股票
python /Users/colin/.claude/skills/pokieticker/query.py --list

# 搜索股票
python /Users/colin/.claude/skills/pokieticker/query.py --search "Apple"
```

## 依赖

- PokieTicker 数据库 (`pokieticker.db`)
- Python 3.10+
- SQLite3

## 数据库路径

默认路径: `/Users/colin/Desktop/File/PokieTicker-main/pokieticker.db`

如需修改，编辑 `query.py` 中的 `DB_PATH` 变量。

## 注意事项

- 数据库仅包含美股数据
- 数据来源：Polygon.io + Claude AI 情感分析
- 仅供学习参考，不构成投资建议
