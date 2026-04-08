const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const fs = require('fs-extra');
const path = require('path');
const readline = require('readline');

class AntigravityConnector {
    constructor() {
        this.app = express();
        this.port = process.env.AG_PORT || 33335;
        
        // Define endpoints for communication with Bridge Server
        this.bridgeEndpoint = process.env.BRIDGE_URL || 'http://localhost:33333';
        
        // Path to store our persistent platform identity
        this.configPath = path.join(__dirname, '..', '.ag_connector_config.json');
        
        // This is local to wherever the connector is run 
        this.workspaceDir = path.join(__dirname, '..', 'workspace', 'antigravity_tasks');
        
        this.setupMiddleware();
        this.setupRoutes();
        this.ensureDirectories();
    }

    setupMiddleware() {
        this.app.use(bodyParser.json({ limit: '50mb', type: ['application/json', 'application/*+json', 'application/json;charset=utf-8', 'application/json; charset=utf-8'] }));
        this.app.use(bodyParser.urlencoded({ extended: true, limit: '50mb' }));
        
        this.app.use((req, res, next) => {
            console.log(`[Antigravity Connector] ${new Date().toISOString()} - ${req.method} ${req.path}`);
            next();
        });
    }

    setupRoutes() {
        // Health check endpoint (used by Bridge to ensure we are alive)
        this.app.get('/health', (req, res) => {
            res.json({ 
                status: 'healthy', 
                version: '1.0.0',
                timestamp: new Date().toISOString() 
            });
        });

        // 新增：心跳脉冲监听路由 (Pulse Endpoint)
        this.app.post('/pulse', (req, res) => {
            const pulse = req.body;
            console.log(`\n[BRIDGE] 💓 收到心跳脉冲!`);
            console.log(`    Agent: ${pulse.agent_id} | Status: ${pulse.status}`);
            console.log(`    Timestamp: ${pulse.timestamp}`);
            res.json({ success: true, message: 'Pulse received and logged.' });
        });

        // Receive task from Bridge
        this.app.post('/tasks', this.handleReceiveTask.bind(this));
        
        // Let Bridge poll for status (though we will also push completion)
        this.app.get('/tasks/:taskId', this.handleGetTaskStatus.bind(this));
        
        // Cancel task
        this.app.post('/tasks/:taskId/cancel', this.handleCancelTask.bind(this));
    }

    async ensureDirectories() {
        await fs.ensureDir(this.workspaceDir);
    }

    async handleReceiveTask(req, res) {
        try {
            const task = req.body;
            console.log(`\n[!] Received new task from Bridge: ${task.title}`);
            console.log(`    Task ID: ${task.id}`);
            
            // Format task as Markdown and save it so the Agent can read it easily
            const taskFilePath = path.join(this.workspaceDir, `${task.id}.md`);
            
            let markdownContent = `# Task: ${task.title}\n`;
            markdownContent += `**Type**: ${task.type} | **Priority**: ${task.priority}\n`;
            markdownContent += `**Received**: ${new Date().toISOString()}\n\n`;
            markdownContent += `## Description\n${task.description}\n\n`;
            
            if (task.requirements && task.requirements.length > 0) {
                markdownContent += `## Requirements\n`;
                for (const req of task.requirements) {
                    markdownContent += `- ${req}\n`;
                }
                markdownContent += `\n`;
            }
            
            if (task.files && task.files.length > 0) {
                markdownContent += `## Provided Context Files\n`;
                for (const file of task.files) {
                    markdownContent += `### ${file.name}\n`;
                    markdownContent += `\`\`\`\n${file.content}\n\`\`\`\n\n`;
                }
            }
            
            // Write with UTF-8 BOM so editors/Powershell definitely know it's UTF-8
            await fs.writeFile(taskFilePath, '\ufeff' + markdownContent, 'utf8');
            
            // Write a status tracker stub
            const statusFilePath = path.join(this.workspaceDir, `${task.id}_status.json`);
            await fs.writeJson(statusFilePath, {
                id: task.id,
                metadata: task.metadata,
                status: 'in_progress',
                progress: 0,
                updatedAt: new Date().toISOString()
            }, { spaces: 2 });
            
            console.log(`[v] Task written to: ${taskFilePath}`);
            console.log(`[i] Task archived. Waiting for Dialog Trigger from OpenClaw-Atom.`);
            
            res.json({ 
                success: true, 
                id: task.id,
                message: 'Task received and saved to disk.'
            });
            
        } catch (error) {
            console.error('[x] Error handling task:', error);
            res.status(500).json({ error: error.message });
        }
    }

