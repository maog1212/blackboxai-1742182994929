-- 企业筛选资源体系数据库结构
-- Enterprise Filter System Database Schema

-- 企业信息表
CREATE TABLE IF NOT EXISTS enterprises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,                    -- 企业名称
    code TEXT UNIQUE,                      -- 企业代码/统一社会信用代码
    industry TEXT NOT NULL,                -- 所属行业
    scale TEXT NOT NULL,                   -- 企业规模（小型/中型/大型）
    region TEXT NOT NULL,                  -- 所在地区
    city TEXT,                             -- 所在城市
    registered_capital REAL,               -- 注册资本（万元）
    established_date TEXT,                 -- 成立日期
    legal_person TEXT,                     -- 法人代表
    business_scope TEXT,                   -- 经营范围
    contact_person TEXT,                   -- 联系人
    contact_phone TEXT,                    -- 联系电话
    contact_email TEXT,                    -- 联系邮箱
    address TEXT,                          -- 详细地址
    website TEXT,                          -- 官方网站
    employee_count INTEGER,                -- 员工数量
    annual_revenue REAL,                   -- 年营收（万元）
    certification TEXT,                    -- 资质认证（ISO9001,ISO14001等）
    credit_rating TEXT,                    -- 信用评级（AAA/AA/A/B/C）
    status TEXT DEFAULT 'active',          -- 状态（active/inactive/suspended）
    description TEXT,                      -- 企业描述
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 行业分类表
CREATE TABLE IF NOT EXISTS industries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,             -- 行业名称
    parent_id INTEGER,                     -- 父级行业ID
    code TEXT,                             -- 行业代码
    description TEXT,                      -- 行业描述
    FOREIGN KEY (parent_id) REFERENCES industries(id)
);

-- 标签表
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,             -- 标签名称
    category TEXT,                         -- 标签分类
    description TEXT,                      -- 标签描述
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 企业标签关联表
CREATE TABLE IF NOT EXISTS enterprise_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE(enterprise_id, tag_id)
);

-- 企业资源表
CREATE TABLE IF NOT EXISTS enterprise_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enterprise_id INTEGER NOT NULL,
    resource_type TEXT NOT NULL,           -- 资源类型（技术/人才/设备/专利等）
    resource_name TEXT NOT NULL,           -- 资源名称
    resource_description TEXT,             -- 资源描述
    quantity INTEGER,                      -- 数量
    unit TEXT,                             -- 单位
    status TEXT DEFAULT 'available',       -- 状态
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE
);

-- 筛选历史表
CREATE TABLE IF NOT EXISTS filter_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filter_criteria TEXT NOT NULL,         -- 筛选条件（JSON格式）
    result_count INTEGER,                  -- 结果数量
    user_ip TEXT,                          -- 用户IP
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_enterprises_industry ON enterprises(industry);
CREATE INDEX IF NOT EXISTS idx_enterprises_region ON enterprises(region);
CREATE INDEX IF NOT EXISTS idx_enterprises_scale ON enterprises(scale);
CREATE INDEX IF NOT EXISTS idx_enterprises_status ON enterprises(status);
CREATE INDEX IF NOT EXISTS idx_enterprises_credit_rating ON enterprises(credit_rating);
CREATE INDEX IF NOT EXISTS idx_enterprise_tags_enterprise_id ON enterprise_tags(enterprise_id);
CREATE INDEX IF NOT EXISTS idx_enterprise_tags_tag_id ON enterprise_tags(tag_id);
CREATE INDEX IF NOT EXISTS idx_enterprise_resources_enterprise_id ON enterprise_resources(enterprise_id);
CREATE INDEX IF NOT EXISTS idx_enterprise_resources_type ON enterprise_resources(resource_type);
