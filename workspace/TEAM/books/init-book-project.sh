#!/bin/bash
# 《智算基石》书籍项目初始化脚本
# 创建GitHub仓库并初始化项目结构

set -e

echo "=========================================="
echo "《智算基石》书籍项目初始化"
echo "=========================================="

# 配置
GITHUB_USER="xieyz1980"
REPO_NAME="books"
BOOK_DIR="智算基石"

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
        --description "技术书籍撰写项目 - 小煤球团队" \
        --add-readme
    echo "✅ 仓库创建成功"
fi

# 克隆仓库
echo ""
echo "克隆仓库到本地..."
cd /workspace/projects
if [ -d "${REPO_NAME}" ]; then
    echo "目录已存在，跳过克隆"
else
    git clone "https://xieyz1980:$(gh auth token)@github.com/${GITHUB_USER}/${REPO_NAME}.git"
    echo "✅ 克隆完成"
fi

# 创建书籍目录结构
echo ""
echo "创建《${BOOK_DIR}》目录结构..."
cd "${REPO_NAME}"
mkdir -p "${BOOK_DIR}"/chapters
mkdir -p "${BOOK_DIR}"/images/{diagrams,photos,charts}
mkdir -p "${BOOK_DIR}"/references/{papers,articles,books}
mkdir -p "${BOOK_DIR}"/drafts
mkdir -p "${BOOK_DIR}"/reviews
mkdir -p "${BOOK_DIR}"/publish/{manuscript,figures,metadata}

# 复制已有的文件
echo ""
echo "复制项目文件..."
cp -r /workspace/projects/workspace/TEAM/books/智算基石/* "${BOOK_DIR}"/ 2>/dev/null || true

# 创建.gitignore
cat > "${BOOK_DIR}/.gitignore" << 'EOF'
# 编译输出
*.pdf
*.epub
*.mobi

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
cat > "${BOOK_DIR}/README.md" << EOF
# 智算基石

**副标题**: AI时代的基础设施革命  
**作者**: 谢友泽  
**项目周期**: 2026-03-05 至 2026-03-20 (15天)  
**目标字数**: 15万字

---

## 📖 项目简介

本书是一本面向企业CTO、CIO、AI从业者及AI专业学生的技术专著，结合作者20年从业经验，深入剖析AI时代基础设施面临的全新挑战与应对策略。

## 📅 项目进度

**当前状态**: 🔄 进行中  
**完成章节**: 前言  
**总进度**: 5%

## 📁 目录结构

\`\`\`
智算基石/
├── README.md           # 项目说明
├── outline.md          # 完整大纲
├── schedule.md         # 写作计划
├── chapters/           # 章节文件
├── images/             # 图片资源
├── references/         # 参考资料
├── drafts/             # 草稿箱
├── reviews/            # 审校意见
└── publish/            # 出版文件
\`\`\`

## 👥 团队

- **作者**: 谢友泽
- **编辑**: 王编辑
- **技术审校**: James
- **插图设计**: Dora
- **文档**: Jason
- **项目管理**: 小煤球

## 📜 版权

© 2026 谢友泽. All rights reserved.

未经作者书面许可，不得以任何形式复制或传播本书内容。
EOF

# 提交到GitHub
echo ""
echo "提交到GitHub..."
cd "${BOOK_DIR}"
git config user.email "45018045@qq.com"
git config user.name "xieyz1980"

git add .
git commit -m "📚 init: 《智算基石》书籍项目初始化

- 创建完整目录结构
- 添加项目文档和大纲
- 创建前言初稿
- 建立写作计划

项目周期: 2026-03-05 至 2026-03-20 (15天)" 2>/dev/null || echo "无新文件提交"

git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "推送失败，请手动推送"

echo ""
echo "=========================================="
echo "《智算基石》项目初始化完成!"
echo "=========================================="
echo ""
echo "📁 本地路径: /workspace/projects/${REPO_NAME}/${BOOK_DIR}"
echo "🔗 GitHub地址: https://github.com/${GITHUB_USER}/${REPO_NAME}/tree/main/${BOOK_DIR}"
echo ""
echo "📋 下一步:"
echo "  1. 谢友泽开始Day 1写作 (前言+第1章)"
echo "  2. Dora准备插图设计"
echo "  3. Jason准备排版模板"
echo "  4. 18:00提交第一章初稿"
echo ""
echo "📅 项目周期: 2026-03-05 至 2026-03-20 (15天)"
echo "🎯 目标: 15万字出版质量技术专著"
