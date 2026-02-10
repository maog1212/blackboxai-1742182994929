#!/usr/bin/env bash
###############################################################################
# OpenClaw 全能压缩精华版 — 一键部署脚本
# 全自动: 安装 Node.js → 安装 OpenClaw → 配置 → 启动 Gateway
# 支持: Docker / NPM / 源码编译 三种模式
###############################################################################
set -euo pipefail

# ── 全局配置 ─────────────────────────────────────────────────────────────────
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
OPENCLAW_WORKSPACE="${OPENCLAW_HOME}/workspace"
OPENCLAW_LOG="${OPENCLAW_HOME}/deploy.log"
GATEWAY_PORT="${OPENCLAW_GATEWAY_PORT:-18789}"
DEPLOY_MODE="${DEPLOY_MODE:-auto}"          # auto | docker | npm | source
AI_PROVIDER="${AI_PROVIDER:-anthropic}"     # anthropic | openai | ollama
AI_MODEL="${AI_MODEL:-}"
API_KEY="${API_KEY:-}"
NVM_DIR_PATH="${NVM_DIR:-$HOME/.nvm}"
NODE_MIN_VERSION=22

# ── 颜色 ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# ── 日志函数 ─────────────────────────────────────────────────────────────────
_log()      { echo -e "$1[$(date +%H:%M:%S)]${NC} $2" | tee -a "$OPENCLAW_LOG" 2>/dev/null; }
log()       { _log "$CYAN" "$*"; }
ok()        { _log "$GREEN" "[OK] $*"; }
warn()      { _log "$YELLOW" "[!] $*"; }
err()       { _log "$RED" "[ERR] $*"; }

# 进度报告 — 供 server.py 的 SSE 解析
progress() {
    local pct="$1" msg="$2" status="${3:-running}"
    echo "PROGRESS:{\"percent\":$pct,\"message\":\"$msg\",\"status\":\"$status\"}"
}

trap 'if [ $? -ne 0 ]; then err "部署失败，查看日志: $OPENCLAW_LOG"; progress 0 "部署失败" "error"; fi' EXIT

# ══════════════════════════════════════════════════════════════════════════════
#  操作系统检测
# ══════════════════════════════════════════════════════════════════════════════
detect_os() {
    OS_TYPE="$(uname -s)"
    case "$OS_TYPE" in
        Linux*)  OS="linux" ;;
        Darwin*) OS="macos" ;;
        MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
        *)       OS="unknown" ;;
    esac

    ARCH="$(uname -m)"
    case "$ARCH" in
        x86_64|amd64)  ARCH="x64" ;;
        aarch64|arm64) ARCH="arm64" ;;
    esac

    # 发行版检测
    DISTRO="unknown"
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO="${ID:-unknown}"
    fi

    log "系统: $OS ($DISTRO) | 架构: $ARCH"
}

