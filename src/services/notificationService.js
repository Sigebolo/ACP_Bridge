const { v4: uuidv4 } = require('uuid');
const fs = require('fs-extra');
const path = require('path');
const EventEmitter = require('events');

class NotificationService extends EventEmitter {
    constructor() {
        super();
        this.subscriptions = new Map();
        this.notifications = new Map();
        this.dataPath = path.join(__dirname, '..', '..', 'data');
        this.ensureDataDirectory();
    }

    async ensureDataDirectory() {
        await fs.ensureDir(this.dataPath);
        await this.loadData();
    }

    async loadData() {
        try {
            const notificationsPath = path.join(this.dataPath, 'notifications.json');
            if (await fs.pathExists(notificationsPath)) {
                const notificationsData = await fs.readJson(notificationsPath);
                this.notifications = new Map(Object.entries(notificationsData));
            }
        } catch (error) {
            console.error('Error loading notifications data:', error);
        }
    }

    async saveData() {
        try {
            await fs.writeJson(
                path.join(this.dataPath, 'notifications.json'),
                Object.fromEntries(this.notifications),
                { spaces: 2 }
            );
        } catch (error) {
            console.error('Error saving notifications data:', error);
        }
    }

    subscribe(clientId, websocket, filters = {}) {
        const subscription = {
            id: uuidv4(),
            clientId: clientId,
            websocket: websocket,
            filters: filters,
            subscribedAt: new Date().toISOString(),
            lastActivity: new Date().toISOString(),
            active: true
        };

        this.subscriptions.set(clientId, subscription);
        
        console.log(`Client subscribed: ${clientId} with filters:`, filters);
        
        return subscription;
    }

    unsubscribe(clientId) {
        const subscription = this.subscriptions.get(clientId);
        if (subscription) {
            subscription.active = false;
            this.subscriptions.delete(clientId);
            console.log(`Client unsubscribed: ${clientId}`);
        }
    }

    async createNotification(type, data, priority = 'normal') {
        const notification = {
            id: uuidv4(),
            type: type,
            data: data,
            priority: priority,
            timestamp: new Date().toISOString(),
            read: false,
            metadata: {
                source: 'bridge-service',
                version: '1.0.0'
            }
        };

        this.notifications.set(notification.id, notification);
        await this.saveData();
        
        return notification;
    }

    async broadcast(type, data, priority = 'normal') {
        const notification = await this.createNotification(type, data, priority);
        
        let sentCount = 0;
        let failedCount = 0;

        for (const [clientId, subscription] of this.subscriptions) {
            if (subscription.active && this.shouldSendNotification(subscription, notification)) {
                try {
                    const message = {
                        type: 'notification',
                        notification: notification
                    };

                    subscription.websocket.send(JSON.stringify(message));
                    subscription.lastActivity = new Date().toISOString();
                    sentCount++;
                } catch (error) {
                    console.error(`Failed to send notification to client ${clientId}:`, error);
                    failedCount++;
                    
                    if (error.code === 'ECONNRESET' || error.code === 'EPIPE') {
                        this.unsubscribe(clientId);
                    }
                }
            }
        }

        console.log(`Broadcast notification ${type}: sent to ${sentCount} clients, ${failedCount} failed`);
        
        this.emit('notificationBroadcasted', {
            notification,
            sentCount,
            failedCount
        });

        return {
            notification,
            sentCount,
            failedCount
        };
    }

    shouldSendNotification(subscription, notification) {
        const filters = subscription.filters;
        
        if (!filters || Object.keys(filters).length === 0) {
            return true;
        }

        if (filters.types && !filters.types.includes(notification.type)) {
            return false;
        }

        if (filters.priority && filters.priority !== notification.priority) {
            return false;
        }

        if (filters.minPriority && this.getPriorityLevel(notification.priority) < this.getPriorityLevel(filters.minPriority)) {
            return false;
        }

        if (filters.source && notification.metadata.source !== filters.source) {
            return false;
        }

        if (filters.dataFilters) {
            for (const [key, value] of Object.entries(filters.dataFilters)) {
                if (notification.data[key] !== value) {
                    return false;
                }
            }
        }

        return true;
    }

    getPriorityLevel(priority) {
        const levels = {
            'low': 1,
            'normal': 2,
            'high': 3,
            'critical': 4
        };
        return levels[priority] || 2;
    }

    async sendToClient(clientId, type, data, priority = 'normal') {
        const subscription = this.subscriptions.get(clientId);
        if (!subscription || !subscription.active) {
            throw new Error(`Client not found or inactive: ${clientId}`);
        }

        const notification = await this.createNotification(type, data, priority);
        
        try {
            const message = {
                type: 'notification',
                notification: notification
            };

            subscription.websocket.send(JSON.stringify(message));
            subscription.lastActivity = new Date().toISOString();
            
            return { success: true, notification };
        } catch (error) {
            console.error(`Failed to send notification to client ${clientId}:`, error);
            throw error;
        }
    }

