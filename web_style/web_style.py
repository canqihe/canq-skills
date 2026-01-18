#!/usr/bin/env python3
"""
网站设计风格选择器
从 styles 目录读取21种设计风格
"""

import os
import json
from pathlib import Path

# 获取脚本所在目录的 styles 子目录
SCRIPT_DIR = Path(__file__).parent
STYLE_DIR = SCRIPT_DIR / "styles"


def get_all_styles():
    """获取所有设计风格的名称和描述"""
    styles = []

    for file_path in sorted(STYLE_DIR.glob("*.txt")):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    name = lines[0].strip()
                    # 跳过空行,找到第一个非空行作为描述
                    description = ""
                    for i in range(1, len(lines)):
                        line = lines[i].strip()
                        if line and not line.startswith("<"):
                            description = line
                            break
                    styles.append({
                        "name": name,
                        "description": description,
                        "filename": file_path.name
                    })
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=os.sys.stderr)

    return styles


def get_style_prompt(style_filename):
    """获取完整的设计风格prompt（包括role和design-system）"""
    file_path = STYLE_DIR / style_filename

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 查找 "Prompt:" 标记
        if "Prompt:" in content:
            prompt_start = content.find("Prompt:") + len("Prompt:")
            return content[prompt_start:].strip()
        else:
            # 如果没有Prompt:标记，返回前两行之后的所有内容
            lines = content.split("\n")
            return "\n".join(lines[2:]).strip()
    except Exception as e:
        return f"Error reading file: {e}"


def format_style_list():
    """格式化风格列表用于展示"""
    styles = get_all_styles()
    output = ["## 选择您喜欢的设计风格\n"]

    for i, style in enumerate(styles, 1):
        output.append(f"{i}. **{style['name']}**")
        output.append(f"   {style['description']}")
        output.append("")

    return "\n".join(output)


def find_style_by_name(name_input):
    """根据用户输入的风格名称查找对应的文件"""
    styles = get_all_styles()

    # 精确匹配
    for style in styles:
        if name_input.lower() == style['name'].lower():
            return style['filename'], style['name']

    # 模糊匹配
    for style in styles:
        if name_input.lower() in style['name'].lower():
            return style['filename'], style['name']

    # 按数字匹配
    if name_input.isdigit():
        index = int(name_input) - 1
        if 0 <= index < len(styles):
            return styles[index]['filename'], styles[index]['name']

    return None, None


def main():
    """主函数 - 支持命令行调用"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            print(format_style_list())
        elif command == "get":
            if len(sys.argv) > 2:
                filename = sys.argv[2]
                print(get_style_prompt(filename))
            else:
                print("Usage: python web_style.py get <filename>")
        elif command == "find":
            if len(sys.argv) > 2:
                name_input = sys.argv[2]
                filename, style_name = find_style_by_name(name_input)
                if filename:
                    print(f"Found: {style_name} -> {filename}")
                    print("\n" + get_style_prompt(filename))
                else:
                    print(f"Style '{name_input}' not found.")
            else:
                print("Usage: python web_style.py find <style_name>")
        elif command == "json":
            styles = get_all_styles()
            print(json.dumps(styles, ensure_ascii=False, indent=2))
        else:
            print("Usage:")
            print("  python web_style.py list          # 列出所有风格")
            print("  python web_style.py get <file>    # 获取特定风格的完整prompt")
            print("  python web_style.py find <name>   # 根据名称查找风格")
            print("  python web_style.py json          # 输出JSON格式的风格列表")
    else:
        print(format_style_list())


if __name__ == "__main__":
    main()
