#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无依赖网络爬虫 - 仅使用Python标准库
No-Dependency Web Crawler - Using Only Python Standard Library
"""

import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
import json
import os
import time
import re
from collections import defaultdict
from datetime import datetime


class HTMLDataExtractor(HTMLParser):
    """HTML数据提取器 - 使用标准库的HTMLParser"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.images = []
        self.text_content = []
        self.meta_data = {}

        # 状态跟踪
        self._in_title = False
        self._in_script = False
        self._in_style = False
        self._current_tag = None

    def handle_starttag(self, tag, attrs):
        """处理开始标签"""
        self._current_tag = tag
        attrs_dict = dict(attrs)

        # 提取标题
        if tag == 'title':
            self._in_title = True

        # 提取链接
        elif tag == 'a' and 'href' in attrs_dict:
            self.links.append({
                'url': attrs_dict['href'],
                'text': ''
            })

        # 提取图片
        elif tag == 'img':
            img_data = {
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', ''),
                'title': attrs_dict.get('title', '')
            }
            self.images.append(img_data)

        # 提取meta信息
        elif tag == 'meta':
            name = attrs_dict.get('name', attrs_dict.get('property', ''))
            content = attrs_dict.get('content', '')
            if name and content:
                self.meta_data[name] = content

        # 跟踪script和style标签
        elif tag == 'script':
            self._in_script = True
        elif tag == 'style':
            self._in_style = True

    def handle_endtag(self, tag):
        """处理结束标签"""
        if tag == 'title':
            self._in_title = False
        elif tag == 'script':
            self._in_script = False
        elif tag == 'style':
            self._in_style = False

    def handle_data(self, data):
        """处理文本数据"""
        # 提取标题
        if self._in_title:
            self.title += data.strip()

        # 提取链接文本
        if self._current_tag == 'a' and self.links:
            self.links[-1]['text'] += data.strip()

        # 提取正文内容（跳过script和style）
        if not self._in_script and not self._in_style:
            text = data.strip()
            if text and len(text) > 10:  # 只保留有意义的文本
                self.text_content.append(text)


