# 豆包识别自动生成系统 / Doubao AI Generator

🤖 基于AI的智能识别与内容自动生成系统，支持文本识别、情感分析、实体提取和多种内容自动生成功能。

## ✨ 核心功能

### 🔍 AI智能识别
- **文本识别** - 自动识别文本中的关键信息
- **实体提取** - 提取人名、地名、机构名等实体
- **情感分析** - 分析文本的情感倾向（积极/消极/中性）
- **分类识别** - 自动将文本分类到不同类别
- **关键词提取** - 提取文本核心关键词
- **自动摘要** - 生成文本摘要

### ✨ 内容自动生成
- **文章生成** - 根据主题自动生成完整文章
- **摘要生成** - 浓缩长文本为简洁摘要
- **标题生成** - 生成吸引人的标题
- **描述生成** - 生成产品/服务描述
- **关键词生成** - 生成SEO关键词列表
- **问答生成** - 自动生成常见问答

### 📝 模板管理
- **预设模板** - 内置5+常用生成模板
- **自定义模板** - 创建个性化生成模板
- **模板复用** - 一键使用热门模板
- **使用统计** - 跟踪模板使用情况

### 📊 数据统计
- **任务统计** - 识别/生成任务数据分析
- **成功率追踪** - 任务成功率实时监控
- **字数统计** - 总生成字数统计
- **性能指标** - 处理时间等性能数据

## 🚀 快速开始

### 方法一：Replit 一键部署（最简单）

