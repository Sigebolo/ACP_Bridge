/**
 * Companion Billing Skill - 主入口
 * 提供订阅管理、支付处理和权限控制功能
 */

const BillingManager = require('./billing-manager');
const PaymentProcessor = require('./payment-processor');
const TelegramCommands = require('./telegram-commands');

class CompanionBillingSkill {
    constructor() {
        this.billingManager = new BillingManager();
        this.paymentProcessor = new PaymentProcessor(this.billingManager);
        this.telegramCommands = new TelegramCommands(this.billingManager, this.paymentProcessor);
    }

    /**
     * 技能初始化
     */
    async init() {
        try {
            await this.billingManager.init();
            console.log('Companion Billing Skill initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Companion Billing Skill:', error);
            throw error;
        }
    }

    /**
     * 权限检查中间件
     * 在用户执行受限操作前调用
     */
    async checkPermission(userId, action, context = {}) {
        try {
            const canProceed = await this.billingManager.checkLimits(userId, action);
            
            if (!canProceed) {
                const billing = await this.billingManager.getUserBilling(userId);
                const tier = billing.subscription.tier;
                const limits = this.billingManager.getTierLimits(tier);
                
                return {
                    allowed: false,
                    reason: this.getLimitExceededMessage(action, tier, limits),
                    upgrade_suggestion: this.getUpgradeSuggestion(action, tier)
                };
            }

            // 记录使用量
            await this.billingManager.recordUsage(userId, action);
            
            return {
                allowed: true,
                usage_remaining: await this.getUsageRemaining(userId, action)
            };
        } catch (error) {
            console.error(`Permission check failed for user ${userId}, action ${action}:`, error);
            return {
                allowed: false,
                reason: '权限检查失败，请稍后重试'
            };
        }
    }

    /**
     * 获取使用量剩余
     */
    async getUsageRemaining(userId, action) {
        const billing = await this.billingManager.getUserBilling(userId);
        const limits = this.billingManager.getTierLimits(billing.subscription.tier);
        const usage = billing.usage;

        switch (action) {
            case 'message':
                return limits.daily_messages === -1 ? '无限' : Math.max(0, limits.daily_messages - usage.daily_messages);
            case 'voice':
                return limits.daily_voice === -1 ? '无限' : Math.max(0, limits.daily_voice - usage.daily_voice);
            case 'photo':
                return limits.daily_photos === -1 ? '无限' : Math.max(0, limits.daily_photos - usage.daily_photos);
            case 'companion':
                return Math.max(0, limits.max_companions - usage.companions_count);
            default:
                return 0;
        }
    }

    /**
     * 获取限制超出的提示信息
     */
    getLimitExceededMessage(action, tier, limits) {
        const messages = {
            message: `今日消息次数已达上限 (${limits.daily_messages} 条)`,
            voice: `今日语音次数已达上限 (${limits.daily_voice} 条)`,
            photo: `今日照片次数已达上限 (${limits.daily_photos} 张)`,
            companion: `伴侣数量已达上限 (${limits.max_companions} 个)`
        };

        return messages[action] || '使用限制已达上限';
    }

    /**
     * 获取升级建议
     */
    getUpgradeSuggestion(action, currentTier) {
        const suggestions = {
            free: {
                message: '升级到 Heartbeat 档位享受无限消息',
                voice: '升级到 Heartbeat 档位解锁语音功能',
                photo: '升级到 Heartbeat 档位解锁照片功能',
                companion: '升级到 Heartbeat 档位可创建更多伴侣'
            },
            heartbeat: {
                companion: '升级到 True Love 档位可创建最多10个伴侣'
            }
        };

        return suggestions[currentTier]?.[action] || '升级订阅档位以获得更多功能';
    }

