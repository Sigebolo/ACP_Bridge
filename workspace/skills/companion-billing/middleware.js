/**
 * 权限检查和使用量跟踪中间件
 * 集成到 OpenClaw 系统中，自动检查用户权限
 */

const CompanionBillingSkill = require('./index');

class BillingMiddleware {
    constructor() {
        this.billingSkill = new CompanionBillingSkill();
        this.initialized = false;
    }

    /**
     * 初始化中间件
     */
    async init() {
        if (!this.initialized) {
            await this.billingSkill.init();
            this.initialized = true;
        }
    }

    /**
     * 消息发送前权限检查
     */
    async beforeMessage(context) {
        await this.init();
        
        const userId = context.user_id;
        const result = await this.billingSkill.checkPermission(userId, 'message');
        
        if (!result.allowed) {
            throw new Error(`🚫 ${result.reason}\n💡 ${result.upgrade_suggestion}\n\n使用 /bill 查看详细状态`);
        }
        
        return {
            allowed: true,
            usage_remaining: result.usage_remaining
        };
    }

    /**
     * 语音发送前权限检查
     */
    async beforeVoice(context) {
        await this.init();
        
        const userId = context.user_id;
        const result = await this.billingSkill.checkPermission(userId, 'voice');
        
        if (!result.allowed) {
            throw new Error(`🚫 ${result.reason}\n💡 ${result.upgrade_suggestion}\n\n使用 /bill 查看详细状态`);
        }
        
        return {
            allowed: true,
            usage_remaining: result.usage_remaining
        };
    }

    /**
     * 照片发送前权限检查
     */
    async beforePhoto(context) {
        await this.init();
        
        const userId = context.user_id;
        const result = await this.billingSkill.checkPermission(userId, 'photo');
        
        if (!result.allowed) {
            throw new Error(`🚫 ${result.reason}\n💡 ${result.upgrade_suggestion}\n\n使用 /bill 查看详细状态`);
        }
        
        return {
            allowed: true,
            usage_remaining: result.usage_remaining
        };
    }

    /**
     * 伴侣创建前权限检查
     */
    async beforeCompanionCreate(context) {
        await this.init();
        
        const userId = context.user_id;
        const result = await this.billingSkill.checkPermission(userId, 'companion');
        
        if (!result.allowed) {
            throw new Error(`🚫 ${result.reason}\n💡 ${result.upgrade_suggestion}\n\n使用 /bill 查看详细状态`);
        }
        
        return {
            allowed: true,
            usage_remaining: result.usage_remaining
        };
    }

    /**
     * 获取用户当前状态（用于显示）
     */
    async getUserStatus(userId) {
        await this.init();
        
        try {
            return await this.billingSkill.getUserBillingStatus(userId);
        } catch (error) {
            console.error(`Failed to get user status for ${userId}:`, error);
            return null;
        }
    }

    /**
     * 格式化使用状态信息
     */
    formatUsageStatus(billingStatus) {
        if (!billingStatus) return '状态获取失败';
        
        const { subscription, balance, usage, limits } = billingStatus;
        const tierNames = {
            free: '免费版',
            heartbeat: 'Heartbeat 💝',
            true_love: 'True Love 💕'
        };
        
        let status = `📊 *当前状态*\n\n`;
        status += `🎯 订阅: ${tierNames[subscription.tier] || '免费版'}\n`;
        status += `💰 金币: ${balance}\n\n`;
        status += `📱 今日使用:\n`;
        
        status += `• 消息: ${usage.daily_messages}/${limits.daily_messages === -1 ? '∞' : limits.daily_messages}\n`;
        status += `• 语音: ${usage.daily_voice}/${limits.daily_voice === -1 ? '∞' : limits.daily_voice}\n`;
        status += `• 照片: ${usage.daily_photos}/${limits.daily_photos === -1 ? '∞' : limits.daily_photos}\n`;
        status += `• 伴侣: ${usage.companions_count}/${limits.max_companions}\n`;
        
        return status;
    }

    /**
     * 检查是否需要升级提示
     */
    shouldPromptUpgrade(billingStatus) {
        if (!billingStatus) return false;
        
        const { usage, limits } = billingStatus;
        
        // 如果任何使用量达到80%以上，提示升级
        const messageUsage = limits.daily_messages === -1 ? 0 : usage.daily_messages / limits.daily_messages;
        const voiceUsage = limits.daily_voice === -1 ? 0 : usage.daily_voice / limits.daily_voice;
        const photoUsage = limits.daily_photos === -1 ? 0 : usage.daily_photos / limits.daily_photos;
        const companionUsage = usage.companions_count / limits.max_companions;
        
        const maxUsage = Math.max(messageUsage, voiceUsage, photoUsage, companionUsage);
        
        return maxUsage >= 0.8 && billingStatus.subscription.tier !== 'true_love';
    }

    /**
     * 生成升级提示
     */
    generateUpgradePrompt(billingStatus) {
        if (!billingStatus) return '';
        
        const currentTier = billingStatus.subscription.tier;
        
        if (currentTier === 'free') {
            return '💡 *升级建议*\n\n您的使用量接近限制，升级到 **Heartbeat** 档位可享受：\n• 无限消息\n• 每日10条语音\n• 每日3张照片\n• 最多3个伴侣\n\n使用 /subscribe 查看详情';
        } else if (currentTier === 'heartbeat') {
            return '💡 *升级建议*\n\n升级到 **True Love** 档位可享受：\n• 无限语音和照片\n• 最多10个伴侣\n• 深度记忆解锁\n• 专属礼物反应\n\n使用 /subscribe 查看详情';
        }
        
        return '';
    }

    /**
     * 处理权限错误的统一响应
     */
    async handlePermissionError(error, context) {
        const userId = context.user_id;
        const billingStatus = await this.getUserStatus(userId);
        
        let response = error.message;
        
        if (billingStatus) {
            response += '\n\n' + this.formatUsageStatus(billingStatus);
            
            if (this.shouldPromptUpgrade(billingStatus)) {
                response += '\n\n' + this.generateUpgradePrompt(billingStatus);
            }
        }
        
        return response;
    }

    /**
     * 创建使用量统计报告
     */
    async generateUsageReport(userId, period = 'daily') {
        await this.init();
        
        const billingStatus = await this.getUserStatus(userId);
        if (!billingStatus) {
            return '无法生成使用报告';
        }
        
        const { usage, limits, subscription } = billingStatus;
        
        let report = `📈 *使用报告*\n\n`;
        report += `📊 订阅档位: ${subscription.tier.toUpperCase()}\n`;
        report += `📅 统计周期: ${period === 'daily' ? '今日' : '本周'}\n\n`;
        
        report += `💬 消息使用: ${usage.daily_messages}/${limits.daily_messages === -1 ? '∞' : limits.daily_messages}\n`;
        report += `🎤 语音使用: ${usage.daily_voice}/${limits.daily_voice === -1 ? '∞' : limits.daily_voice}\n`;
        report += `📷 照片使用: ${usage.daily_photos}/${limits.daily_photos === -1 ? '∞' : limits.daily_photos}\n`;
        report += `👥 伴侣数量: ${usage.companions_count}/${limits.max_companions}\n`;
        
        // 计算使用率
        if (limits.daily_messages !== -1) {
            const messageRate = (usage.daily_messages / limits.daily_messages * 100).toFixed(1);
            report += `\n📊 消息使用率: ${messageRate}%`;
        }
        
        return report;
    }
}

module.exports = BillingMiddleware;
