const db = require('../database/db');
const aiService = require('./aiService');

class TaskService {
    /**
     * 创建识别任务
     */
    async createRecognitionTask(data) {
        const { task_name, task_type, input_content } = data;

        const sql = `
            INSERT INTO recognition_tasks (task_name, task_type, input_content, status)
            VALUES (?, ?, ?, 'processing')
        `;

        const result = await db.run(sql, [task_name, task_type, input_content]);
        const taskId = result.id;

        // 执行识别
        try {
            const startTime = Date.now();
            const recognition = await aiService.recognizeText(input_content);
            const processingTime = Date.now() - startTime;

            await db.run(`
                UPDATE recognition_tasks
                SET recognition_result = ?,
                    confidence_score = ?,
                    status = 'completed',
                    processing_time = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            `, [
                JSON.stringify(recognition.data),
                recognition.confidence,
                processingTime,
                taskId
            ]);

            return await this.getRecognitionTaskById(taskId);
        } catch (error) {
            await db.run(`
                UPDATE recognition_tasks
                SET status = 'failed',
                    error_message = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            `, [error.message, taskId]);

            throw error;
        }
    }

    /**
     * 创建生成任务
     */
    async createGenerationTask(data) {
        const { task_name, template_id, generation_type, prompt, context } = data;

        const sql = `
            INSERT INTO generation_tasks (task_name, template_id, generation_type, prompt, status)
            VALUES (?, ?, ?, ?, 'processing')
        `;

        const result = await db.run(sql, [task_name, template_id, generation_type, prompt]);
        const taskId = result.id;

        // 获取模板
        const template = await db.get('SELECT * FROM templates WHERE id = ?', [template_id]);

        if (!template) {
            throw new Error('模板不存在');
        }

        // 执行生成
        try {
            const startTime = Date.now();
            const generation = await aiService.generateContent(template, context);
            const processingTime = Date.now() - startTime;
            const wordCount = generation.data.length;

            await db.run(`
                UPDATE generation_tasks
                SET generated_content = ?,
                    quality_score = ?,
                    word_count = ?,
                    status = 'completed',
                    processing_time = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            `, [
                generation.data,
                generation.quality_score,
                wordCount,
                processingTime,
                taskId
            ]);

            // 更新模板使用次数
            await db.run('UPDATE templates SET usage_count = usage_count + 1 WHERE id = ?', [template_id]);

            return await this.getGenerationTaskById(taskId);
        } catch (error) {
            await db.run(`
                UPDATE generation_tasks
                SET status = 'failed',
                    error_message = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            `, [error.message, taskId]);

            throw error;
        }
    }

    /**
     * 获取识别任务列表
     */
    async getRecognitionTasks(page = 1, pageSize = 20, filters = {}) {
        const offset = (page - 1) * pageSize;
        const conditions = [];
        const params = [];

        if (filters.status) {
            conditions.push('status = ?');
            params.push(filters.status);
        }

        if (filters.task_type) {
            conditions.push('task_type = ?');
            params.push(filters.task_type);
        }

        const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

        const sql = `
            SELECT * FROM recognition_tasks
            ${whereClause}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        `;

        params.push(pageSize, offset);
        const tasks = await db.query(sql, params);

        // 解析JSON结果
        tasks.forEach(task => {
            if (task.recognition_result) {
                task.recognition_result = JSON.parse(task.recognition_result);
            }
        });

        const countSql = `SELECT COUNT(*) as total FROM recognition_tasks ${whereClause}`;
        const countResult = await db.get(countSql, params.slice(0, -2));

        return {
            data: tasks,
            total: countResult.total,
            page,
            pageSize,
            totalPages: Math.ceil(countResult.total / pageSize)
        };
    }

    /**
     * 获取生成任务列表
     */
    async getGenerationTasks(page = 1, pageSize = 20, filters = {}) {
        const offset = (page - 1) * pageSize;
        const conditions = [];
        const params = [];

        if (filters.status) {
            conditions.push('status = ?');
            params.push(filters.status);
        }

        if (filters.generation_type) {
            conditions.push('generation_type = ?');
            params.push(filters.generation_type);
        }

        const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

        const sql = `
            SELECT g.*, t.template_name
            FROM generation_tasks g
            LEFT JOIN templates t ON g.template_id = t.id
            ${whereClause}
            ORDER BY g.created_at DESC
            LIMIT ? OFFSET ?
        `;

        params.push(pageSize, offset);
        const tasks = await db.query(sql, params);

        const countSql = `SELECT COUNT(*) as total FROM generation_tasks ${whereClause}`;
        const countResult = await db.get(countSql, params.slice(0, -2));

        return {
            data: tasks,
            total: countResult.total,
            page,
            pageSize,
            totalPages: Math.ceil(countResult.total / pageSize)
        };
    }

