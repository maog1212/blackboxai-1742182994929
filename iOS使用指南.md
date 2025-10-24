# 📱 iPhone/iPad 爬虫使用指南

本项目提供了两种在苹果手机上运行网络爬虫的方式，**完全无需安装任何依赖**！

---

## 🎯 方式一：手机浏览器访问（推荐⭐）

这是最简单的方式，无需在手机上安装Python！

### 步骤：

#### 1️⃣ 在电脑上启动服务器

```bash
python mobile_crawler_server.py
```

启动后会显示：
```
📱 移动端网络爬虫服务器
==================================================
🚀 服务器启动在端口: 8080

📱 在手机浏览器中打开:
   http://192.168.1.100:8080    # 你的实际IP

💻 在本机浏览器中打开:
   http://localhost:8080
```

#### 2️⃣ 在iPhone上打开浏览器

1. 确保手机和电脑**连接同一个WiFi**
2. 打开Safari浏览器（或Chrome、Edge等）
3. 输入地址：`http://你的电脑IP:8080`
4. 即可开始使用！

### 功能特性：

✅ **精美的移动端界面**
- 专为触摸屏优化
- 支持深色模式
- 响应式设计，完美适配iPhone

✅ **实时爬取**
- 输入任何URL开始爬取
- 实时显示爬取状态
- 查看提取的链接、图片、文本

✅ **快捷链接**
- 一键测试示例网站
- 保存常用网址

✅ **详细统计**
- 爬取的页面数
- 发现的链接数
- 提取的图片数
- 错误统计

### 使用技巧：

- **添加到主屏幕**：在Safari中点击"分享" → "添加到主屏幕"，创建App图标
- **横屏模式**：旋转手机获得更好的浏览体验
- **刷新页面**：下拉页面即可刷新

---

## 🐍 方式二：在iPhone上直接运行Python

需要在iPhone上安装Python应用，但功能更强大！

### 推荐的iOS Python应用：

#### 1. **Pythonista 3** ⭐ 最推荐
- App Store: https://apps.apple.com/app/pythonista-3/id1085978097
- 价格: ¥68（一次性付费）
- 特点: 功能最完整，UI最友好

#### 2. **a-Shell** ⭐ 免费
- App Store: https://apps.apple.com/app/a-shell/id1473805438
- 价格: 免费
- 特点: 完整的命令行环境

#### 3. **Pyto - Python 3**
- App Store: https://apps.apple.com/app/pyto-python-3/id1436650069
- 价格: 免费（内购解锁功能）

---

## 📲 在Pythonista中使用

### 方法A: 从iCloud/Files导入

1. **下载代码到iPhone**
   - 使用AirDrop从Mac传输
   - 通过iCloud Drive同步
   - 或直接在iPhone上下载zip文件

2. **在Pythonista中打开**
   - 打开Pythonista应用
   - 点击"+"按钮
   - 选择"Import" → 找到`ios_crawler.py`

3. **运行**
   - 点击播放按钮▶️运行
   - 按提示输入URL

### 方法B: 直接粘贴代码

1. 在Pythonista中新建文件
2. 将`ios_crawler.py`的内容全部复制粘贴
3. 保存并运行

### 使用示例：

#### 交互模式（推荐）

```python
# 直接运行脚本
python ios_crawler.py
```

界面示例：
```
==================================================
📱 iOS 网络爬虫
==================================================

提示: 输入 'q' 退出, 's' 保存结果

🔍 输入URL (或命令): http://example.com

==================================================
📱 正在爬取: http://example.com
==================================================

✅ 标题: Example Domain
🔗 链接数: 1
🖼️  图片数: 0

📋 主要标题:
  1. Example Domain

==================================================
```

#### 快速爬取模式

```python
# 命令行参数
python ios_crawler.py http://example.com
```

#### 批量爬取模式

```python
# 一次爬取多个URL
python ios_crawler.py url1 url2 url3
```

#### 在代码中使用

```python
import ios_crawler

# 爬取单个URL
ios_crawler.crawl('http://example.com')

# 爬取多个URL
ios_crawler.crawl_multiple(
    'http://example.com',
    'http://localhost:8000'
)
```

---

## 📲 在a-Shell中使用

a-Shell提供了完整的命令行环境，更接近在电脑上的体验。

### 使用步骤：

1. **安装a-Shell**
   - 从App Store安装a-Shell

2. **下载代码**
   ```bash
   # 如果有git
   git clone <your-repo-url>

   # 或者使用curl下载单个文件
   curl -O <raw-file-url>
   ```

3. **运行爬虫**
   ```bash
   # 交互模式
   python ios_crawler.py

   # 快速模式
   python ios_crawler.py http://example.com
   ```

---

## 🎮 交互式命令

