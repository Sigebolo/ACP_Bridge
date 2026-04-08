/**
 * Companion Billing Skill 测试套件
 * 测试订阅管理、支付处理和权限控制功能
 */

const CompanionBillingSkill = require('../index');
const BillingManager = require('../billing-manager');
const PaymentProcessor = require('../payment-processor');
const BillingMiddleware = require('../middleware');

class BillingTestSuite {
    constructor() {
        this.testUserId = 'test_user_123';
        this.billingSkill = new CompanionBillingSkill();
        this.testResults = [];
    }

    /**
     * 运行所有测试
     */
    async runAllTests() {
        console.log('🧪 开始运行 Companion Billing 测试套件...\n');
        
        try {
            await this.billingSkill.init();
            
            // 重置测试数据以开始干净的测试
            await this.resetTestData();

            // 基础功能测试
            await this.testUserBillingCreation();
            await this.testSubscriptionTiers();
            await this.testPermissionChecks();
            await this.testPaymentProcessing();
            await this.testGiftSystem();
            await this.testUsageTracking();
            
            // 边界条件测试
            await this.testLimitExceeded();
            await this.testInvalidPayments();
            await this.testConcurrentUsage();
            
            this.printTestResults();
            
        } catch (error) {
            console.error('❌ 测试套件运行失败:', error);
        }
    }

    /**
     * 重置测试用户数据
     */
    async resetTestData() {
        const billingData = await this.billingSkill.billingManager.loadBillingData();
        delete billingData[this.testUserId];
        await this.billingSkill.billingManager.saveBillingData(billingData);
    }

    /**
     * 测试用户账单创建
     */
    async testUserBillingCreation() {
        console.log('📝 测试用户账单创建...');
        
        try {
            // 创建新用户账单
            const billing = await this.billingSkill.getUserBillingStatus(this.testUserId);
            
            this.assert(billing.subscription.tier === 'free', '新用户应该是免费版');
            this.assert(billing.balance === 0, '新用户余额应该是0');
            this.assert(billing.usage.daily_messages === 0, '新用户每日消息应该是0');
            this.assert(billing.usage.companions_count === 0, '新用户伴侣数量应该是0');
            
            this.recordTest('用户账单创建', true);
            
        } catch (error) {
            this.recordTest('用户账单创建', false, error.message);
        }
    }

    /**
     * 测试订阅档位
     */
    async testSubscriptionTiers() {
        console.log('📊 测试订阅档位...');
        
        try {
            // 测试免费版限制
            const freeLimits = this.billingSkill.billingManager.getTierLimits('free');
            this.assert(freeLimits.daily_messages === 20, '免费版每日消息限制应该是20');
            this.assert(freeLimits.daily_voice === 0, '免费版语音限制应该是0');
            this.assert(freeLimits.max_companions === 1, '免费版伴侣限制应该是1');
            
            // 测试 Heartbeat 档位
            const heartbeatLimits = this.billingSkill.billingManager.getTierLimits('heartbeat');
            this.assert(heartbeatLimits.daily_messages === -1, 'Heartbeat 档位消息应该是无限');
            this.assert(heartbeatLimits.daily_voice === 10, 'Heartbeat 档位语音限制应该是10');
            this.assert(heartbeatLimits.max_companions === 3, 'Heartbeat 档位伴侣限制应该是3');
            
            // 测试 True Love 档位
            const trueLoveLimits = this.billingSkill.billingManager.getTierLimits('true_love');
            this.assert(trueLoveLimits.daily_messages === -1, 'True Love 档位消息应该是无限');
            this.assert(trueLoveLimits.daily_voice === -1, 'True Love 档位语音应该是无限');
            this.assert(trueLoveLimits.max_companions === 10, 'True Love 档位伴侣限制应该是10');
            
            this.recordTest('订阅档位', true);
            
        } catch (error) {
            this.recordTest('订阅档位', false, error.message);
        }
    }