    async handleGetTaskStatus(req, res) {
        try {
            const taskId = req.params.taskId;
            const statusFilePath = path.join(this.workspaceDir, `${taskId}_status.json`);
            
            if (await fs.pathExists(statusFilePath)) {
                const status = await fs.readJson(statusFilePath);
                res.json(status);
            } else {
                res.status(404).json({ error: 'Task status not found' });
            }
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    async handleCancelTask(req, res) {
        console.log(`[!] Bridge requested cancellation of task: ${req.params.taskId}`);
        // In a real implementation you'd flag the local task status as cancelled for the agent to stop
        res.json({ success: true, message: 'Cancellation acknowledged.' });
    }

    async registerWithBridge() {
        console.log(`Registering Antigravity Connector with Bridge Server at ${this.bridgeEndpoint}...`);
        
        try {
            // Check if we have a saved platformId
            let savedPlatformId = null;
            if (await fs.pathExists(this.configPath)) {
                const config = await fs.readJson(this.configPath);
                savedPlatformId = config.platformId;
                console.log(`[i] Found saved Platform ID: ${savedPlatformId}`);
            }

            const platformConfig = {
                id: savedPlatformId, // Bridge will reuse if it exists, otherwise create new
                name: 'Antigravity IDE',
                type: 'antigravity',
                description: 'Google Advanced Agentic Coding Assistant Node',
                capabilities: ['development', 'testing', 'code_analysis', 'refactoring', 'command_execution'],
                endpoints: {
                    api: `http://localhost:${this.port}`
                },
                config: {
                    autoConnect: true
                }
            };

            const response = await axios.post(`${this.bridgeEndpoint}/api/platform/register`, platformConfig, {
                timeout: 5000
            });
            
            this.platformId = response.data.platform.id;
            
            // Save it for next time
            await fs.writeJson(this.configPath, { platformId: this.platformId }, { spaces: 2 });
            
            console.log(`[v] Successfully registered with Bridge. Platform ID: ${this.platformId}`);
        } catch (error) {
            console.error(`[x] Failed to register with Bridge Server.`);
            if (error.code === 'ECONNREFUSED') {
                console.error(`    Is the Bridge Server running at ${this.bridgeEndpoint}?`);
            } else {
                console.error(`    Error: ${error.message}`);
            }
        }
    }

    startInteractiveCLI() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        console.log(`\n======================================================`);
        console.log(` Antigravity Connector CLI `);
        console.log(`======================================================`);
        console.log(`Commands:`);
        console.log(`  complete <taskId> [message]  - Mark a task as complete and push to Bridge`);
        console.log(`  status <taskId>              - Check local status of a task`);
        console.log(`  exit                         - Shutdown connector`);
        
        const promptUser = () => {
            rl.question('\nag> ', async (input) => {
                const args = input.trim().split(' ');
                const command = args[0].toLowerCase();
                
                switch(command) {
                    case 'exit':
                        console.log('Shutting down...');
                        process.exit(0);
                        break;
                        
                    case 'status': {
                        if(args.length < 2) {
                            console.log('Usage: status <taskId>');
                            break;
                        }
                        const taskId = args[1];
                        const statusPath = path.join(this.workspaceDir, `${taskId}_status.json`);
                        try {
                            if(await fs.pathExists(statusPath)) {
                                const stat = await fs.readJson(statusPath);
                                console.log(`Task ${taskId} is currently: ${stat.status} (Progress: ${stat.progress}%)`);
                            } else {
                                console.log(`Could not find status file for task: ${taskId}`);
                            }
                        } catch (e) {
                            console.log(`Error reading status: ${e.message}`);
                        }
                        break;
                    }
                        
                    case 'complete': {
                        if(args.length < 2) {
                            console.log('Usage: complete <taskId> [successMessage]');
                            break;
                        }
                        const taskId = args[1];
                        const msg = args.slice(2).join(' ') || 'Task successfully resolved by Antigravity.';
                        await this.pushTaskCompletion(taskId, msg);
                        break;
                    }
                        
                    case '':
                        break;
                        
                    default:
                        console.log(`Unknown command: ${command}`);
                }
                
                promptUser();
            });
        };
        
        promptUser();
    }

    async pushTaskCompletion(taskId, message) {
        if (!this.platformId) {
            console.log('[!] Cannot complete task: Not registered with Bridge.');
            return;
        }

        const statusPath = path.join(this.workspaceDir, `${taskId}_status.json`);
        
        try {
            if(await fs.pathExists(statusPath)) {
                // Update local status
                const stat = await fs.readJson(statusPath);
                stat.status = 'completed';
                stat.progress = 100;
                stat.updatedAt = new Date().toISOString();
                await fs.writeJson(statusPath, stat, { spaces: 2 });
            }

            console.log(`Pushing completion for task ${taskId} to Bridge...`);
            
            const payload = {
                taskId: taskId,
                result: {
                    status: 'success',
                    output: message
                },
                artifacts: [] // could load actual artifacts built by AG here
            };

            await axios.post(`${this.bridgeEndpoint}/api/platform/tasks/${this.platformId}/complete`, payload);
            console.log(`[v] Task ${taskId} successfully completed on the Bridge!`);
            
        } catch(error) {
            console.error(`[x] Failed to push complete status to bridge: ${error.message}`);
        }
    }

    start() {
        this.app.listen(this.port, () => {
            console.log(`\nAntigravity Connector listening locally on port ${this.port}`);
            console.log(`Workspace directory: ${this.workspaceDir}`);
            
            // Try to register with the Bridge service asynchronously
            setTimeout(() => this.registerWithBridge(), 1500);
            
            // Start the interactive CLI loop
            setTimeout(() => this.startInteractiveCLI(), 2000);
        });
    }
}

const connector = new AntigravityConnector();
connector.start();

module.exports = AntigravityConnector;
