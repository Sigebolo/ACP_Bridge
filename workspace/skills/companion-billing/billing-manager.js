/**
 * 伴侣账单管理系统
 * 处理订阅、虚拟货币和权限控制
 */

const fs = require('fs').promises;
const path = require('path');

class BillingManager {
    constructor() {
        this.credentialsDir = path.join(process.cwd(), 'credentials');
        this.billingFile = path.join(this.credentialsDir, 'user_billing.json');
        this.giftCatalogFile = path.join(__dirname, 'gift-catalog.json');
    }

    /**
     * 初始化账单系统
     */
    async init() {
        try {
            await fs.mkdir(this.credentialsDir, { recursive: true });
            
            // 初始化账单文件
            const billingExists = await this.fileExists(this.billingFile);
            if (!billingExists) {
                await fs.writeFile(this.billingFile, JSON.stringify({}), 'utf8');
            }

            // 初始化礼物目录
            const catalogExists = await this.fileExists(this.giftCatalogFile);
            if (!catalogExists) {
                await this.initGiftCatalog();
            }

            console.log('Billing system initialized');
        } catch (error) {
            console.error('Failed to initialize billing system:', error);
            throw error;
        }
    }

    /**
     * 获取用户账单信息
     */
    async getUserBilling(userId) {
        try {
            const billingData = await this.loadBillingData();
            return billingData[userId] || await this.createUserBilling(userId);
        } catch (error) {
            console.error(`Failed to get billing for user ${userId}:`, error);
            throw error;
        }
    }

    /**
     * 创建新用户账单
     */
    async createUserBilling(userId) {
        const defaultBilling = {
            subscription: {
                tier: 'free',
                status: 'active',
                expires_at: null,
                auto_renew: false
            },
            balance: {
                coins: 0,
                last_updated: new Date().toISOString()
            },
            usage: {
                daily_messages: 0,
                daily_voice: 0,
                daily_photos: 0,
                companions_count: 0,
                last_reset: new Date().toISOString()
            },
            payment_history: []
        };

        const billingData = await this.loadBillingData();
        billingData[userId] = defaultBilling;
        await this.saveBillingData(billingData);

        return defaultBilling;
    }

    /**
     * 检查用户订阅等级
     */
    async checkSubscription(userId) {
        const billing = await this.getUserBilling(userId);
        return billing.subscription;
    }

    /**
     * 检查使用限制
     */
    async checkLimits(userId, action) {
        const billing = await this.getUserBilling(userId);
        const tier = billing.subscription.tier;
        const usage = billing.usage;

        // 每日重置检查
        await this.resetDailyUsageIfNeeded(billing);

        const limits = this.getTierLimits(tier);

        switch (action) {
            case 'message':
                return usage.daily_messages < limits.daily_messages;
            case 'voice':
                return usage.daily_voice < limits.daily_voice;
            case 'photo':
                return usage.daily_photos < limits.daily_photos;
            case 'companion':
                return usage.companions_count < limits.max_companions;
            default:
                return false;
        }
    }

    /**
     * 记录使用量
     */
    async recordUsage(userId, action) {
        const billing = await this.getUserBilling(userId);
        await this.resetDailyUsageIfNeeded(billing);

        switch (action) {
            case 'message':
                billing.usage.daily_messages++;
                break;
            case 'voice':
                billing.usage.daily_voice++;
                break;
            case 'photo':
                billing.usage.daily_photos++;
                break;
            case 'companion':
                billing.usage.companions_count++;
                break;
        }

        await this.saveUserBilling(userId, billing);
    }

    /**
     * 获取订阅档位限制
     */
    getTierLimits(tier) {
        const limits = {
            free: {
                daily_messages: 20,
                daily_voice: 0,
                daily_photos: 0,
                max_companions: 1
            },
            heartbeat: {
                daily_messages: -1, // 无限
                daily_voice: 10,
                daily_photos: 3,
                max_companions: 3
            },
            true_love: {
                daily_messages: -1, // 无限
                daily_voice: -1,   // 无限
                daily_photos: -1,  // 无限
                max_companions: 10
            }
        };

        return limits[tier] || limits.free;
    }

    /**
     * 获取用户余额
     */
    async getBalance(userId) {
        const billing = await this.getUserBilling(userId);
        return billing.balance.coins;
    }

    /**
     * 添加金币
     */
    async addCoins(userId, amount, reason = 'topup') {
        const billing = await this.getUserBilling(userId);
        billing.balance.coins += amount;
        billing.balance.last_updated = new Date().toISOString();

        // 记录支付历史
        billing.payment_history.push({
            type: 'credit',
            amount: amount,
            reason: reason,
            timestamp: new Date().toISOString()
        });

        await this.saveUserBilling(userId, billing);
        return billing.balance.coins;
    }

