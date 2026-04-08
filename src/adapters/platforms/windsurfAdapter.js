const fs = require('fs-extra');
const path = require('path');
const axios = require('axios');

class WindsurfAdapter {
    constructor() {
        this.name = 'windsurf';
        this.version = '1.0.0';
        this.config = {};
        this.workingDirectory = path.join(__dirname, '..', '..', '..', 'workspace', 'windsurf');
        this.apiEndpoint = null;
        this.apiKey = null;
    }

    async initialize(platform) {
        this.config = platform.config;
        this.platformId = platform.id;
        this.apiEndpoint = platform.endpoints?.api || 'http://localhost:8080';
        this.apiKey = platform.credentials?.apiKey;
        
        await fs.ensureDir(this.workingDirectory);
        
        console.log(`Windsurf Adapter initialized for platform ${platform.id}`);
        
        if (this.config.autoConnect) {
            await this.testConnection();
        }
    }

    async testConnection() {
        try {
            const response = await this.makeRequest('/health', 'GET');
            console.log('Windsurf connection test successful:', response);
            return true;
        } catch (error) {
            console.error('Windsurf connection test failed:', error);
            throw error;
        }
    }

    async assignTask(task) {
        console.log(`Assigning task to Windsurf: ${task.title}`);
        
        try {
            const windsurfTask = await this.convertToWindsurfTask(task);
            const response = await this.makeRequest('/tasks', 'POST', windsurfTask);
            
            await this.saveTaskMapping(task.id, response.id);
            
            return {
                success: true,
                windsurfTaskId: response.id,
                message: 'Task assigned to Windsurf successfully'
            };
        } catch (error) {
            console.error('Failed to assign task to Windsurf:', error);
            throw error;
        }
    }

    async convertToWindsurfTask(task) {
        const windsurfTask = {
            title: task.title,
            description: task.description,
            type: this.mapTaskType(task.type),
            priority: task.priority,
            metadata: {
                originalTaskId: task.id,
                platformId: this.platformId,
                requirementId: task.requirementId,
                createdAt: task.createdAt
            },
            config: task.config || {},
            requirements: task.dependencies || [],
            artifacts: {
                input: [],
                output: []
            }
        };

        if (task.config && task.config.files) {
            windsurfTask.files = await this.prepareFiles(task.config.files);
        }

        if (task.config && task.config.environment) {
            windsurfTask.environment = task.config.environment;
        }

        return windsurfTask;
    }

    mapTaskType(taskType) {
        const typeMapping = {
            'development': 'code',
            'testing': 'test',
            'deployment': 'deploy',
            'analysis': 'analyze',
            'documentation': 'docs',
            'refactoring': 'refactor',
            'debugging': 'debug'
        };

        return typeMapping[taskType] || 'code';
    }

    async prepareFiles(files) {
        const preparedFiles = [];
        
        for (const file of files) {
            if (file.path) {
                const content = await fs.readFile(file.path, 'utf8');
                preparedFiles.push({
                    name: path.basename(file.path),
                    content: content,
                    language: this.detectLanguage(file.path)
                });
            } else if (file.content) {
                preparedFiles.push({
                    name: file.name || 'untitled',
                    content: file.content,
                    language: file.language || 'text'
                });
            }
        }
        
        return preparedFiles;
    }

    detectLanguage(filePath) {
        const ext = path.extname(filePath).toLowerCase();
        const languageMap = {
            '.js': 'javascript',
            '.ts': 'typescript',
            '.py': 'python',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.less': 'less',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bat': 'batch'
        };

        return languageMap[ext] || 'text';
    }

    async saveTaskMapping(originalTaskId, windsurfTaskId) {
        const mappingPath = path.join(this.workingDirectory, 'task_mappings.json');
        let mappings = {};
        
        if (await fs.pathExists(mappingPath)) {
            mappings = await fs.readJson(mappingPath);
        }
        
        mappings[originalTaskId] = windsurfTaskId;
        await fs.writeJson(mappingPath, mappings, { spaces: 2 });
    }

    async getTaskStatus(taskId) {
        try {
            const mapping = await this.getTaskMapping(taskId);
            if (!mapping) {
                throw new Error(`No mapping found for task ${taskId}`);
            }

            const response = await this.makeRequest(`/tasks/${mapping.windsurfTaskId}`, 'GET');
            return this.convertStatusFromWindsurf(response);
        } catch (error) {
            console.error('Failed to get task status from Windsurf:', error);
            throw error;
        }
    }

