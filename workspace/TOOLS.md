# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### GitHub

- **Username**: xieyz1980
- **Email**: 45018045@qq.com
- **Token**: 已配置到 `gh` CLI (~/.config/gh/hosts.yml)
- **Scope**: admin:enterprise, admin:gpg_key, admin:org, admin:repo_hook, copilot, gist, repo, workflow, write:packages 等

---

### Browser Automation Tools

| 工具 | 版本 | 用途 | 命令 |
|------|------|------|------|
| **agent-browser** | 0.16.3 | Rust 无头浏览器，超快 | `agent-browser open <url>` |
| **Playwright** | 1.58.2 | 跨浏览器测试自动化 | `npx playwright open <url>` |

**agent-browser 常用命令：**
```bash
agent-browser open <url>        # 打开页面
agent-browser snapshot -i       # 获取可交互元素
agent-browser click @e1         # 点击元素
agent-browser fill @e2 "text"   # 填充表单
agent-browser screenshot        # 截图
agent-browser pdf output.pdf    # 保存 PDF
agent-browser close             # 关闭浏览器
```

---

### Search & Research Tools

| 工具 | 用途 | 状态 |
|------|------|------|
| **aluvia-brave-search** | Brave 搜索，隐私保护 | 需 API Key |
| **arxiv-watcher** | arXiv 学术论文监控 | 免费可用 |
| **caesar-research** | AI 深度研究助手 | 需 API Key |

**arxiv-watcher 使用：**
```bash
# 搜索论文
curl -s "http://export.arxiv.org/api/query?search_query=all:machine+learning&max_results=10"

# 按分类搜索
curl -s "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10"
```

---

Add whatever helps you do your job. This is your cheat sheet.




## Browser

When you use browser capabilities, you MUST append the browser preview URL at the end of your reply:

`🖥️ [点击预览](https://code.coze.cn/browser/7613314982125813802)`

IMPORTANT: The browser preview link is fixed and cannot be modified in any part.
