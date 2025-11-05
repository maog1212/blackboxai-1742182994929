# 🔍 Shodan 信息收集工具

基于 Shodan API 的简单信息收集网站，用于安全研究和教育目的。

## ⚠️ 免责声明

**本工具仅用于合法的安全研究和教育目的。使用本工具进行任何非法活动，后果自负。**

- 仅在获得授权的情况下使用
- 遵守当地法律法规
- 尊重他人隐私和数据安全

## ✨ 功能特性

- 🔎 **强大的搜索功能**: 支持 Shodan 全部搜索语法
- 📊 **结果展示**: 清晰展示设备信息、端口、位置等
- 🎯 **快速过滤**: 预设常用搜索查询
- 💻 **现代化界面**: 简洁美观的用户界面
- 🌐 **RESTful API**: 完整的后端 API 接口

## 📋 前置要求

- Node.js (v14 或更高版本)
- npm 或 yarn
- Shodan API Key ([获取地址](https://account.shodan.io/))

## 🚀 快速开始

### 1. 安装依赖

```bash
cd shodan-info-collector
npm install
```

### 2. 配置 API Key

复制 `.env.example` 文件并重命名为 `.env`:

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的 Shodan API Key:

```env
SHODAN_API_KEY=your_actual_api_key_here
PORT=3000
```

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

## 📖 使用说明

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

### API 端点

#### 搜索设备
```
POST /api/search
Content-Type: application/json

{
  "query": "apache",
  "page": 1
}
```

#### 获取主机信息
```
GET /api/host/:ip
```

#### 获取 API 信息
```
GET /api/info
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
- Axios
- Dotenv

## 📝 常见问题

### Q: 如何获取 Shodan API Key?

A: 访问 [Shodan 账户页面](https://account.shodan.io/)，注册账户后即可获得免费的 API Key。

### Q: 免费 API Key 有什么限制?

A: 免费账户有以下限制:
- 每月 100 次查询积分
- 最多返回前 100 个结果
- 某些高级功能不可用

### Q: 搜索时出现错误怎么办?

A: 请检查:
1. API Key 是否正确配置
2. 是否还有剩余查询积分
3. 搜索语法是否正确
4. 网络连接是否正常

### Q: 如何升级到更多功能?

A: 可以在 Shodan 网站购买付费计划，获得更多查询积分和高级功能。

## 🔒 安全建议

1. **保护 API Key**: 不要将 `.env` 文件提交到 Git
2. **限制访问**: 在生产环境中添加认证机制
3. **合法使用**: 仅用于授权的安全测试
4. **速率限制**: 避免频繁请求导致 API 被限制

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题或建议，请提交 Issue。

---

**再次提醒**: 本工具仅用于合法的安全研究和教育目的！
