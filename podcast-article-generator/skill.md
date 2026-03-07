# Podcast Article Generator

将访谈/播客内容制作成网页并集成到 yt-podcast 项目中。

## 使用场景

当你有访谈/播客内容的 Markdown 文件，需要：
1. 制作成符合项目设计系统的网页
2. 集成到 `/Users/colin/yt-podcast` 项目的首页

## 项目路径

- **项目根目录**: `/Users/colin/yt-podcast`
- **设计模板**: `/Users/colin/yt-podcast/design-system/template-standalone.html`
- **设计规范**: `/Users/colin/yt-podcast/design-system/design-spec.md`
- **文章目录**: `/Users/colin/yt-podcast/articles/`
- **首页文件**: `/Users/colin/yt-podcast/index.html`

## ⚠️ 重要：使用内嵌样式

**必须使用内嵌样式（`<style>` 标签），而不是引用外部 CSS 文件！**

参考模板：`/Users/colin/yt-podcast/design-system/template-standalone.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章标题</title>
    <style>
        /* 完整的内嵌样式，从模板复制 */
        :root { ... }
        /* Reset, Container, Header, Badge, Title, etc. */
    </style>
</head>
<body>
    <!-- 内容 -->
</body>
</html>
```

### 为什么用内嵌样式？

1. 模板 `template-standalone.html` 使用的是内嵌样式
2. 每个页面是独立的，不依赖外部文件
3. 确保样式一致性

## 完整页面结构

```
Header（头部）
  ├── badge-wrapper（徽章）
  ├── title（标题）
  ├── subtitle（副标题）
  ├── meta-grid（元信息）
  └── cta-button（按钮）

Section: 核心洞察（points-grid）
  └── 4-6 个 point-card

Divider（分隔线）

Section: 深度洞察（topics）
  ├── section-title: "深度洞察"
  └── 多个 topic
      ├── topic-header
      │   ├── topic-number
      │   └── topic-info
      │       ├── topic-title
      │       └── topic-timestamp
      └── topic-content
          ├── topic-section-title: "核心观点"
          ├── topic-core-point
          ├── 多个 topic-detail
          │   ├── topic-detail-label
          │   └── topic-detail-content
          ├── quote-block（可选）
          └── thought-block（可选）

Divider（分隔线）

Section: 精华收获（takeaways-grid）
  └── 3-4 个 takeaway-card

Footer（页脚）
```

## 动画系统

### Header 动画（页面加载时）

使用 `keyframes` + `animate-in` class：

```html
<div class="badge-wrapper animate-in">
    <span class="badge">分类</span>
</div>
<span class="title-line-1 animate-in delay-1">第一行</span>
<span class="title-line-2 animate-in delay-2">第二行</span>
<p class="subtitle animate-in delay-3">副标题</p>
<div class="meta-grid animate-in delay-4">...</div>
```

### 卡片动画（滚动触发）