# ══════════════════════════════════════════════════════════════════════════════
#  自动选择部署模式
# ══════════════════════════════════════════════════════════════════════════════
auto_select_mode() {
    if [ "$DEPLOY_MODE" != "auto" ]; then
        log "用户指定部署模式: $DEPLOY_MODE"
        return
    fi

    if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
        DEPLOY_MODE="docker"
        log "检测到 Docker，使用 Docker 部署模式"
    elif command -v node &>/dev/null; then
        local ver
        ver=$(node -v 2>/dev/null | sed 's/v//' | cut -d. -f1)
        if [ "${ver:-0}" -ge "$NODE_MIN_VERSION" ]; then
            DEPLOY_MODE="npm"
            log "检测到 Node.js v$ver，使用 NPM 部署模式"
        else
            DEPLOY_MODE="npm"
            log "Node.js 版本过低 (v$ver < v$NODE_MIN_VERSION)，将自动升级"
        fi
    else
        DEPLOY_MODE="npm"
        log "将安装 Node.js 并使用 NPM 部署模式"
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
#  安装 Node.js (>= 22)
# ══════════════════════════════════════════════════════════════════════════════
ensure_node() {
    progress 10 "检查 Node.js 环境..." "running"

    # 检查现有 Node.js 版本
    if command -v node &>/dev/null; then
        local ver
        ver=$(node -v 2>/dev/null | sed 's/v//' | cut -d. -f1)
        if [ "${ver:-0}" -ge "$NODE_MIN_VERSION" ]; then
            ok "Node.js $(node -v) 已满足要求"
            return 0
        fi
        warn "Node.js 版本 $(node -v) 过低，需要 >= v$NODE_MIN_VERSION"
    fi

    progress 12 "正在安装 Node.js v22..." "running"
    log "安装 Node.js v$NODE_MIN_VERSION ..."

    case "$OS" in
        linux)
            # 方法 1: NodeSource 官方安装脚本
            if command -v curl &>/dev/null; then
                # 先安装 curl 如果没有
                if [ "$DISTRO" = "ubuntu" ] || [ "$DISTRO" = "debian" ]; then
                    sudo apt-get update -qq 2>>"$OPENCLAW_LOG" || true
                    sudo apt-get install -y -qq curl ca-certificates 2>>"$OPENCLAW_LOG" || true
                fi

                # 使用 nvm 安装（最可靠的方式）
                if [ ! -d "$NVM_DIR_PATH" ]; then
                    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash 2>>"$OPENCLAW_LOG"
                fi
                export NVM_DIR="$NVM_DIR_PATH"
                # shellcheck disable=SC1091
                [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
                nvm install "$NODE_MIN_VERSION" 2>>"$OPENCLAW_LOG"
                nvm use "$NODE_MIN_VERSION" 2>>"$OPENCLAW_LOG"
                nvm alias default "$NODE_MIN_VERSION" 2>>"$OPENCLAW_LOG"
            fi
            ;;
        macos)
            if command -v brew &>/dev/null; then
                brew install node@22 2>>"$OPENCLAW_LOG"
            else
                curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash 2>>"$OPENCLAW_LOG"
                export NVM_DIR="$NVM_DIR_PATH"
                [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
                nvm install "$NODE_MIN_VERSION" 2>>"$OPENCLAW_LOG"
                nvm use "$NODE_MIN_VERSION" 2>>"$OPENCLAW_LOG"
            fi
            ;;
    esac

    # 验证
    if command -v node &>/dev/null; then
        ok "Node.js $(node -v) 安装完成"
    else
        err "Node.js 安装失败"
        exit 1
    fi
}

# ══════════════════════════════════════════════════════════════════════════════
#  Docker 部署
# ══════════════════════════════════════════════════════════════════════════════
deploy_docker() {
    progress 20 "准备 Docker 部署环境..." "running"

    mkdir -p "$OPENCLAW_HOME" "$OPENCLAW_WORKSPACE"

    # 生成 Gateway Token
    local token
    if command -v openssl &>/dev/null; then
        token="$(openssl rand -hex 32)"
    else
        token="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
    fi

    progress 30 "正在克隆 OpenClaw 仓库..." "running"

    local clone_dir="$OPENCLAW_HOME/openclaw-src"
    if [ -d "$clone_dir/.git" ]; then
        cd "$clone_dir"
        git pull origin main 2>>"$OPENCLAW_LOG" || true
    else
        rm -rf "$clone_dir"
        git clone --depth 1 https://github.com/openclaw/openclaw.git "$clone_dir" 2>>"$OPENCLAW_LOG"
    fi
    cd "$clone_dir"

    progress 45 "正在构建 Docker 镜像（首次较慢）..." "running"

    docker build -t openclaw:local -f Dockerfile . 2>>"$OPENCLAW_LOG"

    progress 70 "正在配置并启动容器..." "running"

    # 写入 .env
    cat > "$clone_dir/.env" << EOF
OPENCLAW_CONFIG_DIR=$OPENCLAW_HOME
OPENCLAW_WORKSPACE_DIR=$OPENCLAW_WORKSPACE
OPENCLAW_GATEWAY_PORT=$GATEWAY_PORT
OPENCLAW_BRIDGE_PORT=18790
OPENCLAW_GATEWAY_BIND=lan
OPENCLAW_GATEWAY_TOKEN=$token
OPENCLAW_IMAGE=openclaw:local
OPENCLAW_EXTRA_MOUNTS=
OPENCLAW_HOME_VOLUME=
OPENCLAW_DOCKER_APT_PACKAGES=
EOF

    # 写入配置
    write_config "$token"

    # 启动
    docker compose up -d openclaw-gateway 2>>"$OPENCLAW_LOG"

    progress 90 "Docker 容器已启动" "running"
    GATEWAY_TOKEN="$token"
}

# ══════════════════════════════════════════════════════════════════════════════
#  NPM 全局安装部署
# ══════════════════════════════════════════════════════════════════════════════
deploy_npm() {
    ensure_node

    progress 25 "正在通过 NPM 安装 OpenClaw..." "running"

    # 确保 npm 可用
    if ! command -v npm &>/dev/null; then
        # 尝试加载 nvm
        export NVM_DIR="$NVM_DIR_PATH"
        [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    fi

    npm install -g openclaw@latest 2>>"$OPENCLAW_LOG"

    progress 50 "OpenClaw 安装完成，正在配置..." "running"

    mkdir -p "$OPENCLAW_HOME" "$OPENCLAW_WORKSPACE"

    # 生成 Gateway Token
    local token
    if command -v openssl &>/dev/null; then
        token="$(openssl rand -hex 32)"
    else
        token="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
    fi

    write_config "$token"

    progress 70 "正在启动 OpenClaw Gateway..." "running"

    # 使用 nohup 启动 gateway
    nohup openclaw gateway \
        --port "$GATEWAY_PORT" \
        --allow-unconfigured \
        >> "$OPENCLAW_HOME/gateway.log" 2>&1 &

    local gw_pid=$!
    echo "$gw_pid" > "$OPENCLAW_HOME/gateway.pid"

    # 等待启动
    local retries=0
    while [ $retries -lt 15 ]; do
        if curl -s "http://127.0.0.1:$GATEWAY_PORT" >/dev/null 2>&1; then
            break
        fi
        sleep 1
        retries=$((retries + 1))
    done

    progress 90 "OpenClaw Gateway 已启动 (PID: $gw_pid)" "running"
    GATEWAY_TOKEN="$token"
}

# ══════════════════════════════════════════════════════════════════════════════
#  源码编译部署
# ══════════════════════════════════════════════════════════════════════════════
deploy_source() {
    ensure_node

    progress 20 "正在克隆 OpenClaw 源码..." "running"

    local src_dir="$OPENCLAW_HOME/openclaw-src"
    if [ -d "$src_dir/.git" ]; then
        cd "$src_dir"
        git pull origin main 2>>"$OPENCLAW_LOG" || true
    else
        rm -rf "$src_dir"
        git clone https://github.com/openclaw/openclaw.git "$src_dir" 2>>"$OPENCLAW_LOG"
    fi
    cd "$src_dir"

    progress 35 "正在安装 pnpm 构建工具..." "running"

    npm install -g pnpm@latest 2>>"$OPENCLAW_LOG"
    corepack enable 2>>"$OPENCLAW_LOG" || true

    progress 40 "正在安装依赖 (pnpm install)..." "running"
    pnpm install 2>>"$OPENCLAW_LOG"

    progress 55 "正在构建 UI..." "running"
    pnpm ui:build 2>>"$OPENCLAW_LOG"

    progress 65 "正在编译项目..." "running"
    pnpm build 2>>"$OPENCLAW_LOG"

    progress 75 "编译完成，正在配置..." "running"

    mkdir -p "$OPENCLAW_HOME" "$OPENCLAW_WORKSPACE"

    local token
    if command -v openssl &>/dev/null; then
        token="$(openssl rand -hex 32)"
    else
        token="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
    fi

    write_config "$token"

    progress 85 "正在启动 OpenClaw Gateway..." "running"

    nohup node dist/index.js gateway \
        --port "$GATEWAY_PORT" \
        --allow-unconfigured \
        >> "$OPENCLAW_HOME/gateway.log" 2>&1 &

    local gw_pid=$!
    echo "$gw_pid" > "$OPENCLAW_HOME/gateway.pid"

    sleep 3
    progress 90 "OpenClaw Gateway 已启动 (PID: $gw_pid)" "running"
    GATEWAY_TOKEN="$token"
}

# ══════════════════════════════════════════════════════════════════════════════
#  写入配置
# ══════════════════════════════════════════════════════════════════════════════
write_config() {
    local token="$1"

    mkdir -p "$OPENCLAW_HOME"

    # 确定模型
    local model_str=""
    if [ -n "$AI_MODEL" ]; then
        model_str="$AI_MODEL"
    else
        case "$AI_PROVIDER" in
            anthropic) model_str="anthropic/claude-sonnet-4-20250514" ;;
            openai)    model_str="openai/gpt-4o" ;;
            ollama)    model_str="ollama/llama3" ;;
            *)         model_str="anthropic/claude-sonnet-4-20250514" ;;
        esac
    fi

    # 写入 openclaw.json
    cat > "$OPENCLAW_HOME/openclaw.json" << JSONEOF
{
  "gateway": {
    "port": $GATEWAY_PORT,
    "auth": "token",
    "token": "$token"
  },
  "agent": {
    "model": "$model_str"
  },
  "channels": {},
  "workspace": {
    "root": "$OPENCLAW_WORKSPACE"
  }
}
JSONEOF

    # 写入 API Key 到环境配置（如果提供）
    if [ -n "$API_KEY" ]; then
        local env_file="$OPENCLAW_HOME/.env"
        case "$AI_PROVIDER" in
            anthropic)
                echo "ANTHROPIC_API_KEY=$API_KEY" > "$env_file"
                ;;
            openai)
                echo "OPENAI_API_KEY=$API_KEY" > "$env_file"
                ;;
        esac
        log "API Key 已写入 $env_file"
    fi

    ok "配置已写入 $OPENCLAW_HOME/openclaw.json"
}