    /**
     * 测试权限检查
     */
    async testPermissionChecks() {
        console.log('🔒 测试权限检查...');
        
        try {
            // 测试免费用户消息权限
            let result = await this.billingSkill.checkPermission(this.testUserId, 'message');
            this.assert(result.allowed === true, '免费用户应该能发送消息');
            
            // 模拟达到消息限制
            const billing = await this.billingSkill.billingManager.getUserBilling(this.testUserId);
            billing.usage.daily_messages = 20; // 达到免费版限制
            await this.billingSkill.billingManager.saveUserBilling(this.testUserId, billing);
            
            result = await this.billingSkill.checkPermission(this.testUserId, 'message');
            this.assert(result.allowed === false, '达到限制后不应该能发送消息');
            this.assert(result.reason.includes('今日消息次数已达上限'), '应该显示正确的错误信息');
            
            // 测试语音权限（免费用户）
            result = await this.billingSkill.checkPermission(this.testUserId, 'voice');
            this.assert(result.allowed === false, '免费用户不应该能发送语音');
            
            this.recordTest('权限检查', true);
            
        } catch (error) {
            this.recordTest('权限检查', false, error.message);
        }
    }

    /**
     * 测试支付处理
     */
    async testPaymentProcessing() {
        console.log('💳 测试支付处理...');
        
        try {
            // 测试测试密钥支付
            const paymentResult = await this.billingSkill.processPayment(
                this.testUserId, 
                'test_key', 
                { key: 'TEST_HEARTBEAT_2026' }
            );
            
            this.assert(paymentResult.status === 'completed', '测试密钥支付应该成功');
            this.assert(paymentResult.tier === 'heartbeat', '应该升级到 Heartbeat 档位');
            
            // 验证订阅升级
            const billing = await this.billingSkill.getUserBillingStatus(this.testUserId);
            this.assert(billing.subscription.tier === 'heartbeat', '用户订阅应该已升级');
            
            // 测试金币充值
            const topupResult = await this.billingSkill.processPayment(
                this.testUserId,
                'test_key',
                { key: 'TEST_COINS_100' }
            );
            
            this.assert(topupResult.status === 'completed', '金币充值应该成功');
            this.assert(topupResult.coins === 100, '应该充值100金币');
            
            // 验证余额
            const updatedBilling = await this.billingSkill.getUserBillingStatus(this.testUserId);
            this.assert(updatedBilling.balance === 100, '用户余额应该是100');
            
            this.recordTest('支付处理', true);
            
        } catch (error) {
            this.recordTest('支付处理', false, error.message);
        }
    }

    /**
     * 测试礼物系统
     */
    async testGiftSystem() {
        console.log('🎁 测试礼物系统...');
        
        try {
            // 获取礼物目录
            const catalog = await this.billingSkill.getGiftCatalog();
            this.assert(catalog.gifts.length > 0, '礼物目录应该不为空');
            
            // 购买礼物
            const giftResult = await this.billingSkill.purchaseGift(
                this.testUserId,
                'rose',
                'companion_123'
            );
            
            this.assert(giftResult.gift.id === 'rose', '应该购买到正确的礼物');
            this.assert(giftResult.companion_id === 'companion_123', '应该记录正确的伴侣ID');
            
            // 验证金币扣除
            const billing = await this.billingSkill.getUserBillingStatus(this.testUserId);
            this.assert(billing.balance === 90, '余额应该扣除10金币'); // 100 - 10 = 90
            
            this.recordTest('礼物系统', true);
            
        } catch (error) {
            this.recordTest('礼物系统', false, error.message);
        }
    }

    /**
     * 测试使用量跟踪
     */
    async testUsageTracking() {
        console.log('📈 测试使用量跟踪...');
        
        try {
            // 获取初始状态
            const initialBilling = await this.billingSkill.getUserBillingStatus(this.testUserId);
            const initialMessages = initialBilling.usage.daily_messages;
            const initialCompanions = initialBilling.usage.companions_count;

            // 记录消息使用
            await this.billingSkill.billingManager.recordUsage(this.testUserId, 'message');
            
            const billing = await this.billingSkill.getUserBillingStatus(this.testUserId);
            this.assert(billing.usage.daily_messages === initialMessages + 1, '每日消息应该增加1');
            
            // 记录伴侣创建
            await this.billingSkill.billingManager.recordUsage(this.testUserId, 'companion');
            
            const updatedBilling = await this.billingSkill.getUserBillingStatus(this.testUserId);
            this.assert(updatedBilling.usage.companions_count === initialCompanions + 1, '伴侣数量应该增加1');
            
            this.recordTest('使用量跟踪', true);
            
        } catch (error) {
            this.recordTest('使用量跟踪', false, error.message);
        }
    }

