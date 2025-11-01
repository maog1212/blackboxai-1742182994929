const db = require('../database/db');

// 示例模板数据
const sampleTemplates = [
    {
        template_name: '产品介绍文章模板',
        template_type: 'article',
        description: '用于生成产品介绍文章',
        prompt_template: '请根据以下信息生成一篇专业的产品介绍文章：{{topic}}',
        example_output: '示例产品介绍文章...',
        parameters: JSON.stringify({ max_length: 2000, tone: 'professional' })
    },
    {
        template_name: '营销文案模板',
        template_type: 'description',
        description: '生成吸引人的营销文案',
        prompt_template: '为{{topic}}创建一段吸引人的营销文案',
        example_output: '示例营销文案...',
        parameters: JSON.stringify({ max_length: 500, tone: 'persuasive' })
    },
    {
        template_name: '内容摘要模板',
        template_type: 'summary',
        description: '将长文本浓缩为简洁摘要',
        prompt_template: '请为以下内容生成摘要：{{text}}',
        example_output: '示例摘要...',
        parameters: JSON.stringify({ max_length: 200 })
    },
    {
        template_name: 'SEO标题生成器',
        template_type: 'title',
        description: '生成SEO优化的标题',
        prompt_template: '为{{topic}}生成5个SEO优化的标题',
        example_output: '1. 标题一\n2. 标题二...',
        parameters: JSON.stringify({ count: 5, style: 'seo' })
    },
    {
        template_name: '问答内容生成器',
        template_type: 'qa',
        description: '生成常见问答内容',
        prompt_template: '针对{{topic}}生成10个常见问题和答案',
        example_output: 'Q: 问题1\nA: 答案1...',
        parameters: JSON.stringify({ count: 10 })
    }
];

async function seedData() {
    try {
        console.log('开始初始化数据库...');
        await db.init();
        await db.initSchema();

        console.log('开始添加模板数据...');
        let count = 0;

        for (const template of sampleTemplates) {
            try {
                await db.run(`
                    INSERT INTO templates (
                        template_name, template_type, description,
                        prompt_template, example_output, parameters
                    ) VALUES (?, ?, ?, ?, ?, ?)
                `, [
                    template.template_name,
                    template.template_type,
                    template.description,
                    template.prompt_template,
                    template.example_output,
                    template.parameters
                ]);

                count++;
                console.log(`✓ 已添加: ${template.template_name}`);
            } catch (err) {
                if (err.message.includes('UNIQUE constraint')) {
                    console.log(`- 跳过（已存在）: ${template.template_name}`);
                } else {
                    console.error(`✗ 添加失败: ${template.template_name}`, err.message);
                }
            }
        }

        console.log(`\n数据初始化完成！`);
        console.log(`- 已添加 ${count} 个模板`);
        console.log(`- 数据库文件: ${require('path').join(__dirname, '../database/doubao_generator.db')}`);

    } catch (error) {
        console.error('数据初始化失败:', error);
    } finally {
        await db.close();
    }
}

// 执行数据填充
seedData();
