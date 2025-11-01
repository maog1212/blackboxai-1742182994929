// 企业筛选资源体系 - 前端应用

const API_BASE_URL = '/api';

// 全局状态
let currentPage = 1;
let pageSize = 20;
let totalPages = 1;
let currentFilters = {};
let filterOptions = {};

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    setupEventListeners();
    await loadFilterOptions();
    await loadEnterprises();
}

// 设置事件监听器
function setupEventListeners() {
    // 导航按钮
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchView(e.target.dataset.view);
        });
    });

    // 表单提交
    document.getElementById('add-enterprise-form').addEventListener('submit', handleFormSubmit);

    // 关键词搜索 - 实时搜索
    document.getElementById('keyword').addEventListener('input', debounce(applyFilters, 500));
}

// 切换视图
function switchView(viewName) {
    // 更新导航按钮
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.view === viewName) {
            btn.classList.add('active');
        }
    });

    // 更新视图
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });

    const targetView = document.getElementById(`${viewName}-view`);
    if (targetView) {
        targetView.classList.add('active');
    }

    // 加载对应视图的数据
    if (viewName === 'statistics') {
        loadStatistics();
    } else if (viewName === 'list') {
        loadEnterprises();
    }
}

// 加载筛选选项
async function loadFilterOptions() {
    try {
        const response = await fetch(`${API_BASE_URL}/filter-options`);
        const result = await response.json();

        if (result.success) {
            filterOptions = result.data;
            populateFilterSelects();
        }
    } catch (error) {
        console.error('加载筛选选项失败:', error);
    }
}

// 填充筛选下拉框
function populateFilterSelects() {
    // 行业
    populateSelect('industry', filterOptions.industries);

    // 规模
    populateSelect('scale', filterOptions.scales);

    // 地区
    populateSelect('region', filterOptions.regions);

    // 城市
    populateSelect('city', filterOptions.cities);

    // 信用评级
    populateSelect('creditRating', filterOptions.creditRatings);

    // 标签
    populateSelect('tags', filterOptions.tags);
}

function populateSelect(id, options) {
    const select = document.getElementById(id);
    if (!select) return;

    select.innerHTML = '';
    options.forEach(option => {
        const optionEl = document.createElement('option');
        optionEl.value = option;
        optionEl.textContent = option;
        select.appendChild(optionEl);
    });
}

