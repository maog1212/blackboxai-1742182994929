# 图标设置说明

## 快速开始（使用在线工具）

1. **使用 icon.svg 生成所有尺寸**

   访问 https://realfavicongenerator.net/ 或 https://favicon.io/

   上传 `public/icon.svg` 文件，生成所有需要的尺寸：
   - icon-72.png
   - icon-96.png
   - icon-128.png
   - icon-144.png
   - icon-152.png (iOS)
   - icon-167.png (iOS iPad)
   - icon-180.png (iOS)
   - icon-192.png (Android)
   - icon-384.png
   - icon-512.png (PWA)
   - favicon-16.png
   - favicon-32.png

2. **下载生成的图标**

   将所有图标文件放到 `public/` 目录

## 使用命令行工具（可选）

如果你安装了 ImageMagick，可以使用以下命令：

```bash
cd public/

# 生成各种尺寸
convert icon.svg -resize 72x72 icon-72.png
convert icon.svg -resize 96x96 icon-96.png
convert icon.svg -resize 128x128 icon-128.png
convert icon.svg -resize 144x144 icon-144.png
convert icon.svg -resize 152x152 icon-152.png
convert icon.svg -resize 167x167 icon-167.png
convert icon.svg -resize 180x180 icon-180.png
convert icon.svg -resize 192x192 icon-192.png
convert icon.svg -resize 384x384 icon-384.png
convert icon.svg -resize 512x512 icon-512.png
convert icon.svg -resize 32x32 favicon-32.png
convert icon.svg -resize 16x16 favicon-16.png
```

## 自定义图标

如果你想自定义图标设计：

1. 编辑 `public/icon.svg` 文件
2. 使用设计工具（如 Figma, Sketch, Illustrator）创建 512x512 的图标
3. 导出为 SVG 格式
4. 使用上述方法生成各种尺寸

## 验证图标

1. 在 iOS Safari 中打开网站
2. 点击"分享"按钮
3. 选择"添加到主屏幕"
4. 检查图标显示是否正确

## 临时解决方案

如果暂时没有图标文件，网站仍然可以正常运行。浏览器会使用默认图标。
