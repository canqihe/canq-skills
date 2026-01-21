# Data Analyst Skill (GLM版本)

使用自然语言分析你的数据文件，无需懂 SQL

## 快速开始

### 1. 安装依赖

```bash
pip install pandas numpy duckdb matplotlib seaborn zhipuai
```

### 2. 获取 GLM API Key

访问 [智谱 AI 开放平台](https://open.bigmodel.cn/) 获取 API Key

### 3. 使用方法

#### 第一次使用（上传文件）

```bash
python ~/.claude/skills/data-analyst/data_analyst_core.py upload <文件路径> "<你的问题>" --api-key <GLM_API_Key>
```

#### 继续提问

```bash
python ~/.claude/skills/data-analyst/data_analyst_core.py query "<你的问题>" --api-key <GLM_API_Key>
```

## 使用示例

```bash
# 上传销售数据并查询
python ~/.claude/skills/data-analyst/data_analyst_core.py upload \
  ~/Documents/sales.csv \
  "销售额最高的5个产品是哪些？" \
  --api-key your_glm_api_key_here

# 继续分析
python ~/.claude/skills/data-analyst/data_analyst_core.py query \
  "按地区统计平均销售额" \
  --api-key your_glm_api_key_here

python ~/.claude/skills/data-analyst/data_analyst_core.py query \
  "哪个月份的销售增长最快？" \
  --api-key your_glm_api_key_here
```

## 输出位置

- 分析结果：直接显示在终端
- HTML 报告：`~/data_analysis_output/analysis_report_*.html`
- 图表文件：`~/data_analysis_output/*.png`

## 功能特点

- 自然语言查询，自动转换为 SQL
- 支持 CSV 和 Excel 文件
- 自动数据清洗和类型推断
- 生成 HTML 可视化报告
- 支持多轮对话分析
- 使用 GLM-4-Flash 模型（快速且经济）

## 技术架构

- **AI 模型**: GLM-4-Flash (智谱 AI)
- **数据库**: DuckDB (高性能分析)
- **数据处理**: Pandas
- **可视化**: Matplotlib + Seaborn

## 工作流程

1. 上传数据文件 → 自动解析并保存会话
2. 提出问题 → GLM 理解问题并生成 SQL
3. 执行 SQL → DuckDB 返回结果
4. AI 解读 → GLM 用中文解读结果
5. 生成报告 → HTML + 可视化图表

## 提示词

GLM 使用两个提示词：
1. **SQL 生成提示词**：根据数据结构将自然语言转换为 DuckDB SQL
2. **结果解读提示词**：用简洁易懂的中文解读查询结果
