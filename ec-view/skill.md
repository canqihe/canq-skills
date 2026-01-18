---
name: ec-view
description: 电商KV视觉系统提示词生成器 - 智能识别产品信息，生成10张海报的完整中英文双语提示词（9:16竖版格式）
---

# EC-View - 电商KV视觉系统提示词生成器

**版本**: 1.1
**输出格式**: 9:16 竖版海报
**默认模式**: 仅生成提示词（不生成图片）
**文件格式**: TXT（严格按照ec-prompt.txt格式）
**更新说明**: 移除海报选择询问步骤，直接生成全部11张海报

---

## 📋 工作流程

### ⚠️ 核心原则
- **严格按照4步流程执行**
- **所有选择由用户决定**（不自动推荐或跳过）
- **输出格式必须是TXT文件，严格按照示例格式**
- **默认生成全部11张海报（包含LOGO生成提示词）**

---

### **第一步：产品信息智能提取（如果上传了图片）**

请仔细分析用户上传的产品图片，自动提取以下信息：

#### 自动识别项目：

**1. 品牌名称识别**
- 从包装/产品上识别品牌LOGO文字
- 识别中文品牌名和英文品牌名
- 提取品牌标志的设计风格（字体、图标、配色）

**2. 产品类型判断**
- 识别产品所属类别（服装/食品/电子/美妆/家居/宠物用品等）
- 识别具体产品名称（从包装文字或产品形态判断）
- 识别产品规格（尺寸、容量、重量等）

**3. 卖点提取**
- 从包装上的文案提取核心卖点关键词
- 从产品图标/认证标识提取卖点（如：有机认证、无添加、进口等）
- 从产品视觉特征推断卖点（如：颜色、材质、工艺）
- 提取数据卖点（如：百分比、含量、时长等）

**4. 配色方案分析**
- 提取包装主色调（RGB/HEX色值）
- 识别辅助色和点缀色
- 分析配色风格（清新/沉稳/鲜艳/高级等）

**5. 设计风格判断**
- 识别包装设计风格（极简/复古/可爱/科技/艺术等）
- 识别字体风格（衬线/无衬线/手写等）
- 识别图案元素（水彩/几何/插画/摄影）

**6. 目标受众推断**
- 根据包装风格推断目标用户群体
- 根据产品类型推断年龄段
- 根据价格定位推断消费层级

**7. 产品参数提取**
- 从包装文字提取产品规格（净含量/尺码/功率等）
- 提取成分信息/配料表/营养成分
- 提取使用说明/注意事项
- 提取生产日期/保质期/储存方式

**8. 产品细节识别**
- 识别产品材质质感（光滑/粗糙/哑光/高光等）
- 识别产品结构特点（可拆卸/折叠/便携等）
- 识别包装特色（自封袋/泵头/喷雾/滴管等）

#### 输出格式：

```markdown
【识别报告】
品牌名称：[中文] / [英文]
产品类型：[大类] - [具体产品]
产品规格：[具体规格]
核心卖点：
1. [卖点1 - 中英文]
2. [卖点2 - 中英文]
3. [卖点3 - 中英文]
4. [卖点4 - 中英文]
5. [卖点5 - 中英文]
主色调：[颜色名称] (#HEX) + [颜色名称] (#HEX)
辅助色：[颜色名称] (#HEX)
设计风格：[风格描述]
目标受众：[用户画像]
品牌调性：[调性描述]
包装亮点：[特殊设计元素]
```

---

### **第二步：视觉风格选择**

基于识别的产品信息，**请推荐最适合的视觉风格**（也可手动指定）：

```
请选择视觉风格（输入对应的数字或名称）：

1. 杂志编辑风格（高级、专业、大片感、粗衬线标题、极简留白）

2. 水彩艺术风格（温暖、柔和、晕染效果、手绘质感）

3. 科技未来风格（冷色调、几何图形、数据可视化、蓝光效果）

4. 复古胶片风格（颗粒质感、暖色调、怀旧氛围、宝丽来边框）

5. 极简北欧风格（性冷淡、大留白、几何线条、黑白灰）

6. 霓虹赛博风格（荧光色、描边发光、未来都市、暗色背景）

7. 自然有机风格（植物元素、大地色系、手工质感、环保理念）

AI推荐依据：
- 根据产品类型自动匹配最佳风格
- 根据包装设计风格延续品牌调性
- 根据目标受众审美偏好推荐

请输入您的选择（1-7）：
```

