const express = require('express');
const axios = require('axios');
const cors = require('cors');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs-extra');
const path = require('path');
const bodyParser = require('body-parser');

const StatusManager = require('./managers/statusManager');
const ArtifactManager = require('./managers/artifactManager');
const NotificationService = require('./services/notificationService');
const OpenClawAdapter = require('./adapters/openclawAdapter');
const PlatformAdapterManager = require('./adapters/platformAdapterManager');
const { exec } = require('child_process');

class BridgeServer {
    constructor() {
        this.app = express();
        this.port = process.env.PORT || 33333;
        this.wsPort = process.env.WS_PORT || 33334;
        
        this.statusManager = new StatusManager();
        this.artifactManager = new ArtifactManager();
        this.notificationService = new NotificationService();
        this.openClawAdapter = new OpenClawAdapter(this.statusManager, this.artifactManager);
        this.platformAdapterManager = new PlatformAdapterManager(this.statusManager, this.artifactManager);
        
        this.setupMiddleware();
        this.setupRoutes();
        this.setupWebSocket();
        this.ensureDirectories();
        
        // Real-time Review Stream
        this.reviewStream = [];
    }

    setupMiddleware() {
        this.app.use(cors());
        this.app.use(bodyParser.json({ limit: '50mb' }));
        this.app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));
        
        this.app.use((req, res, next) => {
            console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }

    setupRoutes() {
        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ status: 'healthy', timestamp: new Date().toISOString() });
        });

        // OpenClaw PM endpoints
        this.app.post('/api/pm/requirements', this.handleCreateRequirement.bind(this));
        this.app.get('/api/pm/requirements', this.handleGetRequirements.bind(this));
        this.app.post('/api/pm/decisions', this.handleMakeDecision.bind(this));
        this.app.get('/api/pm/status', this.handleGetPMStatus.bind(this));

        // Platform endpoints
        this.app.post('/api/platform/register', this.handleRegisterPlatform.bind(this));
        
        // Add direct task assignment
        this.app.post('/api/platform/tasks', this.handleCreatePlatformTask.bind(this));
        
        this.app.get('/api/platform/tasks/:platformId', this.handleGetPlatformTasks.bind(this));
        this.app.post('/api/platform/tasks/:platformId/complete', this.handleCompleteTask.bind(this));
        this.app.post('/api/platform/artifacts', this.handleUploadArtifact.bind(this));

        // Status and artifacts
        this.app.get('/api/status', this.handleGetGlobalStatus.bind(this));
        this.app.get('/api/artifacts', this.handleGetArtifacts.bind(this));
        this.app.get('/api/artifacts/:artifactId', this.handleDownloadArtifact.bind(this));

        // Notifications
        this.app.post('/api/notifications/subscribe', this.handleSubscribeNotifications.bind(this));

        // Gemini CLI Input Hooks - "Telephone for Gemini CLI"
        this.app.post('/api/gemini/message', this.handleGeminiMessage.bind(this));
        this.app.post('/api/gemini/review', this.handleGeminiReview.bind(this));
        this.app.post('/api/gemini/suggestion', this.handleGeminiSuggestion.bind(this));

        // Real-time Review Endpoints
        this.app.post('/antigravity/review-step', this.handleAddReviewStep.bind(this));
        this.app.get('/antigravity/review-step/:id', this.handleGetReviewStep.bind(this));
        this.app.get('/antigravity/review-history', this.handleGetReviewHistory.bind(this));
        this.app.get('/antigravity/live-review', this.handleLiveReviewStream.bind(this));
    }

    setupWebSocket() {
        this.wss = new WebSocket.Server({ port: this.wsPort });
        
        this.wss.on('connection', (ws) => {
            const clientId = uuidv4();
            ws.clientId = clientId;
            
            console.log(`WebSocket client connected: ${clientId}`);
            
            ws.on('message', async (message) => {
                try {
                    const data = JSON.parse(message);
                    await this.handleWebSocketMessage(ws, data);
                } catch (error) {
                    console.error('WebSocket message error:', error);
                    ws.send(JSON.stringify({ error: 'Invalid message format' }));
                }
            });

            ws.on('close', () => {
                console.log(`WebSocket client disconnected: ${clientId}`);
                this.notificationService.unsubscribe(clientId);
            });

            ws.send(JSON.stringify({ 
                type: 'connected', 
                clientId,
                timestamp: new Date().toISOString()
            }));
        });
    }

    async handleWebSocketMessage(ws, data) {
        switch (data.type) {
            case 'subscribe':
                this.notificationService.subscribe(ws.clientId, ws, data.filters);
                break;
            case 'status_update':
                await this.statusManager.updateStatus(data.taskId, data.status);
                this.notificationService.broadcast('status_update', data);
                break;
            case 'artifact_notification':
                this.notificationService.broadcast('artifact_created', data.artifact);
                break;
        }
    }

    async ensureDirectories() {
        const dirs = ['artifacts', 'logs', 'config'];
        for (const dir of dirs) {
            await fs.ensureDir(path.join(__dirname, '..', dir));
        }
    }

    // Route handlers
    async handleCreateRequirement(req, res) {
        try {
            const requirement = await this.openClawAdapter.createRequirement(req.body);
            this.notificationService.broadcast('requirement_created', requirement);
            res.json({ success: true, requirement });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetRequirements(req, res) {
        try {
            const requirements = await this.openClawAdapter.getRequirements();
            res.json(requirements);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleMakeDecision(req, res) {
        try {
            const decision = await this.openClawAdapter.makeDecision(req.body);
            this.notificationService.broadcast('decision_made', decision);
            res.json({ success: true, decision });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetPMStatus(req, res) {
        try {
            const status = await this.openClawAdapter.getStatus();
            res.json(status);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleRegisterPlatform(req, res) {
        try {
            const platform = await this.platformAdapterManager.registerPlatform(req.body);
            this.notificationService.broadcast('platform_registered', platform);
            res.json({ success: true, platform });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetPlatformTasks(req, res) {
        try {
            const tasks = await this.platformAdapterManager.getTasks(req.params.platformId);
            res.json(tasks);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleCreatePlatformTask(req, res) {
        try {
            const platformId = req.body.platformId;
            if (!platformId) throw new Error('platformId is required');
            const task = await this.platformAdapterManager.assignTaskToPlatform(req.body, platformId);
            res.json({ success: true, task });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleCompleteTask(req, res) {
        try {
            const result = await this.platformAdapterManager.completeTask(
                req.params.platformId, 
                req.body
            );
            this.notificationService.broadcast('task_completed', result);
            res.json({ success: true, result });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleUploadArtifact(req, res) {
        try {
            const artifact = await this.artifactManager.saveArtifact(req.body);
            this.notificationService.broadcast('artifact_uploaded', artifact);
            res.json({ success: true, artifact });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetGlobalStatus(req, res) {
        try {
            const status = await this.statusManager.getGlobalStatus();
            res.json(status);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetArtifacts(req, res) {
        try {
            const artifacts = await this.artifactManager.getArtifacts(req.query);
            res.json(artifacts);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleDownloadArtifact(req, res) {
        try {
            const artifactPath = await this.artifactManager.getArtifactPath(req.params.artifactId);
            res.download(artifactPath);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleSubscribeNotifications(req, res) {
        try {
            const subscription = this.notificationService.createSubscription(req.body);
            res.json({ success: true, subscription });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    // Real-time Review Handlers
    async handleAddReviewStep(req, res) {
        try {
            const step = {
                id: uuidv4(),
                timestamp: new Date().toISOString(),
                ...req.body
            };
            
            console.log(`[Review] New step received: ${step.event} - ${step.file || step.cmd || ''}`);
            this.reviewStream.push(step);
            
            // Limit stream size to prevent memory leak
            if (this.reviewStream.length > 100) {
                this.reviewStream.shift();
            }
            
            // Also notify via standard notification service
            this.notificationService.broadcast('review_step', step);
            
            // 2. Automatic RPA Trigger for Antigravity (Real-time "Informing")
            this.triggerAntigravityRPA(step);
            
            // 3. Agentic Task Delivery: Push to local Antigravity Connector (8081)
            this.triggerAntigravityTask(step);
            
            res.json({ ok: 1, id: step.id });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async triggerAntigravityTask(step) {
        try {
            const connectorUrl = 'http://localhost:33335/tasks';
            const task = {
                id: `sync_${step.id.slice(0, 8)}`,
                title: `Windsurf Review: ${step.file || 'Action'}`,
                description: `Real-time synchronization action detected from Windsurf Cascade.\n\nEvent: ${step.event}\nFile: ${step.file || 'N/A'}\n\n## Action Content\n\`\`\`\n${step.diff || step.cmd || step.output || 'No diff/output'}\n\`\`\``,
                type: 'review',
                priority: 'high',
                requirements: [
                    'Perform a real-time code review of the changes',
                    'Log any potential issues or suggestions in the chat'
                ],
                files: step.file ? [{ name: step.file, content: step.diff || '' }] : []
            };

            console.log(`[Connector] Pushing sync task to Antigravity Connector (33335)...`);
            await axios.post(connectorUrl, task);
            console.log(`[Connector Success] Task injected for step: ${step.id}`);
        } catch (error) {
            console.error(`[Connector Error] Failed to push task to 33335: ${error.message}`);
        }
    }

    async handleGetReviewHistory(req, res) {
        try {
            const limit = parseInt(req.query.limit) || 10;
            const history = (this.reviewStream || []).slice(-limit);
            res.json(history);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetReviewStep(req, res) {
        try {
            const stepId = req.params.id;
            const step = this.reviewStream.find(s => s.id === stepId);
            if (!step) {
                return res.status(404).json({ error: 'Step not found' });
            }
            res.json(step);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    triggerAntigravityRPA(step) {
        // Only trigger on "important" events to avoid disruption
        const importantEvents = ['write', 'cmd', 'mcp'];
        if (!importantEvents.includes(step.event)) return;

        const scriptPath = path.join(__dirname, '..', 'scripts', 'trigger-antigravity.ps1');
        
        // Minimalist Mission Briefing for Agent focus
        const taskFileName = `sync_${step.id.slice(0, 8)}.md`;
        const message = `[Windsurf Sync] 🚀 New action on ${step.file || 'workspace'}. 📘 Task: workspace/antigravity_tasks/${taskFileName}. Please review.`;

        console.log(`[RPA] Pinging Antigravity IDE (Improved RPA) for step: ${step.id}...`);
        
        const command = `powershell -ExecutionPolicy Bypass -File "${scriptPath}" "${message}"`;
        
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`[RPA Error] Trigger failed: ${error.message}`);
                return;
            }
            if (stderr) {
                console.log(`[RPA Stderr] ${stderr}`);
            }
            console.log(`[RPA Success] Antigravity informed.`);
        });
    }

    handleLiveReviewStream(req, res) {
        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');
        res.flushHeaders();

        console.log(`[SSE] Client connected to live-review stream`);

        const sendEvent = (data) => {
            res.write(`data: ${JSON.stringify(data)}\n\n`);
        };

        // Send existing items in stream first (optional, but good for context)
        /* 
        if (this.reviewStream.length > 0) {
            this.reviewStream.forEach(step => sendEvent(step));
        }
        */

        const onReviewStep = (step) => {
            sendEvent(step);
        };

        this.notificationService.on('notificationBroadcasted', (event) => {
            if (event.notification.type === 'review_step') {
                onReviewStep(event.notification.data);
            }
        });

        req.on('close', () => {
            console.log(`[SSE] Client disconnected from live-review stream`);
        });
    }

    // Gemini CLI Input Hook Handlers - "Telephone operators"
    async handleGeminiMessage(req, res) {
        try {
            console.log(`[Gemini Phone] Incoming message from Gemini CLI`);
            
            const messageData = {
                type: req.body.type || 'message',
                content: req.body.content || '',
                priority: req.body.priority || 'normal',
                action_required: req.body.action_required || false
            };

            // Create notification file for Windsurf
            const notificationId = `gemini_${Date.now()}`;
            const notificationPath = path.join(__dirname, '../windsurf_notifications', `${notificationId}.json`);
            
            await fs.ensureDir(path.dirname(notificationPath));
            
            const notification = {
                type: 'gemini_message',
                title: `Gemini CLI - ${messageData.type.charAt(0).toUpperCase() + messageData.type.slice(1)}`,
                content: messageData.content,
                priority: messageData.priority,
                timestamp: new Date().toISOString(),
                action_required: messageData.action_required
            };

            await fs.writeJSON(notificationPath, notification);
            
            console.log(`[Gemini Phone] Message displayed: ${notificationPath}`);
            
            res.json({ status: 'received', message_id: notificationId });
            
        } catch (error) {
            console.error(`[Gemini Phone] Error handling message:`, error);
            res.status(500).json({ status: 'error', error: error.message });
        }
    }

    async handleGeminiReview(req, res) {
        try {
            console.log(`[Gemini Phone] Code review received from Gemini CLI`);
            
            const reviewData = {
                file: req.body.file || '',
                review: req.body.review || '',
                suggestions: req.body.suggestions || []
            };

            const notificationId = `review_${Date.now()}`;
            const notificationPath = path.join(__dirname, '../windsurf_notifications', `${notificationId}.json`);
            
            await fs.ensureDir(path.dirname(notificationPath));
            
            const notification = {
                type: 'code_review',
                title: `Code Review - ${reviewData.file}`,
                content: reviewData.review,
                suggestions: reviewData.suggestions,
                priority: 'high',
                timestamp: new Date().toISOString(),
                file: reviewData.file
            };

            await fs.writeJSON(notificationPath, notification);
            
            console.log(`[Gemini Phone] Review displayed: ${notificationPath}`);
            
            res.json({ status: 'review_received', review_id: notificationId });
            
        } catch (error) {
            console.error(`[Gemini Phone] Error handling review:`, error);
            res.status(500).json({ status: 'error', error: error.message });
        }
    }

    async handleGeminiSuggestion(req, res) {
        try {
            console.log(`[Gemini Phone] Suggestion received from Gemini CLI`);
            
            const suggestionData = {
                context: req.body.context || '',
                suggestion: req.body.suggestion || '',
                confidence: req.body.confidence || 0.8
            };

            const notificationId = `suggestion_${Date.now()}`;
            const notificationPath = path.join(__dirname, '../windsurf_notifications', `${notificationId}.json`);
            
            await fs.ensureDir(path.dirname(notificationPath));
            
            const notification = {
                type: 'suggestion',
                title: `Suggestion - ${suggestionData.context}`,
                content: suggestionData.suggestion,
                confidence: suggestionData.confidence,
                timestamp: new Date().toISOString()
            };

            await fs.writeJSON(notificationPath, notification);
            
            console.log(`[Gemini Phone] Suggestion displayed: ${notificationPath}`);
            
            res.json({ status: 'suggestion_received', suggestion_id: notificationId });
            
        } catch (error) {
            console.error(`[Gemini Phone] Error handling suggestion:`, error);
            res.status(500).json({ status: 'error', error: error.message });
        }
    }

    start() {
        this.app.listen(this.port, () => {
            console.log(`Bridge server running on port ${this.port}`);
            console.log(`WebSocket server running on port ${this.wsPort}`);
            console.log(`[Gemini Phone] Telephone lines open for Gemini CLI calls!`);
        });
    }
}

const server = new BridgeServer();
server.start();

module.exports = BridgeServer;