使用 `transition` + IntersectionObserver：

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.point-card, .takeaway-card, .topic').forEach(el => {
    observer.observe(el);
});
```

**CSS 中卡片初始状态**：
```css
.point-card,
.takeaway-card,
.topic {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.point-card.animate-in,
.takeaway-card.animate-in,
.topic.animate-in {
    opacity: 1;
    transform: translateY(0);
}
```

## 组件类速查

### Header 区域
- `.header` - 头部容器（全屏高度）
- `.header-content` - 头部内容
- `.badge-wrapper` - 徽章包裹器（flex）
- `.badge` - 徽章（胶囊形状）
- `.title` - 标题容器
- `.title-line-1` - 标题第一行（白→灰渐变）
- `.title-line-2` - 标题第二行（橙→青渐变）
- `.subtitle` - 副标题
- `.meta-grid` - 元信息网格
- `.meta-item` / `.meta-label` / `.meta-value`
- `.cta-button` - 行动按钮（渐变背景）

### 核心洞察区域
- `.section` - 章节容器（120px 上下内边距）
- `.section-title` - 章节标题
- `.points-grid` - 要点网格
- `.point-card` - 要点卡片
- `.point-number` - 要点编号
- `.point-title` - 要点标题（橙色）
- `.point-desc` - 要点描述

### 主题章节区域
- `.topic` - 主题（80px 下边距）
- `.topic-header` - 主题头部（flex）
- `.topic-number` - 主题编号（大号，渐变）
- `.topic-info` - 主题信息
- `.topic-title` - 主题标题
- `.topic-timestamp` - 时间戳（青色，等宽字体）
- `.topic-content` - 主题内容卡片
- `.topic-section-title` - 主题章节标题（橙色，全大写）
- `.topic-core-point` - 核心观点
- `.topic-detail` - 详细内容（左侧边框）
- `.topic-detail-label` - 详细标签
- `.topic-detail-content` - 详细内容

### 特殊块
- `.quote-block` - 引用块（左侧橙色边框）
- `.thought-block` - 思考块（灰色边框，圆角）
- `.divider` - 分隔线（1px）

### 精华收获区域
- `.takeaways-grid` - 收获网格
- `.takeaway-card` - 收获卡片
- `.takeaway-emoji` - 表情符号
- `.takeaway-title` - 标题
- `.takeaway-desc` - 描述

### Footer
- `.footer` - 页脚（120px 上下内边距）
- `.footer-title` - 页脚标题
- `.footer-desc` - 页脚描述
- `.footer-quote` - 页脚引用（渐变）
- `.footer-note` - 页脚注释

## 首页集成规范

### 文章卡片样式

首页使用不同的卡片样式（属于首页自己的设计系统）：

```html
<a href="articles/文件名.html" class="article-card card-{类别} reveal" target="_blank" rel="noopener">
    <div class="card-header">
        <span class="card-category">分类</span>
        <span class="card-meta">2026-02-25</span>
    </div>
    <h3 class="card-title">文章标题</h3>
    <p class="card-excerpt">摘要内容...</p>
    <div class="card-tags">
        <span class="card-tag">#标签1</span>
        <span class="card-tag">#标签2</span>
        <span class="card-tag">#标签3</span>
    </div>
    <div class="card-footer">
        <span class="read-link">
            阅读全文
            <span class="read-arrow">→</span>
        </span>
        <span class="card-stat">⏱ 约 XX 分钟</span>
    </div>
</a>
```

### 卡片类别映射

| 内容主题 | CSS类 | 颜色 |
|---------|-------|------|
| AI / 深度学习 / LLM | `card-ai` | 蓝色 |
| 未来科技 / 哲学 / 太空 | `card-future` | 紫色 |
| 金融 / 投资 / VC / 财报 | `card-finance` | 金色 |
| 硬科技 / 工程 / 芯片 | `card-tech` | 青色 |

### 添加位置

将新文章卡片添加到 `index.html` 的 `<div class="articles-grid">` 中，作为第一个元素（最新文章）。

### 更新计数

更新首页文章计数：
```html
<span class="section-subtitle">已收录 <span class="count-highlight">N</span> 篇深度洞察</span>
```

## 工作流程

### 1. 读取模板和内容

- 读取 `/Users/colin/yt-podcast/design-system/template-standalone.html` 获取完整样式
- 读取用户提供的 Markdown 文件

### 2. 解析内容结构

提取元信息：
- 标题
- 主持人/作者
- 嘉宾
- 时长
- 视频链接

解析章节：
- 核心洞察（3-6 个要点）
- 主题章节（带时间戳）
- 精华收获（3-4 个）
- Footer 内容

### 3. 生成 HTML

- **复制模板的完整 `<style>` 块**
- 填充内容到对应结构
- 确保 Header 有 `animate-in` 和 `delay-*` 类
- 确保三个 section 都存在：核心洞察、深度洞察、精华收获

### 4. 保存和集成

- 保存到 `/Users/colin/yt-podcast/articles/文件名.html`
- 更新 `/Users/colin/yt-podcast/index.html`
  - 添加文章卡片到 `articles-grid` 开头
  - 更新文章计数

## 文件命名规范

- 使用小写字母
- 单词用连字符连接
- 格式：`主题-人名.html` 或 `主题-关键词.html`
- 示例：`coatue-lucas-swisher.html`、`ben-horowitz-ai-singularity.html`

## 参考示例

### 正确示例

- `/Users/colin/yt-podcast/articles/ben-horowitz-ai-singularity.html` ✅
- `/Users/colin/yt-podcast/articles/coatue-lucas-swisher.html` ✅

这两个文件都使用内嵌样式，结构完整。

## ⚠️ 常见错误（避免）

### ❌ 错误做法

```html
<!-- 引用外部 CSS -->
<link rel="stylesheet" href="../design-system/design-tokens.css">
<link rel="stylesheet" href="../design-system/style.css">
```

### ✅ 正确做法

```html
<!-- 内嵌完整样式 -->
<style>
    /* 完整的 CSS，从 template-standalone.html 复制 */
    :root { ... }
    /* ... 所有样式 ... */
</style>
```

### ❌ 错误：缺少"深度洞察"章节

```html
<div class="divider"></div>
<!-- 直接开始 topic，缺少 section 包装和标题 -->
<div class="topic">
```

### ✅ 正确：完整的"深度洞察"章节

```html
<div class="divider"></div>

<section class="section">
    <h2 class="section-title">深度洞察</h2>

    <div class="topic">
        <!-- topic 内容 -->
    </div>
    <!-- 更多 topic -->
</section>
```

## 调用方式

```
请使用 podcast-article-generator skill 将以下访谈内容制作成网页：
[文件路径或内容]
```

## 输出

- 新创建的 HTML 文件路径
- 首页更新确认
- 文章计数更新确认
