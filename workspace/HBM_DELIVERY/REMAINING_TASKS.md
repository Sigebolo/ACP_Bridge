# HBM-2026 剩余开发任务清单

**生成时间**: 2026-02-25 17:50 (NZDT)  
**PM**: Atom  
**项目**: 心跳回忆 2.0

---

## 📊 任务状态总览

| Phase | 任务 | 状态 | 负责人 |
|-------|------|------|--------|
| Phase 1 | HBM-001: Archetype 模板 x8 | ✅ 完成 | Antigravity |
| Phase 1 | HBM-002: companion-memory skill | ✅ 完成 | Antigravity |
| Phase 1 | HBM-003: Telegram /create 命令 | ✅ 完成 | Antigravity |
| Phase 1 | HBM-004: Cron 主动交互 | ✅ 完成 | Antigravity |
| Phase 1 | HBM-005: Web Canvas UI | ✅ 完成 | Windsurf |
| Phase 2 | HBM-006: 支付与订阅系统 | ✅ 完成 | Windsurf |
| Phase 2 | HBM-007: companion-voice skill | 🔴 待开始 | Antigravity |
| Phase 2 | HBM-008: agent-selfie 增强 | 🔴 待开始 | Windsurf |
| Phase 2 | HBM-009: companion-gifts skill | 🔴 待开始 | Antigravity |
| Phase 2 | HBM-010: 男性 Archetype 模板 | 🔴 待开始 | Antigravity |
| Phase 3 | HBM-011: Web 管理界面优化 | 🔴 待开始 | Windsurf |
| Phase 3 | HBM-012: 多伴侣路由优化 | 🔴 待开始 | Antigravity |
| Phase 3 | HBM-013: Beta 测试 (100用户) | 🔴 待开始 | Windsurf |
| Phase 4 | HBM-014: 社区分享功能 | 🔴 待开始 | Windsurf |
| Phase 5 | HBM-015: Live2D 头像集成 | 🔴 待开始 | Antigravity |
| Phase 5 | HBM-016: TTS 唇形同步 | 🔴 待开始 | Antigravity |
| Phase 5 | HBM-017: WebRTC 视频通话 | 🔴 待开始 | Windsurf |
| Phase 6 | HBM-018: 记忆小游戏 | 🔴 待开始 | Antigravity |
| Phase 6 | HBM-019: 故事冒险游戏 | 🔴 待开始 | Antigravity |
| Phase 6 | HBM-020: Telegram Mini App | 🔴 待开始 | Windsurf |

---

## 🔴 立即待开始的任务 (优先级排序)

### 第一批 (本周内启动)

#### HBM-006-HOTFIX: 支付系统 Bug 修复
**优先级**: 🔴 CRITICAL  
**负责人**: Windsurf  
**预估时间**: 1-2 小时  
**问题**: 使用量跟踪测试失败 (88.9% 通过率)

**具体修复项**:
1. 修复 `trackUsage()` 方法中的每日消息计数逻辑
2. 确保使用量在每日重置时正确清零
3. 补充缺失的使用量初始化逻辑
4. 重新运行测试确保 100% 通过

**交付物**: 更新后的 `billing-manager.js` + 测试通过截图

---

#### HBM-007: companion-voice skill 开发
**优先级**: 🟠 HIGH  
**负责人**: Antigravity  
**预估时间**: 3-4 天  
**截止**: 2026-03-05

**功能需求**:
- 集成 Qwen TTS (阿里云百炼) 作为主方案
- ElevenLabs 作为备选方案
- 8 个 Archetype 对应的独特音色
- 语音消息生成和缓存机制
- Telegram 语音消息发送集成

**交付物**:
- `skills/companion-voice/` 完整实现
- `SKILL.md` 文档
- 音色配置文件 `voice-profiles.json`
- 测试套件 `tests/voice-test.js`

**验收标准**:
- 每个 Archetype 能生成对应音色的语音
- 语音质量 > 80% 满意度
- 响应时间 < 3 秒

---

#### HBM-008: agent-selfie 增强集成
**优先级**: 🟠 HIGH  
**负责人**: Windsurf  
**预估时间**: 2-3 天  
**截止**: 2026-03-05

