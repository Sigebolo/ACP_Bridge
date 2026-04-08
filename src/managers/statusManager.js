const { v4: uuidv4 } = require('uuid');
const fs = require('fs-extra');
const path = require('path');
const EventEmitter = require('events');

class StatusManager extends EventEmitter {
    constructor() {
        super();
        this.tasks = new Map();
        this.globalStatus = {
            totalTasks: 0,
            activeTasks: 0,
            completedTasks: 0,
            failedTasks: 0,
            lastUpdated: new Date().toISOString()
        };
        this.dataPath = path.join(__dirname, '..', '..', 'data');
        this.ensureDataDirectory();
    }

    async ensureDataDirectory() {
        await fs.ensureDir(this.dataPath);
        await this.loadData();
    }

    async loadData() {
        try {
            const tasksPath = path.join(this.dataPath, 'status_tasks.json');
            const globalStatusPath = path.join(this.dataPath, 'global_status.json');
            
            if (await fs.pathExists(tasksPath)) {
                const tasksData = await fs.readJson(tasksPath);
                this.tasks = new Map(Object.entries(tasksData));
            }
            
            if (await fs.pathExists(globalStatusPath)) {
                const globalStatusData = await fs.readJson(globalStatusPath);
                this.globalStatus = globalStatusData;
            }
        } catch (error) {
            console.error('Error loading status data:', error);
        }
    }

    async saveData() {
        try {
            await fs.writeJson(
                path.join(this.dataPath, 'status_tasks.json'),
                Object.fromEntries(this.tasks),
                { spaces: 2 }
            );
            
            await fs.writeJson(
                path.join(this.dataPath, 'global_status.json'),
                this.globalStatus,
                { spaces: 2 }
            );
        } catch (error) {
            console.error('Error saving status data:', error);
        }
    }

    async createTask(taskId, taskData) {
        const task = {
            id: taskId,
            type: taskData.type || 'general',
            title: taskData.title,
            status: taskData.status || 'pending',
            priority: taskData.priority || 'medium',
            platformId: taskData.platformId || null,
            requirementId: taskData.requirementId || null,
            progress: 0,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            startedAt: null,
            completedAt: null,
            metadata: taskData.metadata || {},
            history: [
                {
                    timestamp: new Date().toISOString(),
                    status: 'pending',
                    message: 'Task created'
                }
            ]
        };

        this.tasks.set(taskId, task);
        await this.updateGlobalStatus();
        await this.saveData();
        
        this.emit('taskCreated', task);
        
        console.log(`Status task created: ${taskId} - ${task.title}`);
        return task;
    }

    async updateTask(taskId, updates) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        const previousStatus = task.status;
        const previousProgress = task.progress;

        const updatedTask = {
            ...task,
            ...updates,
            updatedAt: new Date().toISOString()
        };

        if (updates.status && updates.status !== previousStatus) {
            updatedTask.history.push({
                timestamp: new Date().toISOString(),
                status: updates.status,
                message: updates.statusMessage || `Status changed from ${previousStatus} to ${updates.status}`
            });

            if (updates.status === 'in_progress' && previousStatus !== 'in_progress') {
                updatedTask.startedAt = new Date().toISOString();
            }

            if (updates.status === 'completed' && previousStatus !== 'completed') {
                updatedTask.completedAt = new Date().toISOString();
                updatedTask.progress = 100;
            }
        }

        if (updates.progress !== undefined && updates.progress !== previousProgress) {
            updatedTask.history.push({
                timestamp: new Date().toISOString(),
                status: updatedTask.status,
                progress: updates.progress,
                message: `Progress updated to ${updates.progress}%`
            });
        }

        this.tasks.set(taskId, updatedTask);
        await this.updateGlobalStatus();
        await this.saveData();
        
        this.emit('taskUpdated', updatedTask);
        
