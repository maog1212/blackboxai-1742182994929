# 简单网络爬虫 Simple Web Crawler

一个简单易用的Python网络爬虫示例，适合学习爬虫基础知识。

## 功能特点

- 自动爬取网页内容
- 提取页面标题、段落、图片等信息
- 自动发现并爬取同域名下的链接
- 遵守爬虫礼仪（设置请求延迟）
- 保存结果到文本文件
- 错误处理和异常捕获

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1: 交互式运行

```bash
python simple_crawler.py
```

然后按照提示选择爬取模式：
1. 爬取本地Naruto网站
2. 爬取自定义URL
3. 使用默认示例

### 方法2: 在代码中使用

```python
from simple_crawler import SimpleCrawler

# 创建爬虫实例
crawler = SimpleCrawler(
    base_url="http://example.com",  # 起始URL
    max_pages=10,                    # 最多爬取10个页面
    delay=1                          # 每次请求间隔1秒
)

# 开始爬取
crawler.crawl()
```

## 测试本地网站

首先启动本地Naruto网站服务器：

```bash
cd naruto-website
python serve.py
```

然后在另一个终端运行爬虫：

```bash
python simple_crawler.py
# 选择选项 1 (爬取本地Naruto网站)
```

## 输出结果

爬虫会将结果保存到 `crawler_results.txt` 文件中，包含：
- 页面URL
- 页面标题
- 段落数量
- 图片数量
- 图片链接列表

## 主要类和方法

### SimpleCrawler 类

**初始化参数:**
- `base_url`: 起始URL
- `max_pages`: 最大爬取页面数（默认10）
- `delay`: 请求间隔时间（默认1秒）

**主要方法:**
- `crawl()`: 开始爬取
- `get_page_content(url)`: 获取页面内容
- `extract_links(soup, current_url)`: 提取页面链接
- `extract_data(soup, url)`: 提取页面数据
- `save_to_file(data)`: 保存结果到文件

## 注意事项

1. **遵守robots.txt**: 在爬取网站前，应该检查网站的robots.txt文件
2. **请求频率**: 默认设置了1秒延迟，避免对服务器造成压力
3. **合法使用**: 仅用于学习和合法的数据收集
4. **尊重版权**: 不要爬取受版权保护的内容

## 示例输出

```
🚀 开始爬取: http://localhost:8000
📝 最大页面数: 10
⏱️  请求延迟: 1秒

📄 正在爬取 [1/10]: http://localhost:8000
   ✅ 标题: Naruto Website
   📊 段落: 5, 图片: 3

✨ 爬取完成！
📈 总共爬取了 3 个页面
💾 结果已保存到 crawler_results.txt
```

## 扩展功能建议

可以根据需要添加以下功能：
- 支持多线程/异步爬取
- 添加数据库存储
- 支持JavaScript渲染页面（使用Selenium）
- 添加代理支持
- 导出为JSON/CSV格式
- 添加robots.txt检查
- 图片下载功能

## 许可证

本项目仅供学习和教育用途。
