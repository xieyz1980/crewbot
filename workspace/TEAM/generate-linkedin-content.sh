#!/bin/bash
# LinkedIn内容每日生成脚本
# 每天自动生成LinkedIn文章

set -e

DATE=$(date +%Y-%m-%d)
WEEKDAY=$(date +%u)  # 1=周一, 7=周日
CONTENT_DIR="/workspace/projects/workspace/TEAM/linkedin-content"
POSTS_DIR="$CONTENT_DIR/posts"

echo "=========================================="
echo "LinkedIn内容生成 - $DATE"
echo "=========================================="

mkdir -p "$POSTS_DIR"

# 根据星期确定内容类型
case $WEEKDAY in
    1) TYPE="技术洞察"; THEME="行业趋势分析" ;;
    2) TYPE="实战经验"; THEME="项目复盘/案例" ;;
    3) TYPE="技术教程"; THEME="架构设计指南" ;;
    4) TYPE="行业观点"; THEME="深度思考文章" ;;
    5) TYPE="经验分享"; THEME="职场/成长" ;;
    6) TYPE="个人品牌"; THEME="《智算基石》进展" ;;
    7) TYPE="互动内容"; THEME="提问/投票/话题" ;;
esac

POST_FILE="$POSTS_DIR/linkedin-post-${DATE}.md"

cat > "$POST_FILE" << EOF
# LinkedIn文章 - ${DATE}

**日期**: ${DATE}  
**类型**: ${TYPE}  
**主题**: ${THEME}  
**状态**: 🔄 待撰写

---

## 文章标题
[待填写]

## 核心观点
[3-5个要点]

## 正文内容
[中文+英文双语版本]

## 配图建议
[描述需要的配图]

## CTA (行动号召)
[引导评论/私信/关注]

## 标签
\#AIInfrastructure \#CloudComputing \#MLEngineering

---

## 发布计划
- **撰写时间**: 09:00-11:00
- **审核时间**: 11:00-12:00 (谢友泽)
- **发布时间**: [根据类型选择时间]
- **互动时间**: 发布后2小时内回复评论

---

*模板生成时间: $(date '+%H:%M:%S')*
EOF

echo "✅ 文章模板已创建: $POST_FILE"
echo ""
echo "📋 今日内容计划:"
echo "  类型: $TYPE"
echo "  主题: $THEME"
echo ""
echo "📝 下一步:"
echo "  1. 9:00开始撰写内容"
echo "  2. 11:00前完成初稿"
echo "  3. 12:00前谢友泽审核"
echo "  4. 按计划时间发布"
