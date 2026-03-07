# Podcast Article Generator

将访谈/播客内容制作成网页并集成到 yt-podcast 项目的自动化工具。

## 功能

- ✅ 将 Markdown 格式的访谈内容转换为符合设计系统的 HTML 网页
- ✅ 自动提取元数据（标题、主持人、嘉宾、时长、视频链接）
- ✅ 自动识别章节和时间戳
- ✅ 生成符合项目设计规范的网页
- ✅ 自动集成到项目首页
- ✅ 更新文章计数

## 使用方法

### 方式1：通过 Skill 调用（推荐）

```
请使用 podcast-article-generator skill 处理这个访谈内容：
/path/to/interview.md
```

### 方式2：直接提供内容

```
请使用 podcast-article-generator skill 将以下访谈制作成网页：

# **访谈标题**
* **主持人**：XXX
* **嘉宾**：XXX
* **链接**：https://youtube.com/...
* **时长**：01:00:00

## **详细内容**
### 1. **第一章节 [00:00-10:00]**
章节内容...
```

## 输入格式

访谈内容应为 Markdown 格式，包含以下信息：

```markdown
# **文章标题**

* **标题**：显示的标题
* **作者/主持人**：姓名
* **嘉宾**：姓名
* **链接**：https://youtube.com/watch?v=xxx
* **时长**：HH:MM:SS

## ---

**开篇引入**

开场白内容...

## ---

**详细内容**

### **1. 章节标题 [00:00-10:00]**

**核心观点**：...

**深度阐述**：...

**重要原话**：
"引用内容"

## ---

**精华收获**

1. 要点一
2. 要点二
```

## 输出

1. **HTML 文件**：保存在 `/Users/colin/yt-podcast/articles/` 目录
2. **首页更新**：自动添加文章卡片到首页
3. **计数更新**：自动更新文章总数

## 设计系统

项目使用深色渐变风格设计系统：

- **配色**：橙色 → 青色渐变
- **主题**：深色科技风
- **布局**：卡片式网格
- **交互**：Hover 提升 + 滚动动画

所有组件遵循 `/Users/colin/yt-podcast/design-system/` 中的规范。

## 文件结构

```
/Users/colin/.claude/skills/podcast-article-generator/
├── skill.md              # Skill 定义文件（AI 调用入口）
├── podcast_generator.py  # Python 辅助脚本
└── README.md             # 本文档
```

## 项目路径

- **项目根目录**: `/Users/colin/yt-podcast`
- **文章目录**: `/Users/colin/yt-podcast/articles/`
- **首页文件**: `/Users/colin/yt-podcast/index.html`
- **设计系统**: `/Users/colin/yt-podcast/design-system/`

## 卡片类别

根据内容类型选择合适的卡片样式：

| 类别 | CSS类 | 适用内容 |
|------|-------|----------|
| AI | `card-ai` | AI相关、人工智能 |
| 未来/科技 | `card-future` | 前沿科技、哲学思考 |
| 金融/投资 | `card-finance` | 金融、投资、VC、财报 |
| 技术 | `card-tech` | 硬科技、工程、技术 |

## 示例

查看已创建的文章作为参考：

- `coatue-lucas-swisher.html` - VC访谈（card-finance）
- `dario-amodei-ai-briefing.html` - AI战略（card-ai）
- `quantum_interview.html` - 前沿技术（card-tech）

## 注意事项

1. **文件命名**：使用小写字母和连字符，如 `coatue-lucas-swisher.html`
2. **日期格式**：使用 `2026-02-25` 格式
3. **时间格式**：使用 `HH:MM:SS` 格式
4. **标签**：使用 `#标签名` 格式，首字母大写
5. **阅读时间**：估算分钟数，如 "约 50 分钟"

## 版本历史

- **v1.0** (2026-02-25): 初始版本
