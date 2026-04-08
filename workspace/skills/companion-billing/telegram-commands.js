/**
 * Telegram 机器人命令处理
 * 处理 /bill, /topup, /subscribe 等账单相关命令
 */

class TelegramCommands {
    constructor(billingManager, paymentProcessor) {
        this.billingManager = billingManager;
        this.paymentProcessor = paymentProcessor;
    }

    /**
     * 处理 /bill 命令 - 查看账单状态
     */
    async handleBillCommand(userId, chatId, bot) {
        try {
            const billing = await this.billingManager.getUserBilling(userId);
            const subscription = billing.subscription;
            const balance = billing.balance.coins;
            const usage = billing.usage;

            // 重置每日使用量（如果需要）
            await this.billingManager.resetDailyUsageIfNeeded(billing);

            const message = this.formatBillingMessage(subscription, balance, usage);
            
            await bot.sendMessage(chatId, message, {
                parse_mode: 'Markdown',
                reply_markup: {
                    inline_keyboard: [
                        [
                            { text: '💰 充值金币', callback_data: 'action_topup' },
                            { text: '⬆️ 升级订阅', callback_data: 'action_subscribe' }
                        ],
                        [
                            { text: '🎁 礼物商店', callback_data: 'action_gifts' },
                            { text: '📊 使用明细', callback_data: 'action_usage' }
                        ]
                    ]
                }
            });
        } catch (error) {
            console.error(`Failed to handle /bill for user ${userId}:`, error);
            await bot.sendMessage(chatId, '❌ 查询账单失败，请稍后重试。');
        }
    }

    /**
     * 处理 /topup 命令 - 充值金币
     */
    async handleTopupCommand(userId, chatId, bot) {
        try {
            const options = this.paymentProcessor.getPaymentOptions();
            const coinsOptions = options.coins;

            const message = '💰 *金币充值选项*\n\n' +
                coinsOptions.map((option, index) => {
                    const totalCoins = option.amount + option.bonus;
                    const bonusText = option.bonus > 0 ? ` (+${option.bonus} 赠送)` : '';
                    return `${index + 1}. ${totalCoins} 金币 - $${option.price}${bonusText}`;
                }).join('\n') +
                '\n\n请选择充值金额：';

            const keyboard = coinsOptions.map((option, index) => [
                { text: `${option.amount + option.bonus} 金币 ($${option.price})`, callback_data: `topup_${option.amount}_${option.price}` }
            ]);

            await bot.sendMessage(chatId, message, {
                parse_mode: 'Markdown',
                reply_markup: {
                    inline_keyboard: keyboard
                }
            });
        } catch (error) {
            console.error(`Failed to handle /topup for user ${userId}:`, error);
            await bot.sendMessage(chatId, '❌ 获取充值选项失败，请稍后重试。');
        }
    }

    /**
     * 处理 /subscribe 命令 - 订阅管理
     */
    async handleSubscribeCommand(userId, chatId, bot) {
        try {
            const currentSubscription = await this.billingManager.checkSubscription(userId);
            const options = this.paymentProcessor.getPaymentOptions();
            const subscriptionOptions = options.subscription;

            const message = this.formatSubscriptionMessage(currentSubscription, subscriptionOptions);

            const keyboard = subscriptionOptions.map(option => [
                { text: `${option.name} - $${option.price}/月`, callback_data: `subscribe_${option.tier}` }
            ]);

            await bot.sendMessage(chatId, message, {
                parse_mode: 'Markdown',
                reply_markup: {
                    inline_keyboard: keyboard
                }
            });
        } catch (error) {
            console.error(`Failed to handle /subscribe for user ${userId}:`, error);
            await bot.sendMessage(chatId, '❌ 获取订阅信息失败，请稍后重试。');
        }
    }

    /**
     * 处理回调查询
     */
    async handleCallbackQuery(userId, chatId, bot, callbackData) {
        try {
            const [action, ...params] = callbackData.split('_');

            switch (action) {
                case 'action':
                    await this.handleActionCallback(userId, chatId, bot, params[0]);
                    break;
                case 'topup':
                    await this.handleTopupCallback(userId, chatId, bot, params);
                    break;
                case 'subscribe':
                    await this.handleSubscribeCallback(userId, chatId, bot, params[0]);
                    break;
                case 'gifts':
                    await this.handleGiftsCallback(userId, chatId, bot);
                    break;
                case 'usage':
                    await this.handleUsageCallback(userId, chatId, bot);
                    break;
                default:
                    await bot.sendMessage(chatId, '❌ 未知操作');
            }
        } catch (error) {
            console.error(`Failed to handle callback ${callbackData} for user ${userId}:`, error);
            await bot.sendMessage(chatId, '❌ 操作失败，请稍后重试。');
        }
    }

    /**
     * 处理动作回调查询
     */
    async handleActionCallback(userId, chatId, bot, action) {
        switch (action) {
            case 'topup':
                await this.handleTopupCommand(userId, chatId, bot);
                break;
            case 'subscribe':
                await this.handleSubscribeCommand(userId, chatId, bot);
                break;
            case 'gifts':
                await this.handleGiftsCallback(userId, chatId, bot);
                break;
            case 'usage':
                await this.handleUsageCallback(userId, chatId, bot);
                break;
        }
    }

    /**
     * 处理充值回调查询
     */
    async handleTopupCallback(userId, chatId, bot, params) {
        const [amount, price] = params;
        const message = `💰 *确认充值*\n\n` +
            `充值金额: ${amount} 金币\n` +
            `价格: $${price}\n\n` +
            `请选择支付方式：`;

        const keyboard = [
            [
                { text: '🧪 使用测试密钥', callback_data: `pay_test_${amount}_coins` }
            ],
            [
                { text: '📝 手动确认支付', callback_data: `pay_manual_${amount}_coins_${price}` }
            ]
        ];

        await bot.sendMessage(chatId, message, {
            parse_mode: 'Markdown',
            reply_markup: {
                inline_keyboard: keyboard
            }
        });
    }

