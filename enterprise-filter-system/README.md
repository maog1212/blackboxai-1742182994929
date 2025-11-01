# 企业筛选资源体系 / Enterprise Filter System

一个完整的企业筛选资源管理系统，提供强大的企业信息管理、多维度筛选、数据统计和导出功能。

A complete enterprise filtering resource management system that provides powerful enterprise information management, multi-dimensional filtering, data statistics, and export capabilities.

## 📋 功能特性 / Features

### 核心功能 / Core Features

- **企业信息管理** - 完整的企业信息录入、编辑、查询
  - Enterprise Information Management - Complete enterprise data entry, editing, and querying

- **多维度筛选** - 支持按行业、规模、地区、标签等多种条件组合筛选
  - Multi-dimensional Filtering - Supports filtering by industry, scale, region, tags, and more

- **高级搜索** - 关键词全文搜索，快速定位目标企业
  - Advanced Search - Full-text keyword search for quick enterprise location

- **数据统计** - 实时统计分析，多维度数据可视化
  - Data Statistics - Real-time statistical analysis with multi-dimensional visualization

- **数据导出** - 支持筛选结果导出为CSV格式
  - Data Export - Export filtered results to CSV format

- **响应式设计** - 适配桌面端和移动端
  - Responsive Design - Optimized for desktop and mobile devices

### 筛选维度 / Filtering Dimensions

- 行业分类 / Industry Classification
- 企业规模 / Enterprise Scale
- 地理区域 / Geographic Region
- 城市分布 / City Distribution
- 信用评级 / Credit Rating
- 注册资本范围 / Registered Capital Range
- 员工数量范围 / Employee Count Range
- 年营收范围 / Annual Revenue Range
- 企业标签 / Enterprise Tags
- 企业状态 / Enterprise Status

## 🚀 快速开始 / Quick Start

### 环境要求 / Requirements

- Node.js >= 14.0.0
- npm >= 6.0.0

### 安装步骤 / Installation

1. **克隆项目 / Clone the repository**
   ```bash
   cd enterprise-filter-system
   ```

2. **安装依赖 / Install dependencies**
   ```bash
   npm install
   ```

3. **配置环境变量 / Configure environment**
   ```bash
   cp .env.example .env
   ```

4. **初始化数据库 / Initialize database**
   ```bash
   npm run seed
   ```

5. **启动服务 / Start server**
   ```bash
   npm start
   ```

6. **访问系统 / Access system**
   ```
   打开浏览器访问: http://localhost:3000
   Open browser and visit: http://localhost:3000
   ```

## 📁 项目结构 / Project Structure

```
enterprise-filter-system/
├── database/               # 数据库相关
│   ├── db.js              # 数据库连接和操作
│   └── schema.sql         # 数据库表结构
├── public/                # 前端静态文件
│   ├── css/
│   │   └── style.css     # 样式文件
│   ├── js/
│   │   └── app.js        # 前端应用逻辑
│   └── index.html        # 主页面
├── routes/                # API路由
│   └── api.js            # API接口定义
├── scripts/               # 工具脚本
│   └── seed-data.js      # 示例数据脚本
├── services/              # 业务逻辑层
│   └── enterpriseService.js  # 企业服务
├── .env.example          # 环境配置示例
├── .gitignore           # Git忽略文件
├── package.json         # 项目配置
├── README.md           # 项目说明
└── server.js           # 服务器入口
```

## 🔌 API接口 / API Endpoints

### 企业管理 / Enterprise Management

- `GET /api/enterprises` - 获取企业列表
- `GET /api/enterprises/:id` - 获取企业详情
- `POST /api/enterprises` - 创建企业
- `PUT /api/enterprises/:id` - 更新企业
- `DELETE /api/enterprises/:id` - 删除企业

### 筛选与统计 / Filtering & Statistics

- `POST /api/enterprises/filter` - 高级筛选
- `GET /api/statistics` - 获取统计数据
- `GET /api/filter-options` - 获取筛选选项
- `POST /api/export` - 导出数据

## 🎨 技术栈 / Tech Stack

### 后端 / Backend
- **Node.js** - JavaScript运行环境
- **Express** - Web应用框架
- **SQLite3** - 轻量级数据库
- **CORS** - 跨域资源共享

### 前端 / Frontend
- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **Vanilla JavaScript** - 交互逻辑
- **Responsive Design** - 响应式布局

## 📊 数据模型 / Data Model

### 核心表 / Core Tables

1. **enterprises** - 企业信息表
   - 基本信息、联系方式、财务数据、资质认证等

2. **industries** - 行业分类表
   - 支持层级化的行业分类

3. **tags** - 标签表
   - 灵活的标签系统

4. **enterprise_tags** - 企业标签关联表
   - 多对多关系

5. **enterprise_resources** - 企业资源表
   - 企业拥有的各类资源

6. **filter_history** - 筛选历史表
   - 记录筛选操作

## 🔍 使用示例 / Usage Examples

### 筛选示例 / Filter Example

```javascript
// 筛选广东省的高新技术企业
POST /api/enterprises/filter
{
  "filters": {
    "region": ["广东省"],
    "tags": ["高新技术"],
    "creditRating": ["AAA", "AA"]
  },
  "page": 1,
  "pageSize": 20
}
```

### 统计查询 / Statistics Query

```javascript
// 获取企业统计数据
GET /api/statistics

Response:
{
  "success": true,
  "data": {
    "total": 100,
    "byIndustry": [...],
    "byScale": [...],
    "byRegion": [...]
  }
}
```

## 🛠️ 开发指南 / Development Guide

### 开发模式 / Development Mode

```bash
npm run dev
```

### 重置数据库 / Reset Database

```bash
rm database/enterprise_filter.db
npm run seed
```

### 数据库迁移 / Database Migration

数据库schema定义在 `database/schema.sql`，修改后需要重新初始化数据库。

Database schema is defined in `database/schema.sql`. After modification, reinitialize the database.

## 📝 配置说明 / Configuration

### 环境变量 / Environment Variables

参考 `.env.example` 文件进行配置：

- `PORT` - 服务器端口（默认: 3000）
- `DB_PATH` - 数据库文件路径
- `CORS_ORIGIN` - CORS配置
- `LOG_LEVEL` - 日志级别
- `DEFAULT_PAGE_SIZE` - 默认分页大小

## 🔒 安全建议 / Security Recommendations

1. 生产环境请修改默认端口
2. 配置适当的CORS策略
3. 添加身份验证和授权机制
4. 定期备份数据库
5. 使用HTTPS协议

## 🚧 扩展建议 / Extension Suggestions

- [ ] 添加用户认证和权限管理
- [ ] 支持更多导出格式（Excel, PDF）
- [ ] 添加企业对比功能
- [ ] 实现数据导入功能
- [ ] 添加高级数据可视化（图表）
- [ ] 支持企业评分和排名
- [ ] 添加邮件通知功能
- [ ] 实现API限流和缓存

## 📄 许可证 / License

MIT License

## 👥 贡献 / Contributing

欢迎提交Issue和Pull Request！

Welcome to submit Issues and Pull Requests!

## 📞 联系方式 / Contact

如有问题或建议，请通过以下方式联系：

For questions or suggestions, please contact via:

- Issue Tracker
- Email

---

**企业筛选资源体系** - 让企业管理更高效 🚀

**Enterprise Filter System** - Make enterprise management more efficient 🚀