    /**
     * 消费金币
     */
    async spendCoins(userId, amount, reason = 'purchase') {
        const billing = await this.getUserBilling(userId);
        
        if (billing.balance.coins < amount) {
            throw new Error('Insufficient balance');
        }

        billing.balance.coins -= amount;
        billing.balance.last_updated = new Date().toISOString();

        // 记录支付历史
        billing.payment_history.push({
            type: 'debit',
            amount: amount,
            reason: reason,
            timestamp: new Date().toISOString()
        });

        await this.saveUserBilling(userId, billing);
        return billing.balance.coins;
    }

    /**
     * 升级订阅
     */
    async upgradeSubscription(userId, newTier) {
        const billing = await this.getUserBilling(userId);
        const oldTier = billing.subscription.tier;

        if (oldTier === newTier) {
            throw new Error('Already subscribed to this tier');
        }

        // 更新订阅信息
        billing.subscription.tier = newTier;
        billing.subscription.status = 'active';
        billing.subscription.expires_at = this.calculateExpiryDate(newTier);
        billing.subscription.last_updated = new Date().toISOString();

        // 记录升级历史
        billing.payment_history.push({
            type: 'subscription',
            action: 'upgrade',
            from_tier: oldTier,
            to_tier: newTier,
            timestamp: new Date().toISOString()
        });

        await this.saveUserBilling(userId, billing);
        return billing.subscription;
    }

    /**
     * 计算订阅到期时间
     */
    calculateExpiryDate(tier) {
        const now = new Date();
        if (tier === 'free') {
            return null;
        }
        // 一个月后
        const expiry = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
        return expiry.toISOString();
    }

    /**
     * 重置每日使用量
     */
    async resetDailyUsageIfNeeded(billing) {
        const now = new Date();
        const lastReset = new Date(billing.usage.last_reset);
        
        // 如果是新的一天，重置使用量
        if (now.toDateString() !== lastReset.toDateString()) {
            billing.usage.daily_messages = 0;
            billing.usage.daily_voice = 0;
            billing.usage.daily_photos = 0;
            billing.usage.last_reset = now.toISOString();
        }
    }

    /**
     * 获取礼物目录
     */
    async getGiftCatalog() {
        try {
            const catalogData = await fs.readFile(this.giftCatalogFile, 'utf8');
            return JSON.parse(catalogData);
        } catch (error) {
            console.error('Failed to load gift catalog:', error);
            return { gifts: [] };
        }
    }

    /**
     * 购买礼物
     */
    async purchaseGift(userId, giftId, companionId) {
        const catalog = await this.getGiftCatalog();
        const gift = catalog.gifts.find(g => g.id === giftId);
        
        if (!gift) {
            throw new Error('Gift not found');
        }

        // 扣除金币
        await this.spendCoins(userId, gift.price, `gift_${giftId}_to_${companionId}`);

        // 返回礼物信息和反应模板
        return {
            gift: gift,
            companion_id: companionId,
            reaction_template: gift.reaction_template,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * 加载账单数据
     */
    async loadBillingData() {
        try {
            const data = await fs.readFile(this.billingFile, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            return {};
        }
    }

    /**
     * 保存账单数据
     */
    async saveBillingData(data) {
        await fs.writeFile(this.billingFile, JSON.stringify(data, null, 2), 'utf8');
    }

    /**
     * 保存用户账单
     */
    async saveUserBilling(userId, billing) {
        const billingData = await this.loadBillingData();
        billingData[userId] = billing;
        await this.saveBillingData(billingData);
    }

    /**
     * 初始化礼物目录
     */
    async initGiftCatalog() {
        const catalog = {
            gifts: [
                {
                    id: 'rose',
                    name: '玫瑰',
                    price: 10,
                    category: 'romantic',
                    reaction_template: '收到玫瑰时，伴侣会脸红并说："谢谢你，这真让我心动..."'
                },
                {
                    id: 'chocolate',
                    name: '巧克力',
                    price: 15,
                    category: 'sweet',
                    reaction_template: '收到巧克力时，伴侣会开心地说："我最喜欢巧克力了！你真懂我~"'
                },
                {
                    id: 'teddy_bear',
                    name: '泰迪熊',
                    price: 30,
                    category: 'comfort',
                    reaction_template: '收到泰迪熊时，伴侣会抱住它说："这让我想起了你温暖的拥抱..."'
                },
                {
                    id: 'necklace',
                    name: '项链',
                    price: 50,
                    category: 'precious',
                    reaction_template: '收到项链时，伴侣会感动地说："这太珍贵了...我会永远珍惜的"'
                },
                {
                    id: 'love_letter',
                    name: '情书',
                    price: 5,
                    category: 'romantic',
                    reaction_template: '收到情书时，伴侣会认真阅读并回应你的真挚情感'
                }
            ]
        };

        await fs.writeFile(this.giftCatalogFile, JSON.stringify(catalog, null, 2), 'utf8');
    }

    /**
     * 检查文件是否存在
     */
    async fileExists(filePath) {
        try {
            await fs.access(filePath);
            return true;
        } catch {
            return false;
        }
    }
}

module.exports = BillingManager;
