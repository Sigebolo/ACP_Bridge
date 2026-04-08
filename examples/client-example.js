const WebSocket = require('ws');
const axios = require('axios');

class BridgeClient {
    constructor(apiUrl = 'http://localhost:3000', wsUrl = 'ws://localhost:3001') {
        this.apiUrl = apiUrl;
        this.wsUrl = wsUrl;
        this.ws = null;
        this.clientId = null;
    }

    // REST API Methods
    async createRequirement(requirementData) {
        try {
            const response = await axios.post(`${this.apiUrl}/api/pm/requirements`, requirementData);
            return response.data;
        } catch (error) {
            console.error('Error creating requirement:', error.response?.data || error.message);
            throw error;
        }
    }

    async getRequirements(filters = {}) {
        try {
            const params = new URLSearchParams(filters);
            const response = await axios.get(`${this.apiUrl}/api/pm/requirements?${params}`);
            return response.data;
        } catch (error) {
            console.error('Error getting requirements:', error.response?.data || error.message);
            throw error;
        }
    }

    async makeDecision(decisionData) {
        try {
            const response = await axios.post(`${this.apiUrl}/api/pm/decisions`, decisionData);
            return response.data;
        } catch (error) {
            console.error('Error making decision:', error.response?.data || error.message);
            throw error;
        }
    }

    async registerPlatform(platformData) {
        try {
            const response = await axios.post(`${this.apiUrl}/api/platform/register`, platformData);
            return response.data;
        } catch (error) {
            console.error('Error registering platform:', error.response?.data || error.message);
            throw error;
        }
    }

    async getPlatformTasks(platformId, filters = {}) {
        try {
            const params = new URLSearchParams(filters);
            const response = await axios.get(`${this.apiUrl}/api/platform/tasks/${platformId}?${params}`);
            return response.data;
        } catch (error) {
            console.error('Error getting platform tasks:', error.response?.data || error.message);
            throw error;
        }
    }

    async completeTask(platformId, completionData) {
        try {
            const response = await axios.post(`${this.apiUrl}/api/platform/tasks/${platformId}/complete`, completionData);
            return response.data;
        } catch (error) {
            console.error('Error completing task:', error.response?.data || error.message);
            throw error;
        }
    }

    async getGlobalStatus() {
        try {
            const response = await axios.get(`${this.apiUrl}/api/status`);
            return response.data;
        } catch (error) {
            console.error('Error getting global status:', error.response?.data || error.message);
            throw error;
        }
    }

    async getArtifacts(filters = {}) {
        try {
            const params = new URLSearchParams(filters);
            const response = await axios.get(`${this.apiUrl}/api/artifacts?${params}`);
            return response.data;
        } catch (error) {
            console.error('Error getting artifacts:', error.response?.data || error.message);
            throw error;
        }
    }

    // WebSocket Methods
    connect() {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(this.wsUrl);

            this.ws.on('open', () => {
                console.log('Connected to Bridge Service WebSocket');
            });

            this.ws.on('message', (data) => {
                try {
                    const message = JSON.parse(data);
                    this.handleMessage(message);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                }
            });

            this.ws.on('close', () => {
                console.log('Disconnected from Bridge Service WebSocket');
                this.clientId = null;
            });

            this.ws.on('error', (error) => {
                console.error('WebSocket error:', error);
                reject(error);
            });

            // Wait for connection message
            this.ws.once('message', (data) => {
                try {
                    const message = JSON.parse(data);
                    if (message.type === 'connected') {
                        this.clientId = message.clientId;
                        console.log(`Client ID: ${this.clientId}`);
                        resolve();
                    }
                } catch (error) {
                    reject(error);
                }
            });
        });
    }

    subscribe(filters = {}) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket not connected');
        }

        const message = {
            type: 'subscribe',
            filters: filters
        };

        this.ws.send(JSON.stringify(message));
        console.log('Subscribed to notifications with filters:', filters);
    }

    sendStatusUpdate(taskId, status, progress = null) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket not connected');
        }

        const message = {
            type: 'status_update',
            taskId: taskId,
            status: status,
            progress: progress
        };

        this.ws.send(JSON.stringify(message));
    }

    sendArtifactNotification(artifact) {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
            throw new Error('WebSocket not connected');
        }

        const message = {
            type: 'artifact_notification',
            artifact: artifact
        };

        this.ws.send(JSON.stringify(message));
    }

    handleMessage(message) {
        switch (message.type) {
            case 'notification':
                this.handleNotification(message.notification);
                break;
            case 'connected':
                console.log('Connected confirmation received');
                break;
            default:
                console.log('Unknown message type:', message.type);
        }
    }

    handleNotification(notification) {
        console.log(`Notification received: ${notification.type}`);
        console.log('Data:', notification.data);
        
        // Override this method in your client to handle notifications
        this.onNotification(notification);
    }

    onNotification(notification) {
        // Override this method in your implementation
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
            this.clientId = null;
        }
    }
}

