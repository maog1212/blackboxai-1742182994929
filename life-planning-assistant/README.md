# 🎯 人生规划助手 (Life Planning Assistant)

一个基于 DeepSeek AI 的智能人生规划助手，帮助您制定和实现人生目标。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![DeepSeek](https://img.shields.io/badge/Powered%20by-DeepSeek-purple.svg)

## ✨ 功能特点

- 📋 **目标设定与规划**：帮助制定短期、中期和长期目标
- 💼 **职业发展指导**：提供职业规划和发展建议
- 📚 **学习成长计划**：个性化学习路线图制定
- ⏰ **时间管理**：优化时间分配，提高效率
- ⚖️ **工作生活平衡**：在事业、家庭、健康等方面找到平衡
- 💰 **财务规划建议**：基础理财思路和建议
- 🎯 **目标追踪**：定期回顾进展，调整计划
- 💬 **智能对话**：自然流畅的中文交流体验

## 🚀 快速开始

### 1. 获取 DeepSeek API Key

访问 [DeepSeek 官网](https://platform.deepseek.com/) 注册账号并获取 API Key。

### 2. 本地运行

```bash
# 克隆项目
git clone <your-repo-url>

# 进入项目目录
cd life-planning-assistant

# 直接使用浏览器打开 index.html
# 或使用本地服务器（推荐）
python -m http.server 8000
# 或
npx serve
```

### 3. 配置 API Key

1. 在浏览器中打开应用
2. 点击右下角的 ⚙️ 设置按钮
3. 输入您的 DeepSeek API Key
4. 点击"保存设置"

### 4. 开始使用

现在您可以开始与人生规划助手对话了！尝试以下问题：

- "帮我制定一个3个月的学习计划"
- "我想规划一下职业发展，给我一些建议"
- "帮我分析如何平衡工作和生活"
- "我想设定一些人生目标，你能帮我吗？"

## 📁 项目结构

```
life-planning-assistant/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── app.js          # 应用逻辑和 API 集成
└── README.md           # 项目文档
```

## 🔧 技术栈

- **前端**：HTML5, CSS3, 原生 JavaScript
- **AI 模型**：DeepSeek Chat API
- **存储**：浏览器 LocalStorage

## 💡 使用技巧

1. **持续对话**：应用会保存对话历史，助手能记住之前的内容
2. **快捷按钮**：使用界面上的快捷按钮快速开始常见话题
3. **清空对话**：点击右下角的 🗑️ 按钮可以清空对话历史
4. **隐私安全**：API Key 仅保存在您的浏览器本地，不会上传到任何服务器

## 🎨 功能演示

### 主界面
- 现代化的渐变背景设计
- 响应式布局，支持移动端
- 流畅的动画效果

### 对话功能
- 用户消息显示在右侧（紫色气泡）
- 助手回复显示在左侧（灰色气泡）
- 打字指示器显示 AI 正在思考

### 快捷操作
- 学习计划、职业规划、生活平衡、目标设定等快捷按钮
- 一键发送常见问题

## ⚙️ API 配置说明

应用使用 DeepSeek Chat API，配置参数如下：

```javascript
{
  model: 'deepseek-chat',
  temperature: 0.7,      // 控制回复的创造性
  max_tokens: 2000,      // 最大回复长度
  top_p: 0.95,          // 核采样参数
}
```

## 🔐 隐私与安全

- ✅ API Key 仅存储在浏览器本地
- ✅ 对话记录仅保存在您的设备上
- ✅ 不会收集或上传任何用户数据
- ✅ 支持随时清空对话历史

## 📱 浏览器兼容性

- ✅ Chrome (推荐)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ 现代移动浏览器

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 感谢 [DeepSeek](https://www.deepseek.com/) 提供强大的 AI 能力
- 项目使用了现代化的 Web 技术栈

## 📞 联系方式

如有问题或建议，欢迎提 Issue！

---

**开始规划您的人生，让 AI 助手成为您的成长伙伴！** 🚀