        return updatedTask;
    }

    async getTask(taskId) {
        return this.tasks.get(taskId);
    }

    async getTasks(filters = {}) {
        let tasks = Array.from(this.tasks.values());

        if (filters.status) {
            tasks = tasks.filter(task => task.status === filters.status);
        }

        if (filters.type) {
            tasks = tasks.filter(task => task.type === filters.type);
        }

        if (filters.priority) {
            tasks = tasks.filter(task => task.priority === filters.priority);
        }

        if (filters.platformId) {
            tasks = tasks.filter(task => task.platformId === filters.platformId);
        }

        if (filters.requirementId) {
            tasks = tasks.filter(task => task.requirementId === filters.requirementId);
        }

        if (filters.createdAfter) {
            const afterDate = new Date(filters.createdAfter);
            tasks = tasks.filter(task => new Date(task.createdAt) > afterDate);
        }

        if (filters.createdBefore) {
            const beforeDate = new Date(filters.createdBefore);
            tasks = tasks.filter(task => new Date(task.createdAt) < beforeDate);
        }

        return tasks.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
    }

    async deleteTask(taskId) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        this.tasks.delete(taskId);
        await this.updateGlobalStatus();
        await this.saveData();
        
        this.emit('taskDeleted', { taskId, task });
        
        return true;
    }

    async updateGlobalStatus() {
        const tasks = Array.from(this.tasks.values());
        
        this.globalStatus = {
            totalTasks: tasks.length,
            activeTasks: tasks.filter(t => t.status === 'in_progress').length,
            completedTasks: tasks.filter(t => t.status === 'completed').length,
            failedTasks: tasks.filter(t => t.status === 'failed').length,
            pendingTasks: tasks.filter(t => t.status === 'pending').length,
            lastUpdated: new Date().toISOString()
        };

        this.emit('globalStatusUpdated', this.globalStatus);
    }

    async getGlobalStatus() {
        await this.updateGlobalStatus();
        return this.globalStatus;
    }

    async getTaskHistory(taskId) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        return task.history;
    }

    async addTaskHistory(taskId, historyEntry) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        const entry = {
            timestamp: new Date().toISOString(),
            ...historyEntry
        };

        task.history.push(entry);
        task.updatedAt = entry.timestamp;

        this.tasks.set(taskId, task);
        await this.saveData();
        
        this.emit('taskHistoryAdded', { taskId, entry });
        
        return entry;
    }

    async getTasksByPlatform(platformId) {
        return await this.getTasks({ platformId });
    }

    async getTasksByRequirement(requirementId) {
        return await this.getTasks({ requirementId });
    }

    async getTaskStatistics() {
        const tasks = Array.from(this.tasks.values());
        
        const stats = {
            byStatus: {},
            byType: {},
            byPriority: {},
            byPlatform: {},
            averageCompletionTime: 0,
            completionRate: 0
        };

        tasks.forEach(task => {
            stats.byStatus[task.status] = (stats.byStatus[task.status] || 0) + 1;
            stats.byType[task.type] = (stats.byType[task.type] || 0) + 1;
            stats.byPriority[task.priority] = (stats.byPriority[task.priority] || 0) + 1;
            
            if (task.platformId) {
                stats.byPlatform[task.platformId] = (stats.byPlatform[task.platformId] || 0) + 1;
            }
        });

        const completedTasks = tasks.filter(t => t.status === 'completed' && t.startedAt && t.completedAt);
        if (completedTasks.length > 0) {
            const totalTime = completedTasks.reduce((sum, task) => {
                return sum + (new Date(task.completedAt) - new Date(task.startedAt));
            }, 0);
            stats.averageCompletionTime = totalTime / completedTasks.length;
        }

        if (tasks.length > 0) {
            stats.completionRate = (stats.byStatus.completed || 0) / tasks.length * 100;
        }

        return stats;
    }

    async getActiveTasks() {
        return await this.getTasks({ status: 'in_progress' });
    }

    async getPendingTasks() {
        return await this.getTasks({ status: 'pending' });
    }

    async getCompletedTasks() {
        return await this.getTasks({ status: 'completed' });
    }

    async getFailedTasks() {
        return await this.getTasks({ status: 'failed' });
    }

    async retryTask(taskId) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        if (task.status !== 'failed') {
            throw new Error(`Cannot retry task with status: ${task.status}`);
        }

        return await this.updateTask(taskId, {
            status: 'pending',
            progress: 0,
            startedAt: null,
            completedAt: null,
            statusMessage: 'Task queued for retry'
        });
    }

    async cancelTask(taskId) {
        const task = this.tasks.get(taskId);
        if (!task) {
            throw new Error(`Task not found: ${taskId}`);
        }

        if (['completed', 'failed'].includes(task.status)) {
            throw new Error(`Cannot cancel task with status: ${task.status}`);
        }

        return await this.updateTask(taskId, {
            status: 'cancelled',
            statusMessage: 'Task cancelled by user'
        });
    }
}

module.exports = StatusManager;
