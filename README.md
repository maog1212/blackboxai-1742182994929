# 🕷️ 零依赖 Python 网络爬虫套件

一套完整的网络爬虫解决方案，**完全不需要安装任何依赖**！仅使用 Python 标准库，支持桌面和移动设备。

Built by https://www.blackbox.ai

---

## ✨ 特性

- ✅ **零依赖** - 仅使用 Python 标准库
- 📱 **移动优化** - 完美支持 iPhone/iPad
- 🎨 **精美界面** - 现代化 Web UI
- 🚀 **开箱即用** - 无需配置，立即使用
- 🌙 **深色模式** - 自动适配系统主题
- 💾 **数据导出** - JSON 格式保存
- 🔍 **实时爬取** - 即时显示结果

---

## 📦 包含工具

### 1. 📱 mobile_crawler_server.py - Web 界面版（推荐）

**最简单的使用方式！**

在电脑上启动服务器，通过手机浏览器访问：

```bash
python mobile_crawler_server.py
```

然后在 iPhone Safari 中打开 `http://你的电脑IP:8080`

**特性：**
- 🎯 触摸优化的移动端界面
- 📊 实时统计数据
- 🔗 链接和图片提取
- 🌓 深色模式支持
- 📱 添加到主屏幕作为 App

### 2. 📲 ios_crawler.py - iOS 命令行版

专为 iPhone/iPad 的 Pythonista、a-Shell 等应用设计：

```bash
# 交互模式
python ios_crawler.py

# 快速爬取
python ios_crawler.py http://example.com

# 批量爬取
python ios_crawler.py url1 url2 url3
```

**特性：**
- 🎮 交互式命令界面
- 💾 JSON 数据导出
- 📝 简洁的移动端输出
- 🔌 可作为模块导入

### 3. 💻 stdlib_crawler.py - 完整功能版

桌面端完整版，功能最强大：

```bash
python stdlib_crawler.py
```

**特性：**
- 📁 保存完整 HTML
- 🖼️ 下载图片到本地
- 🔍 深度链接发现
- 📊 详细统计报告
- 🗂️ 结构化数据存储

### 4. 🎓 simple_crawler.py - 学习版

使用 BeautifulSoup 的简化版（需要依赖）：

```bash
pip install -r requirements.txt
python simple_crawler.py
```

---

## 🚀 快速开始

### 方式一：手机浏览器（最简单）

1. 在电脑上：
   ```bash
   python mobile_crawler_server.py
   ```

2. 在 iPhone 上：
   - 连接同一 WiFi
   - 打开 Safari
   - 访问显示的地址
   - 开始爬取！

### 方式二：iPhone Python 应用