    async getTaskMapping(taskId) {
        const mappingPath = path.join(this.workingDirectory, 'task_mappings.json');
        
        if (await fs.pathExists(mappingPath)) {
            const mappings = await fs.readJson(mappingPath);
            return {
                originalTaskId: taskId,
                windsurfTaskId: mappings[taskId]
            };
        }
        
        return null;
    }

    convertStatusFromWindsurf(windsurfStatus) {
        return {
            taskId: windsurfStatus.metadata.originalTaskId,
            status: this.mapStatus(windsurfStatus.status),
            progress: windsurfStatus.progress || 0,
            result: windsurfStatus.result,
            artifacts: windsurfStatus.artifacts,
            logs: windsurfStatus.logs,
            timestamp: windsurfStatus.updatedAt
        };
    }

    mapStatus(windsurfStatus) {
        const statusMapping = {
            'pending': 'pending',
            'running': 'in_progress',
            'completed': 'completed',
            'failed': 'failed',
            'cancelled': 'cancelled'
        };

        return statusMapping[windsurfStatus] || 'unknown';
    }

    async getTaskArtifacts(taskId) {
        try {
            const mapping = await this.getTaskMapping(taskId);
            if (!mapping) {
                throw new Error(`No mapping found for task ${taskId}`);
            }

            const response = await this.makeRequest(`/tasks/${mapping.windsurfTaskId}/artifacts`, 'GET');
            return response;
        } catch (error) {
            console.error('Failed to get task artifacts from Windsurf:', error);
            throw error;
        }
    }

    async downloadArtifact(artifactId, localPath) {
        try {
            const response = await this.makeRequest(`/artifacts/${artifactId}`, 'GET');
            
            if (response.content) {
                await fs.writeFile(localPath, response.content);
                return localPath;
            } else if (response.downloadUrl) {
                const fileResponse = await axios.get(response.downloadUrl, {
                    responseType: 'arraybuffer'
                });
                await fs.writeFile(localPath, fileResponse.data);
                return localPath;
            } else {
                throw new Error('No content or download URL found for artifact');
            }
        } catch (error) {
            console.error('Failed to download artifact from Windsurf:', error);
            throw error;
        }
    }

    async cancelTask(taskId) {
        try {
            const mapping = await this.getTaskMapping(taskId);
            if (!mapping) {
                throw new Error(`No mapping found for task ${taskId}`);
            }

            await this.makeRequest(`/tasks/${mapping.windsurfTaskId}/cancel`, 'POST');
            return { success: true };
        } catch (error) {
            console.error('Failed to cancel task in Windsurf:', error);
            throw error;
        }
    }

    async makeRequest(endpoint, method = 'GET', data = null) {
        const url = `${this.apiEndpoint}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json'
        };

        if (this.apiKey) {
            headers['Authorization'] = `Bearer ${this.apiKey}`;
        }

        const config = {
            method,
            url,
            headers,
            timeout: 30000
        };

        if (data) {
            config.data = data;
        }

        try {
            const response = await axios(config);
            return response.data;
        } catch (error) {
            if (error.response) {
                throw new Error(`Windsurf API error: ${error.response.status} - ${error.response.data.message || error.response.statusText}`);
            } else if (error.request) {
                throw new Error('No response from Windsurf API');
            } else {
                throw new Error(`Request error: ${error.message}`);
            }
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
            'code_generation',
            'code_review',
            'performance_analysis',
            'security_analysis'
        ];
    }

    async getProjectStructure(projectPath) {
        try {
            const response = await this.makeRequest('/projects/structure', 'POST', {
                path: projectPath
            });
            return response;
        } catch (error) {
            console.error('Failed to get project structure from Windsurf:', error);
            throw error;
        }
    }

    async analyzeCode(filePath) {
        try {
            const content = await fs.readFile(filePath, 'utf8');
            const response = await this.makeRequest('/code/analyze', 'POST', {
                file: {
                    name: path.basename(filePath),
                    content: content,
                    language: this.detectLanguage(filePath)
                }
            });
            return response;
        } catch (error) {
            console.error('Failed to analyze code with Windsurf:', error);
            throw error;
        }
    }
}

module.exports = WindsurfAdapter;