在交互模式中，支持以下命令：

| 命令 | 功能 |
|------|------|
| `直接输入URL` | 开始爬取该URL |
| `s` | 保存结果到JSON文件 |
| `q` | 退出程序 |
| `h` 或 `?` | 显示帮助 |
| `demo` | 选择演示URL |

---

## 💡 实用场景

### 1. 研究网页结构
```python
# 查看网页包含哪些链接
ios_crawler.crawl('https://news.ycombinator.com')
```

### 2. 提取文章链接
```python
# 爬取博客首页，获取所有文章链接
ios_crawler.crawl('https://your-blog.com')
```

### 3. 监控网站变化
```python
# 定期爬取，保存结果对比
ios_crawler.crawl('https://example.com')
# 结果保存为JSON，可以对比历史数据
```

---

## 📁 输出文件

### JSON结果文件

运行后可以保存为`crawler_results.json`：

```json
[
  {
    "url": "http://example.com",
    "time": "2025-10-24T23:30:00",
    "data": {
      "title": "Example Domain",
      "links": ["http://..."],
      "images": 0,
      "headings": ["Example Domain"]
    }
  }
]
```

### 查看保存的文件

在Pythonista中：
- 点击"📁"图标查看文件
- 可以通过"Share"分享到其他应用

在a-Shell中：
```bash
# 查看文件
cat crawler_results.json

# 美化显示
python -m json.tool crawler_results.json
```

---

## 🔧 常见问题

### Q: 无法访问网页服务器？
A:
1. 确保手机和电脑在**同一WiFi**
2. 检查电脑防火墙设置
3. 在电脑上运行`ipconfig`(Windows)或`ifconfig`(Mac)确认IP地址

### Q: Pythonista中如何输入中文？
A: 使用iPhone自带键盘即可，Pythonista完整支持中文

### Q: 可以爬取需要登录的网站吗？
A: 当前版本不支持，需要手动添加Cookie处理

### Q: 速度慢怎么办？
A:
- 使用WiFi而非蜂窝数据
- 减少爬取的页面数量
- 选择网速快的时段

### Q: 可以下载图片吗？
A: `ios_crawler.py`暂不支持，但`mobile_crawler_server.py`的Web版本会显示图片数量

---

## 🚀 高级技巧

### 1. 自定义保存文件名

```python
crawler = IOSCrawler()
crawler.crawl('http://example.com')
crawler.save_json('my_results.json')  # 自定义文件名
```

### 2. 在Pythonista中查看结果

```python
import ios_crawler
import json

# 爬取
crawler = ios_crawler.IOSCrawler()
result = crawler.crawl('http://example.com')

# 在控制台美化显示JSON
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 3. 定时爬取

```python
import time
import ios_crawler

urls = ['http://example.com']

while True:
    for url in urls:
        ios_crawler.crawl(url)

    print("等待60秒...")
    time.sleep(60)  # 每60秒爬取一次
```

---

## 📊 性能对比

| 方式 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| **Web界面** | 无需安装应用<br>界面美观<br>操作简单 | 需要电脑支持 | 临时使用<br>展示给他人 |
| **Pythonista** | 功能完整<br>离线可用<br>可定制 | 需付费购买 | 经常使用<br>开发学习 |
| **a-Shell** | 完全免费<br>命令行完整 | 界面较简陋 | 极客用户<br>命令行爱好者 |

---

## 🎓 学习资源

### Pythonista学习
- 官方文档: http://omz-software.com/pythonista/docs/
- 示例代码: Pythonista内置Examples

### Python网络编程
- `urllib`文档: https://docs.python.org/3/library/urllib.html
- `HTMLParser`文档: https://docs.python.org/3/library/html.parser.html

---

## 📝 快速参考

### 启动Web服务器
```bash
python mobile_crawler_server.py
```

### 运行iOS版本
```bash
# 交互模式
python ios_crawler.py

# 快速模式
python ios_crawler.py http://example.com

# 批量模式
python ios_crawler.py url1 url2 url3
```

### 在Python中导入使用
```python
import ios_crawler

# 单个URL
ios_crawler.crawl('http://example.com')

# 多个URL
ios_crawler.crawl_multiple('url1', 'url2')
```

---

## 💬 支持

如有问题：
1. 检查本文档的"常见问题"部分
2. 查看代码注释
3. 在Issues中提问

---

## ✨ 总结

现在你有**三个强大的工具**可以在iPhone上爬取网页：

1. **mobile_crawler_server.py** - Web界面，最简单
2. **ios_crawler.py** - 命令行版本，最灵活
3. **stdlib_crawler.py** - 完整功能，最强大

**全部零依赖，开箱即用！** 🎉

选择最适合你的方式，开始探索网络世界吧！