# ══════════════════════════════════════════════════════════════════════════════
#  创建管理脚本
# ══════════════════════════════════════════════════════════════════════════════
create_management_scripts() {
    # 停止脚本
    cat > "$OPENCLAW_HOME/stop.sh" << 'STOPEOF'
#!/usr/bin/env bash
echo "正在停止 OpenClaw..."
if [ -f "$HOME/.openclaw/gateway.pid" ]; then
    kill "$(cat "$HOME/.openclaw/gateway.pid")" 2>/dev/null || true
    rm -f "$HOME/.openclaw/gateway.pid"
    echo "OpenClaw Gateway 已停止"
else
    pkill -f "openclaw gateway" 2>/dev/null || true
    echo "已尝试停止所有 OpenClaw 进程"
fi
STOPEOF
    chmod +x "$OPENCLAW_HOME/stop.sh"

    # 重启脚本
    cat > "$OPENCLAW_HOME/restart.sh" << 'RESTARTEOF'
#!/usr/bin/env bash
echo "正在重启 OpenClaw..."
bash "$HOME/.openclaw/stop.sh"
sleep 2
if command -v openclaw &>/dev/null; then
    nohup openclaw gateway --port 18789 --allow-unconfigured >> "$HOME/.openclaw/gateway.log" 2>&1 &
    echo $! > "$HOME/.openclaw/gateway.pid"
fi
echo "OpenClaw Gateway 已重启"
RESTARTEOF
    chmod +x "$OPENCLAW_HOME/restart.sh"

    # 状态检查脚本
    cat > "$OPENCLAW_HOME/status.sh" << 'STATUSEOF'
#!/usr/bin/env bash
echo "=== OpenClaw 状态 ==="
if [ -f "$HOME/.openclaw/gateway.pid" ]; then
    pid=$(cat "$HOME/.openclaw/gateway.pid")
    if kill -0 "$pid" 2>/dev/null; then
        echo "Gateway: 运行中 (PID: $pid)"
    else
        echo "Gateway: 已停止 (PID 文件残留)"
    fi
else
    echo "Gateway: 未运行"
fi
echo "配置目录: $HOME/.openclaw"
echo "工作空间: $HOME/.openclaw/workspace"
if command -v openclaw &>/dev/null; then
    echo "OpenClaw: $(openclaw --version 2>/dev/null || echo '已安装')"
fi
STATUSEOF
    chmod +x "$OPENCLAW_HOME/status.sh"
}

