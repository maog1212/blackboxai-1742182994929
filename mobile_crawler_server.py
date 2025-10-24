#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端网络爬虫 Web 服务器
适合在手机浏览器中使用 - 零依赖
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
import json
import os
import time
from datetime import datetime
import threading


class HTMLDataExtractor(HTMLParser):
    """HTML数据提取器"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.images = []
        self.text_content = []
        self._in_title = False
        self._in_script = False
        self._in_style = False
        self._current_tag = None

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        attrs_dict = dict(attrs)

        if tag == 'title':
            self._in_title = True
        elif tag == 'a' and 'href' in attrs_dict:
            self.links.append({'url': attrs_dict['href'], 'text': ''})
        elif tag == 'img':
            self.images.append({
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', '')
            })
        elif tag == 'script':
            self._in_script = True
        elif tag == 'style':
            self._in_style = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
        elif tag == 'script':
            self._in_script = False
        elif tag == 'style':
            self._in_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        if self._current_tag == 'a' and self.links:
            self.links[-1]['text'] += data.strip()
        if not self._in_script and not self._in_style:
            text = data.strip()
            if text and len(text) > 10:
                self.text_content.append(text)


class MobileCrawler:
    """移动端爬虫核心类"""

    def __init__(self):
        self.is_crawling = False
        self.current_status = "就绪"
        self.results = []
        self.stats = {
            'pages': 0,
            'links': 0,
            'images': 0,
            'errors': 0
        }

    def fetch_page(self, url):
        """获取网页内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
            }
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                content = response.read()
                try:
                    return content.decode('utf-8')
                except:
                    return content.decode('utf-8', errors='ignore')
        except Exception as e:
            raise Exception(f"获取失败: {str(e)}")

    def parse_html(self, html_content, base_url):
        """解析HTML"""
        parser = HTMLDataExtractor()
        try:
            parser.feed(html_content)
        except:
            pass

        # 标准化链接
        links = []
        for link in parser.links[:20]:  # 限制链接数
            try:
                full_url = urllib.parse.urljoin(base_url, link['url'])
                links.append({'url': full_url, 'text': link['text'][:50]})
            except:
                pass

        # 标准化图片
        images = []
        for img in parser.images[:10]:  # 限制图片数
            try:
                full_url = urllib.parse.urljoin(base_url, img['src'])
                images.append({'url': full_url, 'alt': img['alt'][:50]})
            except:
                pass

        return {
            'title': parser.title or '无标题',
            'links': links,
            'images': images,
            'text_preview': ' '.join(parser.text_content[:5])[:200]
        }

    def crawl_single_page(self, url):
        """爬取单个页面"""
        try:
            self.current_status = f"正在爬取: {url}"
            html = self.fetch_page(url)
            data = self.parse_html(html, url)

            result = {
                'url': url,
                'title': data['title'],
                'links_count': len(data['links']),
                'images_count': len(data['images']),
                'text_preview': data['text_preview'],
                'links': data['links'],
                'images': data['images'],
                'time': datetime.now().strftime('%H:%M:%S'),
                'status': '成功'
            }

            self.stats['pages'] += 1
            self.stats['links'] += len(data['links'])
            self.stats['images'] += len(data['images'])

            return result

        except Exception as e:
            self.stats['errors'] += 1
            return {
                'url': url,
                'title': '错误',
                'status': '失败',
                'error': str(e),
                'time': datetime.now().strftime('%H:%M:%S')
            }


# 全局爬虫实例
crawler = MobileCrawler()


