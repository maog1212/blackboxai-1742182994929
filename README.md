# blackboxai-1742182994929

Built by https://www.blackbox.ai

## 抖音 / 快手截图程序（manual + OpenClaw + Mobile Portal）

脚本：`douyin_kuaishou_screenshot.py`

### 1) 手动截图（manual）

```bash
python douyin_kuaishou_screenshot.py \
  --mode manual \
  --url "https://www.douyin.com/user/你的用户ID" \
  --output "./shots/user.png" \
  --full-page
```

### 2) OpenClaw + DeepSeek 自动规划

```bash
export DEEPSEEK_API_KEY="你的 key"
python douyin_kuaishou_screenshot.py \
  --mode openclaw \
  --platform douyin \
  --request-text "我要用户主页第一屏截图" \
  --url "https://www.douyin.com/user/你的用户ID" \
  --output "./shots/auto.png"
```


### 快速入口（本地默认）
- 网页版 URL：`http://127.0.0.1:8765`
- Android 安装包：`http://127.0.0.1:8765/download/android`
- iOS 安装包：`http://127.0.0.1:8765/download/ios`

> 启动后将 `127.0.0.1` 替换为你的服务器IP，即可给手机访问。

### 3) 手机下载门户（Android/iOS + 一键检测修复）

```bash
python douyin_kuaishou_screenshot.py \
  --mode portal \
  --host 0.0.0.0 \
  --port 8765 \
  --android-package ./mobile_downloads/app-release.apk \
  --ios-package ./mobile_downloads/app-release.ipa
```

手机打开：`http://你的服务器IP:8765`

- 支持下载 Android / iOS 安装包（替换成你自己的真实包）。
- 新增 **OpenClaw 一键安装检测/修复重装** 按钮（检测未安装、损坏会自动重装占位包）。
- 新增 **API 配置更新** 区域，用户可随时更换 API Key / Model / Base URL，保存后立即生效。
- 内置 OpenClaw 计划接口 `/api/openclaw-plan`，与 DeepSeek 联动。

详细说明见：`USAGE_抖音快手截图工具.md`。