# ══════════════════════════════════════════════════════════════════════════════
#  完成
# ══════════════════════════════════════════════════════════════════════════════
finish() {
    create_management_scripts

    local access_url="http://127.0.0.1:${GATEWAY_PORT}?token=${GATEWAY_TOKEN}"

    progress 100 "部署完成！访问地址: $access_url" "done"

    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║       🦞  OpenClaw 全能精华版 — 一键部署成功!               ║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║  部署模式:  ${NC}${BOLD}$DEPLOY_MODE${NC}"
    echo -e "${GREEN}║  访问地址:  ${NC}${BOLD}$access_url${NC}"
    echo -e "${GREEN}║  配置目录:  ${NC}${BOLD}$OPENCLAW_HOME${NC}"
    echo -e "${GREEN}║  工作空间:  ${NC}${BOLD}$OPENCLAW_WORKSPACE${NC}"
    echo -e "${GREEN}║  Gateway:   ${NC}${BOLD}端口 $GATEWAY_PORT${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}║  管理命令:                                                 ║${NC}"
    echo -e "${GREEN}║    停止:  ${NC}${BOLD}bash $OPENCLAW_HOME/stop.sh${NC}"
    echo -e "${GREEN}║    重启:  ${NC}${BOLD}bash $OPENCLAW_HOME/restart.sh${NC}"
    echo -e "${GREEN}║    状态:  ${NC}${BOLD}bash $OPENCLAW_HOME/status.sh${NC}"
    echo -e "${GREEN}║                                                            ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ══════════════════════════════════════════════════════════════════════════════
#  主入口
# ══════════════════════════════════════════════════════════════════════════════
main() {
    mkdir -p "$OPENCLAW_HOME"
    : > "$OPENCLAW_LOG"

    echo ""
    echo -e "${BOLD}${CYAN}"
    echo "  ╔═══════════════════════════════════════════════════════╗"
    echo "  ║   🦞  OpenClaw 全能压缩精华版 — 一键部署系统         ║"
    echo "  ║   原名 MoltBot / Clawdbot | 开源个人 AI 助手        ║"
    echo "  ╚═══════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    progress 0 "开始部署..." "running"

    detect_os
    auto_select_mode

    progress 5 "部署模式: $DEPLOY_MODE | 开始安装..." "running"

    case "$DEPLOY_MODE" in
        docker) deploy_docker ;;
        npm)    deploy_npm    ;;
        source) deploy_source ;;
        *)
            err "未知部署模式: $DEPLOY_MODE"
            exit 1
            ;;
    esac

    finish
}

main "$@"
