const db = require('../database/db');

class EnterpriseService {
    /**
     * 获取所有企业列表（支持分页）
     */
    async getAllEnterprises(page = 1, pageSize = 20) {
        const offset = (page - 1) * pageSize;

        const sql = `
            SELECT e.*, GROUP_CONCAT(t.name) as tags
            FROM enterprises e
            LEFT JOIN enterprise_tags et ON e.id = et.enterprise_id
            LEFT JOIN tags t ON et.tag_id = t.id
            GROUP BY e.id
            ORDER BY e.created_at DESC
            LIMIT ? OFFSET ?
        `;

        const enterprises = await db.query(sql, [pageSize, offset]);

        // 获取总数
        const countResult = await db.get('SELECT COUNT(*) as total FROM enterprises');

        return {
            data: enterprises.map(e => ({
                ...e,
                tags: e.tags ? e.tags.split(',') : []
            })),
            total: countResult.total,
            page,
            pageSize,
            totalPages: Math.ceil(countResult.total / pageSize)
        };
    }

    /**
     * 根据ID获取企业详情
     */
    async getEnterpriseById(id) {
        const enterprise = await db.get('SELECT * FROM enterprises WHERE id = ?', [id]);

        if (!enterprise) {
            return null;
        }

        // 获取标签
        const tags = await db.query(`
            SELECT t.* FROM tags t
            JOIN enterprise_tags et ON t.id = et.tag_id
            WHERE et.enterprise_id = ?
        `, [id]);

        // 获取资源
        const resources = await db.query(
            'SELECT * FROM enterprise_resources WHERE enterprise_id = ?',
            [id]
        );

        return {
            ...enterprise,
            tags,
            resources
        };
    }

