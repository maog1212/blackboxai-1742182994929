# 🔍 Shodan 信息收集工具 + 🤖 DeepSeek AI 分析

基于 Shodan 平台的智能信息收集网站，集成 DeepSeek AI 进行结果分析，用于安全研究和教育目的。

**🔓 完全开放 | 无功能限制 | 自由使用**

## ⚠️ 免责声明

**本工具仅用于合法的安全研究和教育目的。使用本工具进行任何非法活动，后果自负。**

- 仅在获得授权的情况下使用
- 遵守当地法律法规
- 尊重他人隐私和数据安全

## ✨ 功能特性

### 核心功能
- 🔎 **强大的搜索功能**: 支持 Shodan 全部搜索语法，无限制搜索
- 🤖 **AI 智能分析**: 使用 DeepSeek AI 自动分析搜索结果，无次数限制
- 📊 **结果展示**: 清晰展示设备信息、端口、位置等
- 🎯 **快速过滤**: 预设常用搜索查询
- 💻 **现代化界面**: 简洁美观的用户界面，支持浅色/深色模式
- 🕷️ **无需 API Key**: 直接从 Shodan 平台爬取数据
- 🌐 **RESTful API**: 完整的后端 API 接口，无 CORS 限制

### 移动端优化
- 📱 **iPhone 15 Pro Max 完美适配**: 专为最新 iPhone 优化
- 🎨 **PWA 应用**: 可添加到主屏幕，像原生 App 一样使用
- ⚡ **离线缓存**: Service Worker 支持离线访问
- 🌙 **深色模式**: 自动适配系统深色模式
- 🔄 **Dynamic Island 支持**: 完美支持 iPhone 15 Pro 系列
- 📐 **响应式设计**: 适配所有屏幕尺寸（iPhone SE 到 iPhone 15 Pro Max）
- 👆 **触摸优化**: 48px 最小触摸目标，符合 iOS 设计规范

### 自动化和 CI/CD
- 🤖 **GitHub Actions 自动化**: 自动测试多设备适配
- 🚀 **持续集成**: 自动构建和部署
- 📊 **Lighthouse 性能监控**: 自动移动端性能测试
- ✅ **自动验证**: HTML/CSS/JS 语法自动检查

### 完全开放
- 🔓 **无功能限制**: 所有功能完全开放，无需付费
- 🆓 **无使用限制**: 无搜索次数、频率、数据量限制
- 📖 **开源代码**: MIT 许可证，可自由修改和商业使用
- 🔒 **隐私保护**: 不收集用户数据，完全匿名使用

## 📋 前置要求

