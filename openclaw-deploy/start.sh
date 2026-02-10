#!/usr/bin/env bash
###############################################################################
# OpenClaw 全能压缩精华版 — 一键启动器
# 用法: bash start.sh
# 功能: 启动 Web 控制台，打开浏览器，用户点击按钮即可完成部署
###############################################################################
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${DEPLOY_PORT:-8080}"

# ── 颜色 ────────────────────────────────────────────────
GREEN='\033[0;32m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

echo ""
echo -e "${BOLD}${CYAN}"
echo "  ╔═══════════════════════════════════════════════════════╗"
echo "  ║   🦞  OpenClaw 全能压缩精华版 — 一键部署系统         ║"
echo "  ║   原名 MoltBot / Clawdbot | 开源个人 AI 助手        ║"
echo "  ╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ── 检查 Python3 ──────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "正在安装 Python3..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y -qq python3 2>/dev/null
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y python3 2>/dev/null
    elif command -v brew &>/dev/null; then
        brew install python3 2>/dev/null
    else
        echo "错误: 请先安装 Python 3"
        exit 1
    fi
fi

# ── 确保 deploy.sh 可执行 ──────────────────────────────────
chmod +x "$SCRIPT_DIR/deploy.sh" 2>/dev/null || true

# ── 尝试打开浏览器 ──────────────────────────────────────
open_browser() {
    local url="http://127.0.0.1:$PORT"
    sleep 1
    if command -v xdg-open &>/dev/null; then
        xdg-open "$url" 2>/dev/null &
    elif command -v open &>/dev/null; then
        open "$url" 2>/dev/null &
    elif command -v start &>/dev/null; then
        start "$url" 2>/dev/null &
    else
        echo -e "${GREEN}请在浏览器中打开: ${BOLD}$url${NC}"
    fi
}

open_browser &

# ── 启动 Web 服务器 ──────────────────────────────────────
exec python3 "$SCRIPT_DIR/server.py"
