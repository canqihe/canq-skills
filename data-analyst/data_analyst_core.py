#!/usr/bin/env python3
"""
AI Data Analyst Skill - Core Analysis Engine (GLM版本)
支持交互式数据分析，通过自然语言查询 CSV/Excel 文件
使用智谱 GLM-4 模型
"""

import os
import sys
import json
import pickle
import tempfile
import csv
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import duckdb
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import seaborn as sns
from zhipuai import ZhipuAI

# 配置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 会话和输出目录
SESSION_DIR = Path.home() / '.claude' / 'skills' / 'data-analyst' / 'session'
OUTPUT_DIR = Path.home() / 'data_analysis_output'
SESSION_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SESSION_FILE = SESSION_DIR / 'current_session.pkl'


def preprocess_file(file_path):
    """预处理数据文件"""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return None, None, None, f"文件不存在: {file_path}"

        # 读取文件
        if file_path.suffix.lower() == '.csv':
            df = pd.read_csv(file_path, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, na_values=['NA', 'N/A', 'missing'])
        else:
            return None, None, None, "不支持的文件格式，请上传 CSV 或 Excel 文件"

        # 字符串列处理
        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)

        # 日期和数值列处理
        for col in df.columns:
            if 'date' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
            elif df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    pass

        # 保存为临时 CSV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_path = temp_file.name
            df.to_csv(temp_path, index=False, quoting=csv.QUOTE_ALL)

        return temp_path, df.columns.tolist(), df, None
    except Exception as e:
        return None, None, None, f"处理文件时出错: {e}"


def save_session(temp_path, columns, df_info, api_key):
    """保存会话状态"""
    session_data = {
        'temp_path': temp_path,
        'columns': columns,
        'df_info': {
            'shape': df_info.shape,
            'dtypes': df_info.dtypes.astype(str).to_dict(),
            'head': df_info.head(3).to_dict(),
            'description': df_info.describe().to_dict() if len(df_info.describe()) > 0 else {}
        },
        'created_at': datetime.now().isoformat()
    }
    with open(SESSION_FILE, 'wb') as f:
        pickle.dump(session_data, f)
    return session_data


def load_session():
    """加载会话状态"""
    if SESSION_FILE.exists():
        with open(SESSION_FILE, 'rb') as f:
            return pickle.load(f)
    return None


def get_data_schema(temp_path, columns):
    """获取数据结构信息，用于生成 SQL"""
    try:
        conn = duckdb.connect()
        conn.execute(f"CREATE TABLE uploaded_data AS SELECT * FROM read_csv('{temp_path}')")

        # 获取表结构
        schema_info = conn.execute("DESCRIBE uploaded_data").fetchall()

        # 获取示例数据
        sample_data = conn.execute("SELECT * FROM uploaded_data LIMIT 3").fetchdf()

        conn.close()

        schema_desc = "数据表 uploaded_data 的结构：\n"
        schema_desc += f"列名: {', '.join(columns)}\n\n"
        schema_desc += "字段详情:\n"
        for col in schema_info:
            schema_desc += f"  - {col[0]} ({col[1]})\n"

        schema_desc += f"\n示例数据（前3行）:\n{sample_data.to_string()}\n"

        return schema_desc
    except Exception as e:
        return f"获取数据结构失败: {e}"


