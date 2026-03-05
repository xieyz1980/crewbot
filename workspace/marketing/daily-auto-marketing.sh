#!/bin/bash
# 每日内容营销自动化脚本
# 每天早上9:00自动运行，生成当日所有推广内容

set -e

DATE=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%u)

echo "=========================================="
echo "每日内容营销自动化 - ${DATE}"
echo "=========================================="

# 配置
BOOKS_REPO="/workspace/projects/books"
LINKEDIN_REPO="/workspace/projects/linkedin-content"
MARKETING_REPO="/workspace/projects/workspace/marketing"

mkdir -p ${MARKETING_REPO}/{daily,weekly,zhihu,v2ex,analytics}

# 根据星期确定内容主题
case $DAY_OF_WEEK in
    1) 
        THEME="技术趋势"
        TOPIC="AI基础设施最新趋势分析"
        ;;
    2) 
        THEME="实战经验"
        TOPIC="项目复盘与踩坑记录"
        ;;
    3) 
        THEME="技术教程"
        TOPIC="架构设计指南与最佳实践"
        ;;
    4) 
        THEME="深度观点"
        TOPIC="行业思考与技术预测"
        ;;
    5) 
        THEME="成长分享"
        TOPIC="职业发展与技术学习"
        ;;
    6) 
        THEME="书籍进展"
        TOPIC="《智算基石》写作进度"
        ;;
    7) 
        THEME="互动问答"
        TOPIC="读者问答与话题讨论"
        ;;
esac

echo ""
echo "📅 今日主题: ${THEME}"
echo "📝 内容方向: ${TOPIC}"

# ==================== LinkedIn内容 ====================
echo ""
echo "📝 生成LinkedIn内容..."

LINKEDIN_FILE="${LINKEDIN_REPO}/posts/$(date +%Y-%m)/linkedin-post-${DATE}.md"
mkdir -p "$(dirname $LINKEDIN_FILE)"

cat > "$LINKEDIN_FILE" << EOF
# LinkedIn文章 - ${DATE}

**日期**: ${DATE}  
**主题**: ${THEME}  
**类型**: ${TOPIC}  
**状态**: ✅ 待发布

---

## 标题
[待填写 - 基于${THEME}主题]

## 正文

### 中文版本

[内容待生成 - 基于今日主题: ${TOPIC}]

### English Version

