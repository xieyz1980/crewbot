#!/bin/bash
# 团队GitHub仓库初始化脚本
# 创建团队所需的GitHub仓库结构

set -e

echo "=========================================="
echo "初始化团队GitHub仓库"
echo "=========================================="

# 配置
GITHUB_USER="xieyz1980"
TEAM_REPOS=(
    "team-management:团队管理与日报系统"
    "ai-commit-assistant:AI Commit Assistant项目"
    "resumes:简历定制与求职管理系统"
    "ai-infra-materials:AI架构学习资料库"
    "books:技术书籍撰写项目"
    "tech-docs:技术文档与知识库"
    "dev-tools:开发工具与脚本集合"
)

echo ""
echo "检查GitHub认证状态..."
gh auth status || {
    echo "❌ GitHub未认证，请先运行: gh auth login"
    exit 1
}

echo ""
echo "将创建以下仓库:"
for repo_info in "${TEAM_REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    echo "  - $repo_name: $repo_desc"
done

echo ""
read -p "确认创建这些仓库? (y/n): " confirm

if [[ $confirm != "y" ]]; then
    echo "已取消"
    exit 0
fi

# 创建仓库
for repo_info in "${TEAM_REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    echo ""
    echo "创建仓库: $repo_name"
    
    # 检查仓库是否已存在
    if gh repo view "${GITHUB_USER}/${repo_name}" &>/dev/null; then
        echo "  ⚠️ 仓库已存在，跳过"
        continue
    fi
    
    # 创建仓库
    gh repo create "${repo_name}" \
        --public \
        --description "${repo_desc} - 小煤球团队" \
        --add-readme 2>&1 || {
        echo "  ❌ 创建失败: $repo_name"
        continue
    }
    
    echo "  ✅ 创建成功: https://github.com/${GITHUB_USER}/${repo_name}"
    
    # 等待一下避免API限流
    sleep 2
done

echo ""
echo "=========================================="
echo "仓库创建完成!"
echo "=========================================="
echo ""
echo "仓库列表:"
for repo_info in "${TEAM_REPOS[@]}"; do
    IFS=':' read -r repo_name repo_desc <<< "$repo_info"
    echo "  • https://github.com/${GITHUB_USER}/${repo_name}"
done

echo ""
echo "下一步:"
echo "1. 克隆仓库到本地"
echo "2. 初始化项目结构"
echo "3. 分配给团队成员"