// 加载企业列表
async function loadEnterprises(filters = {}) {
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/enterprises/filter`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filters,
                page: currentPage,
                pageSize
            })
        });

        const result = await response.json();

        if (result.success) {
            displayEnterprises(result.data);
            updatePagination(result);
        } else {
            showToast('加载失败: ' + result.message, 'error');
        }
    } catch (error) {
        console.error('加载企业列表失败:', error);
        showToast('加载失败，请稍后重试', 'error');
    } finally {
        showLoading(false);
    }
}

// 显示企业列表
function displayEnterprises(enterprises) {
    const listContainer = document.getElementById('enterprise-list');

    if (enterprises.length === 0) {
        listContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <div class="empty-text">没有找到符合条件的企业</div>
            </div>
        `;
        return;
    }

    listContainer.innerHTML = enterprises.map(enterprise => `
        <div class="enterprise-card" onclick="showEnterpriseDetail(${enterprise.id})">
            <div class="card-header">
                <div>
                    <div class="card-title">${enterprise.name}</div>
                    <div class="card-code">${enterprise.code || '未提供企业代码'}</div>
                </div>
                <span class="card-badge badge-${enterprise.status}">
                    ${getStatusText(enterprise.status)}
                </span>
            </div>

            <div class="card-info">
                <div class="info-item">
                    <span class="info-icon">🏭</span>
                    <span class="info-label">行业：</span>
                    <span class="info-value">${enterprise.industry}</span>
                </div>
                <div class="info-item">
                    <span class="info-icon">📊</span>
                    <span class="info-label">规模：</span>
                    <span class="info-value">${enterprise.scale}</span>
                </div>
                <div class="info-item">
                    <span class="info-icon">📍</span>
                    <span class="info-label">地区：</span>
                    <span class="info-value">${enterprise.region}</span>
                </div>
                <div class="info-item">
                    <span class="info-icon">⭐</span>
                    <span class="info-label">信用：</span>
                    <span class="info-value">${enterprise.credit_rating || 'N/A'}</span>
                </div>
                ${enterprise.employee_count ? `
                <div class="info-item">
                    <span class="info-icon">👥</span>
                    <span class="info-label">员工：</span>
                    <span class="info-value">${enterprise.employee_count}人</span>
                </div>
                ` : ''}
                ${enterprise.annual_revenue ? `
                <div class="info-item">
                    <span class="info-icon">💰</span>
                    <span class="info-label">营收：</span>
                    <span class="info-value">${enterprise.annual_revenue}万元</span>
                </div>
                ` : ''}
            </div>

            ${enterprise.tags && enterprise.tags.length > 0 ? `
                <div class="card-tags">
                    ${enterprise.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

// 显示企业详情
async function showEnterpriseDetail(id) {
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/enterprises/${id}`);
        const result = await response.json();

        if (result.success) {
            const enterprise = result.data;
            const modal = document.getElementById('detail-modal');
            const modalBody = document.getElementById('modal-body');

            modalBody.innerHTML = `
                <div class="detail-header">
                    <h2 class="detail-title">${enterprise.name}</h2>
                    <div class="card-code">${enterprise.code || '未提供企业代码'}</div>
                </div>

                <div class="detail-grid">
                    <div class="detail-item">
                        <div class="detail-label">所属行业</div>
                        <div class="detail-value">${enterprise.industry}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">企业规模</div>
                        <div class="detail-value">${enterprise.scale}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">所在地区</div>
                        <div class="detail-value">${enterprise.region}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">所在城市</div>
                        <div class="detail-value">${enterprise.city || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">注册资本</div>
                        <div class="detail-value">${enterprise.registered_capital ? enterprise.registered_capital + ' 万元' : 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">成立日期</div>
                        <div class="detail-value">${enterprise.established_date || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">法人代表</div>
                        <div class="detail-value">${enterprise.legal_person || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">员工数量</div>
                        <div class="detail-value">${enterprise.employee_count ? enterprise.employee_count + ' 人' : 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">年营收</div>
                        <div class="detail-value">${enterprise.annual_revenue ? enterprise.annual_revenue + ' 万元' : 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">信用评级</div>
                        <div class="detail-value">${enterprise.credit_rating || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">联系人</div>
                        <div class="detail-value">${enterprise.contact_person || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">联系电话</div>
                        <div class="detail-value">${enterprise.contact_phone || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">联系邮箱</div>
                        <div class="detail-value">${enterprise.contact_email || 'N/A'}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">官方网站</div>
                        <div class="detail-value">${enterprise.website ? `<a href="${enterprise.website}" target="_blank">${enterprise.website}</a>` : 'N/A'}</div>
                    </div>
                    <div class="detail-item full-width">
                        <div class="detail-label">详细地址</div>
                        <div class="detail-value">${enterprise.address || 'N/A'}</div>
                    </div>
                    <div class="detail-item full-width">
                        <div class="detail-label">经营范围</div>
                        <div class="detail-value">${enterprise.business_scope || 'N/A'}</div>
                    </div>
                    <div class="detail-item full-width">
                        <div class="detail-label">企业描述</div>
                        <div class="detail-value">${enterprise.description || 'N/A'}</div>
                    </div>
                    ${enterprise.tags && enterprise.tags.length > 0 ? `
                    <div class="detail-item full-width">
                        <div class="detail-label">标签</div>
                        <div class="card-tags">
                            ${enterprise.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
                        </div>
                    </div>
                    ` : ''}
                </div>
            `;

            modal.classList.add('active');
        }
    } catch (error) {
        console.error('加载企业详情失败:', error);
        showToast('加载详情失败', 'error');
    } finally {
        showLoading(false);
    }
}

// 关闭模态框
function closeModal() {
    document.getElementById('detail-modal').classList.remove('active');
}

// 应用筛选
async function applyFilters() {
    currentPage = 1;

    const filters = {
        keyword: document.getElementById('keyword').value,
        industry: getMultiSelectValues('industry'),
        scale: getMultiSelectValues('scale'),
        region: getMultiSelectValues('region'),
        city: getMultiSelectValues('city'),
        creditRating: getMultiSelectValues('creditRating'),
        tags: getMultiSelectValues('tags'),
        status: document.getElementById('status').value,
        minCapital: document.getElementById('minCapital').value,
        maxCapital: document.getElementById('maxCapital').value,
        minEmployees: document.getElementById('minEmployees').value,
        maxEmployees: document.getElementById('maxEmployees').value,
        minRevenue: document.getElementById('minRevenue').value,
        maxRevenue: document.getElementById('maxRevenue').value
    };

    // 移除空值
    Object.keys(filters).forEach(key => {
        if (!filters[key] || (Array.isArray(filters[key]) && filters[key].length === 0)) {
            delete filters[key];
        }
    });

    currentFilters = filters;
    await loadEnterprises(filters);
}

// 重置筛选
function resetFilters() {
    document.getElementById('keyword').value = '';
    document.querySelectorAll('.filter-select').forEach(select => {
        select.selectedIndex = -1;
    });
    document.querySelectorAll('.filter-input[type="number"]').forEach(input => {
        input.value = '';
    });
    document.getElementById('status').value = '';

    currentFilters = {};
    currentPage = 1;
    loadEnterprises();
}

// 获取多选框的值
function getMultiSelectValues(id) {
    const select = document.getElementById(id);
    return Array.from(select.selectedOptions).map(option => option.value);
}

// 更新分页信息
function updatePagination(result) {
    totalPages = result.totalPages;
    document.getElementById('total-count').textContent = `总计: ${result.total} 家企业`;
    document.getElementById('page-info').textContent = `第 ${result.page} / ${result.totalPages} 页`;

    document.getElementById('prev-page').disabled = result.page <= 1;
    document.getElementById('next-page').disabled = result.page >= result.totalPages;
}

// 上一页
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        loadEnterprises(currentFilters);
    }
}

// 下一页
function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        loadEnterprises(currentFilters);
    }
}

// 加载统计数据
async function loadStatistics() {
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const result = await response.json();

        if (result.success) {
            displayStatistics(result.data);
        }
    } catch (error) {
        console.error('加载统计数据失败:', error);
        showToast('加载统计数据失败', 'error');
    } finally {
        showLoading(false);
    }
}

// 显示统计数据
function displayStatistics(stats) {
    document.getElementById('stat-total').textContent = stats.total;

    displayChart('chart-industry', stats.byIndustry);
    displayChart('chart-scale', stats.byScale);
    displayChart('chart-region', stats.byRegion);
    displayChart('chart-rating', stats.byCreditRating);
}

// 显示图表
function displayChart(containerId, data) {
    const container = document.getElementById(containerId);
    const maxCount = Math.max(...data.map(d => d.count));

    container.innerHTML = data.map(item => {
        const percentage = (item.count / maxCount) * 100;
        const label = item.industry || item.scale || item.region || item.credit_rating;

        return `
            <div class="chart-item">
                <span class="chart-label">${label}</span>
                <span class="chart-value">${item.count}</span>
                <div class="chart-bar" style="width: ${percentage}%"></div>
            </div>
        `;
    }).join('');
}

// 表单提交
async function handleFormSubmit(e) {
    e.preventDefault();
    showLoading(true);

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // 处理标签
    if (data.tags) {
        data.tags = data.tags.split(',').map(t => t.trim()).filter(t => t);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/enterprises`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showToast('企业添加成功！', 'success');
            e.target.reset();
            switchView('list');
            loadEnterprises();
        } else {
            showToast('添加失败: ' + result.message, 'error');
        }
    } catch (error) {
        console.error('添加企业失败:', error);
        showToast('添加失败，请稍后重试', 'error');
    } finally {
        showLoading(false);
    }
}

// 导出数据
async function exportData() {
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filters: currentFilters })
        });

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `企业数据_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showToast('导出成功！', 'success');
    } catch (error) {
        console.error('导出失败:', error);
        showToast('导出失败，请稍后重试', 'error');
    } finally {
        showLoading(false);
    }
}

// 工具函数

// 显示/隐藏加载提示
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.add('active');
    } else {
        loading.classList.remove('active');
    }
}

// 显示提示消息
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// 获取状态文本
function getStatusText(status) {
    const statusMap = {
        'active': '活跃',
        'inactive': '不活跃',
        'suspended': '暂停'
    };
    return statusMap[status] || status;
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('detail-modal');
    if (event.target === modal) {
        closeModal();
    }
}