    /**
     * 处理 Telegram 命令
     */
    async handleTelegramCommand(command, userId, chatId, bot) {
        try {
            switch (command) {
                case '/bill':
                    await this.telegramCommands.handleBillCommand(userId, chatId, bot);
                    break;
                case '/topup':
                    await this.telegramCommands.handleTopupCommand(userId, chatId, bot);
                    break;
                case '/subscribe':
                    await this.telegramCommands.handleSubscribeCommand(userId, chatId, bot);
                    break;
                default:
                    await bot.sendMessage(chatId, '❌ 未知命令。可用命令: /bill, /topup, /subscribe');
            }
        } catch (error) {
            console.error(`Failed to handle Telegram command ${command}:`, error);
            await bot.sendMessage(chatId, '❌ 命令执行失败，请稍后重试。');
        }
    }

    /**
     * 处理 Telegram 回调查询
     */
    async handleTelegramCallback(userId, chatId, bot, callbackData) {
        try {
            await this.telegramCommands.handleCallbackQuery(userId, chatId, bot, callbackData);
        } catch (error) {
            console.error(`Failed to handle Telegram callback ${callbackData}:`, error);
            await bot.sendMessage(chatId, '❌ 操作失败，请稍后重试。');
        }
    }

    /**
     * 处理支付
     */
    async processPayment(userId, paymentMethod, paymentData) {
        try {
            return await this.paymentProcessor.processSubscriptionPayment(userId, paymentMethod, paymentData);
        } catch (error) {
            console.error(`Payment processing failed for user ${userId}:`, error);
            throw error;
        }
    }

    /**
     * 购买礼物
     */
    async purchaseGift(userId, giftId, companionId) {
        try {
            return await this.billingManager.purchaseGift(userId, giftId, companionId);
        } catch (error) {
            console.error(`Gift purchase failed for user ${userId}, gift ${giftId}:`, error);
            throw error;
        }
    }

    /**
     * 获取用户账单状态
     */
    async getUserBillingStatus(userId) {
        try {
            const billing = await this.billingManager.getUserBilling(userId);
            const balance = await this.billingManager.getBalance(userId);
            const subscription = await this.billingManager.checkSubscription(userId);
            
            return {
                subscription,
                balance,
                usage: billing.usage,
                limits: this.billingManager.getTierLimits(subscription.tier)
            };
        } catch (error) {
            console.error(`Failed to get billing status for user ${userId}:`, error);
            throw error;
        }
    }

    /**
     * 获取支付选项
     */
    getPaymentOptions() {
        return this.paymentProcessor.getPaymentOptions();
    }

    /**
     * 获取礼物目录
     */
    async getGiftCatalog() {
        try {
            return await this.billingManager.getGiftCatalog();
        } catch (error) {
            console.error('Failed to get gift catalog:', error);
            return { gifts: [] };
        }
    }

    /**
     * 管理员功能：确认手动支付
     */
    async confirmManualPayment(paymentId, confirmedBy) {
        try {
            return await this.paymentProcessor.confirmManualPayment(paymentId, confirmedBy);
        } catch (error) {
            console.error(`Failed to confirm manual payment ${paymentId}:`, error);
            throw error;
        }
    }

    /**
     * 管理员功能：获取待确认支付
     */
    async getPendingPayments() {
        try {
            return await this.paymentProcessor.getAllPendingPayments();
        } catch (error) {
            console.error('Failed to get pending payments:', error);
            return [];
        }
    }

    /**
     * 定时任务：清理过期支付
     */
    async cleanupExpiredPayments() {
        try {
            const cleanedCount = await this.paymentProcessor.cleanupExpiredPayments();
            if (cleanedCount > 0) {
                console.log(`Cleaned up ${cleanedCount} expired payments`);
            }
        } catch (error) {
            console.error('Failed to cleanup expired payments:', error);
        }
    }

    /**
     * 定时任务：检查订阅到期
     */
    async checkSubscriptionExpiry() {
        // 这里可以实现订阅到期检查逻辑
        // 比如发送续费提醒、自动降级到免费版等
        console.log('Checking subscription expiry...');
    }
}

module.exports = CompanionBillingSkill;