    /**
     * 测试限制超出
     */
    async testLimitExceeded() {
        console.log('🚫 测试限制超出...');
        
        try {
            // 将用户降级到免费版
            await this.billingSkill.billingManager.upgradeSubscription(this.testUserId, 'free');
            
            // 模拟达到伴侣限制
            const billing = await this.billingSkill.billingManager.getUserBilling(this.testUserId);
            billing.usage.companions_count = 1; // 免费版限制
            await this.billingSkill.billingManager.saveUserBilling(this.testUserId, billing);
            
            const result = await this.billingSkill.checkPermission(this.testUserId, 'companion');
            this.assert(result.allowed === false, '达到伴侣限制时不应该能创建新伴侣');
            
            this.recordTest('限制超出', true);
            
        } catch (error) {
            this.recordTest('限制超出', false, error.message);
        }
    }

    /**
     * 测试无效支付
     */
    async testInvalidPayments() {
        console.log('❌ 测试无效支付...');
        
        try {
            // 测试无效测试密钥
            try {
                await this.billingSkill.processPayment(
                    this.testUserId,
                    'test_key',
                    { key: 'INVALID_KEY' }
                );
                this.assert(false, '无效密钥应该抛出错误');
            } catch (error) {
                this.assert(error.message.includes('Invalid test key'), '应该显示密钥无效错误');
            }
            
            // 测试余额不足购买礼物
            try {
                // 先清空余额
                const billing = await this.billingSkill.billingManager.getUserBilling(this.testUserId);
                billing.balance.coins = 0;
                await this.billingSkill.billingManager.saveUserBilling(this.testUserId, billing);
                
                await this.billingSkill.purchaseGift(this.testUserId, 'necklace', 'companion_123');
                this.assert(false, '余额不足应该抛出错误');
            } catch (error) {
                this.assert(error.message.includes('Insufficient balance'), '应该显示余额不足错误');
            }
            
            this.recordTest('无效支付', true);
            
        } catch (error) {
            this.recordTest('无效支付', false, error.message);
        }
    }

    /**
     * 测试并发使用
     */
    async testConcurrentUsage() {
        console.log('⚡ 测试并发使用...');
        
        try {
            // 模拟并发权限检查
            const promises = [];
            for (let i = 0; i < 5; i++) {
                promises.push(this.billingSkill.checkPermission(this.testUserId, 'message'));
            }
            
            const results = await Promise.all(promises);
            
            // 所有结果应该一致
            const firstResult = results[0];
            results.forEach(result => {
                this.assert(result.allowed === firstResult.allowed, '并发检查结果应该一致');
            });
            
            this.recordTest('并发使用', true);
            
        } catch (error) {
            this.recordTest('并发使用', false, error.message);
        }
    }

    /**
     * 断言函数
     */
    assert(condition, message) {
        if (!condition) {
            throw new Error(`断言失败: ${message}`);
        }
    }

    /**
     * 记录测试结果
     */
    recordTest(testName, passed, error = null) {
        this.testResults.push({
            name: testName,
            passed: passed,
            error: error,
            timestamp: new Date().toISOString()
        });
        
        console.log(`  ${passed ? '✅' : '❌'} ${testName}${error ? ': ' + error : ''}`);
    }

    /**
     * 打印测试结果
     */
    printTestResults() {
        console.log('\n📊 测试结果汇总:');
        console.log('='.repeat(50));
        
        const passed = this.testResults.filter(r => r.passed).length;
        const total = this.testResults.length;
        
        console.log(`总测试数: ${total}`);
        console.log(`通过: ${passed}`);
        console.log(`失败: ${total - passed}`);
        console.log(`成功率: ${(passed / total * 100).toFixed(1)}%`);
        
        if (passed < total) {
            console.log('\n❌ 失败的测试:');
            this.testResults
                .filter(r => !r.passed)
                .forEach(r => {
                    console.log(`  • ${r.name}: ${r.error}`);
                });
        }
        
        console.log('\n🎉 测试完成!');
    }
}

// 如果直接运行此文件，执行测试
if (require.main === module) {
    const testSuite = new BillingTestSuite();
    testSuite.runAllTests().catch(console.error);
}

module.exports = BillingTestSuite;