    /**
     * 创建新企业
     */
    async createEnterprise(data) {
        const {
            name, code, industry, scale, region, city,
            registered_capital, established_date, legal_person,
            business_scope, contact_person, contact_phone, contact_email,
            address, website, employee_count, annual_revenue,
            certification, credit_rating, description, tags
        } = data;

        const sql = `
            INSERT INTO enterprises (
                name, code, industry, scale, region, city,
                registered_capital, established_date, legal_person,
                business_scope, contact_person, contact_phone, contact_email,
                address, website, employee_count, annual_revenue,
                certification, credit_rating, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        const result = await db.run(sql, [
            name, code, industry, scale, region, city,
            registered_capital, established_date, legal_person,
            business_scope, contact_person, contact_phone, contact_email,
            address, website, employee_count, annual_revenue,
            certification, credit_rating, description
        ]);

        // 添加标签
        if (tags && tags.length > 0) {
            await this.addTagsToEnterprise(result.id, tags);
        }

        return result.id;
    }

    /**
     * 更新企业信息
     */
    async updateEnterprise(id, data) {
        const fields = [];
        const values = [];

        Object.keys(data).forEach(key => {
            if (key !== 'tags' && key !== 'id') {
                fields.push(`${key} = ?`);
                values.push(data[key]);
            }
        });

        values.push(id);

        const sql = `UPDATE enterprises SET ${fields.join(', ')}, updated_at = CURRENT_TIMESTAMP WHERE id = ?`;
        await db.run(sql, values);

        // 更新标签
        if (data.tags) {
            await db.run('DELETE FROM enterprise_tags WHERE enterprise_id = ?', [id]);
            await this.addTagsToEnterprise(id, data.tags);
        }

        return true;
    }

    /**
     * 删除企业
     */
    async deleteEnterprise(id) {
        await db.run('DELETE FROM enterprises WHERE id = ?', [id]);
        return true;
    }

    /**
     * 为企业添加标签
     */
    async addTagsToEnterprise(enterpriseId, tagNames) {
        for (const tagName of tagNames) {
            // 查找或创建标签
            let tag = await db.get('SELECT id FROM tags WHERE name = ?', [tagName]);

            if (!tag) {
                const result = await db.run('INSERT INTO tags (name) VALUES (?)', [tagName]);
                tag = { id: result.id };
            }

            // 添加关联
            try {
                await db.run(
                    'INSERT INTO enterprise_tags (enterprise_id, tag_id) VALUES (?, ?)',
                    [enterpriseId, tag.id]
                );
            } catch (err) {
                // 忽略重复插入错误
                if (!err.message.includes('UNIQUE constraint')) {
                    throw err;
                }
            }
        }
    }

    /**
     * 高级筛选企业
     */
    async filterEnterprises(filters, page = 1, pageSize = 20) {
        const offset = (page - 1) * pageSize;
        const conditions = [];
        const params = [];

        // 行业筛选
        if (filters.industry && filters.industry.length > 0) {
            const placeholders = filters.industry.map(() => '?').join(',');
            conditions.push(`e.industry IN (${placeholders})`);
            params.push(...filters.industry);
        }

        // 规模筛选
        if (filters.scale && filters.scale.length > 0) {
            const placeholders = filters.scale.map(() => '?').join(',');
            conditions.push(`e.scale IN (${placeholders})`);
            params.push(...filters.scale);
        }

        // 地区筛选
        if (filters.region && filters.region.length > 0) {
            const placeholders = filters.region.map(() => '?').join(',');
            conditions.push(`e.region IN (${placeholders})`);
            params.push(...filters.region);
        }

        // 城市筛选
        if (filters.city && filters.city.length > 0) {
            const placeholders = filters.city.map(() => '?').join(',');
            conditions.push(`e.city IN (${placeholders})`);
            params.push(...filters.city);
        }

        // 信用评级筛选
        if (filters.creditRating && filters.creditRating.length > 0) {
            const placeholders = filters.creditRating.map(() => '?').join(',');
            conditions.push(`e.credit_rating IN (${placeholders})`);
            params.push(...filters.creditRating);
        }

        // 注册资本范围
        if (filters.minCapital) {
            conditions.push('e.registered_capital >= ?');
            params.push(filters.minCapital);
        }
        if (filters.maxCapital) {
            conditions.push('e.registered_capital <= ?');
            params.push(filters.maxCapital);
        }

        // 员工数量范围
        if (filters.minEmployees) {
            conditions.push('e.employee_count >= ?');
            params.push(filters.minEmployees);
        }
        if (filters.maxEmployees) {
            conditions.push('e.employee_count <= ?');
            params.push(filters.maxEmployees);
        }

        // 年营收范围
        if (filters.minRevenue) {
            conditions.push('e.annual_revenue >= ?');
            params.push(filters.minRevenue);
        }
        if (filters.maxRevenue) {
            conditions.push('e.annual_revenue <= ?');
            params.push(filters.maxRevenue);
        }

        // 状态筛选
        if (filters.status) {
            conditions.push('e.status = ?');
            params.push(filters.status);
        }

        // 关键词搜索
        if (filters.keyword) {
            conditions.push(`(
                e.name LIKE ? OR
                e.business_scope LIKE ? OR
                e.description LIKE ?
            )`);
            const keyword = `%${filters.keyword}%`;
            params.push(keyword, keyword, keyword);
        }

        // 标签筛选
        let tagJoin = '';
        if (filters.tags && filters.tags.length > 0) {
            tagJoin = `
                JOIN enterprise_tags et ON e.id = et.enterprise_id
                JOIN tags t ON et.tag_id = t.id
            `;
            const placeholders = filters.tags.map(() => '?').join(',');
            conditions.push(`t.name IN (${placeholders})`);
            params.push(...filters.tags);
        }

        const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

        const sql = `
            SELECT DISTINCT e.*, GROUP_CONCAT(DISTINCT tags.name) as tags
            FROM enterprises e
            ${tagJoin}
            LEFT JOIN enterprise_tags et2 ON e.id = et2.enterprise_id
            LEFT JOIN tags ON et2.tag_id = tags.id
            ${whereClause}
            GROUP BY e.id
            ORDER BY e.created_at DESC
            LIMIT ? OFFSET ?
        `;

        params.push(pageSize, offset);
        const enterprises = await db.query(sql, params);

        // 获取筛选后的总数
        const countSql = `
            SELECT COUNT(DISTINCT e.id) as total
            FROM enterprises e
            ${tagJoin}
            ${whereClause}
        `;
        const countParams = params.slice(0, -2); // 移除 LIMIT 和 OFFSET 参数
        const countResult = await db.get(countSql, countParams);

        return {
            data: enterprises.map(e => ({
                ...e,
                tags: e.tags ? e.tags.split(',') : []
            })),
            total: countResult.total,
            page,
            pageSize,
            totalPages: Math.ceil(countResult.total / pageSize),
            filters
        };
    }

    /**
     * 获取统计数据
     */
    async getStatistics() {
        const stats = {};

        // 总企业数
        const totalResult = await db.get('SELECT COUNT(*) as total FROM enterprises');
        stats.total = totalResult.total;

        // 按行业统计
        stats.byIndustry = await db.query(`
            SELECT industry, COUNT(*) as count
            FROM enterprises
            GROUP BY industry
            ORDER BY count DESC
        `);

        // 按规模统计
        stats.byScale = await db.query(`
            SELECT scale, COUNT(*) as count
            FROM enterprises
            GROUP BY scale
            ORDER BY count DESC
        `);

        // 按地区统计
        stats.byRegion = await db.query(`
            SELECT region, COUNT(*) as count
            FROM enterprises
            GROUP BY region
            ORDER BY count DESC
        `);

        // 按信用评级统计
        stats.byCreditRating = await db.query(`
            SELECT credit_rating, COUNT(*) as count
            FROM enterprises
            WHERE credit_rating IS NOT NULL
            GROUP BY credit_rating
            ORDER BY count DESC
        `);

        // 按状态统计
        stats.byStatus = await db.query(`
            SELECT status, COUNT(*) as count
            FROM enterprises
            GROUP BY status
        `);

        return stats;
    }

    /**
     * 获取所有可用的筛选选项
     */
    async getFilterOptions() {
        const options = {};

        // 获取所有行业
        const industries = await db.query('SELECT DISTINCT industry FROM enterprises ORDER BY industry');
        options.industries = industries.map(i => i.industry);

        // 获取所有地区
        const regions = await db.query('SELECT DISTINCT region FROM enterprises ORDER BY region');
        options.regions = regions.map(r => r.region);

        // 获取所有城市
        const cities = await db.query('SELECT DISTINCT city FROM enterprises WHERE city IS NOT NULL ORDER BY city');
        options.cities = cities.map(c => c.city);

        // 获取所有标签
        const tags = await db.query('SELECT name FROM tags ORDER BY name');
        options.tags = tags.map(t => t.name);

        // 规模选项
        options.scales = ['小型', '中型', '大型', '超大型'];

        // 信用评级选项
        options.creditRatings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'C'];

        // 状态选项
        options.statuses = ['active', 'inactive', 'suspended'];

        return options;
    }
}

module.exports = new EnterpriseService();
