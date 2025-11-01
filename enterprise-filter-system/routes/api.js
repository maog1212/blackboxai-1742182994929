const express = require('express');
const router = express.Router();
const enterpriseService = require('../services/enterpriseService');

/**
 * @route   GET /api/enterprises
 * @desc    获取企业列表（支持分页）
 * @query   page, pageSize
 */
router.get('/enterprises', async (req, res) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const pageSize = parseInt(req.query.pageSize) || 20;

        const result = await enterpriseService.getAllEnterprises(page, pageSize);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        console.error('获取企业列表失败:', error);
        res.status(500).json({
            success: false,
            message: '获取企业列表失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/enterprises/:id
 * @desc    获取企业详情
 */
router.get('/enterprises/:id', async (req, res) => {
    try {
        const enterprise = await enterpriseService.getEnterpriseById(req.params.id);

        if (!enterprise) {
            return res.status(404).json({
                success: false,
                message: '企业不存在'
            });
        }

        res.json({
            success: true,
            data: enterprise
        });
    } catch (error) {
        console.error('获取企业详情失败:', error);
        res.status(500).json({
            success: false,
            message: '获取企业详情失败',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/enterprises
 * @desc    创建新企业
 */
router.post('/enterprises', async (req, res) => {
    try {
        const enterpriseId = await enterpriseService.createEnterprise(req.body);

        res.status(201).json({
            success: true,
            message: '企业创建成功',
            id: enterpriseId
        });
    } catch (error) {
        console.error('创建企业失败:', error);
        res.status(500).json({
            success: false,
            message: '创建企业失败',
            error: error.message
        });
    }
});

/**
 * @route   PUT /api/enterprises/:id
 * @desc    更新企业信息
 */
router.put('/enterprises/:id', async (req, res) => {
    try {
        await enterpriseService.updateEnterprise(req.params.id, req.body);

        res.json({
            success: true,
            message: '企业信息更新成功'
        });
    } catch (error) {
        console.error('更新企业失败:', error);
        res.status(500).json({
            success: false,
            message: '更新企业失败',
            error: error.message
        });
    }
});

/**
 * @route   DELETE /api/enterprises/:id
 * @desc    删除企业
 */
router.delete('/enterprises/:id', async (req, res) => {
    try {
        await enterpriseService.deleteEnterprise(req.params.id);

        res.json({
            success: true,
            message: '企业删除成功'
        });
    } catch (error) {
        console.error('删除企业失败:', error);
        res.status(500).json({
            success: false,
            message: '删除企业失败',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/enterprises/filter
 * @desc    高级筛选企业
 * @body    filters对象，包含各种筛选条件
 */
router.post('/enterprises/filter', async (req, res) => {
    try {
        const filters = req.body.filters || {};
        const page = parseInt(req.body.page) || 1;
        const pageSize = parseInt(req.body.pageSize) || 20;

        const result = await enterpriseService.filterEnterprises(filters, page, pageSize);

        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        console.error('筛选企业失败:', error);
        res.status(500).json({
            success: false,
            message: '筛选企业失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/statistics
 * @desc    获取统计数据
 */
router.get('/statistics', async (req, res) => {
    try {
        const stats = await enterpriseService.getStatistics();

        res.json({
            success: true,
            data: stats
        });
    } catch (error) {
        console.error('获取统计数据失败:', error);
        res.status(500).json({
            success: false,
            message: '获取统计数据失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/filter-options
 * @desc    获取所有可用的筛选选项
 */
router.get('/filter-options', async (req, res) => {
    try {
        const options = await enterpriseService.getFilterOptions();

        res.json({
            success: true,
            data: options
        });
    } catch (error) {
        console.error('获取筛选选项失败:', error);
        res.status(500).json({
            success: false,
            message: '获取筛选选项失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/export
 * @desc    导出筛选结果为CSV
 */
router.post('/export', async (req, res) => {
    try {
        const filters = req.body.filters || {};
        const result = await enterpriseService.filterEnterprises(filters, 1, 10000);

        // 生成CSV
        const csv = generateCSV(result.data);

        res.setHeader('Content-Type', 'text/csv; charset=utf-8');
        res.setHeader('Content-Disposition', 'attachment; filename=enterprises.csv');
        res.send('\ufeff' + csv); // 添加BOM以支持中文
    } catch (error) {
        console.error('导出失败:', error);
        res.status(500).json({
            success: false,
            message: '导出失败',
            error: error.message
        });
    }
});

/**
 * 生成CSV内容
 */
function generateCSV(data) {
    const headers = [
        '企业名称', '企业代码', '所属行业', '企业规模', '所在地区', '所在城市',
        '注册资本(万元)', '成立日期', '法人代表', '联系人', '联系电话',
        '联系邮箱', '员工数量', '年营收(万元)', '信用评级', '状态'
    ];

    const rows = data.map(e => [
        e.name, e.code, e.industry, e.scale, e.region, e.city,
        e.registered_capital, e.established_date, e.legal_person,
        e.contact_person, e.contact_phone, e.contact_email,
        e.employee_count, e.annual_revenue, e.credit_rating, e.status
    ]);

    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.map(field => {
            const value = field !== null && field !== undefined ? String(field) : '';
            // 处理包含逗号或引号的字段
            if (value.includes(',') || value.includes('"') || value.includes('\n')) {
                return `"${value.replace(/"/g, '""')}"`;
            }
            return value;
        }).join(','))
    ].join('\n');

    return csvContent;
}

module.exports = router;
