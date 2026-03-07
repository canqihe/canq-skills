#!/usr/bin/env python3
"""
Podcast Article Generator
将访谈内容制作成网页并集成到 yt-podcast 项目
"""

import re
import os
from pathlib import Path
from datetime import datetime

# 项目路径配置
PROJECT_ROOT = Path("/Users/colin/yt-podcast")
DESIGN_SYSTEM = PROJECT_ROOT / "design-system"
ARTICLES_DIR = PROJECT_ROOT / "articles"
INDEX_FILE = PROJECT_ROOT / "index.html"

# 设计系统CSS引用
CSS_LINKS = """    <link rel="stylesheet" href="../design-system/design-tokens.css">
    <link rel="stylesheet" href="../design-system/style.css">"""


class PodcastArticleGenerator:
    """播客文章生成器"""

    def __init__(self, markdown_file: str):
        self.markdown_file = Path(markdown_file)
        self.content = self._read_markdown()
        self.metadata = self._extract_metadata()
        self.sections = self._extract_sections()

    def _read_markdown(self) -> str:
        """读取Markdown文件"""
        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_metadata(self) -> dict:
        """从Markdown中提取元数据"""
        metadata = {
            'title': '',
            'author': '',
            'host': '',
            'guest': '',
            'duration': '',
            'video_url': '',
            'category': 'Podcast',
            'tags': []
        }

        lines = self.content.split('\n')
        for line in lines:
            if line.startswith('# **'):
                # 提取主标题
                metadata['title'] = line.replace('# **', '').replace('**', '').strip()
            elif '标题' in line and '：' in line:
                metadata['title'] = line.split('：', 1)[1].split('(')[0].strip()
            elif '作者' in line or '主持人' in line：
                if '：' in line or ':' in line:
                    metadata['host'] = line.split('：', 1)[-1].split(':', 1)[-1].strip()
            elif '嘉宾' in line or 'Guest' in line：
                if '：' in line or ':' in line:
                    metadata['guest'] = line.split('：', 1)[-1].split(':', 1)[-1].strip()
            elif '时长' in line or 'Duration' in line:
                # 提取时长格式 HH:MM:SS
                time_match = re.search(r'(\d{1,2}:\d{2}:\d{2})', line)
                if time_match:
                    metadata['duration'] = time_match.group(1)
            elif '链接' in line or 'Link' in line or 'http' in line:
                url_match = re.search(r'https?://[^\s\)]+', line)
                if url_match:
                    metadata['video_url'] = url_match.group(0)

        return metadata

    def _extract_sections(self) -> list:
        """提取章节内容"""
        sections = []
        lines = self.content.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            # 匹配章节标题（带时间戳）
            section_match = re.match(r'###\s*\*\*(.+?)\*\*\s*\[([0-9:]+)-([0-9:]+)\]', line)
            if section_match:
                # 保存上一节
                if current_section:
                    current_section['content'] = '\n'.join(current_content).strip()
                    sections.append(current_section)

                # 开始新节
                current_section = {
                    'title': section_match.group(1).strip(),
                    'start_time': section_match.group(2),
                    'end_time': section_match.group(3),
                    'content': ''
                }
                current_content = []
            elif current_section:
                current_content.append(line)
            elif line.startswith('###'):
                # 没有时间戳的章节
                if current_section:
                    current_section['content'] = '\n'.join(current_content).strip()
                    sections.append(current_section)

                title = line.replace('###', '').replace('**', '').strip()
                current_section = {
                    'title': title,
                    'start_time': '',
                    'end_time': '',
                    'content': ''
                }
                current_content = []
            else:
                if current_section is None and line.strip():
                    # 在第一个章节之前的内容
                    pass

        # 保存最后一节
        if current_section:
            current_section['content'] = '\n'.join(current_content).strip()
            sections.append(current_section)

        return sections

    def generate_filename(self) -> str:
        """生成文件名"""
        # 基于标题或嘉宾姓名生成
        title = self.metadata.get('title', '')
        guest = self.metadata.get('guest', '')

        # 清理和转换
        if guest:
            name_part = guest.lower()
            # 移除头衔
            name_part = re.sub(r'\s+(ceo|founder|partner|dr\.|prof\.)', '', name_part, flags=re.IGNORECASE)
            name_part = re.sub(r'[^\w\s-]', '', name_part)
            name_part = '-'.join(name_part.split())

        # 从标题提取关键词
        title_part = title.lower()
        title_part = re.sub(r'[^\w\s-]', '', title_part)
        title_words = title_part.split()[:3]  # 取前3个词
        title_part = '-'.join(title_words)

        if guest:
            return f"{title_part}-{name_part}.html"
        return f"{title_part}.html"

    def generate_html(self) -> str:
        """生成HTML内容"""
        # 这里返回HTML模板字符串
        # 实际实现中，会根据self.metadata和self.sections生成完整的HTML
        return self._build_html_template()

    def _build_html_template(self) -> str:
        """构建HTML模板"""
        # TODO: 实现完整的HTML生成逻辑
        # 这是一个框架，实际使用时由AI来填充具体内容
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.metadata.get('title', '文章标题'}</title>
{CSS_LINKS}
</head>
<body>
    <!-- 内容将由AI根据设计系统生成 -->