- Node.js (v14 或更高版本)
- npm 或 yarn
- DeepSeek API Key ([获取地址](https://platform.deepseek.com/))

## 🚀 快速开始

### 1. 安装依赖

```bash
cd shodan-info-collector
npm install
```

### 2. 配置 DeepSeek API Key

复制 `.env.example` 文件并重命名为 `.env`:

```bash
cp .env.example .env
```

编辑 `.env` 文件（API Key 已预配置）:

```env
DEEPSEEK_API_KEY=sk-d297057f68f248f5af9cba0e365cb27f
PORT=3000
```

**注意**: DeepSeek API Key 已经在代码中预配置，如果需要可以更换为自己的 Key。

### 3. 启动服务器

```bash
npm start
```

或使用开发模式（自动重启）:

```bash
npm run dev
```

### 4. 访问网站

打开浏览器访问: http://localhost:3000

## 📱 iPhone / iPad 使用指南

### 在 Safari 中使用

1. 在 iPhone 的 Safari 浏览器中打开网站
2. 点击底部的"分享"按钮 📤
3. 向下滚动，选择"添加到主屏幕"
4. 编辑名称（默认为"Shodan搜索"），点击"添加"
5. 在主屏幕上找到应用图标，点击打开

### PWA 应用特性

- ✅ 全屏显示，无浏览器地址栏
- ✅ 独立图标和启动画面
- ✅ 离线缓存，部分功能可离线使用
- ✅ 原生应用般的体验

### 移动端优化

- 🎯 触摸友好的按钮（最小 48px，符合最新 iOS 标准）
- 📏 响应式布局，适配各种屏幕
- ⚡ 优化的加载速度
- 🔄 防止 iOS 自动缩放
- 🎨 支持 iPhone 刘海屏安全区域

### iPhone 15 Pro Max 专属优化

- 📱 **屏幕尺寸适配**: 完美支持 6.7 英寸大屏（430x932 分辨率）
- 🎨 **Dynamic Island**: 状态栏完美适配动态岛
- 🌙 **深色模式**: 自动跟随系统深色模式设置
- 📐 **安全区域**: 完整支持刘海区域和圆角屏幕
- 🔄 **横屏模式**: 横屏时自动调整布局
- ⚡ **120Hz 流畅**: 优化动画以支持 ProMotion 显示
- 🎯 **精确触摸**: 符合 iOS 17 最新触摸标准

## 📖 使用说明

### 搜索模式

1. **普通搜索**: 点击"搜索"按钮，快速获取 Shodan 数据
2. **AI 智能搜索**: 点击"🤖 AI 智能搜索"按钮，获取结果并使用 DeepSeek AI 进行深度分析

### 搜索语法示例

| 查询 | 说明 |
|------|------|
| `apache` | 搜索运行 Apache 的服务器 |
| `port:22` | 搜索开放 SSH 端口的设备 |
| `port:3389` | 搜索开放 RDP 端口的设备 |
| `nginx` | 搜索运行 Nginx 的服务器 |
| `country:CN` | 搜索中国的设备 |
| `city:"Beijing"` | 搜索北京的设备 |
| `org:"Google"` | 搜索 Google 组织的设备 |
| `product:MySQL` | 搜索运行 MySQL 的设备 |
| `apache country:US` | 组合查询：美国的 Apache 服务器 |

### AI 分析功能

DeepSeek AI 会自动为你提供:
- 主要发现和安全风险评估
- 按风险等级排序的设备列表
- 安全加固建议
- 统计摘要（国家分布、端口分布、服务类型等）

### API 端点

#### 搜索设备（带可选 AI 分析）
```
POST /api/search
Content-Type: application/json

{
  "query": "apache",
  "page": 1,
  "useAI": true
}
```

#### AI 分析现有数据
```
POST /api/analyze
Content-Type: application/json

{
  "data": [...],
  "query": "apache"
}
```

#### 健康检查
```
GET /health
```

## 🏗️ 项目结构

```
shodan-info-collector/
├── public/                # 前端文件
│   ├── index.html        # 主页面
│   ├── style.css         # 样式文件
│   └── app.js            # 前端 JavaScript
├── server/               # 后端文件
│   └── server.js         # Express 服务器
├── .env.example          # 环境变量模板
├── .gitignore           # Git 忽略文件
├── package.json         # 项目配置
└── README.md            # 项目文档
```

## 🔧 技术栈

### 前端
- HTML5
- CSS3 (响应式设计)
- Vanilla JavaScript

### 后端
- Node.js
- Express.js
- Axios (HTTP 客户端)
- Cheerio (Web 爬虫)
- DeepSeek API (AI 分析)
- Dotenv (环境变量)

## 📝 常见问题

### Q: 为什么不直接使用 Shodan API？

A: 本工具使用 Web 爬虫从 Shodan 平台获取数据，无需申请和配置 Shodan API Key，降低使用门槛。

### Q: DeepSeek AI 分析需要付费吗？

A: DeepSeek API 有免费额度，足够日常使用。如需更多请求，可以在 [DeepSeek 平台](https://platform.deepseek.com/) 充值。

### Q: 爬虫可能被限制吗？

A: 是的，频繁请求可能被 Shodan 限制。建议：
1. 合理控制搜索频率
2. 避免大量并发请求
3. 仅用于学习和研究目的

### Q: AI 分析准确吗？

A: DeepSeek AI 会基于搜索结果提供专业分析，但仅供参考。实际安全评估需要人工确认。

### Q: 搜索时出现错误怎么办？

A: 请检查:
1. 网络连接是否正常
2. DeepSeek API Key 是否有效
3. 搜索语法是否正确
4. 是否被 Shodan 限制访问

## 🤖 GitHub Actions 自动化

本项目集成了完整的 GitHub Actions 工作流，实现自动化测试和部署。

### 自动设备适配测试

每次代码推送时，会自动测试以下设备的适配情况：

- ✅ iPhone 15 Pro Max (430x932)
- ✅ iPhone 15 Pro (393x852)
- ✅ iPhone SE (375x667)
- ✅ iPad Pro (1024x1366)
- ✅ Android 大屏 (412x915)

### 自动化检查项目

1. **代码质量检查**
   - CSS 语法验证
   - HTML 结构验证
   - JavaScript 语法检查
   - manifest.json 格式验证

2. **移动端性能测试**
   - Lighthouse 移动端评分
   - PWA 功能检查
   - 页面加载速度测试
   - 可访问性验证

3. **响应式设计验证**
   - 多设备视口测试
   - 触摸目标大小检查
   - 安全区域适配验证

### 工作流文件

配置文件位于 `.github/workflows/mobile-adaptation.yml`，包含：

- `mobile-adaptation`: 多设备适配测试
- `build-and-deploy`: 构建和部署
- `lighthouse-mobile`: 移动端性能监控

### 手动触发

可以在 GitHub Actions 页面手动触发工作流：

```bash
# 或使用 GitHub CLI
gh workflow run mobile-adaptation.yml
```

## 🔒 安全建议

1. **保护 API Key**: 不要将 `.env` 文件提交到 Git
2. **限制访问**: 在生产环境中添加认证机制
3. **合法使用**: 仅用于授权的安全测试和研究
4. **速率限制**: 避免频繁爬取导致 IP 被封禁
5. **数据安全**: 不要存储或分享敏感的搜索结果

## 🔓 完全开放说明

本项目**完全开放**，无任何功能限制：

- ✅ 无搜索次数限制
- ✅ 无 AI 分析次数限制
- ✅ 无数据访问限制
- ✅ 无速率限制（合理使用）
- ✅ 无需注册账户
- ✅ 无需付费
- ✅ 可自由修改代码
- ✅ 可商业使用

详细的开放特性说明请查看 [FEATURES.md](FEATURES.md)

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题或建议，请提交 Issue。

---

**再次提醒**: 本工具仅用于合法的安全研究和教育目的！
