---
name: web_style
description: 网站设计风格生成器 - 从21种精心设计的前端风格中选择，直接生成符合该设计系统的完整网站代码
license: MIT
---

这个skill帮助用户选择一种网站设计风格，并直接生成符合该设计系统的完整网站代码。

## 工作流程

当用户请求使用网站设计风格时：

1. **读取并展示风格列表**：从 skill 内置的 `styles/` 目录读取所有21种设计风格
2. **用户选择风格**：展示所有风格（名称 + 简短描述），等待用户选择
3. **了解用户需求**：询问用户想要生成什么类型的网站/页面
4. **加载风格Prompt**：读取选定风格的完整 `<role>` 和 `<design-system>` 内容
5. **生成网站代码**：使用该风格的设计系统规范，直接为用户生成完整的前端代码

## 实现步骤

### 第一步：展示风格选项

向用户展示所有21种可用风格，格式为：

```
## 选择您喜欢的设计风格

1. **Art Deco**
   1920s Gatsby elegance, geometric precision, metallic gold accents, architectural symmetry, luxury heritage.

2. **Bauhaus**
   Bold geometric modernism with circles, squares, and triangles...

[全部21种风格]
```

### 第二步：获取用户需求

用户选择风格后，询问：
- 想要生成什么类型的网站？（落地页、仪表板、博客、电商等）
- 需要哪些功能模块？
- 有特殊要求吗？

### 第三步：生成代码

使用Python脚本读取选定风格的完整prompt内容，然后：
1. 采用该prompt的 `<role>` 部分（作为开发专家的角色定位）
2. 严格遵循 `<design-system>` 中的设计规范
3. 生成完整可用的HTML/CSS/JS或React代码

## 使用示例

```
用户：我想用web_style生成一个网站

助手：[展示21种设计风格列表]

用户：我选Clay风格，做一个产品落地页

助手：[读取Clay风格的完整设计系统]
     [按照Clay规范生成产品落地页代码]
     [包括Nunito字体、rounded-2xl圆角、4层阴影stack、浮动blob背景等]
```

## Python脚本功能

`web_style.py` 提供以下功能：

- `list_styles()` - 列出所有风格（名称+描述）
- `get_style_prompt(filename)` - 获取完整的设计系统prompt
- `get_all_styles()` - 获取所有风格的JSON格式数据

## 关键原则

- **直接生成**：不是返回prompt让用户自己用，而是直接用prompt生成网站
- **严格遵循设计系统**：颜色、字体、圆角、阴影、动画等必须严格符合选定风格
- **完整可用**：生成的代码应该是直接可运行的完整网站
- **高质量**：参考设计系统中的"Bold Factor"和"Anti-Patterns"，避免generic设计
