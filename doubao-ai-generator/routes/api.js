const express = require('express');
const router = express.Router();
const taskService = require('../services/taskService');

/**
 * @route   POST /api/recognition
 * @desc    创建识别任务
 */
router.post('/recognition', async (req, res) => {
    try {
        const task = await taskService.createRecognitionTask(req.body);
        res.json({
            success: true,
            message: '识别任务创建成功',
            data: task
        });
    } catch (error) {
        console.error('创建识别任务失败:', error);
        res.status(500).json({
            success: false,
            message: '创建识别任务失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/recognition
 * @desc    获取识别任务列表
 */
router.get('/recognition', async (req, res) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const pageSize = parseInt(req.query.pageSize) || 20;
        const filters = {
            status: req.query.status,
            task_type: req.query.task_type
        };

        const result = await taskService.getRecognitionTasks(page, pageSize, filters);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        console.error('获取识别任务列表失败:', error);
        res.status(500).json({
            success: false,
            message: '获取识别任务列表失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/recognition/:id
 * @desc    获取识别任务详情
 */
router.get('/recognition/:id', async (req, res) => {
    try {
        const task = await taskService.getRecognitionTaskById(req.params.id);
        if (!task) {
            return res.status(404).json({
                success: false,
                message: '任务不存在'
            });
        }
        res.json({
            success: true,
            data: task
        });
    } catch (error) {
        console.error('获取识别任务详情失败:', error);
        res.status(500).json({
            success: false,
            message: '获取识别任务详情失败',
            error: error.message
        });
    }
});

/**
 * @route   DELETE /api/recognition/:id
 * @desc    删除识别任务
 */
router.delete('/recognition/:id', async (req, res) => {
    try {
        await taskService.deleteRecognitionTask(req.params.id);
        res.json({
            success: true,
            message: '任务删除成功'
        });
    } catch (error) {
        console.error('删除识别任务失败:', error);
        res.status(500).json({
            success: false,
            message: '删除识别任务失败',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/generation
 * @desc    创建生成任务
 */
router.post('/generation', async (req, res) => {
    try {
        const task = await taskService.createGenerationTask(req.body);
        res.json({
            success: true,
            message: '生成任务创建成功',
            data: task
        });
    } catch (error) {
        console.error('创建生成任务失败:', error);
        res.status(500).json({
            success: false,
            message: '创建生成任务失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/generation
 * @desc    获取生成任务列表
 */
router.get('/generation', async (req, res) => {
    try {
        const page = parseInt(req.query.page) || 1;
        const pageSize = parseInt(req.query.pageSize) || 20;
        const filters = {
            status: req.query.status,
            generation_type: req.query.generation_type
        };

        const result = await taskService.getGenerationTasks(page, pageSize, filters);
        res.json({
            success: true,
            ...result
        });
    } catch (error) {
        console.error('获取生成任务列表失败:', error);
        res.status(500).json({
            success: false,
            message: '获取生成任务列表失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/generation/:id
 * @desc    获取生成任务详情
 */
router.get('/generation/:id', async (req, res) => {
    try {
        const task = await taskService.getGenerationTaskById(req.params.id);
        if (!task) {
            return res.status(404).json({
                success: false,
                message: '任务不存在'
            });
        }
        res.json({
            success: true,
            data: task
        });
    } catch (error) {
        console.error('获取生成任务详情失败:', error);
        res.status(500).json({
            success: false,
            message: '获取生成任务详情失败',
            error: error.message
        });
    }
});

/**
 * @route   DELETE /api/generation/:id
 * @desc    删除生成任务
 */
router.delete('/generation/:id', async (req, res) => {
    try {
        await taskService.deleteGenerationTask(req.params.id);
        res.json({
            success: true,
            message: '任务删除成功'
        });
    } catch (error) {
        console.error('删除生成任务失败:', error);
        res.status(500).json({
            success: false,
            message: '删除生成任务失败',
            error: error.message
        });
    }
});

/**
 * @route   GET /api/templates
 * @desc    获取模板列表
 */
router.get('/templates', async (req, res) => {
    try {
        const active_only = req.query.active_only !== 'false';
        const templates = await taskService.getTemplates(active_only);
        res.json({
            success: true,
            data: templates
        });
    } catch (error) {
        console.error('获取模板列表失败:', error);
        res.status(500).json({
            success: false,
            message: '获取模板列表失败',
            error: error.message
        });
    }
});

/**
 * @route   POST /api/templates
 * @desc    创建模板
 */
router.post('/templates', async (req, res) => {
    try {
        const id = await taskService.createTemplate(req.body);
        res.json({
            success: true,
            message: '模板创建成功',
            id
        });
    } catch (error) {
        console.error('创建模板失败:', error);
        res.status(500).json({
            success: false,
            message: '创建模板失败',
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
        const stats = await taskService.getStatistics();
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

module.exports = router;
