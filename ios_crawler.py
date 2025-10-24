#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS 优化版网络爬虫
专为 iPhone/iPad 的 Pythonista、a-Shell 等应用设计
零依赖 - 仅使用Python标准库
"""

import urllib.request
import urllib.parse
from html.parser import HTMLParser
import json
import sys
from datetime import datetime


class SimpleHTMLParser(HTMLParser):
    """简化的HTML解析器"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.images = []
        self.headings = []
        self._in_title = False
        self._current_heading = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == 'title':
            self._in_title = True
        elif tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        elif tag == 'img' and 'src' in attrs_dict:
            self.images.append(attrs_dict['src'])
        elif tag in ['h1', 'h2', 'h3']:
            self._current_heading = tag

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        elif tag in ['h1', 'h2', 'h3']:
            self._current_heading = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif self._current_heading:
            text = data.strip()
            if text:
                self.headings.append(text)


class IOSCrawler:
    """iOS优化的爬虫类"""

    def __init__(self):
        self.results = []

    def fetch(self, url):
        """获取网页"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                data = response.read()
                try:
                    return data.decode('utf-8')
                except:
                    return data.decode('utf-8', errors='ignore')
        except Exception as e:
            return None

    def parse(self, html, base_url):
        """解析HTML"""
        parser = SimpleHTMLParser()
        try:
            parser.feed(html)
        except:
            pass

        # 处理链接
        links = []
        for link in parser.links[:15]:
            try:
                full_url = urllib.parse.urljoin(base_url, link)
                if full_url.startswith('http'):
                    links.append(full_url)
            except:
                pass

        return {
            'title': parser.title or '无标题',
            'links': links,
            'images': len(parser.images),
            'headings': parser.headings[:10]
        }

    def crawl(self, url):
        """爬取单个URL"""
        if not url.startswith('http'):
            url = 'http://' + url

        print(f"\n{'='*50}")
        print(f"📱 正在爬取: {url}")
        print(f"{'='*50}\n")

        html = self.fetch(url)

        if not html:
            print("❌ 获取失败\n")
            return None

        data = self.parse(html, url)

        # 显示结果
        print(f"✅ 标题: {data['title']}")
        print(f"🔗 链接数: {len(data['links'])}")
        print(f"🖼️  图片数: {data['images']}")

        if data['headings']:
            print(f"\n📋 主要标题:")
            for i, h in enumerate(data['headings'][:5], 1):
                print(f"  {i}. {h}")

        if data['links']:
            print(f"\n🔗 发现的链接:")
            for i, link in enumerate(data['links'][:10], 1):
                # 缩短显示
                display = link if len(link) < 50 else link[:47] + '...'
                print(f"  {i}. {display}")

        print(f"\n{'='*50}\n")

        result = {
            'url': url,
            'time': datetime.now().isoformat(),
            'data': data
        }

        self.results.append(result)
        return result

    def save_json(self, filename='crawler_results.json'):
        """保存为JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"💾 已保存到: {filename}")


def interactive_mode():
    """交互模式 - 适合手机使用"""
    crawler = IOSCrawler()

    print("\n" + "="*50)
    print("📱 iOS 网络爬虫")
    print("="*50)
    print("\n提示: 输入 'q' 退出, 's' 保存结果\n")

    while True:
        try:
            url = input("🔍 输入URL (或命令): ").strip()

            if not url:
                continue

            if url.lower() == 'q':
                print("\n👋 再见!")
                break

            if url.lower() == 's':
                if crawler.results:
                    crawler.save_json()
                else:
                    print("⚠️  暂无结果可保存")
                continue

            if url.lower() == 'h' or url == '?':
                print("\n📖 帮助:")
                print("  - 直接输入URL开始爬取")
                print("  - 's' = 保存结果到JSON")
                print("  - 'q' = 退出程序")
                print("  - 'demo' = 运行演示\n")
                continue

            if url.lower() == 'demo':
                demo_urls = [
                    'http://example.com',
                    'http://localhost:8000'
                ]
                print("\n选择演示URL:")
                for i, u in enumerate(demo_urls, 1):
                    print(f"  {i}. {u}")

                choice = input("\n选择 (1-2): ").strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(demo_urls):
                        url = demo_urls[idx]
                    else:
                        continue
                except:
                    continue

            # 爬取
            crawler.crawl(url)

        except KeyboardInterrupt:
            print("\n\n👋 已中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")

    # 退出时询问是否保存
    if crawler.results:
        save = input("\n💾 保存结果? (y/n): ").strip().lower()
        if save == 'y':
            crawler.save_json()


def quick_crawl(url):
    """快速爬取单个URL"""
    crawler = IOSCrawler()
    result = crawler.crawl(url)

    if result:
        save = input("\n💾 保存结果? (y/n): ").strip().lower()
        if save == 'y':
            crawler.save_json()


def batch_crawl(urls):
    """批量爬取"""
    crawler = IOSCrawler()

    print(f"\n📋 批量爬取 {len(urls)} 个URL\n")

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}]")
        crawler.crawl(url)

    crawler.save_json()
    print(f"\n✅ 完成! 共爬取 {len(crawler.results)} 个页面")


def main():
    """主函数"""

    # 检查命令行参数
    if len(sys.argv) > 1:
        url = sys.argv[1]

        # 批量模式
        if len(sys.argv) > 2:
            urls = sys.argv[1:]
            batch_crawl(urls)
        else:
            quick_crawl(url)
    else:
        # 交互模式
        interactive_mode()


# 为Pythonista等应用提供的快捷函数
def crawl(url):
    """
    快捷函数 - 爬取单个URL

    用法:
        import ios_crawler
        ios_crawler.crawl('http://example.com')
    """
    quick_crawl(url)


def crawl_multiple(*urls):
    """
    快捷函数 - 爬取多个URL

    用法:
        import ios_crawler
        ios_crawler.crawl_multiple('url1', 'url2', 'url3')
    """
    batch_crawl(list(urls))


if __name__ == "__main__":
    main()
