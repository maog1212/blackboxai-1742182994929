/**
 * 小莫 DeepSeek-OCR 前端交互脚本
 */

// API配置
const API_BASE_URL = 'http://localhost:5000';

// 全局状态
let selectedFiles = [];
let currentMode = 'ocr';

// DOM元素
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const fileListContent = document.getElementById('fileListContent');
const uploadBtn = document.getElementById('uploadBtn');
const clearBtn = document.getElementById('clearBtn');
const loadingArea = document.getElementById('loadingArea');
const resultsArea = document.getElementById('resultsArea');
const resultText = document.getElementById('resultText');
const resultInfo = document.getElementById('resultInfo');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const statusBtn = document.getElementById('statusBtn');
const resolutionSelect = document.getElementById('resolutionSelect');
const modeButtons = document.querySelectorAll('.mode-btn');

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkServerStatus();
});

function initializeEventListeners() {
    // 上传区域点击
    uploadArea.addEventListener('click', () => fileInput.click());

    // 文件选择
    fileInput.addEventListener('change', handleFileSelect);

    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files);
        addFiles(files);
    });

    // 按钮事件
    uploadBtn.addEventListener('click', handleUpload);
    clearBtn.addEventListener('click', clearFiles);
    copyBtn.addEventListener('click', copyResult);
    downloadBtn.addEventListener('click', downloadResult);
    statusBtn.addEventListener('click', checkServerStatus);

    // 模式切换
    modeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            modeButtons.forEach(b => {
                b.classList.remove('active', 'bg-purple-100', 'text-purple-700');
                b.classList.add('bg-gray-100', 'text-gray-700');
            });
            btn.classList.remove('bg-gray-100', 'text-gray-700');
            btn.classList.add('active', 'bg-purple-100', 'text-purple-700');
            currentMode = btn.dataset.mode;
        });
    });
}

function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function addFiles(files) {
    files.forEach(file => {
        if (!selectedFiles.find(f => f.name === file.name)) {
            selectedFiles.push(file);
        }
    });
    updateFileList();
}

function updateFileList() {
    if (selectedFiles.length === 0) {
        fileList.classList.add('hidden');
        uploadBtn.disabled = true;
        return;
    }

    fileList.classList.remove('hidden');
    uploadBtn.disabled = false;

    fileListContent.innerHTML = selectedFiles.map((file, index) => `
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div class="flex items-center space-x-3">
                <i class="fas ${getFileIcon(file.name)} text-purple-600"></i>
                <div>
                    <p class="font-medium">${file.name}</p>
                    <p class="text-sm text-gray-500">${formatFileSize(file.size)}</p>
                </div>
            </div>
            <button onclick="removeFile(${index})" class="text-red-500 hover:text-red-700">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    updateFileList();
}

function clearFiles() {
    selectedFiles = [];
    fileInput.value = '';
    updateFileList();
    resultsArea.classList.add('hidden');
}

function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    if (['jpg', 'jpeg', 'png', 'gif', 'bmp'].includes(ext)) {
        return 'fa-image';
    } else if (ext === 'pdf') {
        return 'fa-file-pdf';
    }
    return 'fa-file';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

async function handleUpload() {
    if (selectedFiles.length === 0) {
        alert('请先选择文件');
        return;
    }

    // 显示加载状态
    loadingArea.classList.remove('hidden');
    resultsArea.classList.add('hidden');
    uploadBtn.disabled = true;

    try {
        const formData = new FormData();
        const resolution = resolutionSelect.value;

        if (selectedFiles.length === 1) {
            // 单文件处理
            const file = selectedFiles[0];
            formData.append('file', file);
            formData.append('mode', currentMode);
            formData.append('resolution', resolution);

            const endpoint = file.name.endsWith('.pdf') ? '/api/ocr/pdf' : '/api/ocr/image';
            const result = await uploadFile(endpoint, formData);
            displayResult(result);
        } else {
            // 批量处理
            selectedFiles.forEach(file => {
                formData.append('files', file);
            });
            formData.append('mode', currentMode);
            formData.append('resolution', resolution);

            const result = await uploadFile('/api/ocr/batch', formData);
            displayBatchResults(result);
        }
    } catch (error) {
        alert('处理失败: ' + error.message);
        console.error(error);
    } finally {
        loadingArea.classList.add('hidden');
        uploadBtn.disabled = false;
    }
}

async function uploadFile(endpoint, formData) {
    const response = await fetch(API_BASE_URL + endpoint, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        throw new Error('服务器响应错误: ' + response.status);
    }

    return await response.json();
}

function displayResult(result) {
    if (!result.success) {
        alert('识别失败: ' + result.error);
        return;
    }

    resultsArea.classList.remove('hidden');

    // 显示结果信息
    resultInfo.innerHTML = `
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
                <span class="text-gray-600">模式:</span>
                <span class="font-semibold ml-2">${getModeLabel(result.mode || currentMode)}</span>
            </div>
            <div>
                <span class="text-gray-600">分辨率:</span>
                <span class="font-semibold ml-2">${result.resolution || '1024x1024'}</span>
            </div>
            <div>
                <span class="text-gray-600">处理时间:</span>
                <span class="font-semibold ml-2">${result.process_time || 'N/A'}</span>
            </div>
            <div>
                <span class="text-gray-600">状态:</span>
                <span class="font-semibold ml-2 text-green-600">
                    <i class="fas fa-check-circle mr-1"></i>成功
                </span>
            </div>
        </div>
    `;

    // 显示识别文本
    resultText.textContent = result.text || '无识别结果';

    // 滚动到结果区域
    resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function displayBatchResults(result) {
    if (!result.success) {
        alert('批量处理失败: ' + result.error);
        return;
    }

    resultsArea.classList.remove('hidden');

    // 显示批量结果信息
    resultInfo.innerHTML = `
        <div class="text-sm">
            <span class="text-gray-600">批量处理完成，共处理</span>
            <span class="font-semibold mx-1">${result.total}</span>
            <span class="text-gray-600">个文件</span>
        </div>
    `;

    // 合并所有结果
    const allTexts = result.results
        .filter(r => r.success)
        .map((r, i) => `--- 文件 ${i + 1} ---\n${r.text}\n`)
        .join('\n');

    resultText.textContent = allTexts || '无识别结果';

    resultsArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function getModeLabel(mode) {
    const labels = {
        'ocr': '通用OCR',
        'doc2md': '文档转Markdown',
        'figure': '图表解析'
    };
    return labels[mode] || mode;
}

function copyResult() {
    const text = resultText.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check mr-2"></i>已复制';
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
        }, 2000);
    }).catch(err => {
        alert('复制失败: ' + err);
    });
}

function downloadResult() {
    const text = resultText.textContent;
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ocr_result_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

async function checkServerStatus() {
    try {
        const response = await fetch(API_BASE_URL + '/api/status');
        const data = await response.json();

        if (data.status === 'ready') {
            alert('服务状态: 正常运行\n模型已加载: ' + (data.model_loaded ? '是' : '否'));
        } else {
            alert('服务状态: 初始化中\n请稍后再试');
        }
    } catch (error) {
        alert('无法连接到服务器\n请确保后端服务已启动\n\n错误: ' + error.message);
    }
}
