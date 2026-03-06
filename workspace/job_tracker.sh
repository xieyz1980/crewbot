#!/bin/bash
# 每日职位筛选脚本
# 运行时间: 每天早8点
# 功能: 搜索AI架构师、CTO、解决方案架构师相关职位，保存到日期文件

set -e

# 配置
DATE=$(date +%Y-%m-%d)
JOB_DIR="/workspace/projects/jobs"
RETENTION_DAYS=7

# 创建职位目录
mkdir -p "$JOB_DIR/AI架构师"
mkdir -p "$JOB_DIR/CTO"
mkdir -p "$JOB_DIR/解决方案架构师"

echo "=========================================="
echo "职位筛选任务 - $DATE"
echo "=========================================="

# 搜索函数
search_jobs() {
    local position=$1
    local keywords=$2
    local output_file="$JOB_DIR/$position/${DATE}.md"
    
    echo "# ${position}职位筛选 - ${DATE}" > "$output_file"
    echo "" >> "$output_file"
    echo "**筛选时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$output_file"
    echo "" >> "$output_file"
    echo "**关键词**: $keywords" >> "$output_file"
    echo "" >> "$output_file"
    echo "---" >> "$output_file"
    echo "" >> "$output_file"
    
    # 这里可以集成实际的职位搜索API
    # 例如: LinkedIn API、BOSS直聘API、猎聘API等
    
    echo "## 待搜索职位来源" >> "$output_file"
    echo "" >> "$output_file"
    echo "### LinkedIn" >> "$output_file"
    echo "- [ ] AI Architect职位" >> "$output_file"
    echo "- [ ] CTO职位" >> "$output_file"
    echo "- [ ] Solutions Architect职位" >> "$output_file"
    echo "" >> "$output_file"
    
    echo "### BOSS直聘" >> "$output_file"
    echo "- [ ] AI架构师" >> "$output_file"
    echo "- [ ] 技术总监/CTO" >> "$output_file"
    echo "- [ ] 解决方案架构师" >> "$output_file"
    echo "" >> "$output_file"
    
    echo "### 猎聘" >> "$output_file"
    echo "- [ ] AI架构师" >> "$output_file"
    echo "- [ ] CTO" >> "$output_file"
    echo "- [ ] 解决方案架构师" >> "$output_file"
    echo "" >> "$output_file"
    
    echo "---" >> "$output_file"
    echo "" >> "$output_file"
    echo "## 今日行动计划" >> "$output_file"
    echo "" >> "$output_file"
    echo "1. [ ] 浏览各平台新增职位" >> "$output_file"
    echo "2. [ ] 筛选匹配度高的职位" >> "$output_file"
    echo "3. [ ] 准备定制化简历投递" >> "$output_file"
    echo "4. [ ] 跟进已投递职位进度" >> "$output_file"
    
    echo "✅ $position 职位文件已创建: $output_file"
}

# 搜索三个职位
search_jobs "AI架构师" "AI架构师, 大模型架构, LLM, RAG, AI Agent"
search_jobs "CTO" "CTO, 技术总监, VP of Engineering, 首席技术官"
search_jobs "解决方案架构师" "解决方案架构师, 售前架构师, 技术顾问, Solution Architect"

# 清理7天前的旧文件
echo ""
echo "清理7天前的旧文件..."
find "$JOB_DIR" -name "*.md" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
echo "✅ 清理完成"

# 生成汇总报告
echo ""
echo "=========================================="
echo "今日职位筛选完成"
echo "=========================================="
echo "职位文件位置: $JOB_DIR"
echo "保留期限: $RETENTION_DAYS 天"
echo ""
ls -la "$JOB_DIR"/*/
