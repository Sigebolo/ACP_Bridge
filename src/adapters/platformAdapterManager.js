const { v4: uuidv4 } = require('uuid');
const fs = require('fs-extra');
const path = require('path');
const GoogleCLIAdapter = require('./platforms/googleCLIAdapter');
const WindsurfAdapter = require('./platforms/windsurfAdapter');
const AntigravityAdapter = require('./platforms/antigravityAdapter');

class PlatformAdapterManager {
    constructor(statusManager, artifactManager) {
        this.statusManager = statusManager;
        this.artifactManager = artifactManager;
        this.platforms = new Map();
        this.tasks = new Map();
        this.adapters = new Map();
        this.dataPath = path.join(__dirname, '..', '..', 'data');
        
        this.initializeAdapters();
        this.ensureDataDirectory();
    }

    initializeAdapters() {
        this.adapters.set('google-cli', new GoogleCLIAdapter());
        this.adapters.set('windsurf', new WindsurfAdapter());
        this.adapters.set('antigravity', new AntigravityAdapter());
    }

    async ensureDataDirectory() {
        await fs.ensureDir(this.dataPath);
        await this.loadData();
    }

    async loadData() {
        try {
            const platformsPath = path.join(this.dataPath, 'platforms.json');
            const tasksPath = path.join(this.dataPath, 'tasks.json');
            
            if (await fs.pathExists(platformsPath)) {
                const platformsData = await fs.readJson(platformsPath);
                this.platforms = new Map(Object.entries(platformsData));
            }
            
            if (await fs.pathExists(tasksPath)) {
                const tasksData = await fs.readJson(tasksPath);
                this.tasks = new Map(Object.entries(tasksData));
            }
        } catch (error) {
            console.error('Error loading platform data:', error);
        }

        // Initialize adapters for loaded platforms
        for (const [id, platform] of this.platforms) {
            const adapter = this.adapters.get(platform.type);
            if (adapter) {
                try {
                    await adapter.initialize(platform);
                } catch (error) {
                    console.error(`Failed to initialize restored platform ${platform.name}:`, error);
                }
            }
        }
    }

    async saveData() {
        try {
            await fs.writeJson(
                path.join(this.dataPath, 'platforms.json'),
                Object.fromEntries(this.platforms),
                { spaces: 2 }
            );
            
            await fs.writeJson(
                path.join(this.dataPath, 'tasks.json'),
                Object.fromEntries(this.tasks),
                { spaces: 2 }
            );
        } catch (error) {
            console.error('Error saving platform data:', error);
        }
    }

    async registerPlatform(platformData) {
        const platform = {
            id: platformData.id || uuidv4(),
            name: platformData.name,
            type: platformData.type,
            description: platformData.description || '',
            capabilities: platformData.capabilities || [],
            status: 'active',
            config: platformData.config || {},
            endpoints: platformData.endpoints || {},
            credentials: platformData.credentials || {},
            metadata: platformData.metadata || {},
            registeredAt: new Date().toISOString(),
            lastSeen: new Date().toISOString(),
            stats: {
                tasksCompleted: 0,
                artifactsGenerated: 0,
                averageCompletionTime: 0
            }
        };

        this.platforms.set(platform.id, platform);
        await this.saveData();

        const adapter = this.adapters.get(platform.type);
        if (adapter) {
            try {
                await adapter.initialize(platform);
                console.log(`Platform ${platform.name} (${platform.type}) initialized successfully`);
            } catch (error) {
                console.error(`Failed to initialize platform ${platform.name}:`, error);
                platform.status = 'error';
                platform.error = error.message;
            }
        }

        return platform;
    }

    async getPlatforms(filters = {}) {
        let platforms = Array.from(this.platforms.values());

        if (filters.type) {
            platforms = platforms.filter(p => p.type === filters.type);
        }

        if (filters.status) {
            platforms = platforms.filter(p => p.status === filters.status);
        }

        return platforms;
    }

    async getPlatform(id) {
        return this.platforms.get(id);
    }

    async updatePlatform(id, updates) {
        const platform = this.platforms.get(id);
        if (!platform) {
            throw new Error(`Platform not found: ${id}`);
        }

        const updatedPlatform = {
            ...platform,
            ...updates,
            lastSeen: new Date().toISOString()
        };

        this.platforms.set(id, updatedPlatform);
        await this.saveData();

        return updatedPlatform;
    }