class MobileCrawlerHandler(http.server.SimpleHTTPRequestHandler):
    """处理HTTP请求"""

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.get_main_page().encode('utf-8'))

        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            status = {
                'is_crawling': crawler.is_crawling,
                'status': crawler.current_status,
                'stats': crawler.stats,
                'results_count': len(crawler.results)
            }
            self.wfile.write(json.dumps(status, ensure_ascii=False).encode('utf-8'))

        elif self.path == '/api/results':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(crawler.results, ensure_ascii=False).encode('utf-8'))

        else:
            self.send_error(404)

    def do_POST(self):
        """处理POST请求"""
        if self.path == '/api/crawl':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            url = data.get('url', '').strip()
            if not url:
                self.send_json_response({'success': False, 'error': 'URL不能为空'})
                return

            if not url.startswith('http'):
                url = 'http://' + url

            # 在后台线程中爬取
            def crawl_task():
                crawler.is_crawling = True
                result = crawler.crawl_single_page(url)
                crawler.results.insert(0, result)  # 最新的放在前面
                if len(crawler.results) > 50:  # 限制结果数量
                    crawler.results = crawler.results[:50]
                crawler.is_crawling = False
                crawler.current_status = "就绪"

            thread = threading.Thread(target=crawl_task)
            thread.daemon = True
            thread.start()

            self.send_json_response({'success': True, 'message': '爬取任务已启动'})

        elif self.path == '/api/clear':
            crawler.results = []
            crawler.stats = {'pages': 0, 'links': 0, 'images': 0, 'errors': 0}
            self.send_json_response({'success': True, 'message': '已清空'})

        else:
            self.send_error(404)

    def send_json_response(self, data):
        """发送JSON响应"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def get_main_page(self):
        """生成主页面HTML"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>📱 移动爬虫</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left);
        }

        .container {
            max-width: 100%;
            padding: 15px;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        h1 {
            font-size: 24px;
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-top: 15px;
        }

        .stat-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-value {
            font-size: 20px;
            font-weight: bold;
            display: block;
        }

        .stat-label {
            font-size: 11px;
            opacity: 0.9;
            display: block;
            margin-top: 2px;
        }

        .control-panel {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        input[type="text"] {
            flex: 1;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }

        input[type="text"]:focus {
            border-color: #667eea;
        }

        button {
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, opacity 0.2s;
            -webkit-tap-highlight-color: transparent;
        }

        button:active {
            transform: scale(0.95);
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            flex: 1;
        }

        .btn-secondary {
            background: #f0f0f0;
            color: #666;
            padding: 12px 15px;
        }

        .status {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 14px;
            color: #666;
            text-align: center;
        }

        .status.active {
            background: #e3f2fd;
            color: #1976d2;
        }

        .results {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .result-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }

        .result-item.error {
            border-left-color: #f44336;
        }

        .result-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
            font-size: 16px;
        }

        .result-url {
            color: #667eea;
            font-size: 12px;
            word-break: break-all;
            margin-bottom: 8px;
        }

        .result-meta {
            display: flex;
            gap: 15px;
            font-size: 12px;
            color: #666;
            margin-bottom: 8px;
        }

        .result-preview {
            font-size: 13px;
            color: #555;
            line-height: 1.4;
            margin-bottom: 8px;
        }

        .expandable {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .expandable.show {
            max-height: 2000px;
        }

        .toggle-btn {
            background: #e3f2fd;
            color: #1976d2;
            padding: 8px 12px;
            font-size: 12px;
            display: inline-block;
            margin-top: 5px;
        }

        .links-list, .images-list {
            margin-top: 10px;
        }

        .link-item {
            background: white;
            padding: 8px;
            margin: 5px 0;
            border-radius: 5px;
            font-size: 12px;
        }

        .link-url {
            color: #667eea;
            word-break: break-all;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }

        .quick-links {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .quick-link {
            background: #f0f0f0;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 12px;
            color: #667eea;
            cursor: pointer;
            -webkit-tap-highlight-color: transparent;
        }

        .quick-link:active {
            background: #e0e0e0;
        }

        @media (prefers-color-scheme: dark) {
            body {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            }

            .header, .control-panel, .results {
                background: rgba(30, 30, 30, 0.95);
            }

            h1 {
                color: #a0b4ff;
            }

            input[type="text"] {
                background: #2a2a2a;
                color: white;
                border-color: #444;
            }

            .result-item {
                background: #2a2a2a;
            }

            .result-title {
                color: #e0e0e0;
            }

            .link-item {
                background: #1a1a1a;
                color: #ccc;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 移动端网络爬虫</h1>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-value" id="stat-pages">0</span>
                    <span class="stat-label">页面</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="stat-links">0</span>
                    <span class="stat-label">链接</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="stat-images">0</span>
                    <span class="stat-label">图片</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value" id="stat-errors">0</span>
                    <span class="stat-label">错误</span>
                </div>
            </div>
        </div>

        <div class="control-panel">
            <div class="input-group">
                <input type="text" id="url-input" placeholder="输入网址 (如: example.com)" value="http://example.com">
                <button class="btn-secondary" onclick="clearResults()">清空</button>
            </div>
            <button class="btn-primary" onclick="startCrawl()">🚀 开始爬取</button>

            <div class="quick-links">
                <div class="quick-link" onclick="setUrl('http://example.com')">示例网站</div>
                <div class="quick-link" onclick="setUrl('http://localhost:8000')">本地服务</div>
            </div>

            <div class="status" id="status">就绪</div>
        </div>

        <div class="results">
            <div id="results-container" class="empty-state">
                <p>🔍 输入URL开始爬取</p>
            </div>
        </div>
    </div>

    <script>
        let autoRefresh = null;

        function setUrl(url) {
            document.getElementById('url-input').value = url;
        }

        async function startCrawl() {
            const url = document.getElementById('url-input').value.trim();
            if (!url) {
                alert('请输入URL');
                return;
            }

            try {
                const response = await fetch('/api/crawl', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });

                const result = await response.json();
                if (result.success) {
                    startAutoRefresh();
                } else {
                    alert(result.error);
                }
            } catch (error) {
                alert('请求失败: ' + error.message);
            }
        }

        async function clearResults() {
            if (!confirm('确定要清空所有结果吗？')) return;

            try {
                await fetch('/api/clear', {method: 'POST'});
                updateUI();
            } catch (error) {
                alert('清空失败: ' + error.message);
            }
        }

        function toggleDetails(id) {
            const elem = document.getElementById(id);
            elem.classList.toggle('show');
        }

        async function updateUI() {
            try {
                const statusResp = await fetch('/api/status');
                const status = await statusResp.json();

                const resultsResp = await fetch('/api/results');
                const results = await resultsResp.json();

                // 更新统计
                document.getElementById('stat-pages').textContent = status.stats.pages;
                document.getElementById('stat-links').textContent = status.stats.links;
                document.getElementById('stat-images').textContent = status.stats.images;
                document.getElementById('stat-errors').textContent = status.stats.errors;

                // 更新状态
                const statusElem = document.getElementById('status');
                statusElem.textContent = status.status;
                statusElem.className = status.is_crawling ? 'status active' : 'status';

                // 更新结果
                const container = document.getElementById('results-container');
                if (results.length === 0) {
                    container.innerHTML = '<div class="empty-state"><p>🔍 暂无结果</p></div>';
                } else {
                    container.innerHTML = results.map((r, i) => `
                        <div class="result-item ${r.status === '失败' ? 'error' : ''}">
                            <div class="result-title">${escapeHtml(r.title)}</div>
                            <div class="result-url">${escapeHtml(r.url)}</div>
                            <div class="result-meta">
                                <span>⏰ ${r.time}</span>
                                ${r.links_count !== undefined ? `<span>🔗 ${r.links_count}</span>` : ''}
                                ${r.images_count !== undefined ? `<span>🖼️ ${r.images_count}</span>` : ''}
                                <span>${r.status}</span>
                            </div>
                            ${r.text_preview ? `<div class="result-preview">${escapeHtml(r.text_preview)}</div>` : ''}
                            ${r.error ? `<div class="result-preview" style="color: #f44336;">${escapeHtml(r.error)}</div>` : ''}
                            ${r.links && r.links.length > 0 ? `
                                <button class="toggle-btn" onclick="toggleDetails('links-${i}')">
                                    查看 ${r.links.length} 个链接
                                </button>
                                <div id="links-${i}" class="expandable">
                                    <div class="links-list">
                                        ${r.links.slice(0, 10).map(l => `
                                            <div class="link-item">
                                                <div>${escapeHtml(l.text || '无标题')}</div>
                                                <div class="link-url">${escapeHtml(l.url)}</div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    `).join('');
                }

                // 如果正在爬取，继续刷新
                if (status.is_crawling) {
                    startAutoRefresh();
                } else {
                    stopAutoRefresh();
                }

            } catch (error) {
                console.error('更新UI失败:', error);
            }
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function startAutoRefresh() {
            if (autoRefresh) return;
            autoRefresh = setInterval(updateUI, 1000);
        }

        function stopAutoRefresh() {
            if (autoRefresh) {
                clearInterval(autoRefresh);
                autoRefresh = null;
            }
        }

        // 初始加载
        updateUI();

        // 页面可见性变化时的处理
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                updateUI();
            }
        });
    </script>
</body>
</html>'''

    def log_message(self, format, *args):
        """自定义日志格式"""
        pass  # 禁用默认日志


def main():
    """主函数"""
    PORT = 8080

    print("\n" + "=" * 70)
    print("📱 移动端网络爬虫服务器")
    print("=" * 70)
    print(f"\n🚀 服务器启动在端口: {PORT}")
    print(f"\n📱 在手机浏览器中打开:")
    print(f"   http://你的电脑IP:{PORT}")
    print(f"\n💻 在本机浏览器中打开:")
    print(f"   http://localhost:{PORT}")
    print(f"\n📶 获取本机IP地址:")

    # 尝试获取本机IP
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"   http://{local_ip}:{PORT}")
    except:
        print(f"   (请在电脑上运行 ipconfig 或 ifconfig 查看IP)")

    print(f"\n提示:")
    print(f"  • 确保手机和电脑在同一WiFi网络")
    print(f"  • 如无法访问，检查防火墙设置")
    print(f"  • 按 Ctrl+C 停止服务器")
    print("=" * 70 + "\n")

    try:
        with socketserver.TCPServer(("", PORT), MobileCrawlerHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    main()
