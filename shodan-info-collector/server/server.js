const express = require('express');
const axios = require('axios');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const SHODAN_API_KEY = process.env.SHODAN_API_KEY;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// 验证 API Key 是否存在
if (!SHODAN_API_KEY) {
    console.warn('⚠️  警告: 未设置 SHODAN_API_KEY 环境变量');
    console.warn('请在 .env 文件中设置您的 Shodan API Key');
}

// 根路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/index.html'));
});

// API 信息路由
app.get('/api/info', async (req, res) => {
    if (!SHODAN_API_KEY) {
        return res.status(400).json({
            error: '未配置 Shodan API Key',
            message: '请在 .env 文件中设置 SHODAN_API_KEY'
        });
    }

    try {
        const response = await axios.get(`https://api.shodan.io/api-info?key=${SHODAN_API_KEY}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({
            error: 'API 信息获取失败',
            message: error.response?.data?.error || error.message
        });
    }
});

// 搜索路由
app.post('/api/search', async (req, res) => {
    const { query, page = 1 } = req.body;

    if (!query) {
        return res.status(400).json({ error: '搜索查询不能为空' });
    }

    if (!SHODAN_API_KEY) {
        return res.status(400).json({
            error: '未配置 Shodan API Key',
            message: '请在 .env 文件中设置 SHODAN_API_KEY'
        });
    }

    try {
        console.log(`🔍 搜索查询: ${query}, 页码: ${page}`);

        const response = await axios.get('https://api.shodan.io/shodan/host/search', {
            params: {
                key: SHODAN_API_KEY,
                query: query,
                page: page
            }
        });

        console.log(`✅ 找到 ${response.data.total} 个结果`);

        res.json({
            total: response.data.total,
            matches: response.data.matches,
            facets: response.data.facets
        });
    } catch (error) {
        console.error('❌ 搜索错误:', error.response?.data || error.message);

        res.status(500).json({
            error: '搜索失败',
            message: error.response?.data?.error || error.message
        });
    }
});

// 主机信息路由
app.get('/api/host/:ip', async (req, res) => {
    const { ip } = req.params;

    if (!SHODAN_API_KEY) {
        return res.status(400).json({
            error: '未配置 Shodan API Key',
            message: '请在 .env 文件中设置 SHODAN_API_KEY'
        });
    }

    try {
        console.log(`🔍 查询主机: ${ip}`);

        const response = await axios.get(`https://api.shodan.io/shodan/host/${ip}`, {
            params: {
                key: SHODAN_API_KEY
            }
        });

        console.log(`✅ 主机信息获取成功: ${ip}`);

        res.json(response.data);
    } catch (error) {
        console.error('❌ 主机查询错误:', error.response?.data || error.message);

        res.status(500).json({
            error: '主机信息获取失败',
            message: error.response?.data?.error || error.message
        });
    }
});

// 健康检查路由
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        apiKeyConfigured: !!SHODAN_API_KEY
    });
});

// 错误处理中间件
app.use((err, req, res, next) => {
    console.error('服务器错误:', err);
    res.status(500).json({
        error: '服务器内部错误',
        message: err.message
    });
});

// 启动服务器
app.listen(PORT, () => {
    console.log(`🚀 Shodan 信息收集服务器启动成功`);
    console.log(`📍 访问地址: http://localhost:${PORT}`);
    console.log(`🔑 API Key 状态: ${SHODAN_API_KEY ? '已配置 ✅' : '未配置 ⚠️'}`);
    console.log(`\n按 Ctrl+C 停止服务器\n`);
});
