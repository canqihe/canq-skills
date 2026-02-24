# Web Reader & Summary

使用 agent-browser 阅读网页内容，生成带样式的 HTML 摘要报告。

## 功能

- 支持任意网页 URL（包括 X/Twitter 推文、文章等）
- 使用 agent-browser 访问页面
- 提取并总结内容
- 生成带样式的 HTML 报告
- 自动保存到桌面

## 使用方法

```
请帮我阅读并总结这个网页：[URL]
阅读这个页面：[URL]
帮我看看这篇文章：[URL]
理解一下这条推文：[URL]
```

## 输出格式

HTML 文件，包含：
- 文章元信息（标题、来源、URL、日期）
- 内容摘要
- 关键观点提取
- 保存路径：`~/Desktop/[标题]_摘要.html`