</body>
</html>"""

    def save_to_file(self, output_path: str = None) -> str:
        """保存到文件"""
        if output_path is None:
            filename = self.generate_filename()
            output_path = ARTICLES_DIR / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_html())

        return str(output_path)


def update_index_html(article_info: dict):
    """
    更新index.html，添加新文章卡片

    Args:
        article_info: 文章信息字典
            - filename: HTML文件名
            - title: 文章标题
            - category: 分类
            - date: 日期
            - excerpt: 摘要
            - tags: 标签列表
            - reading_time: 阅读时间（分钟）
            - card_class: 卡片样式类 (card-ai, card-finance, etc.)
    """
    # 读取index.html
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 生成文章卡片HTML
    card_html = f"""                <!-- Card: {article_info['title']} (NEWEST) -->
                <a href="articles/{article_info['filename']}" class="article-card {article_info['card_class']} reveal" target="_blank" rel="noopener">
                    <div class="card-header">
                        <span class="card-category">{article_info['category']}</span>
                        <span class="card-meta">{article_info['date']}</span>
                    </div>
                    <h3 class="card-title">{article_info['title']}</h3>
                    <p class="card-excerpt">
                        {article_info['excerpt']}
                    </p>
                    <div class="card-tags">
                        {"".join(f'<span class="card-tag">#{tag}</span>' for tag in article_info['tags'])}
                    </div>
                    <div class="card-footer">
                        <span class="read-link">
                            阅读全文
                            <span class="read-arrow">→</span>
                        </span>
                        <span class="card-stat">⏱ 约 {article_info['reading_time']} 分钟</span>
                    </div>
                </a>
"""

    # 在 articles-grid 后插入卡片
    grid_pattern = r'(<div class="articles-grid">)'
    replacement = r'\1\n' + card_html
    content = re.sub(grid_pattern, replacement, content, count=1)

    # 更新文章计数
    count_pattern = r'已收录 <span class="count-highlight">(\d+)</span> 篇深度洞察'
    current_count = int(re.search(count_pattern, content).group(1))
    new_count = current_count + 1
    content = re.sub(count_pattern, f'已收录 <span class="count-highlight">{new_count}</span> 篇深度洞察', content)

    # 写回文件
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 已更新首页，文章计数: {current_count} → {new_count}")


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python podcast_generator.py <markdown_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]

    # 生成文章
    generator = PodcastArticleGenerator(markdown_file)
    output_path = generator.save_to_file()

    print(f"✅ 文章已生成: {output_path}")
    print(f"   标题: {generator.metadata.get('title')}")
    print(f"   嘉宾: {generator.metadata.get('guest')}")


if __name__ == '__main__':
    main()
