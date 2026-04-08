# Companion Billing Skill

## 技能描述
管理心跳回忆平台的订阅、支付和虚拟货币系统。处理用户权限验证、订阅档位管理、虚拟礼物商店和支付集成。

## 核心功能

### 1. 订阅档位管理
- **Free (免费版)**: 限制每日消息数、仅限 1 个伴侣
- **Heartbeat ($9.9/mo)**: 3 个伴侣、无限消息、每日 10 条语音、3 张照片
- **True Love ($24.9/mo)**: 10 个伴侣、无限语音/照片、深度记忆解锁

### 2. 虚拟货币系统
- Coins 充值和管理
- 虚拟礼物购买
- 伴侣反应触发

### 3. 支付集成
- MVP: 手动确认模式
- 进阶: Stripe/支付宝/微信支付

## API 端点

### 权限检查
- `check_subscription(user_id)` - 检查用户订阅等级
- `check_limits(user_id, action)` - 检查使用限制
- `can_create_companion(user_id)` - 检查是否可创建新伴侣

### 订阅管理
- `get_subscription_status(user_id)` - 获取订阅状态
- `upgrade_subscription(user_id, tier)` - 升级订阅
- `cancel_subscription(user_id)` - 取消订阅

### 虚拟货币
- `get_balance(user_id)` - 获取余额
- `add_coins(user_id, amount)` - 添加金币
- `spend_coins(user_id, amount, reason)` - 消费金币

### 礼物商店
- `get_gift_catalog()` - 获取礼物目录
- `purchase_gift(user_id, gift_id, companion_id)` - 购买礼物

## 数据结构

### 用户账单信息 (credentials/user_billing.json)
```json
{
  "user_id": {
    "subscription": {
      "tier": "free|heartbeat|true_love",
      "status": "active|cancelled|expired",
      "expires_at": "2026-03-25T00:00:00Z",
      "auto_renew": true
    },
    "balance": {
      "coins": 100,
      "last_updated": "2026-02-25T17:00:00Z"
    },
    "usage": {
      "daily_messages": 15,
      "daily_voice": 3,
      "daily_photos": 1,
      "companions_count": 1,
      "last_reset": "2026-02-25T00:00:00Z"
    },
    "payment_history": []
  }
}
```

### 礼物目录
```json
{
  "gifts": [
    {
      "id": "rose",
      "name": "玫瑰",
      "price": 10,
      "category": "romantic",
      "reaction_template": "收到玫瑰时，伴侣会..."
    }
  ]
}
```

## 使用限制规则

### Free 用户
- 每日最多 20 条消息
- 仅能创建 1 个伴侣
- 无语音和照片功能

### Heartbeat 用户  
- 无限消息
- 最多 3 个伴侣
- 每日 10 条语音，3 张照片

### True Love 用户
- 无限消息、语音、照片
- 最多 10 个伴侣
- 深度记忆功能解锁

## Telegram 命令集成

### `/bill` - 查看账单状态
显示当前订阅等级、余额、使用情况

### `/topup` - 充值金币
显示充值选项和支付方式

### `/subscribe` - 订阅管理
显示订阅选项和升级链接

## 技能触发条件

1. **权限检查**: 当用户执行受限操作时自动检查
2. **命令响应**: 响应 Telegram 账单相关命令
3. **Webhook**: 处理支付回调（Stripe 等）
4. **定时任务**: 每日重置使用限制，检查订阅到期

## 错误处理

- 权限不足时给出升级引导
- 支付失败时提供重试选项
- 订阅到期时提醒续费
- 余额不足时推荐充值方案

## 集成要求

- 与 companion-memory 技能集成，记录购买历史
- 与 companion-archetypes 技能集成，限制伴侣创建数量
- 与 Web Canvas 集成，提供充值/订阅界面
- 与 Telegram Bot 集成，提供命令行查询
