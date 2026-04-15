# Worktree Standard

## Worktree使用原则

### 为什么要用Worktree
- **隔离开发环境**: 每个任务独立环境，避免互相干扰
- **并行开发**: 支持多Agent同时工作不冲突
- **安全实验**: 实验性功能不影响主分支稳定性
- **快速切换**: 无需stash即可在不同任务间切换

### Worktree命名规范

#### 格式: `agent/{task-id}/{agent-name}`
- `agent/`: 固定前缀，表示Agent开发专用
- `{task-id}`: 任务编号，如`TASK-001`
- `{agent-name}`: Agent名称，如`windsurf`, `claude`, `gemini`

#### 示例
```
agent/TASK-001/windsurf     # Windsurf执行TASK-001
agent/TASK-002/claude       # Claude执行TASK-002  
agent/TASK-003/gemini       # Gemini执行TASK-003
agent/HOTFIX-001/windsurf   # Windsurf紧急修复
```

#### 特殊类型Worktree
- `agent/REVIEW-xxx/{agent}`: 代码审查专用
- `agent/REFACTOR-xxx/{agent}`: 重构任务专用
- `agent/EXPERIMENT-xxx/{agent}`: 实验性功能
- `agent/RELEASE-xxx/{agent}`: 发布准备

## Worktree创建流程

### 1. 检查前置条件
```bash
# 确保在main分支且工作区干净
git checkout main
git status  # 应该显示working tree clean

# 检查是否已存在同名worktree
git worktree list
```

### 2. 创建Worktree
```bash
# 标准任务worktree
git worktree add agent/TASK-001/windsurf -b feature/TASK-001-windsurf

# 紧急修复worktree
git worktree add agent/HOTFIX-001/claude -b hotfix/HOTFIX-001-claude

# 实验性worktree
git worktree add agent/EXPERIMENT-005/gemini -b experiment/EXPERIMENT-005-gemini
```

### 3. 配置Worktree环境
```bash
cd agent/TASK-001/windsurf

# 设置Agent特定的配置
git config user.name "Windsurf Agent"
git config user.email "windsurf@agent.local"

# 创建任务目录结构
mkdir -p docs/09-PLANNING/TASKS/TASK-001
```

### 4. 记录Worktree信息
在`docs/09-PLANNING/worktree-tracker.md`中记录：
```markdown
## Active Worktrees

| Worktree | Agent | Task | Branch | Created | Status |
|----------|-------|------|--------|---------|--------|
| agent/TASK-001/windsurf | Windsurf | TASK-001 | feature/TASK-001-windsurf | 2026-04-15 | In Progress |
| agent/TASK-002/claude | Claude | TASK-002 | feature/TASK-002-claude | 2026-04-15 | In Progress |
```

## Worktree使用规范

### 日常工作流程
1. **进入Worktree**: `cd agent/TASK-001/windsurf`
2. **同步主分支**: `git fetch origin && git rebase origin/main`
3. **开发工作**: 按任务计划执行开发
4. **定期提交**: 有意义的commit，遵循commit规范
5. **推送分支**: `git push -u origin feature/TASK-001-windsurf`
6. **状态同步**: 通过ACP同步进度给其他Agent

### Commit规范
```bash
# 格式: <type>(<scope>): <description>
feat(adapter): add claude code message validation
fix(protocol): resolve websocket connection timeout
test(e2e): add multi-agent integration tests
docs(walkthrough): standardize walkthrough template
```

### 分支保护规则
- **main分支**: 禁止直接push，必须通过PR
- **feature分支**: 需要至少1个审查才能merge
- **hotfix分支**: 需要P2级别Agent审查
- **experiment分支**: 可以独立开发，不影响main

## Worktree协作规范

### 多Agent并行规则
1. **资源隔离**: 每个Agent独立worktree
2. **通信协调**: 通过ACP Server协调共享资源修改
3. **冲突解决**: 高优先级Agent优先，低优先级Agentrebase
4. **状态同步**: 每30分钟通过ACP同步工作状态

### 共享资源修改流程
1. **检查占用**: 通过ACP检查资源是否被其他Agent占用
2. **申请锁**: 通过ACP申请资源修改锁
3. **执行修改**: 在获得锁后修改共享资源
4. **释放锁**: 修改完成后立即释放锁
5. **通知更新**: 通过ACP通知相关Agent资源已更新