    async getNotifications(filters = {}) {
        let notifications = Array.from(this.notifications.values());

        if (filters.type) {
            notifications = notifications.filter(n => n.type === filters.type);
        }

        if (filters.priority) {
            notifications = notifications.filter(n => n.priority === filters.priority);
        }

        if (filters.read !== undefined) {
            notifications = notifications.filter(n => n.read === filters.read);
        }

        if (filters.source) {
            notifications = notifications.filter(n => n.metadata.source === filters.source);
        }

        if (filters.createdAfter) {
            const afterDate = new Date(filters.createdAfter);
            notifications = notifications.filter(n => new Date(n.timestamp) > afterDate);
        }

        if (filters.createdBefore) {
            const beforeDate = new Date(filters.createdBefore);
            notifications = notifications.filter(n => new Date(n.timestamp) < beforeDate);
        }

        return notifications.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    }

    async markAsRead(notificationId) {
        const notification = this.notifications.get(notificationId);
        if (!notification) {
            throw new Error(`Notification not found: ${notificationId}`);
        }

        notification.read = true;
        await this.saveData();

        return notification;
    }

    async markAllAsRead(clientId) {
        let markedCount = 0;
        
        for (const [id, notification] of this.notifications) {
            if (!notification.read) {
                notification.read = true;
                markedCount++;
            }
        }
        
        if (markedCount > 0) {
            await this.saveData();
        }

        return markedCount;
    }

    async deleteNotification(notificationId) {
        const notification = this.notifications.get(notificationId);
        if (!notification) {
            throw new Error(`Notification not found: ${notificationId}`);
        }

        this.notifications.delete(notificationId);
        await this.saveData();

        return true;
    }

    async clearOldNotifications(olderThanDays = 30) {
        const cutoffDate = new Date();
        cutoffDate.setDate(cutoffDate.getDate() - olderThanDays);
        
        let deletedCount = 0;
        
        for (const [id, notification] of this.notifications) {
            if (new Date(notification.timestamp) < cutoffDate) {
                this.notifications.delete(id);
                deletedCount++;
            }
        }
        
        if (deletedCount > 0) {
            await this.saveData();
        }

        return deletedCount;
    }

    getActiveSubscriptions() {
        const activeSubscriptions = [];
        
        for (const [clientId, subscription] of this.subscriptions) {
            if (subscription.active) {
                activeSubscriptions.push({
                    clientId: subscription.clientId,
                    subscribedAt: subscription.subscribedAt,
                    lastActivity: subscription.lastActivity,
                    filters: subscription.filters
                });
            }
        }

        return activeSubscriptions;
    }

    getSubscriptionStats() {
        const total = this.subscriptions.size;
        let active = 0;
        
        for (const subscription of this.subscriptions.values()) {
            if (subscription.active) {
                active++;
            }
        }

        return {
            total,
            active,
            inactive: total - active
        };
    }

    async getNotificationStats() {
        const notifications = Array.from(this.notifications.values());
        
        const stats = {
            total: notifications.length,
            read: notifications.filter(n => n.read).length,
            unread: notifications.filter(n => !n.read).length,
            byType: {},
            byPriority: {}
        };

        notifications.forEach(notification => {
            stats.byType[notification.type] = (stats.byType[notification.type] || 0) + 1;
            stats.byPriority[notification.priority] = (stats.byPriority[notification.priority] || 0) + 1;
        });

        return stats;
    }

    async createSystemNotification(message, priority = 'normal') {
        return await this.broadcast('system', {
            message: message,
            timestamp: new Date().toISOString()
        }, priority);
    }

    async createRequirementNotification(requirement, action) {
        return await this.broadcast('requirement_updated', {
            requirement: requirement,
            action: action,
            timestamp: new Date().toISOString()
        }, 'high');
    }

    async createTaskNotification(task, action) {
        return await this.broadcast('task_updated', {
            task: task,
            action: action,
            timestamp: new Date().toISOString()
        }, 'normal');
    }

    async createArtifactNotification(artifact, action) {
        return await this.broadcast('artifact_updated', {
            artifact: artifact,
            action: action,
            timestamp: new Date().toISOString()
        }, 'normal');
    }

    async createPlatformNotification(platform, action) {
        return await this.broadcast('platform_updated', {
            platform: platform,
            action: action,
            timestamp: new Date().toISOString()
        }, 'high');
    }

    async createDecisionNotification(decision, action) {
        return await this.broadcast('decision_updated', {
            decision: decision,
            action: action,
            timestamp: new Date().toISOString()
        }, 'high');
    }

    async createErrorNotification(error, context = {}) {
        return await this.broadcast('error', {
            error: error.message || error,
            stack: error.stack,
            context: context,
            timestamp: new Date().toISOString()
        }, 'critical');
    }

    cleanupInactiveSubscriptions(timeoutMinutes = 30) {
        const cutoffTime = new Date();
        cutoffTime.setMinutes(cutoffTime.getMinutes() - timeoutMinutes);
        
        let cleanedCount = 0;
        
        for (const [clientId, subscription] of this.subscriptions) {
            if (new Date(subscription.lastActivity) < cutoffTime) {
                this.unsubscribe(clientId);
                cleanedCount++;
            }
        }

        if (cleanedCount > 0) {
            console.log(`Cleaned up ${cleanedCount} inactive subscriptions`);
        }

        return cleanedCount;
    }
}

module.exports = NotificationService;
