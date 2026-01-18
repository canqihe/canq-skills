---
name: z-image
description: Z-Image 图像生成 Skill - 使用 ModelScope API 生成 AI 图像，支持异步轮询和自动下载
---

# Z-Image 图像生成 Skill

**版本**: 1.0
**领域**: AI 图像生成
**架构**: Python Wrapper
**数据源**: ModelScope API

## 核心功能

使用 ModelScope API 生成 AI 图像：
- 支持多种图像生成模型（默认：Tongyi-MAI/Z-Image-Turbo）
- 异步任务轮询机制
- 自动下载和保存生成的图像
- 安全的 API key 管理（配置文件优先）

---

## 使用方式

### 快速开始

1. **首次使用 - 初始化配置**：
   ```bash
   python scripts/run.py generate.py --setup
   ```
   这将在 skill 目录下创建 `config.json`，请填入你的 API key。

2. **生成图像**：
   ```
   生成一张金猫的图片
   ```

3. **指定模型和文件名**：
   ```
   生成一张日落风景的图片，使用 Z-Image-Turbo 模型，保存为 sunset.jpg
   ```

---

## 命令行接口

```bash
# 基本使用
python scripts/run.py generate.py --prompt "A golden cat"

# 指定模型
python scripts/run.py generate.py --prompt "..." --model "Tongyi-MAI/Z-Image-Turbo"

# 指定输出文件名
python scripts/run.py generate.py --prompt "..." --filename "my_image.jpg"

# 使用命令行传入 API key（不推荐）
python scripts/run.py generate.py --prompt "..." --api-key "your-key"

# 初始化配置文件
python scripts/run.py generate.py --setup
```

---

## 配置文件

`config.json` 格式：
```json
{
  "api_key": "ms-xxxxx-xxxxx-xxxxx",
  "default_model": "Tongyi-MAI/Z-Image-Turbo",
  "output_dir": "/Users/xxx/Desktop"
}
```

**默认输出位置**：用户桌面 (`~/Desktop`)

**API Key 优先级**：
1. 命令行参数 `--api-key`
2. 配置文件 `config.json`
3. 环境变量 `MODELSCOPE_API_KEY`

---

## 工作流程

```
用户请求
    ↓
Claude Code 调用 skill
    ↓
解析参数（prompt, model, filename）
    ↓
读取 API Key（配置文件/环境变量）
    ↓
调用 ModelScope API
    ↓
轮询任务状态（每 5 秒）
    ↓
下载图像到桌面
    ↓
返回图像路径
```

---

## 支持的模型

- `Tongyi-MAI/Z-Image-Turbo`（默认）
- 其他 ModelScope 图像生成模型

---

## 输出示例

**输入**: `生成一张金猫的图片`

**输出**:
```
✅ 图像生成成功！
📁 保存路径: /Users/xxx/Desktop/result_image_20250115_123456.jpg
```

---

## 技术说明

- **异步模式**: 使用 `X-ModelScope-Async-Mode: true` 头部
- **轮询间隔**: 每 5 秒检查一次任务状态
- **超时处理**: 无超时限制，直到任务完成或失败
- **图像格式**: 保存为 JPG 格式

---

**Skill 状态**: ✅ 已实现
**注意**: 暂不支持 LoRA 功能