### Agent优先级规则
- **P1 (Windsurf)**: 主要执行Agent，最高优先级
- **P2 (Claude, Gemini)**: 审查和规划Agent，中等优先级  
- **P3 (Antigravity, OpenClaw)**: 研究和自动化Agent，低优先级

## Worktree清理流程

### 任务完成后清理
1. **确认完成**: 确保任务完全完成，所有测试通过
2. **合并代码**: 通过PR合并到main分支
3. **更新文档**: 更新相关文档和SSoT
4. **写Walkthrough**: 完成walkthrough文档
5. **删除分支**: 删除远程和本地分支
6. **删除Worktree**: 删除worktree目录

### 清理命令
```bash
# 1. 合并完成后删除远程分支
git push origin --delete feature/TASK-001-windsurf

# 2. 删除本地分支
git branch -d feature/TASK-001-windsurf

# 3. 删除worktree
cd ../..
git worktree remove agent/TASK-001/windsurf

# 4. 更新worktree tracker
# 更新docs/09-PLANNING/worktree-tracker.md
```

### 紧急清理
如果Agent异常退出，需要强制清理：
```bash
# 查看所有worktree
git worktree list

# 强制删除损坏的worktree
git worktree prune

# 手动删除目录
rm -rf agent/TASK-001/windsurf
```

## Worktree监控和维护

### 定期检查
```bash
# 每日检查脚本
#!/bin/bash
# daily-worktree-check.sh

echo "=== Worktree Health Check ==="
echo "Active worktrees:"
git worktree list

echo -e "\n\nStale branches (no activity for 7+ days):"
git for-each-ref --sort=committerdate --format='%(refname:short) %(committerdate:short)' refs/heads/ | awk '$2 < "'$(date -d '7 days ago' +%Y-%m-%d)'" {print $1}'

echo -e "\n\nUnmerged worktrees:"
find agent/ -name ".git" -type f | while read gitfile; do
    worktree_dir=$(dirname "$gitfile")
    branch=$(git --git-dir="$gitfile" rev-parse --abbrev-ref HEAD)
    echo "$worktree_dir -> $branch"
done
```

### 自动化清理
```bash
# 自动清理超过14天的已完成worktree
find agent/ -maxdepth 3 -type d -mtime +14 -exec rm -rf {} \;
```

## Worktree最佳实践

### 命名最佳实践
- 使用清晰的任务ID和Agent名称
- 避免特殊字符和空格
- 保持命名一致性
- 包含任务类型信息

### 安全最佳实践
- 不要在worktree中存储敏感信息
- 定期备份重要的worktree
- 使用.gitignore保护临时文件
- 及时清理已完成的worktree

### 性能优化
- 限制同时活跃的worktree数量（建议<10个）
- 定期清理无用的worktree
- 使用本地分支减少网络开销
- 优化.gitignore减少索引大小

## 故障排除

### 常见问题
1. **Worktree损坏**: 使用`git worktree prune`清理
2. **分支冲突**: 使用rebase解决冲突
3. **权限问题**: 检查文件系统权限
4. **磁盘空间**: 定期清理大文件

### 恢复流程
```bash
# 如果worktree目录被误删
git worktree add agent/TASK-001/windsurf feature/TASK-001-windsurf

# 如果分支被误删但worktree还在
cd agent/TASK-001/windsurf
git checkout -b feature/TASK-001-windsurf
```

## Worktree模板和脚本

### 创建worktree脚本模板
```bash
#!/bin/bash
# create-worktree.sh
WORKTREE_PATH="agent/$1/$2"
BRANCH_NAME="feature/$1-$2"

echo "Creating worktree: $WORKTREE_PATH"
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

cd "$WORKTREE_PATH"
git config user.name "$2 Agent"
git config user.email "$2@agent.local"

echo "Worktree $WORKTREE_PATH created successfully"
```

### 批量清理脚本
```bash
#!/bin/bash
# cleanup-completed-worktrees.sh

for worktree in $(find agent/ -maxdepth 2 -type d); do
    if [ -f "$worktree/.git" ]; then
        branch=$(git --git-dir="$worktree/.git" rev-parse --abbrev-ref HEAD)
        # 检查分支是否已合并
        if git merge-base --is-ancestor origin/main "$branch" 2>/dev/null; then
            echo "Cleaning up completed worktree: $worktree"
            git worktree remove "$worktree"
        fi
    fi
done
```
