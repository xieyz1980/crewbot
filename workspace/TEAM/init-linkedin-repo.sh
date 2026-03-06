#!/bin/bash
# LinkedIn内容管理仓库初始化脚本
# 存储每日LinkedIn文章、策略、数据分析

set -e

echo "=========================================="
echo "LinkedIn内容仓库初始化"
echo "=========================================="

# 配置
GITHUB_USER="xieyz1980"
REPO_NAME="linkedin-content"

echo ""
echo "检查GitHub认证..."
gh auth status || {
    echo "❌ GitHub未认证"
    exit 1
}

# 检查仓库是否存在
echo ""
echo "检查仓库 ${GITHUB_USER}/${REPO_NAME}..."
if gh repo view "${GITHUB_USER}/${REPO_NAME}" &>/dev/null; then
    echo "✅ 仓库已存在"
else
    echo "创建仓库 ${REPO_NAME}..."
    gh repo create "${REPO_NAME}" \
        --public \
        --description "LinkedIn个人品牌建设 - 内容管理仓库" \
        --add-readme
    echo "✅ 仓库创建成功"
fi

# 克隆仓库
echo ""
echo "克隆仓库到本地..."
cd /workspace/projects
if [ -d "${REPO_NAME}" ]; then
    echo "目录已存在，跳过克隆"
    cd "${REPO_NAME}"
    git pull origin main 2>/dev/null || git pull origin master 2>/dev/null || true
else
    git clone "https://xieyz1980:$(gh auth token)@github.com/${GITHUB_USER}/${REPO_NAME}.git"
    cd "${REPO_NAME}"
    echo "✅ 克隆完成"
fi

# 创建目录结构
echo ""
echo "创建目录结构..."
mkdir -p posts/{2026-03,2026-04,2026-05}
mkdir -p templates
mkdir -p strategy
mkdir -p analytics/{monthly,weekly}
mkdir -p assets/{images,photos}
mkdir -p scripts