    /**
     * 处理订阅回调查询
     */
    async handleSubscribeCallback(userId, chatId, bot, tier) {
        const options = this.paymentProcessor.getPaymentOptions();
        const subscription = options.subscription.find(s => s.tier === tier);
        
        if (!subscription) {
            await bot.sendMessage(chatId, '❌ 订阅选项不存在');
            return;
        }

        const message = `⬆️ *确认订阅升级*\n\n` +
            `订阅档位: ${subscription.name}\n` +
            `价格: $${subscription.price}/月\n` +
            `功能特权:\n` +
            subscription.features.map(f => `✅ ${f}`).join('\n') +
            `\n\n请选择支付方式：`;

        const keyboard = [
            [
                { text: '🧪 使用测试密钥', callback_data: `pay_test_${tier}_sub` }
            ],
            [
                { text: '📝 手动确认支付', callback_data: `pay_manual_${tier}_sub_${subscription.price}` }
            ]
        ];

        await bot.sendMessage(chatId, message, {
            parse_mode: 'Markdown',
            reply_markup: {
                inline_keyboard: keyboard
            }
        });
    }

    /**
     * 处理礼物商店回调查询
     */
    async handleGiftsCallback(userId, chatId, bot) {
        try {
            const catalog = await this.billingManager.getGiftCatalog();
            const balance = await this.billingManager.getBalance(userId);

            const message = `🎁 *礼物商店*\n\n` +
                `当前余额: ${balance} 金币\n\n` +
                `可选礼物:\n` +
                catalog.gifts.map(gift => 
                    `🎀 ${gift.name} - ${gift.price} 金币\n` +
                    `📝 ${gift.reaction_template.substring(0, 50)}...\n`
                ).join('\n') +
                `\n请选择要购买的礼物：`;

            const keyboard = catalog.gifts.map(gift => [
                { text: `${gift.name} (${gift.price} 金币)`, callback_data: `gift_${gift.id}` }
            ]);

            await bot.sendMessage(chatId, message, {
                parse_mode: 'Markdown',
                reply_markup: {
                    inline_keyboard: keyboard
                }
            });
        } catch (error) {
            console.error(`Failed to show gifts for user ${userId}:`, error);
            await bot.sendMessage(chatId, '❌ 获取礼物商店失败，请稍后重试。');
        }
    }

    /**
     * 处理使用明细回调查询
     */
    async handleUsageCallback(userId, chatId, bot) {
        try {
            const billing = await this.billingManager.getUserBilling(userId);
            const limits = this.billingManager.getTierLimits(billing.subscription.tier);
            const usage = billing.usage;

            const message = `📊 *使用明细*\n\n` +
                `订阅档位: ${billing.subscription.tier.toUpperCase()}\n\n` +
                `📱 消息: ${usage.daily_messages}/${limits.daily_messages === -1 ? '无限' : limits.daily_messages}\n` +
                `🎤 语音: ${usage.daily_voice}/${limits.daily_voice === -1 ? '无限' : limits.daily_voice}\n` +
                `📷 照片: ${usage.daily_photos}/${limits.daily_photos === -1 ? '无限' : limits.daily_photos}\n` +
                `👥 伴侣: ${usage.companions_count}/${limits.max_companions}\n\n` +
                `🔄 重置时间: 每日 00:00 (UTC+8)`;

            await bot.sendMessage(chatId, message, {
                parse_mode: 'Markdown'
            });
        } catch (error) {
            console.error(`Failed to show usage for user ${userId}:`, error);
            await bot.sendMessage(chatId, '❌ 获取使用明细失败，请稍后重试。');
        }
    }

    /**
     * 格式化账单信息
     */
    formatBillingMessage(subscription, balance, usage) {
        const tierName = {
            free: '免费版',
            heartbeat: 'Heartbeat 💝',
            true_love: 'True Love 💕'
        };

        return `💳 *账单状态*\n\n` +
            `📊 订阅档位: ${tierName[subscription.tier] || '免费版'}\n` +
            `💰 金币余额: ${balance}\n` +
            `📱 今日消息: ${usage.daily_messages}\n` +
            `🎤 今日语音: ${usage.daily_voice}\n` +
            `📷 今日照片: ${usage.daily_photos}\n` +
            `👥 伴侣数量: ${usage.companions_count}`;
    }

    /**
     * 格式化订阅信息
     */
    formatSubscriptionMessage(currentSubscription, options) {
        const tierName = {
            free: '免费版',
            heartbeat: 'Heartbeat 💝',
            true_love: 'True Love 💕'
        };

        let message = `⬆️ *订阅管理*\n\n` +
            `当前档位: ${tierName[currentSubscription.tier] || '免费版'}\n` +
            `状态: ${currentSubscription.status}\n`;

        if (currentSubscription.expires_at) {
            const expiryDate = new Date(currentSubscription.expires_at);
            message += `到期时间: ${expiryDate.toLocaleDateString()}\n`;
        }

        message += `\n*升级选项:*\n\n`;

        options.forEach(option => {
            if (option.tier !== currentSubscription.tier) {
                message += `🌟 ${option.name} - $${option.price}/月\n`;
                message += option.features.map(f => `   ✅ ${f}`).join('\n') + '\n\n';
            }
        });

        return message;
    }
}

module.exports = TelegramCommands;
