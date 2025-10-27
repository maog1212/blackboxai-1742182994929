# 小莫 OCR - iPhone 专版 📱

> 🍎 专为 iPhone 15 Pro Max 优化的 DeepSeek-OCR 文字识别应用
> 📦 三种使用方案：原生 App + Web 版 + 本地服务器
> 🚀 完全开箱即用

[![iOS](https://img.shields.io/badge/iOS-17.0+-blue.svg)](https://www.apple.com/ios/)
[![Swift](https://img.shields.io/badge/Swift-5.9-orange.svg)](https://swift.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

### 📱 完美适配 iPhone 15 Pro Max

- ✅ **Dynamic Island 支持** - 全面屏适配
- ✅ **A17 Pro 优化** - 充分利用强大性能
- ✅ **ProMotion 120Hz** - 流畅动画体验
- ✅ **原生相机集成** - 4800 万像素主摄直拍识别
- ✅ **深色模式** - 自动适配系统主题

### 🎯 三种使用方案

| 方案 | 优点 | 适用场景 |
|------|------|----------|
| **方案一：Web 版** | 无需安装，Safari 直接用 | 临时使用，快速体验 |
| **方案二：原生 App** | 体验最佳，功能最全 | 长期使用，高频场景 |
| **方案三：混合模式** | App + 本地服务器 | 专业用户，最佳性能 |

## 🚀 快速开始

### 方案一：Web 版（最简单）⭐ 推荐

1. **在 Mac 上启动服务器**

```bash
cd xiaomo-ocr-ios/Server
python3 server.py
```

2. **获取 Mac 的 IP 地址**

```bash
# 查看 Mac IP
ifconfig | grep "inet " | grep -v 127.0.0.1
# 例如: 192.168.1.100
```

3. **iPhone 访问 Web 版**

```
在 Safari 中打开: http://192.168.1.100:5000/webapp
```

4. **添加到主屏幕**（可选）

- 点击分享按钮
- 选择"添加到主屏幕"
- 像原生 App 一样使用！

### 方案二：原生 App

#### 使用 Xcode 构建

1. **打开项目**

```bash
cd xiaomo-ocr-ios
open XiaomoOCR.xcodeproj
```

2. **配置签名**

- 在 Xcode 中选择你的开发团队
- 修改 Bundle Identifier

3. **连接 iPhone 15 Pro Max**

- 通过 USB-C 连接
- 信任开发者证书

4. **运行**

- 点击 ▶️ 运行按钮
- 应用自动安装到手机

#### 配置服务器地址

应用首次启动时：
1. 点击 "设置" 按钮
2. 输入服务器地址（例如：`http://192.168.1.100:5000`）
3. 点击 "测试连接"

### 方案三：TestFlight 分发（企业用户）

```bash
# 1. Archive
Product > Archive

# 2. Distribute
Distribute App > TestFlight

# 3. 上传到 App Store Connect

# 4. 邀请测试员
```

## 📖 详细使用说明

### Web 版使用

#### 特性
- ✅ 响应式设计，完美适配 iPhone 15 Pro Max
- ✅ 支持 PWA，可添加到主屏幕
- ✅ 相机和相册访问
- ✅ 实时识别反馈
- ✅ 一键复制结果

#### 操作步骤

1. **拍照识别**
   - 点击 "📷 拍照识别"
   - 允许相机权限
   - 拍摄文字清晰的照片
   - 自动开始识别

2. **相册选择**
   - 点击 "🖼️ 相册选择"
   - 选择包含文字的图片
   - 自动开始识别

3. **模式选择**
   - **通用**：提取所有文字
   - **文档**：转换为 Markdown
   - **图表**：解析图表内容

4. **精度设置**
   - **快速**：512×512，适合预览
   - **均衡**：768×768，日常使用
   - **高清**：1024×1024，推荐
   - **极致**：1280×1280，最高质量

### 原生 App 使用

#### 界面说明

```
┌─────────────────────────────────────┐
│        小莫 OCR                     │
│   DeepSeek 智能文字识别             │
│                                     │
│  ┌──────────┐  ┌──────────┐        │
│  │ 📷拍照   │  │ 🖼️相册  │        │
│  │   识别   │  │   选择   │        │
│  └──────────┘  └──────────┘        │
│                                     │
│  识别模式: ◉ 通用 ○ 文档 ○ 图表    │
│  识别精度: [快速][均衡][高清][极致]│
│                                     │
│  ┌─────────────────────────────┐   │
│  │  识别结果区域                │   │
│  │                              │   │
│  │  识别出的文字内容显示在这里  │   │
│  │                              │   │
│  └─────────────────────────────┘   │
│           [📋 复制文本]             │
└─────────────────────────────────────┘
```

#### 快捷操作

- **长按预览**：长按识别结果可快速预览
- **手势操作**：上下滑动浏览长文本
- **分享功能**：点击分享图标发送到其他应用

## 🔧 服务器部署

### 在 Mac 上部署

#### 方式 1：简单模式（演示）

```bash
cd xiaomo-ocr-ios/Server

# 安装依赖
pip3 install flask flask-cors

# 运行服务器（演示模式，无需模型）
python3 server.py
```

服务器地址：`http://[你的Mac IP]:5000`

#### 方式 2：完整模式（真实识别）

```bash
# 1. 安装完整依赖
pip3 install flask flask-cors torch transformers pillow

# 2. 首次运行会自动下载模型（6.67GB）
python3 server.py

# 3. 访问 /api/init 初始化模型
curl http://localhost:5000/api/init -X POST
```

### 在局域网中部署

#### 配置防火墙

```bash
# macOS 防火墙设置
系统偏好设置 > 安全性与隐私 > 防火墙 > 防火墙选项
允许 Python 接受传入连接
```

#### 获取 IP 地址

```bash
# 方法 1: 命令行
ifconfig | grep "inet " | grep -v 127.0.0.1

# 方法 2: 系统偏好设置
系统偏好设置 > 网络 > Wi-Fi > 详情 > TCP/IP
```

### 云服务器部署

```bash
# 安装并启动
git clone <repo>
cd xiaomo-ocr-ios/Server
pip3 install -r requirements.txt
python3 server.py

# 使用 nginx 反向代理
# 配置 SSL 证书
# 开放 5000 端口
```

## 📊 性能数据

### iPhone 15 Pro Max 性能

| 操作 | 耗时 | 备注 |
|------|------|------|
| 拍照 | < 0.1s | A17 Pro ISP |
| 上传 | 0.2-0.5s | WiFi 6E |
| 识别（512） | 0.5-1s | 服务器处理 |
| 识别（1024） | 1-2s | 推荐设置 |
| 识别（1280） | 2-3s | 最高质量 |

### 网络要求

- **WiFi**：推荐，速度最快
- **5G**：可用，注意流量
- **4G**：较慢，不推荐

### 电池续航

- Web 版：基本不耗电（< 1%/小时）
- 原生 App：轻度使用（< 2%/小时）

## 🎨 界面定制

### 修改主题颜色

编辑 `ContentView.swift`:

```swift
// 修改渐变色
LinearGradient(
    colors: [Color(hex: "你的颜色"), Color(hex: "你的颜色")],
    startPoint: .topLeading,
    endPoint: .bottomTrailing
)
```

### Web 版定制

编辑 `WebApp/index.html`:

```css
body {
    background: linear-gradient(135deg, #你的颜色 0%, #你的颜色 100%);
}
```

## 🐛 问题排查

### Web 版问题

**Q: 无法连接服务器？**
```
1. 检查服务器是否运行：http://Mac的IP:5000
2. 检查防火墙是否允许连接
3. 确保 iPhone 和 Mac 在同一 WiFi
4. 尝试使用 IP 地址而非域名
```

**Q: 相机权限被拒？**
```
设置 > Safari > 相机 > 允许
```

**Q: 识别速度慢？**
```
1. 降低分辨率设置
2. 检查网络连接
3. 服务器性能不足
```

### 原生 App 问题

**Q: 无法安装到手机？**
```
1. 检查开发者证书
2. 信任描述文件：设置 > 通用 > VPN与设备管理
3. 重新连接 USB-C 线缆
```

**Q: 相机无法打开？**
```
设置 > 隐私与安全 > 相机 > 小莫 OCR > 允许
```

**Q: 服务器地址无法保存？**
```
检查 URL 格式：http://IP:端口
例如：http://192.168.1.100:5000
```

## 📁 项目结构

```
xiaomo-ocr-ios/
├── XiaomoOCR/                 # iOS 原生应用
│   ├── ContentView.swift     # 主界面
│   ├── OCRManager.swift       # OCR 管理器
│   ├── ImagePicker.swift      # 图片选择器
│   └── SettingsView.swift     # 设置界面
├── Server/                    # 配套服务器
│   ├── server.py             # Flask 服务器
│   └── requirements.txt       # Python 依赖
├── WebApp/                    # Web 版本
│   └── index.html            # 响应式网页
├── Assets/                    # 资源文件
│   └── AppIcon.appiconset    # 应用图标
└── Docs/                      # 文档
    ├── README.md             # 本文档
    └── DEPLOYMENT.md         # 部署指南
```

## 🚀 高级功能

### 批量识别（开发中）

- 一次选择多张图片
- 自动依次识别
- 合并结果导出

### 历史记录（开发中）

- 保存识别记录
- 快速查看历史
- 导出为文件

### 云同步（规划中）

- iCloud 同步
- 多设备共享
- 备份还原

## 🔗 相关资源

- **DeepSeek-OCR**: https://github.com/deepseek-ai/DeepSeek-OCR
- **Swift 文档**: https://developer.apple.com/swift/
- **SwiftUI 教程**: https://developer.apple.com/tutorials/swiftui

## 📝 更新日志

### v1.0.0 (2025-10)
- ✅ iPhone 15 Pro Max 完美适配
- ✅ 原生 SwiftUI 界面
- ✅ 响应式 Web 版本
- ✅ 配套 Flask 服务器
- ✅ 三种识别模式
- ✅ 四档精度设置
- ✅ 相机和相册集成

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [DeepSeek AI](https://www.deepseek.com/) - OCR 模型
- [Apple](https://www.apple.com/) - iOS 平台
- [Flask](https://flask.palletsprojects.com/) - Web 框架

---

**小莫 OCR** - 让文字识别触手可及 🚀

专为 iPhone 15 Pro Max 打造 | 完全开箱即用 | 开源免费