# 复制已有内容
echo ""
echo "复制已有内容..."
if [ -d "/workspace/projects/workspace/TEAM/linkedin-content" ]; then
    cp -r /workspace/projects/workspace/TEAM/linkedin-content/* ./ 2>/dev/null || true
fi

# 复制策略文档
if [ -f "/workspace/projects/workspace/TEAM/linkedin-content-strategy.md" ]; then
    cp /workspace/projects/workspace/TEAM/linkedin-content-strategy.md ./strategy/
fi

if [ -f "/workspace/projects/workspace/TEAM/linkedin-profile-optimization.md" ]; then
    cp /workspace/projects/workspace/TEAM/linkedin-profile-optimization.md ./strategy/
fi

# 创建.gitignore
cat > .gitignore << 'EOF'
# 编译输出
*.pdf
*.epub

# 临时文件
*.tmp
*.temp
*.bak

# 编辑器文件
.vscode/
.idea/
*.swp
*.swo

# OS文件
.DS_Store
Thumbs.db

# 大型图片源文件
*.psd
*.ai
*.sketch
EOF

# 创建README
cat > README.md << 'EOF'
# LinkedIn个人品牌建设

**目标**: 打造AI架构领域专家形象，吸引企业咨询客户  
**平台**: LinkedIn (中文+英文双语)  
**更新频率**: 每日1-2篇  
**负责人**: 谢友泽 (内容审核) / 小煤球 (内容撰写)

---

## 🎯 品牌定位

**"企业AI转型顾问 | 20年基础设施专家 | 《智算基石》作者"**

### 核心价值主张
- 帮助CTO/CIO解决AI基础设施难题
- 实战经验来自VMware/Lenovo大厂
- 前瞻视野+落地能力兼备

---

## 📁 仓库结构

```
linkedin-content/
├── README.md                 # 本文件
├── posts/                    # 每日文章
│   ├── 2026-03/             # 按月归档
│   ├── 2026-04/
│   └── 2026-05/
├── templates/                # 文章模板
│   ├── tech-insight.md      # 技术洞察型
│   ├── case-study.md        # 实战经验型
│   ├── opinion.md           # 观点思考型
│   └── story.md             # 个人故事型
├── strategy/                 # 策略文档
│   ├── content-strategy.md  # 内容策略
│   └── profile-optimization.md  # 资料优化
├── analytics/                # 数据分析
│   ├── monthly/             # 月度报告
│   └── weekly/              # 周报
├── assets/                   # 素材资源
│   ├── images/              # 图片
│   └── photos/              # 照片
└── scripts/                  # 自动化脚本
    └── generate-post.sh     # 内容生成
```

---

## 📝 内容支柱

| 类型 | 占比 | 说明 |
|------|------|------|
| 技术洞察 | 40% | AI基础设施最新趋势、大厂方案解析 |
| 实战经验 | 30% | 项目复盘、踩坑记录、最佳实践 |
| 行业观点 | 20% | 深度思考、技术预测、职业建议 |
| 个人品牌 | 10% | 《智算基石》进展、个人故事 |

---

## 📅 发布日历

| 星期 | 主题 | 发布时间 |
|------|------|----------|
| 周一 | 技术洞察 | 08:30 |
| 周二 | 实战经验 | 12:00 |
| 周三 | 技术教程 | 08:30 |
| 周四 | 行业观点 | 18:00 |
| 周五 | 经验分享 | 12:00 |
| 周六 | 个人品牌 | 10:00 |
| 周日 | 互动内容 | 15:00 |

---

## 📊 成功指标

### 短期目标 (1个月)
- [ ] 发布30篇原创内容
- [ ] 获得500+新关注
- [ ] 单篇最高阅读量10,000+
- [ ] 获得10+咨询意向

### 中期目标 (3个月)
- [ ] 关注数达到2,000+
- [ ] 获得3个付费咨询客户
- [ ] 建立AI架构师社群
- [ ] 《智算基石》预售启动

### 长期目标 (1年)
- [ ] 成为LinkedIn AI架构领域KOL
- [ ] 咨询业务月收入¥50,000+
- [ ] 出版《智算基石》
- [ ] 建立个人品牌矩阵

---

## 🚀 每日工作流程

```
09:00  小煤球撰写LinkedIn文章
11:00  发送给谢友泽审核
12:00  谢友泽发布到LinkedIn
18:00  谢友泽回复评论互动
```

---

## 📈 数据追踪

每月统计：
- 浏览量 (Impressions)
- 互动量 (Engagement)
- 新增关注 (Followers)
- 咨询线索 (Leads)

---

**创建时间**: 2026-03-05  
**仓库地址**: https://github.com/xieyz1980/linkedin-content
EOF

# 创建内容模板
cat > templates/tech-insight.md << 'EOF'
# 模板：技术洞察型

## 标题格式
🔥 [热点事件/技术发布] 对AI基础设施意味着什么？

## 结构
1. 开篇引入热点事件
2. 3个关键分析点
3. 给CTO的具体建议
4. 引导互动的问题

## 标签
#AIInfrastructure #CloudComputing #[相关标签]

## CTA
评论区聊聊你的看法
EOF

cat > templates/case-study.md << 'EOF'
# 模板：实战经验型

## 标题格式
📚 实战复盘：我们是如何[达成某个结果]的

## 结构
1. 项目背景
2. 遇到的挑战
3. 解决方案步骤
4. 量化结果
5. 可复用的经验

## 标签
#MLEngineering #CaseStudy #[相关标签]

## CTA
你有类似经历吗？欢迎分享
EOF

cat > templates/opinion.md << 'EOF'
# 模板：观点思考型

## 标题格式
💭 [一个反直觉的观点/预测]

## 结构
1. 现象描述
2. 深度思考（3个观点）
3. 支撑论据
4. 开放讨论

## 标签
#ThoughtLeadership #AITransformation #[相关标签]

## CTA
你怎么看？评论区讨论
EOF

cat > templates/story.md << 'EOF'
# 模板：个人故事型

## 标题格式
🎯 20年技术路：[某个转折点/感悟]

## 结构
1. 时间+背景
2. 面临的困境/选择
3. 做出的决定
4. 收获/成长
5. 给年轻人的建议

## 标签
#CareerJourney #TechLeadership #Mentorship

## CTA
你的经历是什么？
EOF

# 提交到GitHub
echo ""
echo "提交到GitHub..."
git config user.email "45018045@qq.com"
git config user.name "xieyz1980"

git add .
git commit -m "🚀 init: LinkedIn内容仓库初始化

- 创建完整的目录结构
- 添加4种文章模板
- 上传已有内容策略文档
- 设置README和.gitignore

目标：打造AI架构领域LinkedIn专家形象" 2>/dev/null || echo "无新文件提交"

git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "推送失败，请手动推送"

echo ""
echo "=========================================="
echo "LinkedIn内容仓库初始化完成!"
echo "=========================================="
echo ""
echo "📁 本地路径: /workspace/projects/${REPO_NAME}"
echo "🔗 GitHub地址: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo ""
echo "📋 目录结构:"
echo "  posts/        - 每日LinkedIn文章"
echo "  templates/    - 文章模板"
echo "  strategy/     - 内容策略文档"
echo "  analytics/    - 数据分析报告"
echo "  assets/       - 图片素材"
echo "  scripts/      - 自动化脚本"
echo ""
echo "🚀 下一步:"
echo "  1. 每天9:00我撰写文章放到posts/目录"
echo "  2. 11:00发送给你审核"
echo "  3. 你发布到LinkedIn"
echo ""