**功能需求**:
- 集成现有 `agent-selfie` skill 到伴侣系统
- 支持时段光线自适应 (早/午/晚/夜)
- 情绪状态驱动的表情生成
- 相册自动管理和展示
- Web Canvas 相册页面集成

**交付物**:
- 更新的 `companion-selfie` wrapper skill
- 相册管理 API
- Web Canvas 相册组件
- 测试套件

**验收标准**:
- 伴侣能根据时间生成不同光线的照片
- 相册能正确展示和管理照片
- Web Canvas 相册页面可正常浏览

---

### 第二批 (下周启动)

#### HBM-009: companion-gifts skill 完善
**优先级**: 🟠 HIGH  
**负责人**: Antigravity  
**预估时间**: 2-3 天  
**截止**: 2026-03-08

**功能需求**:
- 完善礼物目录 (当前 5 种，扩展到 15 种)
- 伴侣独特反应机制 (基于 Archetype)
- 礼物赠送历史记录
- 特殊节日礼物推荐
- 与支付系统的完整集成

**交付物**:
- 更新的 `companion-gifts` skill
- 扩展的 `gift-catalog.json`
- 反应模板库
- 测试套件

---

#### HBM-010: 男性 Archetype 模板 x4
**优先级**: 🟠 HIGH  
**负责人**: Antigravity  
**预估时间**: 2-3 天  
**截止**: 2026-03-08

**需要创建的 Archetype**:
1. **Gentleman** (绅士型) - 温文尔雅、体贴周到
2. **Rebel** (叛逆型) - 不羁、自由、有主见
3. **Scholar** (学者型) - 知识渊博、理性思考
4. **Protector** (守护者型) - 可靠、坚定、有责任感

**交付物**:
- 4 个 `{archetype}.md` system.md 模板
- 对应的 `voice-profiles.json` 音色配置
- 对应的 `selfie-prompts.json` 照片生成提示
- 测试验证报告

---

### 第三批 (两周后启动)

#### HBM-011: Web Canvas 管理界面优化
**优先级**: 🟡 MEDIUM  
**负责人**: Windsurf  
**预估时间**: 3-4 天  
**截止**: 2026-03-12

**优化项**:
- 响应式设计 (移动端适配)
- 性能优化 (图片懒加载、虚拟滚动)
- 深色模式支持
- 无障碍访问 (WCAG 2.1 AA)
- 国际化支持 (i18n)

---

#### HBM-012: 多伴侣路由优化
**优先级**: 🟡 MEDIUM  
**负责人**: Antigravity  
**预估时间**: 2-3 天  
**截止**: 2026-03-12

**优化项**:
- OpenClaw Agent 路由性能优化
- 并发伴侣交互处理
- 内存使用优化
- 响应时间基准测试

---

## 📋 任务分配指令

### 给 Antigravity 的任务
1. **立即**: HBM-007 (companion-voice skill)
2. **立即**: HBM-009 (companion-gifts 完善)
3. **立即**: HBM-010 (男性 Archetype x4)
4. **下周**: HBM-012 (多伴侣路由优化)
5. **后续**: HBM-015, HBM-016, HBM-018, HBM-019

### 给 Windsurf 的任务
1. **立即**: HBM-006-HOTFIX (支付系统 Bug 修复)
2. **立即**: HBM-008 (agent-selfie 增强)
3. **下周**: HBM-011 (Web Canvas 优化)
4. **后续**: HBM-013, HBM-014, HBM-017, HBM-020

---

## 🎯 下一步行动

1. **Windsurf**: 立即修复 HBM-006 的使用量跟踪 Bug，目标 100% 测试通过
2. **Antigravity**: 启动 HBM-007 (companion-voice skill) 开发
3. **Atom (PM)**: 每 30 分钟监控进度，通过 Bridge 同步状态

---

**生成者**: Atom (PM)  
**下发时间**: 2026-02-25 17:50 (NZDT)  
**预期完成**: Phase 2 全部任务在 2026-03-15 前完成