// Example usage
class ExampleClient extends BridgeClient {
    constructor() {
        super();
        this.setupNotificationHandlers();
    }

    setupNotificationHandlers() {
        this.onNotification = (notification) => {
            switch (notification.type) {
                case 'requirement_created':
                    console.log(`New requirement: ${notification.data.title}`);
                    break;
                case 'task_completed':
                    console.log(`Task completed: ${notification.data.title}`);
                    break;
                case 'artifact_uploaded':
                    console.log(`New artifact: ${notification.data.name}`);
                    break;
                case 'decision_made':
                    console.log(`Decision made: ${notification.data.title}`);
                    break;
                case 'error':
                    console.error(`Error notification: ${notification.data.error}`);
                    break;
            }
        };
    }

    async demonstrateWorkflow() {
        try {
            console.log('Starting Bridge Service demonstration...');

            // Connect to WebSocket
            await this.connect();
            
            // Subscribe to all notifications
            this.subscribe({
                types: ['requirement_created', 'task_completed', 'artifact_uploaded', 'decision_made'],
                priority: 'high'
            });

            // 1. Create a requirement as OpenClaw PM
            console.log('\n1. Creating requirement...');
            const requirement = await this.createRequirement({
                title: '实现用户认证系统',
                description: '开发一个完整的用户认证和授权系统',
                priority: 'high',
                category: 'security',
                requirements: [
                    '用户注册功能',
                    '邮箱验证',
                    '密码重置',
                    'JWT认证',
                    '角色权限管理'
                ],
                acceptanceCriteria: [
                    '用户可以成功注册和登录',
                    '密码安全存储',
                    'API接口需要认证',
                    '不同角色有不同权限'
                ]
            });
            console.log('Requirement created:', requirement.requirement.id);

            // 2. Register a platform (Google CLI)
            console.log('\n2. Registering Google CLI platform...');
            const platform = await this.registerPlatform({
                name: 'Google CLI Platform',
                type: 'google-cli',
                description: 'Google Cloud CLI integration',
                capabilities: ['deployment', 'infrastructure'],
                config: {
                    project: 'demo-project',
                    region: 'us-central1'
                }
            });
            console.log('Platform registered:', platform.platform.id);

            // 3. Get global status
            console.log('\n3. Getting global status...');
            const status = await this.getGlobalStatus();
            console.log('Global status:', status);

            // Wait a bit to receive notifications
            await new Promise(resolve => setTimeout(resolve, 2000));

            // 4. Make a decision
            console.log('\n4. Making decision...');
            const decision = await this.makeDecision({
                title: '选择认证方案',
                description: '为用户认证系统选择合适的技术方案',
                options: [
                    {
                        name: 'JWT + bcrypt',
                        pros: ['无状态', '性能好', '标准化'],
                        cons: ['需要处理token过期']
                    },
                    {
                        name: 'Session + Redis',
                        pros: ['服务端控制', '安全性高'],
                        cons: ['需要Redis', '有状态']
                    }
                ],
                selectedOption: 'JWT + bcrypt',
                rationale: '考虑到微服务架构和性能要求，选择JWT方案更合适',
                confidence: 'high'
            });
            console.log('Decision made:', decision.decision.id);

            // Wait for notifications
            await new Promise(resolve => setTimeout(resolve, 2000));

            // 5. Simulate task completion
            console.log('\n5. Simulating task completion...');
            const completion = await this.completeTask(platform.platform.id, {
                taskId: 'demo-task-id',
                result: {
                    status: 'success',
                    output: 'User authentication system implemented successfully',
                    metrics: {
                        duration: 3600000,
                        featuresImplemented: 5,
                        testsWritten: 25
                    }
                },
                artifacts: [
                    {
                        name: 'auth-service.zip',
                        content: 'Simulated auth service code...',
                        type: 'archive'
                    },
                    {
                        name: 'test-results.json',
                        content: JSON.stringify({
                            total: 25,
                            passed: 25,
                            failed: 0,
                            coverage: 95
                        }),
                        type: 'json'
                    }
                ]
            });
            console.log('Task completed:', completion);

            // Wait for final notifications
            await new Promise(resolve => setTimeout(resolve, 2000));

            // 6. Get artifacts
            console.log('\n6. Getting artifacts...');
            const artifacts = await this.getArtifacts();
            console.log(`Found ${artifacts.length} artifacts`);

            console.log('\nDemonstration completed successfully!');

        } catch (error) {
            console.error('Demonstration failed:', error.message);
        } finally {
            this.disconnect();
        }
    }
}

// Run the example if this file is executed directly
if (require.main === module) {
    const client = new ExampleClient();
    client.demonstrateWorkflow().catch(console.error);
}

module.exports = BridgeClient;