1. **访问** [Replit.com](https://replit.com) 并登录
2. **导入项目**
   - 点击 `+ Create Repl`
   - 选择 `Import from GitHub`
   - 输入项目地址
3. **点击 Run 按钮** - 完成！
   - 自动安装依赖
   - 自动初始化数据
   - 获得公网URL

### 方法二：本地运行

```bash
# 1. 解压文件
tar -xzf doubao-ai-generator.tar.gz
cd doubao-ai-generator

# 2. 安装依赖
npm install

# 3. 初始化数据库（首次运行）
npm run seed

# 4. 启动服务
npm start

# 5. 访问系统
浏览器打开: http://localhost:3000
```

## 📱 在手机上使用

### iPhone / iPad

1. **Replit部署后**，获取URL（如 `https://your-project.username.repl.co`）

2. **打开Safari浏览器**，输入URL

3. **添加到主屏幕**：
   - 点击 📤 分享按钮
   - 选择"添加到主屏幕"
   - 现在可以像APP一样使用！

## 💡 使用教程

### 第一步：AI识别

1. 点击顶部"AI识别"标签
2. 输入任务名称
3. 选择识别类型
4. 粘贴或输入要识别的文本
5. 点击"开始AI识别"
6. 查看识别结果

### 第二步：内容生成

1. 点击顶部"内容生成"标签
2. 输入任务名称
3. 选择生成模板
4. 选择生成类型
5. 输入提示词或主题
6. 点击"开始AI生成"
7. 查看生成的内容

### 第三步：查看统计

1. 点击顶部"数据统计"标签
2. 查看任务统计、成功率
3. 查看各类型任务分布
4. 查看热门模板排行

## 🎯 核心特性

| 特性 | 说明 |
|------|------|
| 🆓 **完全免费** | 开源免费使用 |
| ⚡ **快速响应** | 平均处理时间<1秒 |
| 🎨 **简洁界面** | 现代化UI设计 |
| 📱 **移动友好** | 完美适配手机 |
| 🔄 **实时处理** | 即时获取结果 |
| 💾 **历史记录** | 保存所有任务 |
| 📊 **数据可视化** | 直观的统计图表 |

## 📁 项目结构

```
doubao-ai-generator/
├── database/              # 数据库
│   ├── db.js             # 数据库连接
│   └── schema.sql        # 数据库结构
├── public/               # 前端资源
│   ├── css/
│   ├── js/
│   └── index.html
├── routes/               # API路由
│   └── api.js
├── scripts/              # 工具脚本
│   ├── auto-init.js     # 自动初始化
│   └── seed-data.js     # 示例数据
├── services/             # 业务逻辑
│   ├── aiService.js     # AI服务
│   └── taskService.js   # 任务服务
├── .replit              # Replit配置
├── package.json         # 项目配置
├── README.md           # 说明文档
└── server.js           # 服务器入口
```

## 🔌 API 接口

### 识别任务

```bash
# 创建识别任务
POST /api/recognition
{
  "task_name": "客户反馈分析",
  "task_type": "sentiment",
  "input_content": "文本内容..."
}

# 获取识别任务列表
GET /api/recognition?page=1&pageSize=20

# 获取识别任务详情
GET /api/recognition/:id

# 删除识别任务
DELETE /api/recognition/:id
```

### 生成任务

```bash
# 创建生成任务
POST /api/generation
{
  "task_name": "产品介绍",
  "template_id": 1,
  "generation_type": "article",
  "prompt": "AI技术",
  "context": { "topic": "人工智能" }
}

# 获取生成任务列表
GET /api/generation?page=1&pageSize=20

# 获取生成任务详情
GET /api/generation/:id

# 删除生成任务
DELETE /api/generation/:id
```

### 模板管理

```bash
# 获取模板列表
GET /api/templates

# 创建模板
POST /api/templates
{
  "template_name": "我的模板",
  "template_type": "article",
  "description": "模板描述",
  "prompt_template": "提示词模板",
  "parameters": {}
}
```

### 统计数据

```bash
# 获取统计数据
GET /api/statistics
```

## 🛠️ 技术栈

### 后端
- **Node.js** - JavaScript运行环境
- **Express** - Web框架
- **SQLite3** - 轻量级数据库
- **CORS** - 跨域支持

### 前端
- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **Vanilla JavaScript** - 交互逻辑
- **响应式设计** - 移动端适配

## 📊 数据库设计

### 核心表

- **recognition_tasks** - 识别任务表
- **generation_tasks** - 生成任务表
- **templates** - 模板表
- **tags** - 标签表
- **statistics** - 统计表

## 🔧 配置说明

### 环境变量

创建 `.env` 文件：

```env
PORT=3000
NODE_ENV=production
```

### 自定义配置

编辑 `package.json` 中的脚本：

```json
{
  "scripts": {
    "start": "node scripts/auto-init.js && node server.js",
    "dev": "nodemon server.js",
    "seed": "node scripts/seed-data.js"
  }
}
```

## 🎓 接入真实AI API

本系统使用模拟AI功能，如需接入真实API（如豆包/OpenAI）：

1. 编辑 `services/aiService.js`
2. 替换模拟函数为真实API调用
3. 添加API密钥配置

示例：

```javascript
// 接入豆包API
async recognizeText(text) {
    const response = await fetch('https://ark.cn-beijing.volces.com/api/v3/...', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${process.env.DOUBAO_API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: 'doubao-pro',
            messages: [{ role: 'user', content: text }]
        })
    });

    return await response.json();
}
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🎁 预设模板

系统内置5个常用模板：

1. **产品介绍文章模板** - 生成专业产品介绍
2. **营销文案模板** - 创建吸引人的营销内容
3. **内容摘要模板** - 浓缩长文本为摘要
4. **SEO标题生成器** - 生成SEO优化标题
5. **问答内容生成器** - 生成常见问答

## 💪 系统优势

- ✅ **零配置部署** - Replit一键运行
- ✅ **智能识别** - 多维度文本分析
- ✅ **批量生成** - 高效内容创作
- ✅ **模板复用** - 提升工作效率
- ✅ **数据统计** - 了解使用情况
- ✅ **移动适配** - 随时随地使用

## 📞 技术支持

- 查看项目文档
- 提交GitHub Issue
- 查看示例代码

---

**🎊 开始使用豆包识别自动生成系统，让AI助力您的内容创作！**
