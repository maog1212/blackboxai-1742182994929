const express = require('express');
const axios = require('axios');
const path = require('path');
const cors = require('cors');
const cheerio = require('cheerio');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY || 'sk-d297057f68f248f5af9cba0e365cb27f';
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// 验证 API Key 是否存在
console.log('🔑 DeepSeek API Key 已配置');

// DeepSeek AI 分析函数
async function analyzeWithDeepSeek(data, userQuery) {
    try {
        const prompt = `你是一个网络安全专家。请分析以下 Shodan 搜索结果，并提供有价值的见解。

用户查询: ${userQuery}

搜索结果数据:
${JSON.stringify(data, null, 2)}

请提供以下分析:
1. 主要发现和安全风险
2. 按风险等级排序的设备列表
3. 建议采取的安全措施
4. 统计摘要（国家分布、端口分布、服务类型等）

请用中文回复，格式清晰易读。`;

        const response = await axios.post(DEEPSEEK_API_URL, {
            model: 'deepseek-chat',
            messages: [
                {
                    role: 'system',
                    content: '你是一个专业的网络安全分析专家，擅长分析 Shodan 数据并提供安全建议。'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            temperature: 0.7,
            max_tokens: 2000
        }, {
            headers: {
                'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        return response.data.choices[0].message.content;
    } catch (error) {
        console.error('DeepSeek API 错误:', error.response?.data || error.message);
        throw new Error('AI 分析失败');
    }
}

// 从 Shodan 网站爬取数据
async function scrapeSholan(query, page = 1) {
    try {
        const url = `https://www.shodan.io/search?query=${encodeURIComponent(query)}&page=${page}`;

        console.log(`🕷️  爬取 URL: ${url}`);

        const response = await axios.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            },
            timeout: 15000
        });

        const $ = cheerio.load(response.data);
        const results = [];

        // 解析搜索结果
        $('.search-result').each((i, element) => {
            const $el = $(element);

            const result = {
                ip_str: $el.find('.ip').text().trim() || $el.find('a.text-dark').first().text().trim(),
                port: $el.find('.port').text().trim() || 'N/A',
                org: $el.find('.company').text().trim() || 'Unknown',
                hostnames: $el.find('.hostname').text().trim() ? [$el.find('.hostname').text().trim()] : [],
                location: {
                    country_name: $el.find('.country').text().trim() || 'Unknown',
                    city: $el.find('.city').text().trim() || ''
                },
                data: $el.find('pre').text().trim() || $el.text().trim().substring(0, 500),
                product: $el.find('.product').text().trim() || '',
                timestamp: new Date().toISOString()
            };

            if (result.ip_str) {
                results.push(result);
            }
        });

        // 获取总结果数
        const totalText = $('.search-stats').text() || $('#search-result-count').text() || '0';
        const totalMatch = totalText.match(/[\d,]+/);
        const total = totalMatch ? parseInt(totalMatch[0].replace(/,/g, '')) : results.length;

        console.log(`✅ 爬取成功，找到 ${results.length} 个结果`);

        return {
            total: total,
            matches: results
        };
    } catch (error) {
        console.error('❌ 爬取错误:', error.message);

        // 返回模拟数据作为后备
        return {
            total: 0,
            matches: [],
            error: '无法从 Shodan 获取数据，请稍后重试'
        };
    }
}

// 根路由
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/index.html'));
});

// 搜索路由（使用爬虫）
app.post('/api/search', async (req, res) => {
    const { query, page = 1, useAI = false } = req.body;

    if (!query) {
        return res.status(400).json({ error: '搜索查询不能为空' });
    }

    try {
        console.log(`🔍 搜索查询: ${query}, 页码: ${page}`);

        // 从 Shodan 网站爬取数据
        const scrapedData = await scrapeSholan(query, page);

        if (scrapedData.error) {
            return res.status(500).json({
                error: scrapedData.error,
                total: 0,
                matches: []
            });
        }

        // 如果请求 AI 分析
        let aiAnalysis = null;
        if (useAI && scrapedData.matches.length > 0) {
            console.log('🤖 使用 DeepSeek AI 分析结果...');
            try {
                aiAnalysis = await analyzeWithDeepSeek(scrapedData.matches, query);
            } catch (error) {
                console.error('AI 分析失败:', error.message);
            }
        }

        console.log(`✅ 找到 ${scrapedData.total} 个结果`);

        res.json({
            total: scrapedData.total,
            matches: scrapedData.matches,
            aiAnalysis: aiAnalysis
        });
    } catch (error) {
        console.error('❌ 搜索错误:', error.message);

        res.status(500).json({
            error: '搜索失败',
            message: error.message
        });
    }
});

// AI 分析路由
app.post('/api/analyze', async (req, res) => {
    const { data, query } = req.body;

    if (!data || !query) {
        return res.status(400).json({ error: '缺少必要参数' });
    }

    try {
        console.log(`🤖 使用 DeepSeek AI 分析数据...`);

        const analysis = await analyzeWithDeepSeek(data, query);

        res.json({
            success: true,
            analysis: analysis
        });
    } catch (error) {
        console.error('❌ AI 分析错误:', error.message);

        res.status(500).json({
            error: 'AI 分析失败',
            message: error.message
        });
    }
});

// 健康检查路由
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        deepseekConfigured: !!DEEPSEEK_API_KEY
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
    console.log(`🤖 DeepSeek AI: 已配置 ✅`);
    console.log(`🕷️  数据来源: Shodan 网站爬虫`);
    console.log(`\n按 Ctrl+C 停止服务器\n`);
});