[Content to be generated based on today's theme]

## 标签建议
#AIInfrastructure #CloudComputing #MLOps #TechLeadership

## 配图建议
[根据内容类型推荐配图]

## 发布时间
建议: 12:00 (中午午休时间)

## CTA (行动号召)
- 引导评论
- 邀请私信交流
- 推荐阅读书籍

---

## 发布后任务
- [ ] 发布后2小时内回复所有评论
- [ ] 点赞5-10个相关行业动态
- [ ] 私信回复咨询意向

*自动生成时间: $(date '+%H:%M:%S')*
EOF

echo "✅ LinkedIn内容已生成: $LINKEDIN_FILE"

# ==================== 知乎专栏 ====================
echo ""
echo "📝 生成知乎专栏内容..."

ZHIHU_FILE="${MARKETING_REPO}/zhihu/zhihu-post-${DATE}.md"

cat > "$ZHIHU_FILE" << EOF
# 知乎专栏文章 - ${DATE}

**日期**: ${DATE}  
**主题**: ${THEME}  
**状态**: ✅ 待发布

---

## 文章标题
[待填写]

## 开篇钩子
吸引读者继续阅读的3-5句话

## 正文结构
1. 背景介绍
2. 问题分析
3. 解决方案
4. 实际案例
5. 总结建议

## 关键要点
- 要点1
- 要点2
- 要点3

## 结尾引导
- 关注作者
- 推荐阅读《智算基石》
- 邀请私信咨询

## 标签
AI基础设施、云计算、架构设计、企业数字化转型

---

*自动生成时间: $(date '+%H:%M:%S')*
EOF

echo "✅ 知乎内容已生成: $ZHIHU_FILE"

# ==================== V2EX分享 ====================
echo ""
echo "📝 生成V2EX分享..."

V2EX_FILE="${MARKETING_REPO}/v2ex/v2ex-post-${DATE}.md"

cat > "$V2EX_FILE" << EOF
# V2EX技术分享 - ${DATE}

**日期**: ${DATE}  
**节点**: [选择合适节点: 推广/云计算/程序员/书籍]

---

## 标题
[简洁有力的技术分享标题]

## 正文
适合V2EX社区风格的内容：
- 开门见山，少说废话
- 有干货，有深度
- 适当自黑，接地气

## 互动引导
- 抛出问题引发讨论
- 邀请分享类似经历

## 注意
- 不要硬广，要软植入
- 回复要及时、真诚

---

*自动生成时间: $(date '+%H:%M:%S')*
EOF

echo "✅ V2EX内容已生成: $V2EX_FILE"

# ==================== 每日工作清单 ====================
echo ""
echo "📋 生成每日工作清单..."

DAILY_FILE="${MARKETING_REPO}/daily/daily-tasks-${DATE}.md"

cat > "$DAILY_FILE" << EOF
# 每日推广工作清单 - ${DATE}

## 📅 今日主题: ${THEME}

---

## ⏰ 时间安排

### 09:00 - 内容准备完成 ✅
- [x] LinkedIn文章已生成
- [x] 知乎文章已生成
- [x] V2EX分享已生成

### 12:00 - LinkedIn发布
- [ ] 复制LinkedIn文章
- [ ] 发布到LinkedIn
- [ ] 截图保存发布链接

### 14:00 - 知乎发布
- [ ] 复制知乎文章
- [ ] 发布到知乎专栏
- [ ] 回答3个相关问题

### 18:00 - 互动回复
- [ ] 回复LinkedIn评论
- [ ] 回复知乎评论
- [ ] 私信回复咨询

### 20:00 - 社区参与
- [ ] V2EX发布分享
- [ ] 浏览5个技术话题
- [ ] 点赞+评论3条优质内容

---

## 📊 今日内容

### LinkedIn
- 文件: \`posts/$(date +%Y-%m)/linkedin-post-${DATE}.md\`
- 主题: ${TOPIC}
- 状态: 待发布

### 知乎
- 文件: \`zhihu/zhihu-post-${DATE}.md\`
- 主题: ${TOPIC}
- 状态: 待发布

### V2EX
- 文件: \`v2ex/v2ex-post-${DATE}.md\`
- 主题: 技术分享
- 状态: 待发布

---

## 📈 数据追踪

### LinkedIn
- 发布前关注数: [记录]
- 发布后关注数: [记录]
- 阅读量: [记录]
- 互动量: [记录]
- 新增咨询: [记录]

### 知乎
- 发布前关注数: [记录]
- 阅读量: [记录]
- 赞同数: [记录]
- 收藏数: [记录]

---

## 💡 今日亮点

[记录今天的重要进展或反馈]

---

*生成时间: $(date '+%H:%M:%S')*
EOF

echo "✅ 每日工作清单已生成: $DAILY_FILE"

# ==================== 提交到GitHub ====================
echo ""
echo "📤 提交到GitHub..."

cd ${MARKETING_REPO}
git add . 2>/dev/null || true
git commit -m "📅 daily: ${DATE}营销内容自动生成

- LinkedIn文章: ${THEME}
- 知乎专栏: ${TOPIC}
- V2EX分享: 技术分享
- 每日工作清单

自动生成时间: $(date '+%H:%M:%S')" 2>/dev/null || true

echo "✅ 本地提交完成"

# ==================== 汇总报告 ====================
echo ""
echo "=========================================="
echo "✅ 每日内容营销自动化完成!"
echo "=========================================="
echo ""
echo "📅 日期: ${DATE}"
echo "📝 主题: ${THEME}"
echo ""
echo "📁 生成文件:"
echo "  1. LinkedIn: ${LINKEDIN_FILE}"
echo "  2. 知乎: ${ZHIHU_FILE}"
echo "  3. V2EX: ${V2EX_FILE}"
echo "  4. 工作清单: ${DAILY_FILE}"
echo ""
echo "⏰ 下一步 (需要你手动完成):"
echo "  12:00 - 发布LinkedIn文章"
echo "  14:00 - 发布知乎文章"
echo "  18:00 - 回复评论互动"
echo "  20:00 - V2EX技术分享"
echo ""
