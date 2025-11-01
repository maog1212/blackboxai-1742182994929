const db = require('../database/db');

// 示例企业数据
const sampleEnterprises = [
    {
        name: '华为技术有限公司',
        code: '91440300279889426H',
        industry: '通信设备制造',
        scale: '超大型',
        region: '广东省',
        city: '深圳市',
        registered_capital: 4000000,
        established_date: '1987-09-15',
        legal_person: '任正非',
        business_scope: '通信设备研发、生产、销售；软件开发；互联网服务',
        contact_person: '张经理',
        contact_phone: '0755-28780808',
        contact_email: 'contact@huawei.com',
        address: '广东省深圳市龙岗区坂田华为基地',
        website: 'https://www.huawei.com',
        employee_count: 197000,
        annual_revenue: 891400000,
        certification: 'ISO9001,ISO14001,ISO27001',
        credit_rating: 'AAA',
        description: '全球领先的信息与通信技术(ICT)解决方案供应商',
        tags: ['高新技术', '创新型', '出口企业', '5G领军']
    },
    {
        name: '阿里巴巴集团控股有限公司',
        code: '91330000712666167W',
        industry: '互联网与相关服务',
        scale: '超大型',
        region: '浙江省',
        city: '杭州市',
        registered_capital: 3000000,
        established_date: '1999-06-28',
        legal_person: '张勇',
        business_scope: '电子商务、云计算、数字娱乐',
        contact_person: '李经理',
        contact_phone: '0571-85022088',
        contact_email: 'info@alibaba.com',
        address: '浙江省杭州市余杭区文一西路969号',
        website: 'https://www.alibaba.com',
        employee_count: 254941,
        annual_revenue: 717200000,
        certification: 'ISO9001,ISO27001',
        credit_rating: 'AAA',
        description: '中国最大的电子商务公司',
        tags: ['互联网', '电商', '云计算', '数字化']
    },
    {
        name: '比亚迪股份有限公司',
        code: '91440300708461136T',
        industry: '汽车制造',
        scale: '大型',
        region: '广东省',
        city: '深圳市',
        registered_capital: 2960000,
        established_date: '1995-02-10',
        legal_person: '王传福',
        business_scope: '新能源汽车、电池、电子产品研发生产',
        contact_person: '王经理',
        contact_phone: '0755-89888888',
        contact_email: 'byd@byd.com',
        address: '广东省深圳市龙岗区葵涌街道延安路',
        website: 'https://www.byd.com',
        employee_count: 290000,
        annual_revenue: 424600000,
        certification: 'ISO9001,ISO14001,IATF16949',
        credit_rating: 'AA',
        description: '全球领先的新能源汽车制造商',
        tags: ['新能源', '汽车制造', '电池技术', '上市公司']
    },
    {
        name: '小米科技有限责任公司',
        code: '91110108551385082Q',
        industry: '电子产品制造',
        scale: '大型',
        region: '北京市',
        city: '北京市',
        registered_capital: 185000,
        established_date: '2010-03-03',
        legal_person: '雷军',
        business_scope: '智能手机、智能硬件、IoT平台服务',
        contact_person: '刘经理',
        contact_phone: '010-60606666',
        contact_email: 'contact@mi.com',
        address: '北京市海淀区清河中街68号',
        website: 'https://www.mi.com',
        employee_count: 28000,
        annual_revenue: 328300000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AA',
        description: '以智能手机、智能硬件和IoT平台为核心的互联网公司',
        tags: ['智能硬件', 'IoT', '互联网', '创新型']
    },
    {
        name: '宁德时代新能源科技股份有限公司',
        code: '91350400MA2YN27Q1K',
        industry: '电池制造',
        scale: '大型',
        region: '福建省',
        city: '宁德市',
        registered_capital: 546600,
        established_date: '2011-12-16',
        legal_person: '曾毓群',
        business_scope: '动力电池、储能电池研发生产',
        contact_person: '陈经理',
        contact_phone: '0593-8979999',
        contact_email: 'info@catl.com',
        address: '福建省宁德市蕉城区漳湾镇新港路2号',
        website: 'https://www.catl.com',
        employee_count: 75000,
        annual_revenue: 329000000,
        certification: 'ISO9001,ISO14001,IATF16949',
        credit_rating: 'AAA',
        description: '全球领先的动力电池系统提供商',
        tags: ['新能源', '电池技术', '上市公司', '高新技术']
    },
    {
        name: '海康威视数字技术股份有限公司',
        code: '913301007799288304',
        industry: '安防设备制造',
        scale: '大型',
        region: '浙江省',
        city: '杭州市',
        registered_capital: 1123600,
        established_date: '2001-11-30',
        legal_person: '陈宗年',
        business_scope: '安防产品及解决方案的研发生产',
        contact_person: '赵经理',
        contact_phone: '0571-88075998',
        contact_email: 'info@hikvision.com',
        address: '浙江省杭州市滨江区阡陌路555号',
        website: 'https://www.hikvision.com',
        employee_count: 42000,
        annual_revenue: 81400000,
        certification: 'ISO9001,ISO14001,ISO27001',
        credit_rating: 'AA',
        description: '全球领先的以视频为核心的智能物联网解决方案提供商',
        tags: ['安防', 'AI', '视频监控', '上市公司']
    },
    {
        name: '京东方科技集团股份有限公司',
        code: '91110000633625764H',
        industry: '显示器件制造',
        scale: '大型',
        region: '北京市',
        city: '北京市',
        registered_capital: 365100,
        established_date: '1993-04-09',
        legal_person: '陈炎顺',
        business_scope: '显示器件、智慧系统、健康服务',
        contact_person: '孙经理',
        contact_phone: '010-65537788',
        contact_email: 'info@boe.com',
        address: '北京市朝阳区酒仙桥路10号',
        website: 'https://www.boe.com',
        employee_count: 70000,
        annual_revenue: 161900000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AA',
        description: '全球领先的半导体显示技术、产品与服务提供商',
        tags: ['显示技术', '半导体', '上市公司', '高新技术']
    },
    {
        name: '美的集团股份有限公司',
        code: '91440606279308840H',
        industry: '家用电器制造',
        scale: '大型',
        region: '广东省',
        city: '佛山市',
        registered_capital: 664000,
        established_date: '1968-05-24',
        legal_person: '方洪波',
        business_scope: '家用电器、暖通空调、机器人与自动化系统',
        contact_person: '周经理',
        contact_phone: '0757-26605678',
        contact_email: 'info@midea.com',
        address: '广东省佛山市顺德区北滘镇美的大道6号',
        website: 'https://www.midea.com',
        employee_count: 150000,
        annual_revenue: 343900000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AAA',
        description: '全球领先的消费电器、暖通空调、机器人及工业自动化系统企业',
        tags: ['家电', '智能制造', '上市公司', '出口企业']
    },
    {
        name: '中兴通讯股份有限公司',
        code: '91440300192243952Q',
        industry: '通信设备制造',
        scale: '大型',
        region: '广东省',
        city: '深圳市',
        registered_capital: 410000,
        established_date: '1985-02-06',
        legal_person: '李自学',
        business_scope: '通信网络设备、手机及相关产品',
        contact_person: '郑经理',
        contact_phone: '0755-26770000',
        contact_email: 'info@zte.com.cn',
        address: '广东省深圳市南山区科技南路55号',
        website: 'https://www.zte.com.cn',
        employee_count: 75000,
        annual_revenue: 122600000,
        certification: 'ISO9001,ISO14001,ISO27001',
        credit_rating: 'AA',
        description: '全球领先的综合通信解决方案提供商',
        tags: ['通信', '5G', '上市公司', '高新技术']
    },
    {
        name: '格力电器股份有限公司',
        code: '914404007099857805',
        industry: '家用电器制造',
        scale: '大型',
        region: '广东省',
        city: '珠海市',
        registered_capital: 601200,
        established_date: '1991-12-26',
        legal_person: '董明珠',
        business_scope: '空调、生活电器、高端装备',
        contact_person: '黄经理',
        contact_phone: '0756-8614883',
        contact_email: 'gree@gree.com',
        address: '广东省珠海市前山金鸡西路',
        website: 'https://www.gree.com',
        employee_count: 90000,
        annual_revenue: 190200000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AAA',
        description: '全球最大的专业化空调企业',
        tags: ['家电', '空调', '上市公司', '智能制造']
    },
    {
        name: '腾讯科技（深圳）有限公司',
        code: '91440300708461136G',
        industry: '互联网与相关服务',
        scale: '超大型',
        region: '广东省',
        city: '深圳市',
        registered_capital: 50000,
        established_date: '1998-11-11',
        legal_person: '马化腾',
        business_scope: '社交网络、游戏、金融科技、云服务',
        contact_person: '吴经理',
        contact_phone: '0755-86013388',
        contact_email: 'info@tencent.com',
        address: '广东省深圳市南山区粤海街道麻岭社区科技中一路腾讯大厦',
        website: 'https://www.tencent.com',
        employee_count: 112771,
        annual_revenue: 554500000,
        certification: 'ISO9001,ISO27001',
        credit_rating: 'AAA',
        description: '中国领先的互联网增值服务提供商',
        tags: ['互联网', '社交', '游戏', '云计算']
    },
    {
        name: '长江实业集团有限公司',
        code: '91320000134567890A',
        industry: '房地产开发',
        scale: '大型',
        region: '江苏省',
        city: '南京市',
        registered_capital: 500000,
        established_date: '1990-03-15',
        legal_person: '李明',
        business_scope: '房地产开发、物业管理、建筑工程',
        contact_person: '张总',
        contact_phone: '025-84567890',
        contact_email: 'info@changjiang.com',
        address: '江苏省南京市鼓楼区中央路123号',
        website: 'https://www.changjiang.com',
        employee_count: 5000,
        annual_revenue: 85000,
        certification: 'ISO9001',
        credit_rating: 'A',
        description: '专注于高端住宅和商业地产开发',
        tags: ['房地产', '物业管理', '建筑']
    },
    {
        name: '天津钢铁集团有限公司',
        code: '91120000234567891B',
        industry: '钢铁冶炼',
        scale: '大型',
        region: '天津市',
        city: '天津市',
        registered_capital: 800000,
        established_date: '1985-06-20',
        legal_person: '王强',
        business_scope: '钢材生产、加工、销售',
        contact_person: '刘部长',
        contact_phone: '022-23456789',
        contact_email: 'steel@tjsteel.com',
        address: '天津市滨海新区港口工业园区',
        website: 'https://www.tjsteel.com',
        employee_count: 25000,
        annual_revenue: 450000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AA',
        description: '华北地区主要的钢铁生产基地',
        tags: ['钢铁', '制造', '重工业']
    },
    {
        name: '上海医药集团股份有限公司',
        code: '91310000345678902C',
        industry: '医药制造',
        scale: '大型',
        region: '上海市',
        city: '上海市',
        registered_capital: 300000,
        established_date: '1994-09-12',
        legal_person: '陈华',
        business_scope: '药品研发、生产、销售；医疗器械',
        contact_person: '林主任',
        contact_phone: '021-54321098',
        contact_email: 'info@shpharma.com',
        address: '上海市浦东新区张江高科技园区',
        website: 'https://www.shpharma.com',
        employee_count: 15000,
        annual_revenue: 230000,
        certification: 'ISO9001,GMP',
        credit_rating: 'AA',
        description: '中国领先的综合性医药集团',
        tags: ['医药', '生物制药', '上市公司', '研发']
    },
    {
        name: '四川长虹电器股份有限公司',
        code: '91510000456789013D',
        industry: '家用电器制造',
        scale: '大型',
        region: '四川省',
        city: '绵阳市',
        registered_capital: 428000,
        established_date: '1958-10-01',
        legal_person: '赵勇',
        business_scope: '彩电、冰箱、空调等家电产品',
        contact_person: '杨经理',
        contact_phone: '0816-2418888',
        contact_email: 'service@changhong.com',
        address: '四川省绵阳市高新区绵兴东路35号',
        website: 'https://www.changhong.com',
        employee_count: 50000,
        annual_revenue: 110000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'A',
        description: '中国知名的家电企业',
        tags: ['家电', '彩电', '上市公司']
    },
    {
        name: '山东黄金集团有限公司',
        code: '91370000567890124E',
        industry: '有色金属冶炼',
        scale: '大型',
        region: '山东省',
        city: '济南市',
        registered_capital: 600000,
        established_date: '1996-12-25',
        legal_person: '满慎刚',
        business_scope: '黄金采选、冶炼、销售',
        contact_person: '孙总',
        contact_phone: '0531-87501234',
        contact_email: 'info@sdgold.com',
        address: '山东省济南市历下区经十路9999号',
        website: 'https://www.sdgold.com',
        employee_count: 18000,
        annual_revenue: 180000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AA',
        description: '中国大型黄金生产企业',
        tags: ['黄金', '采矿', '冶炼', '上市公司']
    },
    {
        name: '重庆长安汽车股份有限公司',
        code: '91500000678901235F',
        industry: '汽车制造',
        scale: '大型',
        region: '重庆市',
        city: '重庆市',
        registered_capital: 455000,
        established_date: '1996-10-31',
        legal_person: '朱华荣',
        business_scope: '汽车及零部件研发、生产、销售',
        contact_person: '何经理',
        contact_phone: '023-67594567',
        contact_email: 'changan@changan.com.cn',
        address: '重庆市江北区建新东路260号',
        website: 'https://www.changan.com.cn',
        employee_count: 90000,
        annual_revenue: 117600000,
        certification: 'ISO9001,IATF16949',
        credit_rating: 'AA',
        description: '中国汽车四大集团之一',
        tags: ['汽车', '新能源', '上市公司', '智能网联']
    },
    {
        name: '湖南中联重科股份有限公司',
        code: '91430000789012346G',
        industry: '工程机械制造',
        scale: '大型',
        region: '湖南省',
        city: '长沙市',
        registered_capital: 770000,
        established_date: '1992-10-07',
        legal_person: '詹纯新',
        business_scope: '工程机械及配件研发、制造、销售',
        contact_person: '曾经理',
        contact_phone: '0731-88923300',
        contact_email: 'zoomlion@zoomlion.com',
        address: '湖南省长沙市岳麓区银盆岭街道麓谷大道',
        website: 'https://www.zoomlion.com',
        employee_count: 23000,
        annual_revenue: 67200000,
        certification: 'ISO9001,ISO14001',
        credit_rating: 'AA',
        description: '全球领先的工程机械制造商',
        tags: ['工程机械', '智能制造', '上市公司']
    }
];