    /**
     * 根据ID获取识别任务
     */
    async getRecognitionTaskById(id) {
        const task = await db.get('SELECT * FROM recognition_tasks WHERE id = ?', [id]);
        if (task && task.recognition_result) {
            task.recognition_result = JSON.parse(task.recognition_result);
        }
        return task;
    }

    /**
     * 根据ID获取生成任务
     */
    async getGenerationTaskById(id) {
        const task = await db.get(`
            SELECT g.*, t.template_name, t.template_type
            FROM generation_tasks g
            LEFT JOIN templates t ON g.template_id = t.id
            WHERE g.id = ?
        `, [id]);
        return task;
    }

    /**
     * 获取所有模板
     */
    async getTemplates(active_only = true) {
        const sql = active_only
            ? 'SELECT * FROM templates WHERE is_active = 1 ORDER BY usage_count DESC'
            : 'SELECT * FROM templates ORDER BY created_at DESC';

        const templates = await db.query(sql);

        templates.forEach(t => {
            if (t.parameters) {
                t.parameters = JSON.parse(t.parameters);
            }
        });

        return templates;
    }

    /**
     * 创建模板
     */
    async createTemplate(data) {
        const { template_name, template_type, description, prompt_template, parameters } = data;

        const sql = `
            INSERT INTO templates (template_name, template_type, description, prompt_template, parameters)
            VALUES (?, ?, ?, ?, ?)
        `;

        const result = await db.run(sql, [
            template_name,
            template_type,
            description,
            prompt_template,
            JSON.stringify(parameters || {})
        ]);

        return result.id;
    }

    /**
     * 获取统计数据
     */
    async getStatistics() {
        const stats = {};

        // 识别任务统计
        const recogTotal = await db.get('SELECT COUNT(*) as total FROM recognition_tasks');
        const recogCompleted = await db.get("SELECT COUNT(*) as total FROM recognition_tasks WHERE status = 'completed'");
        const recogFailed = await db.get("SELECT COUNT(*) as total FROM recognition_tasks WHERE status = 'failed'");

        stats.recognition = {
            total: recogTotal.total,
            completed: recogCompleted.total,
            failed: recogFailed.total,
            success_rate: recogTotal.total > 0 ? (recogCompleted.total / recogTotal.total * 100).toFixed(2) : 0
        };

        // 生成任务统计
        const genTotal = await db.get('SELECT COUNT(*) as total FROM generation_tasks');
        const genCompleted = await db.get("SELECT COUNT(*) as total FROM generation_tasks WHERE status = 'completed'");
        const genFailed = await db.get("SELECT COUNT(*) as total FROM generation_tasks WHERE status = 'failed'");

        stats.generation = {
            total: genTotal.total,
            completed: genCompleted.total,
            failed: genFailed.total,
            success_rate: genTotal.total > 0 ? (genCompleted.total / genTotal.total * 100).toFixed(2) : 0
        };

        // 按类型统计识别任务
        stats.recognitionByType = await db.query(`
            SELECT task_type, COUNT(*) as count
            FROM recognition_tasks
            GROUP BY task_type
            ORDER BY count DESC
        `);

        // 按类型统计生成任务
        stats.generationByType = await db.query(`
            SELECT generation_type, COUNT(*) as count
            FROM generation_tasks
            GROUP BY generation_type
            ORDER BY count DESC
        `);

        // 模板使用统计
        stats.topTemplates = await db.query(`
            SELECT template_name, template_type, usage_count
            FROM templates
            WHERE is_active = 1
            ORDER BY usage_count DESC
            LIMIT 5
        `);

        // 总字数统计
        const wordStats = await db.get('SELECT SUM(word_count) as total_words FROM generation_tasks WHERE status = "completed"');
        stats.totalWordsGenerated = wordStats.total_words || 0;

        // 平均处理时间
        const avgTime = await db.get('SELECT AVG(processing_time) as avg_time FROM generation_tasks WHERE status = "completed"');
        stats.averageProcessingTime = avgTime.avg_time ? Math.round(avgTime.avg_time) : 0;

        return stats;
    }

    /**
     * 删除任务
     */
    async deleteRecognitionTask(id) {
        await db.run('DELETE FROM recognition_tasks WHERE id = ?', [id]);
        return true;
    }

    async deleteGenerationTask(id) {
        await db.run('DELETE FROM generation_tasks WHERE id = ?', [id]);
        return true;
    }
}

module.exports = new TaskService();