1. 安装 [Pythonista](https://apps.apple.com/app/pythonista-3/id1085978097) 或 [a-Shell](https://apps.apple.com/app/a-shell/id1473805438)

2. 导入 `ios_crawler.py`

3. 运行并享受！

详细说明请查看 [iOS使用指南.md](iOS使用指南.md)

---

## 📖 使用示例

### Web 界面版

```bash
# 启动服务器
python mobile_crawler_server.py

# 在浏览器中访问
# http://localhost:8080
```

### iOS 命令行版

```python
import ios_crawler

# 快速爬取
ios_crawler.crawl('http://example.com')

# 批量爬取
ios_crawler.crawl_multiple(
    'http://site1.com',
    'http://site2.com'
)
```

### 桌面完整版

```python
from stdlib_crawler import StdlibCrawler

crawler = StdlibCrawler(
    base_url="http://example.com",
    max_pages=10,
    delay=1,
    download_images=True
)

crawler.crawl()
```

---

## 📱 移动端截图预览

Web 界面包含：
- 📊 实时统计卡片
- 🎯 大号触摸按钮
- 📋 可展开的结果列表
- 🔗 快捷链接选择
- 🌓 自动深色模式

---

## 📁 项目结构

```
├── mobile_crawler_server.py    # Web界面服务器
├── ios_crawler.py              # iOS优化版
├── stdlib_crawler.py           # 桌面完整版
├── simple_crawler.py           # 学习版(需依赖)
├── requirements.txt            # 依赖列表(仅simple版需要)
├── iOS使用指南.md              # 详细的iOS使用教程
├── CRAWLER_README.md           # 爬虫详细文档
└── naruto-website/             # 测试网站
    ├── index.html
    ├── serve.py                # 本地测试服务器
    └── assets/
```

---

## 🎯 使用场景

### 1. 学习网页结构
```bash
python ios_crawler.py https://example.com
```

### 2. 提取文章链接
```bash
python stdlib_crawler.py
# 输入博客地址，获取所有文章链接
```

### 3. 监控网站变化
```python
# 定期爬取并保存，对比JSON数据
ios_crawler.crawl('https://your-site.com')
```

### 4. 批量数据收集
```bash
python stdlib_crawler.py
# 自动爬取同域名下的多个页面
```

---

## 🛠️ 技术栈

**仅使用 Python 标准库：**
- `urllib` - HTTP 请求
- `html.parser` - HTML 解析
- `http.server` - Web 服务器
- `json` - 数据序列化
- `threading` - 并发处理

**无需任何第三方库！**

---

## 📚 文档

- [iOS使用指南.md](iOS使用指南.md) - iPhone/iPad 完整教程
- [CRAWLER_README.md](CRAWLER_README.md) - 爬虫详细文档

---

## 💡 常见问题

### Q: 真的不需要安装任何依赖吗？
A: 是的！`mobile_crawler_server.py`、`ios_crawler.py` 和 `stdlib_crawler.py` 都只使用 Python 标准库。只有 `simple_crawler.py` 需要依赖。

### Q: 可以在 iPhone 上离线使用吗？
A: 可以！使用 Pythonista 或 a-Shell 运行 `ios_crawler.py`，完全离线可用。

### Q: Web 界面需要互联网吗？
A: 不需要！只要手机和电脑在同一 WiFi，即可访问。爬取的网站需要网络。

### Q: 支持哪些 iOS 应用？
A:
- Pythonista 3 (付费，最推荐)
- a-Shell (免费)
- Pyto (免费+内购)

---

## 🎓 学习资源

### Python 标准库文档
- [urllib](https://docs.python.org/3/library/urllib.html)
- [html.parser](https://docs.python.org/3/library/html.parser.html)
- [http.server](https://docs.python.org/3/library/http.server.html)

### iOS Python 应用
- [Pythonista 文档](http://omz-software.com/pythonista/docs/)
- [a-Shell 项目](https://github.com/holzschu/a-shell)

---

## 🧪 测试

项目包含一个本地测试网站：

```bash
# 启动测试网站
cd naruto-website
python serve.py

# 在另一个终端测试爬虫
python stdlib_crawler.py
# 选择选项 1 (本地网站)
```

---

## 📊 性能

| 工具 | 启动速度 | 内存占用 | 适用场景 |
|------|---------|---------|---------|
| Web版 | ⚡⚡⚡ | ~30MB | 展示、移动端 |
| iOS版 | ⚡⚡⚡ | ~20MB | 移动开发 |
| 桌面版 | ⚡⚡ | ~40MB | 批量爬取 |

---

## 🔒 使用须知

1. **遵守 robots.txt** - 尊重网站爬取规则
2. **控制频率** - 使用延迟避免过载服务器
3. **合法使用** - 仅用于学习和合法数据收集
4. **尊重版权** - 不爬取受保护内容

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

本项目仅供学习和教育用途。

---

## ⭐ 快速链接

- 🌐 [在线演示](#) (待添加)
- 📱 [iOS 教程](iOS使用指南.md)
- 📖 [完整文档](CRAWLER_README.md)
- 🐛 [报告问题](#)

---

## 🎉 开始使用

选择最适合你的方式：

```bash
# 1. 手机浏览器 (最简单)
python mobile_crawler_server.py

# 2. iPhone 应用
python ios_crawler.py

# 3. 桌面完整版
python stdlib_crawler.py
```

**享受零依赖爬虫的乐趣！** 🚀
