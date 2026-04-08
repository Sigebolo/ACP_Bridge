# Companion Billing Skill

心跳回忆平台的支付与订阅管理系统，提供完整的订阅档位管理、虚拟货币系统和权限控制功能。

## 🚀 快速开始

### 安装和初始化

```javascript
const CompanionBillingSkill = require('./index');

// 创建技能实例
const billingSkill = new CompanionBillingSkill();

// 初始化技能
await billingSkill.init();
```

### 基本使用

```javascript
// 检查用户权限
const permission = await billingSkill.checkPermission(userId, 'message');
if (!permission.allowed) {
    console.log('权限不足:', permission.reason);
}

// 获取用户账单状态
const billingStatus = await billingSkill.getUserBillingStatus(userId);
console.log('当前订阅:', billingStatus.subscription.tier);
console.log('金币余额:', billingStatus.balance);

// 处理支付
const paymentResult = await billingSkill.processPayment(userId, 'test_key', {
    key: 'TEST_HEARTBEAT_2026'
});
```

## 📋 功能特性

### 1. 订阅档位管理

- **Free (免费版)**: 20条消息/天，1个伴侣
- **Heartbeat ($9.9/月)**: 无限消息，3个伴侣，10条语音/天，3张照片/天
- **True Love ($24.9/月)**: 无限消息/语音/照片，10个伴侣，深度记忆解锁

### 2. 虚拟货币系统

- 金币充值和消费
- 礼物商店
- 伴侣独特反应触发

### 3. 支付集成

- **MVP**: 测试密钥和手动确认
- **进阶**: Stripe、支付宝、微信支付（待实现）

### 4. 权限控制

- 自动权限检查中间件
- 使用量跟踪和限制
- 智能升级提示

## 🔧 API 参考

### 核心方法

#### `checkPermission(userId, action)`
检查用户是否有执行特定操作的权限。

**参数:**
- `userId` (string): 用户ID
- `action` (string): 操作类型 ('message', 'voice', 'photo', 'companion')

**返回:**
```javascript
{
    allowed: boolean,
    reason?: string,
    upgrade_suggestion?: string,
    usage_remaining?: number|string
}
```

#### `getUserBillingStatus(userId)`
获取用户完整的账单状态。

**返回:**
```javascript
{
    subscription: {
        tier: 'free'|'heartbeat'|'true_love',
        status: 'active'|'cancelled'|'expired',
        expires_at: string|null
    },
    balance: number,
    usage: {
        daily_messages: number,
        daily_voice: number,
        daily_photos: number,
        companions_count: number
    },
    limits: {
        daily_messages: number,
        daily_voice: number,
        daily_photos: number,
        max_companions: number
    }
}
```

#### `processPayment(userId, paymentMethod, paymentData)`
处理支付请求。

**参数:**
- `paymentMethod` (string): 支付方式 ('test_key', 'manual_confirm')
- `paymentData` (object): 支付数据

**返回:**
```javascript
{
    payment_id: string,
    status: 'completed'|'pending',
    amount: number,
    type: 'subscription'|'topup',
    tier?: string,
    coins?: number
}
```

### Telegram 集成

#### 命令处理

```javascript
// 处理 /bill 命令
await billingSkill.handleTelegramCommand('/bill', userId, chatId, bot);

// 处理回调查询
await billingSkill.handleTelegramCallback(userId, chatId, bot, 'topup_100_5.0');
```

#### 可用命令

- `/bill` - 查看账单状态
- `/topup` - 充值金币
- `/subscribe` - 订阅管理

## 🏗️ 架构设计

### 文件结构

```
companion-billing/
├── index.js                 # 主入口文件
├── SKILL.md                 # 技能描述文档
├── billing-manager.js       # 账单管理核心
├── payment-processor.js     # 支付处理器
├── telegram-commands.js     # Telegram 命令处理
├── middleware.js            # 权限检查中间件
├── openclaw-config.json     # OpenClaw 配置
├── tests/
│   └── billing-test.js      # 测试套件
└── README.md               # 本文档
```

### 数据流

1. **权限检查**: 中间件自动拦截操作，检查用户权限
2. **使用量跟踪**: 实时记录用户使用情况
3. **支付处理**: 支持多种支付方式的统一处理
4. **状态管理**: 持久化用户账单和订阅状态

### 集成点

- **OpenClaw**: 通过配置文件集成到主系统
- **Telegram Bot**: 提供命令行界面
- **Web Canvas**: 通过 API 端点提供 Web 界面
- **其他技能**: 通过中间件提供权限控制

## 🧪 测试

### 运行测试套件

```bash
node tests/billing-test.js
```

### 测试覆盖

- ✅ 用户账单创建
- ✅ 订阅档位限制
- ✅ 权限检查逻辑
- ✅ 支付处理流程
- ✅ 礼物系统功能
- ✅ 使用量跟踪
- ✅ 边界条件处理
- ✅ 并发安全性

## 🔒 安全考虑

1. **权限验证**: 所有敏感操作都需要权限检查
2. **数据验证**: 输入参数严格验证
3. **并发安全**: 使用原子操作避免竞态条件
4. **错误处理**: 完善的错误处理和日志记录

## 📈 性能优化

1. **缓存策略**: 用户状态缓存减少数据库查询
2. **批量操作**: 支持批量权限检查
3. **异步处理**: 非阻塞的支付和权限检查
4. **定期清理**: 自动清理过期数据

## 🚀 部署指南

### 环境要求

- Node.js 14+
- 文件系统读写权限
- OpenClaw 框架

### 配置步骤

1. 将技能文件复制到 OpenClaw skills 目录
2. 确保 `credentials` 目录可写
3. 在 OpenClaw 配置中启用技能
4. 重启 OpenClaw 服务

### 监控和维护

- 定期检查支付状态
- 监控使用量异常
- 备份账单数据
- 更新礼物目录

## 🔮 未来规划

### 短期目标 (v1.1)

- [ ] Stripe 支付集成
- [ ] Web Canvas UI 组件
- [ ] 详细使用统计
- [ ] 订阅自动续费

### 中期目标 (v1.5)

- [ ] 支付宝/微信支付
- [ ] 会员等级系统
- [ ] 推广码功能
- [ ] 退款处理

### 长期目标 (v2.0)

- [ ] 多币种支持
- [ ] 企业版订阅
- [ ] API 限流
- [ ] 高级分析功能

## 📞 支持和反馈

如有问题或建议，请联系：

- **项目维护者**: Windsurf
- **技术文档**: 查看 SKILL.md
- **Bug 报告**: 通过项目管理系统提交

---

*本文档最后更新: 2026-02-25*