---

### **第三步：文字排版效果选择**

```
请选择文字排版效果（输入对应的数字或名称）：

1. 粗衬线大标题 + 细线装饰 + 网格对齐（杂志风）

2. 玻璃拟态卡片 + 半透明背景 + 柔和圆角（现代风）

3. 3D浮雕文字 + 金属质感 + 光影效果（奢华风）

4. 手写体标注 + 水彩笔触 + 不规则布局（艺术风）

5. 无衬线粗体 + 霓虹描边 + 发光效果（赛博风）

6. 极细线条字 + 大量留白 + 精确对齐（极简风）

请输入您的选择（1-6）：
```

---

### **第四步：生成完整提示词系统**

#### 4.1 确认特殊需求（可选）

询问用户是否有特殊需求：

```markdown
【特殊需求确认】

【是否需要模特】：是 / 否（如果是，描述模特类型）

【是否需要场景】：是 / 否（如果是，描述场景类型）

【是否需要数据可视化】：是 / 否

【其他特殊要求】：[如：必须包含产品实物、需要对比图、需要用户评价等]
```

确认后，**直接生成全部11张海报**（包含LOGO生成提示词 + 10张海报提示词）。

---

#### 4.2 海报清单

```
LOGO生成提示词（中英双语，基于识别的品牌设计风格）
海报01 - 主KV视觉（Hero Shot，必须严格还原上传的产品图）
海报02 - 生活场景/使用场景（Lifestyle，展示产品实际使用）
海报03 - 工艺/技术/概念可视化（Process/Concept，基于识别的卖点）
海报04 - 细节特写01（Detail 01，放大产品细节）
海报05 - 细节特写02（Detail 02，材质/质感特写）
海报06 - 细节特写03（Detail 03，功能细节）
海报07 - 细节特写04 或 用户评价（Detail 04 / Review）
海报08 - 品牌故事/配色灵感（Brand Story / Moodboard，使用识别的配色）
海报09 - 产品参数/规格表（Specifications，使用识别的参数）
海报10 - 使用指南/注意事项（Usage Guide，基于产品类型）
```

---

## 🔴 核心要求（重中之重）

### 1. 产品图还原要求

必须在提示词中明确说明：
- "严格还原上传的产品图，包括包装设计、颜色、LOGO位置、文字内容、图案元素等所有细节"
- "产品外观必须与参考图完全一致，不得改变包装设计、配色方案或品牌元素"
- "保持产品的真实材质质感（哑光/高光/磨砂/金属等）"

**示例**：
```
"使用上传的朗诺RANOVA冻干鸡肉产品包装，保持蓝色袋身、水彩猫咪插画、金色LOGO等所有设计元素完全一致"
```

---

### 2. 文案排版要求（中英文双语）

每张海报的所有文字内容都必须采用中英文双语排版。

#### 标题排版格式（3种可选）：

**格式A - 中英堆叠（最常用）**：
```
纯肉冻干
PURE FREEZE-DRIED
```
- 中文在上（较大字号），英文在下（较小字号）
- 垂直堆叠，居中对齐

**格式B - 中英并列**：
```
纯肉冻干 | PURE FREEZE-DRIED
```
- 中英文横向并列，用竖线或斜杠分隔
- 字号相同或中文略大

**格式C - 中英分离**：
```
纯肉冻干                    [左上角]
              PURE FREEZE-DRIED  [右下角]
```
- 中英文分别放置在不同位置，形成视觉对比

---

#### 卖点/说明文字排版格式：

```
🥩 100%纯肉 / 100% Pure Meat
❄️ 冻干锁鲜 / Freeze-Dried Fresh
🌾 无谷配方 / Grain-Free Formula
```

- 使用图标或符号引导
- 中文在前，英文在后，用斜杠"/"分隔
- 或采用上下堆叠，中文在上，英文在下（字号略小）

---

#### 段落文字排版格式：

```
在慵懒的午后，给爱宠一份天然美味。
On a lazy afternoon, give your pet natural deliciousness.

RANOVA冻干零食，用真材实料定义健康零食新标准。
RANOVA freeze-dried snacks redefine healthy treats with real ingredients.
```

- 中文段落和英文段落分别成段
- 英文段落字号略小（约为中文的80-90%）
- 保持行距舒适（1.5-2.0倍行高）

---

#### 按钮/CTA文字格式：

