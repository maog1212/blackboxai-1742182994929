# 抖音 / 快手截图工具（支持 OpenClaw + DeepSeek + 手机下载门户）

## 1. 安装

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## 2. 截图模式

### 2.1 manual（直接截图）

```bash
python douyin_kuaishou_screenshot.py \
  --mode manual \
  --url "https://www.kuaishou.com/profile/你的用户ID" \
  --output "./shots/kuaishou.png" \
  --wait-ms 7000 \
  --full-page
```

### 2.2 openclaw（DeepSeek 生成截图计划）

```bash
export DEEPSEEK_API_KEY="你的 key"
python douyin_kuaishou_screenshot.py \
  --mode openclaw \
  --platform douyin \
  --request-text "截取主页头像和昵称" \
  --url "https://www.douyin.com/user/你的用户ID" \
  --output "./shots/dy_auto.png"
```

仅预览计划：

```bash
python douyin_kuaishou_screenshot.py \
  --mode openclaw \
  --platform douyin \
  --request-text "截取主页第一屏" \
  --url "https://www.douyin.com/user/你的用户ID" \
  --output "./shots/preview.png" \
  --dry-run-plan
```

## 3. portal（移动端下载门户）

```bash
python douyin_kuaishou_screenshot.py \
  --mode portal \
  --host 0.0.0.0 \
  --port 8765 \
  --android-package ./mobile_downloads/app-release.apk \
  --ios-package ./mobile_downloads/app-release.ipa
```

手机访问 `http://服务器IP:8765` 后可：

- 下载 Android 安装包（APK）
- 下载 iOS 安装包（IPA）
- 点按 **OpenClaw 一键安装检测/修复重装**（检测未安装、安装失败、安装包损坏后可一键重装）
- 在页面更新 API Key / Model / Base URL 并立即生效
- 在页面里直接调用 OpenClaw 接口生成截图计划

> 说明：脚本会自动创建占位安装包文件；你只需把占位文件替换为真实安装包即可。

## 4. 关键接口

- `GET /healthz`：服务健康检查
- `GET /download/android`：下载 Android 包
- `GET /download/ios`：下载 iOS 包
- `GET /api/openclaw/install/check`：检查 OpenClaw 安装完整性
- `POST /api/openclaw/install/repair`：一键检测并修复重装
- `POST /api/openclaw/config`：更新 API 配置（`deepseek_api_key/deepseek_model/deepseek_base_url`）
- `POST /api/openclaw-plan`：请求体含 `platform/url/request_text`，返回计划 JSON

## 5. 注意事项

- 请仅在有授权场景下抓取或截图内容。
- iOS 真机安装 IPA 受苹果签名与分发机制限制（如 TestFlight/企业签名/MDM）。
- 生产环境建议通过 HTTPS + 鉴权保护下载与 API 接口。
