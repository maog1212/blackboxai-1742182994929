let currentResults = [];

// 设置搜索关键词
function setSearch(query) {
    document.getElementById('searchInput').value = query;
    performSearch();
}

// 执行搜索
async function performSearch(useAI = false) {
    const query = document.getElementById('searchInput').value.trim();

    if (!query) {
        showError('请输入搜索查询');
        return;
    }

    // 显示加载状态
    const loadingDiv = document.getElementById('loading');
    const loadingText = loadingDiv.querySelector('p');
    loadingText.textContent = useAI ? '正在搜索并使用 AI 分析...' : '正在搜索...';
    loadingDiv.style.display = 'block';

    document.getElementById('error').style.display = 'none';
    document.getElementById('results').innerHTML = '';
    document.getElementById('statsSection').style.display = 'none';
    document.getElementById('aiAnalysis').style.display = 'none';

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query, useAI })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || '搜索失败');
        }

        currentResults = data.matches || [];
        displayResults(data);
        displayStats(data);

        // 如果有 AI 分析结果，显示它
        if (data.aiAnalysis) {
            displayAIAnalysis(data.aiAnalysis);
        }

    } catch (error) {
        showError(`错误: ${error.message}`);
    } finally {
        loadingDiv.style.display = 'none';
    }
}

// 显示统计信息
function displayStats(data) {
    const statsSection = document.getElementById('statsSection');
    document.getElementById('totalResults').textContent = data.total || 0;
    document.getElementById('currentPage').textContent = '1';
    statsSection.style.display = 'block';
}

// 显示 AI 分析结果
function displayAIAnalysis(analysis) {
    const aiSection = document.getElementById('aiAnalysis');
    const aiContent = document.getElementById('aiContent');

    // 将换行符转换为 HTML 段落
    const formattedAnalysis = analysis
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .map(line => {
            // 检测标题行（数字开头）
            if (/^\d+\./.test(line)) {
                return `<h4>${escapeHtml(line)}</h4>`;
            }
            // 检测列表项（以 - 或 * 开头）
            if (/^[-*]/.test(line)) {
                return `<li>${escapeHtml(line.substring(1).trim())}</li>`;
            }
            return `<p>${escapeHtml(line)}</p>`;
        })
        .join('');

    aiContent.innerHTML = formattedAnalysis;
    aiSection.style.display = 'block';

    // 平滑滚动到 AI 分析区域
    setTimeout(() => {
        aiSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

// 显示搜索结果
function displayResults(data) {
    const resultsDiv = document.getElementById('results');

    if (!data.matches || data.matches.length === 0) {
        resultsDiv.innerHTML = '<p style="text-align:center; color:#666;">未找到结果</p>';
        return;
    }

    const resultsHTML = data.matches.map(result => createResultCard(result)).join('');
    resultsDiv.innerHTML = resultsHTML;
}

// 创建结果卡片
function createResultCard(result) {
    const ip = result.ip_str || 'N/A';
    const port = result.port || 'N/A';
    const org = result.org || 'Unknown';
    const hostnames = result.hostnames ? result.hostnames.join(', ') : 'N/A';
    const location = result.location ?
        `${result.location.city || ''}, ${result.location.country_name || ''}`.trim() :
        'N/A';
    const timestamp = result.timestamp ? new Date(result.timestamp).toLocaleString('zh-CN') : 'N/A';
    const data = result.data ? escapeHtml(result.data.substring(0, 500)) : 'N/A';

    return `
        <div class="result-card">
            <div class="result-header">
                <span class="result-ip">${escapeHtml(ip)}</span>
                <span class="result-port">端口: ${port}</span>
            </div>

            <div class="result-info">
                <div class="info-item">
                    <span class="info-label">组织</span>
                    <span class="info-value">${escapeHtml(org)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">域名</span>
                    <span class="info-value">${escapeHtml(hostnames)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">位置</span>
                    <span class="info-value">${escapeHtml(location)}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">扫描时间</span>
                    <span class="info-value">${timestamp}</span>
                </div>
            </div>

            ${result.product ? `
                <div class="result-info">
                    <div class="info-item">
                        <span class="info-label">产品</span>
                        <span class="info-value">${escapeHtml(result.product)}</span>
                    </div>
                    ${result.version ? `
                        <div class="info-item">
                            <span class="info-label">版本</span>
                            <span class="info-value">${escapeHtml(result.version)}</span>
                        </div>
                    ` : ''}
                </div>
            ` : ''}

            <details>
                <summary style="cursor:pointer; color:#667eea; font-weight:500; margin-top:10px;">查看数据详情</summary>
                <div class="result-data">${data}${result.data && result.data.length > 500 ? '...' : ''}</div>
            </details>
        </div>
    `;
}

// 显示错误信息
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

// 转义 HTML 字符
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 监听回车键
document.getElementById('searchInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        performSearch();
    }
});