```
立即选购 SHOP NOW →
了解更多 LEARN MORE →
```

- 中英文并列或上下排列
- 箭头符号统一使用 →

---

#### 参数表格式：

```
| 营养成分 Nutrients | 含量 Content |
| 粗蛋白 Crude Protein | ≥42% |
```

- 表头必须中英双语
- 每个参数项都要中英文标注

---

### 3. 每张海报必须包含的元素

✅ **中文提示词**（完整详细，600-1000字）
✅ **英文Prompt**（完整翻译，与中文对应）
✅ **负面词**（Negative Prompts，20-30个关键词）
✅ **详细排版布局说明**（自然融入提示词中）：
- 所有文字的具体位置（左上/右下/居中等）
- 所有文字的字号大小关系（超大/大/中/小）
- 所有文字的颜色（具体色值或描述）
- 所有文字的字体风格（粗衬线/细无衬线/手写体等）
- 所有文字的中英文排版格式（堆叠/并列/分离）

✅ **LOGO位置**（通常左上角，统一位置）
✅ **CTA按钮设计**（位置、文字、样式）

---

### 4. 风格统一原则

- 所有海报必须使用相同的文字排版效果
- 所有海报必须使用相同的配色系统（从产品图提取）
- 所有海报必须保持品牌调性一致
- LOGO在每张海报中位置统一（左上角）
- 中英文排版格式在所有海报中保持一致（选定一种格式后，10张海报都使用）

---

## ⚠️ 严格要求：提示词格式

**排版布局必须自然融入提示词中**，不是独立的技术文档。

### 错误示范（禁止）：
```
中文提示词：
[画面描述]

排版布局：
- 左上角：XXX（太技术化）
- 顶部居中：XXX（像素级描述）

英文 Prompt：
[翻译]
```

### 正确格式（必须）：
```
### 海报01｜主KV·水彩猫咪的幸福时刻

提示词（中文）：
9:16竖版高端艺术海报，水彩插画风格。柔和自然光，温暖奶白色背景带有淡淡水彩晕染（蓝色和黄色渐变边缘）。画面中心：一只精致水彩风格的真实猫咪（英短或橘猫），毛发细腻，大眼睛有神，正享受地吃着冻干鸡肉块（产品实物），猫咪周围飘浮着抽象水彩花瓣和羽毛装饰元素（蓝色、黄色、粉色）。

产品展示（严格还原上传图片）：
朗诺RANOVA冻干鸡肉产品包装袋优雅地放置在猫咪旁边，45度角展示正面设计。必须完整还原包装的所有设计元素：
- 蓝色渐变袋身（#4A90E2主色）
- 正面水彩风格猫咪头像插画（蓝色和黄色晕染）
- 顶部金棕色"RANOVA"品牌LOGO和中文"朗诺"
- 中部白色区域"宠物零食 冻干鸡肉"文字
- 底部图标区域：蓝色"100%纯肉"图标、绿色"无谷物"图标、粉色"不含诱食剂"图标
- 右下角"净含量：300克"标注
- 包装材质：哑光塑料袋，带有自封条

排版布局（中英文双语设计）：
左上角：
- RANOVA水彩logo（小号，约占画面5%宽度）

顶部居中：
- 大标题（水彩笔触质感，中英文堆叠排版）：
  - 第一行："纯肉冻干"（金棕色 #C49A6C，粗衬线字体，字号占画面宽度30%）
  - 第二行："PURE FREEZE-DRIED"（海蓝色 #4A90E2，细衬线字体，字号为中文的60%）
  - 中英文之间间距：中文字号的0.5倍

[...继续排版说明...]

负面词 / Negative:
cluttered, busy, multiple patterns, harsh shadows, watermark, logo repeated, messy text, low quality, blurry, artificial, plastic-looking, cartoon, anime style, wrong packaging design, different colors, modified logo, changed text, simplified design

Prompt (English):
9:16 vertical premium artistic poster, watercolor illustration style. Soft natural lighting, warm off-white background with subtle blue and yellow watercolor wash edges. Center: An exquisite watercolor-style real cat (British Shorthair or orange tabby), fine fur detail, bright expressive eyes, happily eating freeze-dried chicken pieces (actual product), surrounded by abstract watercolor petals and feather decorative elements (blue, yellow, pink).
Product Display (Strictly Restore Uploaded Image):
RANOVA freeze-dried chicken product packaging elegantly placed beside cat, 45-degree angle showing front design. Must completely restore all packaging design elements:
- Blue gradient bag body (#4A90E2 primary color)
- Front watercolor-style cat head illustration (blue and yellow wash)
- Top golden brown "RANOVA" brand logo and Chinese "朗诺"
- Middle white area "Pet Snacks Freeze-Dried Chicken" text
- Bottom icon area: blue "100% Pure Meat" icon, green "Grain-Free" icon, pink "No Attractants" icon
- Bottom-right "Net Weight: 300g" notation
- Packaging material: matte plastic bag with zip-lock
Layout (Bilingual Chinese-English Design):
Top-left:
- RANOVA watercolor logo (small, approximately 5% of canvas width)
Top center:
- Main title (watercolor brush texture, Chinese-English stacked layout):
  - Line 1: "纯肉冻干" (golden brown #C49A6C, bold serif font, size 30% of canvas width)
  - Line 2: "PURE FREEZE-DRIED" (sea blue #4A90E2, thin serif font, size 60% of Chinese text)
  - Spacing between Chinese and English: 0.5x Chinese text size
[...继续排版说明...]

Negative:
cluttered, busy, multiple patterns, harsh shadows, watermark, logo repeated, messy text, low quality, blurry, artificial, plastic-looking, cartoon, anime style, wrong packaging design, different colors, modified logo, changed text, simplified design
```