    async createTask(taskData) {
        const task = {
            id: uuidv4(),
            title: taskData.title,
            description: taskData.description,
            type: taskData.type || 'development',
            priority: taskData.priority || 'medium',
            status: 'pending',
            platformId: taskData.platformId,
            requirementId: taskData.requirementId || null,
            assignedTo: taskData.assignedTo || null,
            createdBy: taskData.createdBy || 'system',
            config: taskData.config || {},
            dependencies: taskData.dependencies || [],
            artifacts: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            startedAt: null,
            completedAt: null,
            estimatedTime: taskData.estimatedTime || null,
            actualTime: null,
            progress: 0,
            logs: []
        };

        this.tasks.set(task.id, task);
        await this.saveData();

        await this.statusManager.createTask(task.id, {
            type: 'platform_task',
            title: task.title,
            status: task.status,
            priority: task.priority,
            platformId: task.platformId
        });

        const platform = await this.getPlatform(task.platformId);
        const adapter = this.adapters.get(platform.type);
        
        if (adapter) {
            try {
                await adapter.assignTask(task);
            } catch (error) {
                console.error(`Failed to assign task to platform ${platform.name}:`, error);
                task.status = 'error';
                task.error = error.message;
                await this.saveData();
            }
        }

        return task;
    }

    async getTasks(platformId, filters = {}) {
        let tasks = Array.from(this.tasks.values());

        if (platformId) {
            tasks = tasks.filter(t => t.platformId === platformId);
        }

        if (filters.status) {
            tasks = tasks.filter(t => t.status === filters.status);
        }

        if (filters.type) {
            tasks = tasks.filter(t => t.type === filters.type);
        }

        if (filters.priority) {
            tasks = tasks.filter(t => t.priority === filters.priority);
        }

        return tasks.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    async getTask(id) {
        return this.tasks.get(id);
    }

    async updateTask(id, updates) {
        const task = this.tasks.get(id);
        if (!task) {
            throw new Error(`Task not found: ${id}`);
        }

        const updatedTask = {
            ...task,
            ...updates,
            updatedAt: new Date().toISOString()
        };

        if (updates.status === 'in_progress' && task.status !== 'in_progress') {
            updatedTask.startedAt = new Date().toISOString();
        }

        if (updates.status === 'completed' && task.status !== 'completed') {
            updatedTask.completedAt = new Date().toISOString();
            if (updatedTask.startedAt) {
                updatedTask.actualTime = new Date(updatedTask.completedAt) - new Date(updatedTask.startedAt);
            }
        }

        this.tasks.set(id, updatedTask);
        await this.saveData();

        await this.statusManager.updateTask(id, {
            status: updatedTask.status,
            progress: updatedTask.progress
        });

        return updatedTask;
    }

    async completeTask(platformId, completionData) {
        const { taskId, result, artifacts, logs } = completionData;
        
        const task = await this.getTask(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        if (task.platformId !== platformId) {
            throw new Error(`Task ${taskId} is not assigned to platform ${platformId}`);
        }

        const updatedTask = await this.updateTask(taskId, {
            status: 'completed',
            progress: 100,
            result: result,
            artifacts: artifacts || [],
            logs: logs || []
        });

        const platform = await this.getPlatform(platformId);
        const updatedPlatform = await this.updatePlatform(platformId, {
            stats: {
                ...platform.stats,
                tasksCompleted: platform.stats.tasksCompleted + 1,
                artifactsGenerated: platform.stats.artifactsGenerated + (artifacts ? artifacts.length : 0)
            }
        });

        if (artifacts && artifacts.length > 0) {
            for (const artifactData of artifacts) {
                await this.artifactManager.saveArtifact({
                    ...artifactData,
                    taskId: taskId,
                    platformId: platformId,
                    requirementId: task.requirementId
                });
            }
        }

        return {
            task: updatedTask,
            platform: updatedPlatform
        };
    }

    async getPlatformTasks(platformId) {
        return await this.getTasks(platformId);
    }

    async assignTaskToPlatform(taskData, platformId) {
        const platform = await this.getPlatform(platformId);
        if (!platform) {
            throw new Error(`Platform not found: ${platformId}`);
        }

        const task = await this.createTask({
            ...taskData,
            platformId: platformId
        });

        return task;
    }

    async getPlatformStatus(platformId) {
        const platform = await this.getPlatform(platformId);
        const tasks = await this.getTasks(platformId);

        const status = {
            platform: platform,
            tasks: {
                total: tasks.length,
                pending: tasks.filter(t => t.status === 'pending').length,
                inProgress: tasks.filter(t => t.status === 'in_progress').length,
                completed: tasks.filter(t => t.status === 'completed').length,
                failed: tasks.filter(t => t.status === 'failed').length
            },
            recentActivity: tasks.slice(0, 10)
        };

        return status;
    }

    async getAvailablePlatforms(taskType) {
        const platforms = await this.getPlatforms({ status: 'active' });
        
        return platforms.filter(platform => {
            return platform.capabilities.includes(taskType) || 
                   platform.capabilities.includes('general');
        });
    }
}

module.exports = PlatformAdapterManager;
