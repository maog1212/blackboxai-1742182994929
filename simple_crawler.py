#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的网络爬虫示例
A Simple Web Crawler Example
"""

import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import os


class SimpleCrawler:
    """简单的网络爬虫类"""

    def __init__(self, base_url, max_pages=10, delay=1):
        """
        初始化爬虫

        Args:
            base_url: 起始URL
            max_pages: 最大爬取页面数
            delay: 请求间隔时间（秒），遵守爬虫礼仪
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls = set()
        self.to_visit = [base_url]

        # 设置请求头，模拟浏览器访问
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def is_valid_url(self, url):
        """检查URL是否有效且属于同一域名"""
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)

        # 只爬取同一域名下的页面
        return parsed_url.netloc == parsed_base.netloc

    def get_page_content(self, url):
        """
        获取页面内容

        Args:
            url: 要爬取的URL

        Returns:
            BeautifulSoup对象，如果失败返回None
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding

            return BeautifulSoup(response.text, 'html.parser')

        except requests.RequestException as e:
            print(f"❌ 获取页面失败 {url}: {e}")
            return None

    def extract_links(self, soup, current_url):
        """
        从页面中提取所有链接

        Args:
            soup: BeautifulSoup对象
            current_url: 当前页面URL

        Returns:
            链接列表
        """
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            # 将相对URL转换为绝对URL
            absolute_url = urljoin(current_url, href)

            # 只添加有效的URL
            if self.is_valid_url(absolute_url):
                links.append(absolute_url)

        return links

    def extract_data(self, soup, url):
        """
        从页面中提取数据

        Args:
            soup: BeautifulSoup对象
            url: 页面URL

        Returns:
            提取的数据字典
        """
        # 提取标题
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "无标题"

        # 提取所有段落文本
        paragraphs = [p.get_text().strip() for p in soup.find_all('p')]

        # 提取所有图片
        images = [img.get('src', '') for img in soup.find_all('img')]

        data = {
            'url': url,
            'title': title_text,
            'paragraphs_count': len(paragraphs),
            'images_count': len(images),
            'images': images[:5]  # 只显示前5张图片
        }

        return data

    def save_to_file(self, data, filename='crawler_results.txt'):
        """保存爬取结果到文件"""
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"URL: {data['url']}\n")
            f.write(f"标题: {data['title']}\n")
            f.write(f"段落数: {data['paragraphs_count']}\n")
            f.write(f"图片数: {data['images_count']}\n")
            if data['images']:
                f.write(f"图片列表: {', '.join(data['images'])}\n")

    def crawl(self):
        """开始爬取"""
        print(f"🚀 开始爬取: {self.base_url}")
        print(f"📝 最大页面数: {self.max_pages}")
        print(f"⏱️  请求延迟: {self.delay}秒\n")

        # 如果结果文件存在，先删除
        if os.path.exists('crawler_results.txt'):
            os.remove('crawler_results.txt')

        page_count = 0

        while self.to_visit and page_count < self.max_pages:
            # 获取下一个要访问的URL
            current_url = self.to_visit.pop(0)

            # 跳过已访问的URL
            if current_url in self.visited_urls:
                continue

            print(f"📄 正在爬取 [{page_count + 1}/{self.max_pages}]: {current_url}")

            # 标记为已访问
            self.visited_urls.add(current_url)

            # 获取页面内容
            soup = self.get_page_content(current_url)

            if soup:
                # 提取数据
                data = self.extract_data(soup, current_url)
                print(f"   ✅ 标题: {data['title']}")
                print(f"   📊 段落: {data['paragraphs_count']}, 图片: {data['images_count']}")

                # 保存数据
                self.save_to_file(data)

                # 提取新的链接
                new_links = self.extract_links(soup, current_url)

                # 添加未访问的链接到待访问列表
                for link in new_links:
                    if link not in self.visited_urls and link not in self.to_visit:
                        self.to_visit.append(link)

                page_count += 1

            # 延迟，避免对服务器造成压力
            if page_count < self.max_pages:
                time.sleep(self.delay)

        print(f"\n✨ 爬取完成！")
        print(f"📈 总共爬取了 {page_count} 个页面")
        print(f"💾 结果已保存到 crawler_results.txt")


def main():
    """主函数 - 示例用法"""

    # 示例1: 爬取本地Naruto网站（需要先运行serve.py）
    print("=" * 80)
    print("简单网络爬虫示例")
    print("=" * 80)
    print("\n请选择爬取模式:")
    print("1. 爬取本地Naruto网站 (http://localhost:8000)")
    print("2. 爬取其他网站 (输入URL)")
    print("3. 使用默认示例 (example.com)")

    choice = input("\n请输入选择 (1/2/3): ").strip()

    if choice == "1":
        url = "http://localhost:8000"
        print("\n⚠️  请确保已经运行了 serve.py (python naruto-website/serve.py)")
        input("按回车键继续...")
    elif choice == "2":
        url = input("请输入要爬取的URL: ").strip()
        if not url.startswith('http'):
            url = 'http://' + url
    else:
        url = "http://example.com"

    # 创建爬虫实例
    crawler = SimpleCrawler(
        base_url=url,
        max_pages=10,      # 最多爬取10个页面
        delay=1            # 每次请求间隔1秒
    )

    # 开始爬取
    try:
        crawler.crawl()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断爬取")
        print(f"已爬取 {len(crawler.visited_urls)} 个页面")


if __name__ == "__main__":
    main()
