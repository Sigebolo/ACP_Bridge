const fs = require('fs-extra');
const path = require('path');
const axios = require('axios');

class AntigravityAdapter {
    constructor() {
        this.name = 'antigravity';
        this.version = '1.0.0';
        this.config = {};
        this.workingDirectory = path.join(__dirname, '..', '..', '..', 'workspace', 'antigravity');
        this.connectorEndpoint = null;
    }

    async initialize(platform) {
        this.config = platform.config || {};
        this.platformId = platform.id;
        // The local Antigravity connector listens on 8081 by default
        this.connectorEndpoint = platform.endpoints?.api || 'http://localhost:8081';
        
        await fs.ensureDir(this.workingDirectory);
        
        console.log(`Antigravity Adapter initialized for platform ${platform.id}`);
        
        if (this.config.autoConnect) {
            await this.testConnection();
        }
    }

    async testConnection() {
        try {
            const response = await this.makeRequest('/health', 'GET');
            console.log('Antigravity connection test successful:', response);
            return true;
        } catch (error) {
            console.warn('Antigravity connector might not be running yet (this is normal if starting bridge first).');
            return false;
        }
    }

    async assignTask(task) {
        console.log(`Assigning task to Antigravity: ${task.title}`);
        
        try {
            const agTask = await this.convertToAntigravityTask(task);
            const response = await this.makeRequest('/tasks', 'POST', agTask);
            
            await this.saveTaskMapping(task.id, response.id || task.id);
            
            return {
                success: true,
                antigravityTaskId: response.id || task.id,
                message: 'Task assigned to Antigravity connector successfully'
            };
        } catch (error) {
            console.error('Failed to assign task to Antigravity connector:', error);
            throw error;
        }
    }

    async convertToAntigravityTask(task) {
        const agTask = {
            id: task.id,
            title: task.title,
            description: task.description,
            type: task.type,
            priority: task.priority,
            metadata: {
                originalTaskId: task.id,
                platformId: this.platformId,
                requirementId: task.requirementId,
                createdAt: task.createdAt
            },
            config: task.config || {},
            requirements: task.dependencies || []
        };

        if (task.config && task.config.files) {
            agTask.files = await this.prepareFiles(task.config.files);
        }

        return agTask;
    }

    async prepareFiles(files) {
        const preparedFiles = [];
        for (const file of files) {
            if (file.path) {
                try {
                    const content = await fs.readFile(file.path, 'utf8');
                    preparedFiles.push({
                        name: path.basename(file.path),
                        content: content,
                        originalPath: file.path
                    });
                } catch (e) {
                    console.warn(`Could not read file for task context: ${file.path}`);
                }
            } else if (file.content) {
                preparedFiles.push({
                    name: file.name || 'untitled',
                    content: file.content
                });
            }
        }
        return preparedFiles;
    }

    async saveTaskMapping(originalTaskId, agTaskId) {
        const mappingPath = path.join(this.workingDirectory, 'task_mappings.json');
        let mappings = {};
        
        if (await fs.pathExists(mappingPath)) {
            mappings = await fs.readJson(mappingPath);
        }
        
        mappings[originalTaskId] = agTaskId;
        await fs.writeJson(mappingPath, mappings, { spaces: 2 });
    }

    async getTaskMapping(taskId) {
        const mappingPath = path.join(this.workingDirectory, 'task_mappings.json');
        
        if (await fs.pathExists(mappingPath)) {
            const mappings = await fs.readJson(mappingPath);
            if (mappings[taskId]) {
                return {
                    originalTaskId: taskId,
                    antigravityTaskId: mappings[taskId]
                };
            }
        }
        return null;
    }

    async getTaskStatus(taskId) {
        try {
            const mapping = await this.getTaskMapping(taskId);
            if (!mapping) {
                throw new Error(`No mapping found for task ${taskId}`);
            }

            // Request status from Antigravity connector
            const response = await this.makeRequest(`/tasks/${mapping.antigravityTaskId}`, 'GET');
            return this.convertStatusFromAntigravity(response);
        } catch (error) {
            console.error('Failed to get task status from Antigravity connector:', error);
            throw error;
        }
    }

    convertStatusFromAntigravity(agStatus) {
        return {
            taskId: agStatus.id || agStatus.metadata?.originalTaskId,
            status: agStatus.status || 'unknown',
            progress: agStatus.progress || 0,
            result: agStatus.result,
            artifacts: agStatus.artifacts,
            logs: agStatus.logs,
            timestamp: agStatus.updatedAt || new Date().toISOString()
        };
    }

    async cancelTask(taskId) {
        try {
            const mapping = await this.getTaskMapping(taskId);
            if (!mapping) {
                throw new Error(`No mapping found for task ${taskId}`);
            }

            await this.makeRequest(`/tasks/${mapping.antigravityTaskId}/cancel`, 'POST');
            return { success: true };
        } catch (error) {
            console.error('Failed to cancel task in Antigravity:', error);
            throw error;
        }
    }

    async makeRequest(endpoint, method = 'GET', data = null) {
        const url = `${this.connectorEndpoint}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json'
        };

        const config = {
            method,
            url,
            headers,
            timeout: 5000 // Short timeout since it's local
        };

        if (data) {
            config.data = data;
        }

        try {
            const response = await axios(config);
            return response.data;
        } catch (error) {
            if (error.code === 'ECONNREFUSED') {
                throw new Error(`Antigravity connector is not running at ${this.connectorEndpoint}`);
            }
            if (error.response) {
                throw new Error(`Antigravity connector error: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
            }
            throw new Error(`Request error: ${error.message}`);
        }
    }

    async getStatus() {
        try {
            const response = await this.makeRequest('/health', 'GET');
            return {
                connected: true,
                status: response.status || 'healthy',
                version: response.version,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                connected: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async getCapabilities() {
        return [
            'development',
            'testing',
            'code_analysis',
            'refactoring',
            'debugging',
            'documentation',
            'command_execution',
            'general'
        ];
    }
}

module.exports = AntigravityAdapter;