// 添加行业数据
const industries = [
    { name: '通信设备制造', code: 'C39' },
    { name: '互联网与相关服务', code: 'I64' },
    { name: '汽车制造', code: 'C36' },
    { name: '电子产品制造', code: 'C39' },
    { name: '电池制造', code: 'C38' },
    { name: '安防设备制造', code: 'C40' },
    { name: '显示器件制造', code: 'C39' },
    { name: '家用电器制造', code: 'C38' },
    { name: '房地产开发', code: 'K70' },
    { name: '钢铁冶炼', code: 'C31' },
    { name: '医药制造', code: 'C27' },
    { name: '有色金属冶炼', code: 'C32' },
    { name: '工程机械制造', code: 'C35' }
];

async function seedData() {
    try {
        console.log('开始初始化数据库...');
        await db.init();
        await db.initSchema();

        console.log('开始添加行业数据...');
        for (const industry of industries) {
            try {
                await db.run(
                    'INSERT INTO industries (name, code) VALUES (?, ?)',
                    [industry.name, industry.code]
                );
            } catch (err) {
                // 忽略重复插入
            }
        }
        console.log(`已添加 ${industries.length} 个行业分类`);

        console.log('开始添加企业数据...');
        let count = 0;
        for (const enterprise of sampleEnterprises) {
            const { tags, ...enterpriseData } = enterprise;

            try {
                const result = await db.run(`
                    INSERT INTO enterprises (
                        name, code, industry, scale, region, city,
                        registered_capital, established_date, legal_person,
                        business_scope, contact_person, contact_phone, contact_email,
                        address, website, employee_count, annual_revenue,
                        certification, credit_rating, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                `, [
                    enterpriseData.name,
                    enterpriseData.code,
                    enterpriseData.industry,
                    enterpriseData.scale,
                    enterpriseData.region,
                    enterpriseData.city,
                    enterpriseData.registered_capital,
                    enterpriseData.established_date,
                    enterpriseData.legal_person,
                    enterpriseData.business_scope,
                    enterpriseData.contact_person,
                    enterpriseData.contact_phone,
                    enterpriseData.contact_email,
                    enterpriseData.address,
                    enterpriseData.website,
                    enterpriseData.employee_count,
                    enterpriseData.annual_revenue,
                    enterpriseData.certification,
                    enterpriseData.credit_rating,
                    enterpriseData.description
                ]);

                // 添加标签
                if (tags && tags.length > 0) {
                    for (const tagName of tags) {
                        let tag = await db.get('SELECT id FROM tags WHERE name = ?', [tagName]);

                        if (!tag) {
                            const tagResult = await db.run('INSERT INTO tags (name) VALUES (?)', [tagName]);
                            tag = { id: tagResult.id };
                        }

                        await db.run(
                            'INSERT INTO enterprise_tags (enterprise_id, tag_id) VALUES (?, ?)',
                            [result.id, tag.id]
                        );
                    }
                }

                count++;
                console.log(`✓ 已添加: ${enterpriseData.name}`);
            } catch (err) {
                console.error(`✗ 添加失败: ${enterpriseData.name}`, err.message);
            }
        }

        console.log(`\n数据初始化完成！`);
        console.log(`- 已添加 ${industries.length} 个行业分类`);
        console.log(`- 已添加 ${count} 家企业`);
        console.log(`- 数据库文件: ${require('path').join(__dirname, '../database/enterprise_filter.db')}`);

    } catch (error) {
        console.error('数据初始化失败:', error);
    } finally {
        await db.close();
    }
}

// 执行数据填充
seedData();
