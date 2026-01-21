# Data Analyst Skill

AI 数据分析助手 - 通过自然语言查询你的 CSV/Excel 数据文件

## 使用方法

### 第一次使用（上传文件）

```bash
/data-analyst upload <文件路径> "<你的问题>" --api-key <GLM_API_Key>
```

### 继续提问

```bash
/data-analyst query "<你的问题>" --api-key <GLM_API_Key>
```

## 示例

```bash
# 上传文件并提问
/data-analyst upload ~/sales_data.csv "销售额最高的5个产品是哪些？" --api-key your_glm_api_key

# 继续分析
/data-analyst query "按地区统计平均销售额" --api-key your_glm_api_key
/data-analyst query "绘制月度销售趋势图" --api-key your_glm_api_key
```

## 获取 API Key

访问 [智谱 AI 开放平台](https://open.bigmodel.cn/) 获取 GLM API Key

## 功能特点

- 自然语言查询，无需懂 SQL
- 支持 CSV 和 Excel 文件
- 自动生成可视化图表（PNG + HTML）
- 支持多轮对话，持续分析数据
- 自动数据清洗和类型推断
- 使用 GLM-4-Flash 模型（快速且经济）

## 输出结果

- 文本分析结果（直接显示在终端）
- AI 解读（GLM 用中文解释结果）
- 图表文件保存在 `~/data_analysis_output/`
- HTML 交互报告可在浏览器中查看

## 技术依赖

- Python 3.9+
- GLM API Key（智谱 AI）
- pandas, numpy, duckdb, matplotlib, seaborn, zhipuai