def generate_sql_with_glm(query, data_schema, api_key):
    """使用 GLM 生成 SQL 查询"""
    try:
        client = ZhipuAI(api_key=api_key)

        system_prompt = f"""你是一个专业的数据分析师。你的任务是将用户的自然语言问题转换为 DuckDB SQL 查询。

{data_schema}

重要规则：
1. 表名固定为 'uploaded_data'
2. 只返回 SQL 查询语句，不要任何解释
3. 使用 DuckDB 语法
4. 如果涉及聚合，使用清晰的列名
5. 日期格式使用 ISO 8601

示例：
用户: "销售额最高的5个产品"
SQL: SELECT product_name, SUM(sales) as total_sales FROM uploaded_data GROUP BY product_name ORDER BY total_sales DESC LIMIT 5;

用户: "按地区统计平均销售额"
SQL: SELECT region, AVG(sales) as avg_sales FROM uploaded_data GROUP BY region;
"""

        response = client.chat.completions.create(
            model="glm-4-flash",  # 使用 GLM-4-Flash (快速且经济)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请为以下问题生成 SQL: {query}"}
            ],
            temperature=0.1,
            max_tokens=500
        )

        sql_query = response.choices[0].message.content.strip()

        # 清理可能的 markdown 标记
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()

        return sql_query, None
    except Exception as e:
        return None, f"GLM API 调用失败: {e}"


def execute_sql(sql_query, temp_path):
    """执行 SQL 查询"""
    try:
        conn = duckdb.connect()
        conn.execute(f"CREATE OR REPLACE VIEW uploaded_data AS SELECT * FROM read_csv('{temp_path}')")

        result_df = conn.execute(sql_query).fetchdf()
        conn.close()

        return result_df, None
    except Exception as e:
        return None, f"SQL 执行失败: {e}"


def interpret_results_with_glm(query, result_df, api_key):
    """使用 GLM 解读查询结果"""
    try:
        client = ZhipuAI(api_key=api_key)

        result_text = f"查询结果:\n{result_df.to_string(index=False)}\n\n"
        result_text += f"共 {len(result_df)} 行数据"

        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "system", "content": "你是一个数据分析师，用简洁易懂的中文解读数据查询结果。"},
                {"role": "user", "content": f"用户问题: {query}\n\n{result_text}\n\n请用中文解读这个结果。"}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        interpretation = response.choices[0].message.content
        return interpretation
    except Exception as e:
        return f"结果解读失败: {e}"