---

## 📊 最终输出格式（严格按照示例）

**文件格式**：TXT（纯文本）
**文件命名**：`[产品名称]_海报提示词_[数量]张_[风格].txt`
**保存位置**：`/Users/colin/Desktop/`

**输出结构**：

```
【识别报告】
[完整的产品信息识别报告]

推荐视觉风格：[推荐的风格]
推荐文字效果：[推荐的排版效果]
中英文排版格式：[选择的格式A/B/C]

---

### 海报00｜LOGO生成提示词

提示词（中文）：
[LOGO生成的中文提示词，基于识别的品牌设计风格]

负面词 / Negative:
[负面词]

Prompt (English):
[LOGO生成的英文提示词]

Negative:
[负面词]

---

### 海报01｜[标题]

提示词（中文）：
[完整的中文提示词，包含画面描述、产品展示、排版布局等，所有信息自然融合]

负面词 / Negative:
[负面词]

Prompt (English):
[完整的英文提示词，对应中文版本]

Negative:
[负面词]

---

### 海报02｜[标题]

[相同格式]

---

[以此类推，共10张海报]
```

---

## ⚙️ 配置说明

- **输出格式**：9:16 竖版
- **默认模式**：仅生成提示词（不生成图片）✅
- **海报数量**：默认10张，用户可选择
- **语言**：中英文双语
- **输出内容**：中文提示词 + 英文Prompt + 负面词 + 详细排版说明（自然融入提示词中）
- **文件格式**：TXT（严格按照ec-prompt.txt示例格式）✅
- **自动保存**：提示词自动保存到桌面（必须执行）✅

---

## ✅ 验收标准

成功的标志：
- ✅ 严格按照4步流程执行
- ✅ 所有选择由用户决定
- ✅ 生成完整的10张海报提示词系统
- ✅ 每张海报包含：中文提示词、英文Prompt、负面词、详细排版布局说明（自然融入提示词中）
- ✅ 中英文双语排版完整
- ✅ 产品图严格还原要求明确说明
- ✅ 风格统一（配色、排版、品牌调性）
- ✅ 提示词格式严格按照ec-prompt.txt示例
- ✅ **提示词保存为TXT文件到桌面** ✅ **必须执行**

---

## 💡 使用提示词的方式

用户获得提示词后，可以在以下 AI 绘画工具中使用：

### Midjourney
```
[复制英文 Prompt]
--ar 9:16
--v 6.0
```

### Stable Diffusion
```
[复制英文 Prompt]
Negative: [复制负面词]
Steps: 30, Sampler: DPM++ 2M Karras, CFG scale: 7
```

### DALL-E 3
```
[复制完整的中文+英文描述]
```

---

**Skill 状态**: ✅ 已实现
**版本**: 1.1
**最后更新**: 2026-01-15
**维护者**: EC-View System
**说明**: 严格按照ec-prompt.txt格式要求实现
**更新记录**：
- v1.0: 初始版本
- v1.1: 移除海报选择询问步骤，直接生成全部11张海报（包含LOGO生成提示词）✅