class StdlibCrawler:
    """只使用标准库的网络爬虫"""

    def __init__(self, base_url, max_pages=10, delay=1, download_images=False):
        """
        初始化爬虫

        Args:
            base_url: 起始URL
            max_pages: 最大爬取页面数
            delay: 请求间隔时间（秒）
            download_images: 是否下载图片
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.delay = delay
        self.download_images = download_images

        self.visited_urls = set()
        self.to_visit = [base_url]
        self.pages_data = []
        self.stats = defaultdict(int)

        # 创建输出目录
        self.output_dir = 'crawler_output'
        self.images_dir = os.path.join(self.output_dir, 'images')
        self.pages_dir = os.path.join(self.output_dir, 'pages')

        for directory in [self.output_dir, self.images_dir, self.pages_dir]:
            os.makedirs(directory, exist_ok=True)

    def is_valid_url(self, url):
        """检查URL是否有效且属于同一域名"""
        try:
            parsed_base = urllib.parse.urlparse(self.base_url)
            parsed_url = urllib.parse.urlparse(url)

            # 只爬取同一域名下的页面
            return parsed_url.netloc == parsed_base.netloc
        except:
            return False

    def normalize_url(self, url, base_url):
        """标准化URL"""
        # 移除fragment
        url = urllib.parse.urljoin(base_url, url)
        parsed = urllib.parse.urlparse(url)

        # 重建URL，不包含fragment
        return urllib.parse.urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path,
             parsed.params, parsed.query, '')
        )

    def fetch_page(self, url):
        """
        获取网页内容

        Args:
            url: 要获取的URL

        Returns:
            网页内容（字符串），失败返回None
        """
        try:
            # 设置请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            request = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(request, timeout=10) as response:
                # 获取编码
                content_type = response.headers.get('Content-Type', '')
                encoding = 'utf-8'

                # 尝试从Content-Type提取编码
                charset_match = re.search(r'charset=([^\s;]+)', content_type)
                if charset_match:
                    encoding = charset_match.group(1)

                # 读取内容
                content = response.read()

                try:
                    return content.decode(encoding)
                except:
                    # 如果解码失败，尝试其他编码
                    for enc in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                        try:
                            return content.decode(enc)
                        except:
                            continue
                    return content.decode('utf-8', errors='ignore')

        except urllib.error.HTTPError as e:
            print(f"   ❌ HTTP错误 {e.code}: {url}")
            self.stats['http_errors'] += 1
            return None
        except urllib.error.URLError as e:
            print(f"   ❌ URL错误: {url} - {e.reason}")
            self.stats['url_errors'] += 1
            return None
        except Exception as e:
            print(f"   ❌ 未知错误: {url} - {e}")
            self.stats['other_errors'] += 1
            return None

    def download_image(self, img_url, page_url, index):
        """下载图片"""
        try:
            # 标准化图片URL
            full_url = urllib.parse.urljoin(page_url, img_url)

            # 生成文件名
            parsed = urllib.parse.urlparse(full_url)
            ext = os.path.splitext(parsed.path)[1] or '.jpg'
            filename = f"img_{int(time.time())}_{index}{ext}"
            filepath = os.path.join(self.images_dir, filename)

            # 下载图片
            request = urllib.request.Request(
                full_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())

            self.stats['images_downloaded'] += 1
            return filename
        except Exception as e:
            print(f"   ⚠️  图片下载失败: {img_url} - {e}")
            return None

    def save_page_content(self, url, html_content, page_num):
        """保存网页内容到文件"""
        try:
            # 生成安全的文件名
            filename = f"page_{page_num:03d}.html"
            filepath = os.path.join(self.pages_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"<!-- URL: {url} -->\n")
                f.write(f"<!-- Downloaded: {datetime.now()} -->\n\n")
                f.write(html_content)

            return filename
        except Exception as e:
            print(f"   ⚠️  保存页面失败: {e}")
            return None

    def parse_html(self, html_content, page_url):
        """解析HTML内容"""
        parser = HTMLDataExtractor()

        try:
            parser.feed(html_content)
        except Exception as e:
            print(f"   ⚠️  HTML解析警告: {e}")

        # 标准化所有链接
        normalized_links = []
        for link in parser.links:
            try:
                normalized_url = self.normalize_url(link['url'], page_url)
                normalized_links.append({
                    'url': normalized_url,
                    'text': link['text']
                })
            except:
                pass

        return {
            'title': parser.title or '无标题',
            'links': normalized_links,
            'images': parser.images,
            'text_content': parser.text_content,
            'meta_data': parser.meta_data
        }

    def crawl(self):
        """开始爬取"""
        print("\n" + "=" * 80)
        print("🚀 标准库网络爬虫启动")
        print("=" * 80)
        print(f"📍 起始URL: {self.base_url}")
        print(f"📄 最大页面: {self.max_pages}")
        print(f"⏱️  请求延迟: {self.delay}秒")
        print(f"🖼️  下载图片: {'是' if self.download_images else '否'}")
        print(f"📁 输出目录: {self.output_dir}/")
        print("=" * 80 + "\n")

        page_count = 0
        start_time = time.time()

        while self.to_visit and page_count < self.max_pages:
            # 获取下一个URL
            current_url = self.to_visit.pop(0)

            # 跳过已访问的URL
            if current_url in self.visited_urls:
                continue

            print(f"📄 [{page_count + 1}/{self.max_pages}] {current_url}")

            # 标记为已访问
            self.visited_urls.add(current_url)

            # 获取页面
            html_content = self.fetch_page(current_url)

            if html_content:
                # 保存原始HTML
                saved_file = self.save_page_content(current_url, html_content, page_count + 1)

                # 解析HTML
                parsed_data = self.parse_html(html_content, current_url)

                print(f"   ✅ {parsed_data['title']}")
                print(f"   📊 链接: {len(parsed_data['links'])}, "
                      f"图片: {len(parsed_data['images'])}, "
                      f"文本段: {len(parsed_data['text_content'])}")

                # 下载图片
                if self.download_images and parsed_data['images']:
                    downloaded = []
                    for idx, img in enumerate(parsed_data['images'][:5]):  # 最多5张
                        filename = self.download_image(img['src'], current_url, idx)
                        if filename:
                            downloaded.append(filename)
                    if downloaded:
                        print(f"   🖼️  已下载 {len(downloaded)} 张图片")

                # 保存数据
                page_data = {
                    'url': current_url,
                    'title': parsed_data['title'],
                    'saved_file': saved_file,
                    'links_count': len(parsed_data['links']),
                    'images_count': len(parsed_data['images']),
                    'text_segments': len(parsed_data['text_content']),
                    'meta_data': parsed_data['meta_data']
                }
                self.pages_data.append(page_data)

                # 更新统计
                self.stats['pages_crawled'] += 1
                self.stats['total_links'] += len(parsed_data['links'])
                self.stats['total_images'] += len(parsed_data['images'])

                # 添加新链接到待访问列表
                for link in parsed_data['links']:
                    link_url = link['url']
                    if (self.is_valid_url(link_url) and
                        link_url not in self.visited_urls and
                        link_url not in self.to_visit):
                        self.to_visit.append(link_url)

                page_count += 1

            # 延迟
            if page_count < self.max_pages and self.to_visit:
                time.sleep(self.delay)

        # 计算总时间
        elapsed_time = time.time() - start_time

        # 保存结果
        self.save_results(elapsed_time)

        # 显示统计
        self.print_statistics(elapsed_time)

    def save_results(self, elapsed_time):
        """保存爬取结果为JSON"""
        results = {
            'base_url': self.base_url,
            'crawl_time': datetime.now().isoformat(),
            'elapsed_seconds': round(elapsed_time, 2),
            'statistics': dict(self.stats),
            'pages': self.pages_data
        }

        results_file = os.path.join(self.output_dir, 'results.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n💾 详细结果已保存到: {results_file}")

    def print_statistics(self, elapsed_time):
        """打印统计信息"""
        print("\n" + "=" * 80)
        print("📊 爬取统计")
        print("=" * 80)
        print(f"✅ 成功爬取: {self.stats['pages_crawled']} 个页面")
        print(f"🔗 发现链接: {self.stats['total_links']} 个")
        print(f"🖼️  发现图片: {self.stats['total_images']} 张")

        if self.download_images:
            print(f"📥 下载图片: {self.stats['images_downloaded']} 张")

        if self.stats['http_errors'] or self.stats['url_errors'] or self.stats['other_errors']:
            print(f"\n❌ 错误统计:")
            if self.stats['http_errors']:
                print(f"   HTTP错误: {self.stats['http_errors']}")
            if self.stats['url_errors']:
                print(f"   URL错误: {self.stats['url_errors']}")
            if self.stats['other_errors']:
                print(f"   其他错误: {self.stats['other_errors']}")

        print(f"\n⏱️  总耗时: {elapsed_time:.2f} 秒")
        print(f"📁 输出目录: {os.path.abspath(self.output_dir)}/")
        print("=" * 80)


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🕷️  无依赖网络爬虫 (仅使用Python标准库)")
    print("=" * 80)

    # 获取用户输入
    print("\n请选择爬取模式:")
    print("1. 爬取本地Naruto网站 (http://localhost:8000)")
    print("2. 爬取示例网站 (http://example.com)")
    print("3. 自定义URL")

    choice = input("\n请选择 (1/2/3，默认1): ").strip() or "1"

    if choice == "1":
        url = "http://localhost:8000"
        print("\n⚠️  请确保已运行: cd naruto-website && python serve.py")
        input("确认后按回车继续...")
        download_imgs = True
    elif choice == "2":
        url = "http://example.com"
        download_imgs = False
    else:
        url = input("请输入URL: ").strip()
        if not url.startswith('http'):
            url = 'http://' + url
        download_imgs = input("是否下载图片? (y/n，默认n): ").strip().lower() == 'y'

    # 获取爬取参数
    try:
        max_pages = int(input(f"最大页面数 (默认10): ").strip() or "10")
    except:
        max_pages = 10

    try:
        delay = float(input(f"请求延迟秒数 (默认1): ").strip() or "1")
    except:
        delay = 1

    # 创建爬虫并开始爬取
    crawler = StdlibCrawler(
        base_url=url,
        max_pages=max_pages,
        delay=delay,
        download_images=download_imgs
    )

    try:
        crawler.crawl()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断爬取")
        print(f"已爬取 {crawler.stats['pages_crawled']} 个页面")
        crawler.save_results(0)


if __name__ == "__main__":
    main()