def create_visualization(result_df, query):
    """根据查询结果生成可视化"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    charts_created = []

    try:
        # 检查数据是否适合可视化
        if len(result_df) == 0:
            return charts_created

        # 确定图表类型
        numeric_cols = result_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = result_df.select_dtypes(include=['object']).columns.tolist()

        # 场景1: 有分组和数值（柱状图）
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:
            fig, ax = plt.subplots(figsize=(12, 6))

            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]

            # 限制显示数量
            if len(result_df) > 20:
                plot_df = result_df.head(20)
                title_suffix = f"（前20名，共{len(result_df)}条）"
            else:
                plot_df = result_df
                title_suffix = ""

            plot_df.plot(kind='bar', x=cat_col, y=num_col, ax=ax, color='steelblue')
            ax.set_xlabel(cat_col, fontsize=12)
            ax.set_ylabel(num_col, fontsize=12)
            ax.set_title(f'{query}', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            chart_path = OUTPUT_DIR / f'bar_chart_{timestamp}.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            charts_created.append(str(chart_path))

        # 场景2: 时间序列（如果有日期列）
        elif any('date' in col.lower() or 'time' in col.lower() or '日期' in col or '时间' in col
                 for col in result_df.columns):
            date_col = None
            for col in result_df.columns:
                if 'date' in col.lower() or 'time' in col.lower() or '日期' in col or '时间' in col:
                    date_col = col
                    break

            if date_col and len(numeric_cols) > 0:
                fig, ax = plt.subplots(figsize=(12, 6))
                num_col = numeric_cols[0]

                result_df_sorted = result_df.sort_values(date_col)
                ax.plot(result_df_sorted[date_col], result_df_sorted[num_col],
                       marker='o', linewidth=2, markersize=6)
                ax.set_xlabel(date_col, fontsize=12)
                ax.set_ylabel(num_col, fontsize=12)
                ax.set_title(f'{query}', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()

                chart_path = OUTPUT_DIR / f'line_chart_{timestamp}.png'
                plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                plt.close()
                charts_created.append(str(chart_path))

        # 场景3: 只有数值列（直方图）
        elif len(numeric_cols) >= 1:
            fig, ax = plt.subplots(figsize=(10, 6))
            num_col = numeric_cols[0]

            ax.hist(result_df[num_col].dropna(), bins=20, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_xlabel(num_col, fontsize=12)
            ax.set_ylabel('频数', fontsize=12)
            ax.set_title(f'{query} - 分布', fontsize=14, fontweight='bold')
            plt.tight_layout()

            chart_path = OUTPUT_DIR / f'histogram_{timestamp}.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            charts_created.append(str(chart_path))

    except Exception as e:
        print(f"[可视化] 生成图表时出错: {e}", file=sys.stderr)

    return charts_created


def generate_html_report(query, sql_query, result_df, interpretation, charts):
    """生成 HTML 报告"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>数据分析报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .meta {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
        .query {{ background: #e3f2fd; padding: 15px; border-left: 4px solid #2196F3; border-radius: 4px; margin: 20px 0; }}
        .sql {{ background: #f5f5f5; padding: 15px; border-radius: 4px; font-family: 'Courier New', monospace; font-size: 13px; overflow-x: auto; }}
        .response {{ background: #fff9e6; padding: 20px; border-radius: 8px; margin: 20px 0; line-height: 1.8; }}
        .chart {{ text-align: center; margin: 30px 0; }}
        .chart img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; font-weight: 600; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 数据分析报告</h1>
        <div class="meta">生成时间: {timestamp}</div>

        <h2>❓ 你的问题</h2>
        <div class="query"><strong>{query}</strong></div>

        <h2>🔍 生成的 SQL 查询</h2>
        <div class="sql"><code>{sql_query}</code></div>

        <h2>📈 查询结果</h2>
        <table>
            <tr>
                {"".join(f"<th>{col}</th>" for col in result_df.columns)}
            </tr>
"""

    # 添加数据行（限制前50行）
    for _, row in result_df.head(50).iterrows():
        html_content += "<tr>"
        for val in row:
            html_content += f"<td>{val}</td>"
        html_content += "</tr>"

    html_content += """
        </table>
"""

    if len(result_df) > 50:
        html_content += f"<p><em>（仅显示前50行，共 {len(result_df)} 行数据）</em></p>"

    html_content += f"""
        <h2>💡 AI 解读</h2>
        <div class="response">{interpretation.replace(chr(10), '<br>')}</div>
"""

    if charts:
        html_content += "<h2>📊 可视化图表</h2>"
        for chart_path in charts:
            chart_name = Path(chart_path).name
            # 复制图表到输出目录（如果还没在那里）
            html_content += f"""
            <div class="chart">
                <img src="{chart_name}" alt="图表">
                <p><em>{chart_name}</em></p>
            </div>
            """

    html_content += """
    </div>
</body>
</html>
    """

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_path = OUTPUT_DIR / f'analysis_report_{timestamp}.html'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return html_path


def run_analysis(query, api_key, session_data=None):
    """执行数据分析查询"""
    try:
        # 检查会话
        if not session_data or not session_data.get('temp_path'):
            return None, None, None, "没有找到数据文件，请先使用 upload 命令上传文件"

        temp_path = session_data['temp_path']
        columns = session_data['columns']

        print("  📋 正在分析数据结构...")
        data_schema = get_data_schema(temp_path, columns)

        print("  🤖 使用 GLM 生成 SQL...")
        sql_query, error = generate_sql_with_glm(query, data_schema, api_key)
        if error:
            return None, None, None, error

        print(f"  ✓ SQL: {sql_query[:100]}...")

        print("  📊 执行查询...")
        result_df, error = execute_sql(sql_query, temp_path)
        if error:
            return None, None, None, error

        print(f"  ✓ 返回 {len(result_df)} 行结果")

        print("  💡 AI 解读结果...")
        interpretation = interpret_results_with_glm(query, result_df, api_key)

        print("  📈 生成可视化...")
        charts = create_visualization(result_df, query)

        return sql_query, result_df, interpretation, charts, None

    except Exception as e:
        return None, None, None, None, f"分析出错: {e}"


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("="*60)
        print("📊 AI 数据分析师 (GLM版本)")
        print("="*60)
        print("\n使用方法:")
        print("  上传文件:")
        print("    python data_analyst_core.py upload <文件路径> \"<问题>\" --api-key <GLM_API_KEY>")
        print("\n  继续提问:")
        print("    python data_analyst_core.py query \"<问题>\" --api-key <GLM_API_KEY>")
        print("\n示例:")
        print("    python data_analyst_core.py upload data.csv \"销售额最高的10个产品\" --api-key xxx")
        sys.exit(1)

    command = sys.argv[1].lower()
    api_key = None

    # 解析 API Key
    for i, arg in enumerate(sys.argv):
        if arg == '--api-key' and i + 1 < len(sys.argv):
            api_key = sys.argv[i + 1]
            break

    if not api_key:
        print("❌ 错误: 请提供 --api-key 参数")
        print("获取 GLM API Key: https://open.bigmodel.cn/")
        sys.exit(1)

    # 上传文件命令
    if command == 'upload':
        if len(sys.argv) < 4:
            print("用法: python data_analyst_core.py upload <文件路径> \"<问题>\" --api-key <API_KEY>")
            sys.exit(1)

        file_path = sys.argv[2]
        query = sys.argv[3]

        print(f"📊 正在处理文件: {file_path}")
        temp_path, columns, df, error = preprocess_file(file_path)

        if error:
            print(f"❌ {error}")
            sys.exit(1)

        print(f"✅ 文件加载成功")
        print(f"   - 数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")
        print(f"   - 列名: {', '.join(columns)}")

        # 保存会话
        session_data = save_session(temp_path, columns, df, api_key)
        print(f"💾 会话已保存")

        # 执行分析
        print(f"\n🔍 正在分析: {query}")
        sql_query, result_df, interpretation, charts, error = run_analysis(query, api_key, session_data)

        if error:
            print(f"❌ {error}")
            sys.exit(1)

        # 显示结果
        print("\n" + "="*60)
        print("📈 分析结果")
        print("="*60)
        print(f"\n{interpretation}\n")
        print("数据表格:")
        print(result_df.to_string(index=False))
        print("="*60)

        # 生成报告
        html_path = generate_html_report(query, sql_query, result_df, interpretation, charts)
        print(f"\n📄 HTML 报告: {html_path}")

        if charts:
            print(f"📊 图表文件:")
            for chart in charts:
                print(f"   - {chart}")

        print(f"\n💡 继续提问:")
        print(f"   python {sys.argv[0]} query \"<你的问题>\" --api-key {api_key[:10]}...")

    # 继续查询命令
    elif command == 'query':
        if len(sys.argv) < 3:
            print("用法: python data_analyst_core.py query \"<问题>\" --api-key <API_KEY>")
            sys.exit(1)

        query = sys.argv[2]

        # 加载会话
        session_data = load_session()
        if not session_data:
            print("❌ 没有找到活动会话，请先使用 upload 命令上传文件")
            sys.exit(1)

        print(f"🔍 正在分析: {query}")
        sql_query, result_df, interpretation, charts, error = run_analysis(query, api_key, session_data)

        if error:
            print(f"❌ {error}")
            sys.exit(1)

        # 显示结果
        print("\n" + "="*60)
        print("📈 分析结果")
        print("="*60)
        print(f"\n{interpretation}\n")
        print("数据表格:")
        print(result_df.to_string(index=False))
        print("="*60)

        # 生成报告
        html_path = generate_html_report(query, sql_query, result_df, interpretation, charts)
        print(f"\n📄 HTML 报告: {html_path}")

        if charts:
            print(f"📊 图表文件:")
            for chart in charts:
                print(f"   - {chart}")

    else:
        print(f"❌ 未知命令: {command}")
        print("可用命令: upload, query")
        sys.exit(1)


if __name__ == '__main__':
    main()
