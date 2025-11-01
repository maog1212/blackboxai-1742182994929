-- 豆包识别自动生成系统数据库结构
-- Doubao AI Recognition and Generation System Database Schema

-- 识别任务表
CREATE TABLE IF NOT EXISTS recognition_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,              -- 任务名称
    task_type TEXT NOT NULL,              -- 任务类型（文本识别/图片识别/语音识别）
    input_content TEXT,                   -- 输入内容
    input_file_path TEXT,                 -- 输入文件路径
    recognition_result TEXT,              -- 识别结果（JSON格式）
    confidence_score REAL,                -- 置信度分数
    status TEXT DEFAULT 'pending',        -- 状态（pending/processing/completed/failed）
    error_message TEXT,                   -- 错误信息
    processing_time INTEGER,              -- 处理时间（毫秒）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 内容生成任务表
CREATE TABLE IF NOT EXISTS generation_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recognition_task_id INTEGER,          -- 关联的识别任务ID
    task_name TEXT NOT NULL,              -- 任务名称
    template_id INTEGER,                  -- 使用的模板ID
    generation_type TEXT NOT NULL,        -- 生成类型（文章/摘要/标题/描述等）
    prompt TEXT,                          -- 生成提示词
    generated_content TEXT,               -- 生成的内容
    quality_score REAL,                   -- 质量评分
    word_count INTEGER,                   -- 字数统计
    status TEXT DEFAULT 'pending',        -- 状态
    error_message TEXT,                   -- 错误信息
    processing_time INTEGER,              -- 处理时间
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recognition_task_id) REFERENCES recognition_tasks(id) ON DELETE SET NULL,
    FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE SET NULL
);

-- 生成模板表
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT NOT NULL UNIQUE,   -- 模板名称
    template_type TEXT NOT NULL,          -- 模板类型
    description TEXT,                     -- 模板描述
    prompt_template TEXT NOT NULL,        -- 提示词模板
    example_output TEXT,                  -- 示例输出
    parameters TEXT,                      -- 参数配置（JSON格式）
    is_active INTEGER DEFAULT 1,          -- 是否启用
    usage_count INTEGER DEFAULT 0,        -- 使用次数
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 识别类别表
CREATE TABLE IF NOT EXISTS recognition_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,   -- 类别名称
    category_type TEXT NOT NULL,          -- 类别类型
    confidence_threshold REAL DEFAULT 0.7,-- 置信度阈值
    description TEXT,                     -- 描述
    keywords TEXT,                        -- 关键词（JSON数组）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任务标签表
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT NOT NULL UNIQUE,        -- 标签名称
    tag_type TEXT,                        -- 标签类型
    color TEXT,                           -- 标签颜色
    description TEXT,                     -- 标签描述
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任务标签关联表（识别任务）
CREATE TABLE IF NOT EXISTS task_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    task_type TEXT NOT NULL,              -- 任务类型（recognition/generation）
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE(task_id, tag_id, task_type)
);

-- 系统配置表
CREATE TABLE IF NOT EXISTS system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key TEXT NOT NULL UNIQUE,      -- 配置键
    config_value TEXT,                    -- 配置值
    config_type TEXT,                     -- 配置类型（string/number/boolean/json）
    description TEXT,                     -- 描述
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 统计数据表
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_date DATE NOT NULL,              -- 统计日期
    total_recognition_tasks INTEGER DEFAULT 0,
    total_generation_tasks INTEGER DEFAULT 0,
    successful_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    average_processing_time REAL DEFAULT 0,
    total_words_generated INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stat_date)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_recognition_status ON recognition_tasks(status);
CREATE INDEX IF NOT EXISTS idx_recognition_type ON recognition_tasks(task_type);
CREATE INDEX IF NOT EXISTS idx_recognition_created ON recognition_tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_generation_status ON generation_tasks(status);
CREATE INDEX IF NOT EXISTS idx_generation_type ON generation_tasks(generation_type);
CREATE INDEX IF NOT EXISTS idx_generation_created ON generation_tasks(created_at);
CREATE INDEX IF NOT EXISTS idx_templates_type ON templates(template_type);
CREATE INDEX IF NOT EXISTS idx_templates_active ON templates(is_active);
CREATE INDEX IF NOT EXISTS idx_task_tags_task ON task_tags(task_id, task_type);
CREATE INDEX IF NOT EXISTS idx_task_tags_tag ON task_tags(tag_id);
