const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 数据库文件路径
const DB_PATH = path.join(__dirname, '../database/doubao_generator.db');

console.log('🔍 检查数据库状态...\n');

// 检查数据库文件是否存在
if (!fs.existsSync(DB_PATH)) {
    console.log('⚠️  数据库不存在，开始自动初始化...\n');
    console.log('=' .repeat(50));

    try {
        // 执行数据填充脚本
        console.log('📦 正在初始化示例数据...\n');
        execSync('node scripts/seed-data.js', { stdio: 'inherit' });

        console.log('\n' + '='.repeat(50));
        console.log('✅ 数据库初始化完成！');
        console.log('=' .repeat(50) + '\n');
    } catch (error) {
        console.error('❌ 初始化失败:', error.message);
        console.log('💡 您可以稍后手动运行: npm run seed\n');
    }
} else {
    console.log('✅ 数据库已存在，跳过初始化\n');

    // 检查数据库大小
    const stats = fs.statSync(DB_PATH);
    const fileSizeInBytes = stats.size;
    const fileSizeInKB = (fileSizeInBytes / 1024).toFixed(2);

    console.log(`📊 数据库大小: ${fileSizeInKB} KB`);
    console.log('💡 如需重置数据，请删除数据库文件后运行: npm run seed\n');
}

console.log('🚀 准备启动服务器...\n');
