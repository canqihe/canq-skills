#!/usr/bin/env python3
"""
从Google News RSS获取专业财经新闻
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
from urllib.parse import quote

def get_google_news(stock_list):
    """从Google News RSS获取股票相关新闻"""
    # 构建搜索查询 - 需要URL编码
    query = quote(' OR '.join(stock_list))
    rss_url = f"https://news.google.com/rss/search?q={query}+stock&hl=en-US&gl=US&ceid=US:en"

    print(f"正在获取新闻...")
    print(f"URL: {rss_url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(rss_url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"请求失败: {response.status_code}")
            return []

        # 解析XML
        root = ET.fromstring(response.content)

        # 命名空间
        namespaces = {
            'atom': 'http://www.w3.org/2005/Atom',
            'media': 'http://search.yahoo.com/mrss/'
        }

        items = []
        now = datetime.now(pytz.UTC)

        # 遍历所有item
        for item in root.findall('.//item', namespaces):
            try:
                title_elem = item.find('title')
                link_elem = item.find('link')
                pub_date_elem = item.find('pubDate')
                source_elem = item.find('source')

                if title_elem is None or link_elem is None:
                    continue

                title = title_elem.text
                link = link_elem.text

                # 解析发布时间
                if pub_date_elem is not None and pub_date_elem.text:
                    try:
                        pub_date = datetime.strptime(pub_date_elem.text, '%a, %d %b %Y %H:%M:%S %Z')
                        pub_date = pub_date.replace(tzinfo=pytz.UTC)
                    except:
                        pub_date = now - timedelta(hours=1)
                else:
                    pub_date = now - timedelta(hours=1)

                hours_ago = int((now - pub_date).total_seconds() / 3600)

                # 只显示最近48小时的新闻
                if hours_ago > 48:
                    continue

                # 确定相关股票
                related_stocks = []
                title_upper = title.upper()
                for stock in stock_list:
                    if stock in title_upper:
                        related_stocks.append(stock)

                if not related_stocks:
                    continue

                # 判断影响程度
                high_keywords = ['earnings', 'revenue', 'profit', 'loss', 'guidance', 'layoff',
                               'acquisition', 'merger', 'sec', 'investigation', 'lawsuit',
                               '财报', '营收', '利润', '收购', '裁员', '调查']
                medium_keywords = ['launch', 'product', 'partnership', 'deal', 'analyst',
                                 'upgrade', 'downgrade', 'target', 'forecast',
                                 '发布', '合作', '分析师', '评级', '目标价']

                title_lower = title.lower()
                if any(k in title_lower for k in high_keywords):
                    impact = "高"
                elif any(k in title_lower for k in medium_keywords):
                    impact = "中"
                else:
                    impact = "低"

                # 提取来源
                if source_elem is not None:
                    publisher = source_elem.text
                else:
                    # 从link中提取域名
                    if 'reuters.com' in link:
                        publisher = 'Reuters'
                    elif 'bloomberg.com' in link:
                        publisher = 'Bloomberg'
                    elif 'wsj.com' in link:
                        publisher = 'WSJ'
                    elif 'cnbc.com' in link:
                        publisher = 'CNBC'
                    elif 'yahoo.com' in link:
                        publisher = 'Yahoo Finance'
                    else:
                        publisher = 'News'

                items.append({
                    'title': title,
                    'link': link,
                    'publisher': publisher,
                    'related': related_stocks,
                    'impact': impact,
                    'hours_ago': hours_ago,
                    'pub_date': pub_date
                })

            except Exception as e:
                print(f"解析单条新闻失败: {e}")
                continue

        # 按影响程度和时间排序
        impact_order = {'高': 0, '中': 1, '低': 2}
        items.sort(key=lambda x: (impact_order.get(x['impact'], 3), x['hours_ago']))

        print(f"\n成功获取 {len(items)} 条相关新闻:")
        for item in items[:10]:
            time_str = f"{item['hours_ago']}h前" if item['hours_ago'] > 0 else "刚刚"
            print(f"  [{item['impact']}] {time_str} - {item['title'][:60]}...")
            print(f"      来源: {item['publisher']} | 关联: {', '.join(item['related'])}")

        return items

    except Exception as e:
        print(f"获取新闻失败: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    stocks = ['NVDA', 'TSLA', 'GOOGL', 'MU', 'HOOD', 'RKLB', 'CRWD']
    news = get_google_news(stocks)
