/**
 * 支付处理器
 * MVP 阶段支持手动确认，后续扩展 Stripe 等支付方式
 */

class PaymentProcessor {
    constructor(billingManager) {
        this.billingManager = billingManager;
        this.testKeys = new Map([
            ['TEST_HEARTBEAT_2026', { tier: 'heartbeat', amount: 9.9 }],
            ['TEST_TRUELOVE_2026', { tier: 'true_love', amount: 24.9 }],
            ['TEST_COINS_100', { coins: 100, amount: 5.0 }],
            ['TEST_COINS_500', { coins: 500, amount: 20.0 }],
            ['TEST_COINS_1000', { coins: 1000, amount: 35.0 }]
        ]);
    }

    /**
     * 处理订阅支付
     */
    async processSubscriptionPayment(userId, paymentMethod, paymentData) {
        try {
            if (paymentMethod === 'test_key') {
                return await this.processTestKey(userId, paymentData.key);
            } else if (paymentMethod === 'manual_confirm') {
                return await this.processManualConfirmation(userId, paymentData);
            } else {
                throw new Error(`Payment method ${paymentMethod} not supported yet`);
            }
        } catch (error) {
            console.error(`Payment processing failed for user ${userId}:`, error);
            throw error;
        }
    }

    /**
     * 处理测试密钥支付
     */
    async processTestKey(userId, testKey) {
        const keyData = this.testKeys.get(testKey);
        if (!keyData) {
            throw new Error('Invalid test key');
        }

        const result = {
            payment_id: `test_${Date.now()}`,
            amount: keyData.amount,
            currency: 'USD',
            status: 'completed',
            timestamp: new Date().toISOString()
        };

        if (keyData.tier) {
            // 订阅升级
            await this.billingManager.upgradeSubscription(userId, keyData.tier);
            result.type = 'subscription';
            result.tier = keyData.tier;
        } else if (keyData.coins) {
            // 金币充值
            await this.billingManager.addCoins(userId, keyData.coins, 'test_key_topup');
            result.type = 'topup';
            result.coins = keyData.coins;
        }

        return result;
    }

    /**
     * 处理手动确认支付
     */
    async processManualConfirmation(userId, paymentData) {
        const { type, amount, tier, coins } = paymentData;

        // 创建待确认的支付记录
        const paymentRecord = {
            payment_id: `manual_${Date.now()}`,
            user_id: userId,
            type: type,
            amount: amount,
            currency: 'USD',
            status: 'pending_confirmation',
            created_at: new Date().toISOString(),
            expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24小时后过期
        };

        if (tier) {
            paymentRecord.tier = tier;
        } else if (coins) {
            paymentRecord.coins = coins;
        }

        // 保存待确认记录
        await this.savePendingPayment(paymentRecord);

        return {
            ...paymentRecord,
            message: 'Payment created. Please wait for manual confirmation.',
            confirmation_instructions: this.getConfirmationInstructions(paymentRecord)
        };
    }

    /**
     * 确认手动支付
     */
    async confirmManualPayment(paymentId, confirmedBy) {
        const pendingPayment = await this.getPendingPayment(paymentId);
        if (!pendingPayment) {
            throw new Error('Payment not found or expired');
        }

        if (pendingPayment.status !== 'pending_confirmation') {
            throw new Error('Payment already processed');
        }

        // 更新支付状态
        pendingPayment.status = 'completed';
        pendingPayment.confirmed_at = new Date().toISOString();
        pendingPayment.confirmed_by = confirmedBy;

        // 执行相应的业务逻辑
        if (pendingPayment.tier) {
            await this.billingManager.upgradeSubscription(pendingPayment.user_id, pendingPayment.tier);
        } else if (pendingPayment.coins) {
            await this.billingManager.addCoins(pendingPayment.user_id, pendingPayment.coins, 'manual_topup');
        }

        // 移除待确认记录
        await this.removePendingPayment(paymentId);

        return pendingPayment;
    }

    /**
     * 获取支付选项
     */
    getPaymentOptions() {
        return {
            subscription: [
                {
                    tier: 'heartbeat',
                    name: 'Heartbeat',
                    price: 9.9,
                    period: 'month',
                    features: [
                        '3 个伴侣',
                        '无限消息',
                        '每日 10 条语音',
                        '每日 3 张照片'
                    ]
                },
                {
                    tier: 'true_love',
                    name: 'True Love',
                    price: 24.9,
                    period: 'month',
                    features: [
                        '10 个伴侣',
                        '无限消息、语音、照片',
                        '深度记忆解锁',
                        '专属礼物反应'
                    ]
                }
            ],
            coins: [
                { amount: 100, price: 5.0, bonus: 0 },
                { amount: 500, price: 20.0, bonus: 50 }, // 额外赠送50个
                { amount: 1000, price: 35.0, bonus: 150 } // 额外赠送150个
            ],
            payment_methods: [
                {
                    id: 'test_key',
                    name: '测试密钥',
                    description: '用于开发测试的虚拟支付',
                    test_keys: Array.from(this.testKeys.keys())
                },
                {
                    id: 'manual_confirm',
                    name: '手动确认',
                    description: '提交支付申请，等待管理员确认'
                }
            ]
        };
    }

    /**
     * 获取确认说明
     */
    getConfirmationInstructions(paymentRecord) {
        return {
            steps: [
                '1. 完成银行转账到指定账户',
                '2. 保存转账凭证截图',
                '3. 联系客服并提供支付ID和凭证',
                '4. 等待管理员确认'
            ],
            payment_id: paymentRecord.payment_id,
            amount: paymentRecord.amount,
            expires_at: paymentRecord.expires_at,
            contact_methods: [
                'Telegram: @heartbeat_support',
                'Email: support@heartbeat.ai'
            ]
        };
    }

    /**
     * 获取待确认支付
     */
    async getPendingPayment(paymentId) {
        // 这里应该从数据库或文件中获取
        // 为简化，使用内存存储
        if (!this.pendingPayments) {
            this.pendingPayments = new Map();
        }
        return this.pendingPayments.get(paymentId);
    }

    /**
     * 保存待确认支付
     */
    async savePendingPayment(paymentRecord) {
        if (!this.pendingPayments) {
            this.pendingPayments = new Map();
        }
        this.pendingPayments.set(paymentRecord.payment_id, paymentRecord);
    }

    /**
     * 移除待确认支付
     */
    async removePendingPayment(paymentId) {
        if (this.pendingPayments) {
            this.pendingPayments.delete(paymentId);
        }
    }

    /**
     * 获取所有待确认支付（管理员用）
     */
    async getAllPendingPayments() {
        if (!this.pendingPayments) {
            return [];
        }
        return Array.from(this.pendingPayments.values());
    }

    /**
     * 清理过期支付
     */
    async cleanupExpiredPayments() {
        if (!this.pendingPayments) {
            return;
        }

        const now = new Date();
        const expiredPayments = [];

        for (const [paymentId, payment] of this.pendingPayments) {
            if (new Date(payment.expires_at) < now) {
                expiredPayments.push(paymentId);
            }
        }

        expiredPayments.forEach(id => {
            this.pendingPayments.delete(id);
        });

        return expiredPayments.length;
    }
}

module.exports = PaymentProcessor;
