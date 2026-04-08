const { v4: uuidv4 } = require('uuid');
const fs = require('fs-extra');
const path = require('path');

class OpenClawAdapter {
    constructor(statusManager, artifactManager) {
        this.statusManager = statusManager;
        this.artifactManager = artifactManager;
        this.requirements = new Map();
        this.decisions = new Map();
        this.dataPath = path.join(__dirname, '..', '..', 'data');
        this.ensureDataDirectory();
    }

    async ensureDataDirectory() {
        await fs.ensureDir(this.dataPath);
        await this.loadData();
    }

    async loadData() {
        try {
            const requirementsPath = path.join(this.dataPath, 'requirements.json');
            const decisionsPath = path.join(this.dataPath, 'decisions.json');
            
            if (await fs.pathExists(requirementsPath)) {
                const requirementsData = await fs.readJson(requirementsPath);
                this.requirements = new Map(Object.entries(requirementsData));
            }
            
            if (await fs.pathExists(decisionsPath)) {
                const decisionsData = await fs.readJson(decisionsPath);
                this.decisions = new Map(Object.entries(decisionsData));
            }
        } catch (error) {
            console.error('Error loading OpenClaw data:', error);
        }
    }

    async saveData() {
        try {
            await fs.writeJson(
                path.join(this.dataPath, 'requirements.json'),
                Object.fromEntries(this.requirements),
                { spaces: 2 }
            );
            
            await fs.writeJson(
                path.join(this.dataPath, 'decisions.json'),
                Object.fromEntries(this.decisions),
                { spaces: 2 }
            );
        } catch (error) {
            console.error('Error saving OpenClaw data:', error);
        }
    }

    async createRequirement(requirementData) {
        const requirement = {
            id: uuidv4(),
            title: requirementData.title,
            description: requirementData.description,
            priority: requirementData.priority || 'medium',
            category: requirementData.category || 'general',
            requirements: requirementData.requirements || [],
            acceptanceCriteria: requirementData.acceptanceCriteria || [],
            status: 'pending',
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            assignedTo: requirementData.assignedTo || null,
            estimatedTime: requirementData.estimatedTime || null,
            tags: requirementData.tags || [],
            dependencies: requirementData.dependencies || []
        };

        this.requirements.set(requirement.id, requirement);
        await this.saveData();
        
        await this.statusManager.createTask(requirement.id, {
            type: 'requirement',
            title: requirement.title,
            status: 'pending',
            priority: requirement.priority
        });

        console.log(`Requirement created: ${requirement.id} - ${requirement.title}`);
        return requirement;
    }

    async getRequirements(filters = {}) {
        let requirements = Array.from(this.requirements.values());

        if (filters.status) {
            requirements = requirements.filter(req => req.status === filters.status);
        }

        if (filters.priority) {
            requirements = requirements.filter(req => req.priority === filters.priority);
        }

        if (filters.category) {
            requirements = requirements.filter(req => req.category === filters.category);
        }

        if (filters.assignedTo) {
            requirements = requirements.filter(req => req.assignedTo === filters.assignedTo);
        }

        return requirements.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    async getRequirement(id) {
        return this.requirements.get(id);
    }

    async updateRequirement(id, updates) {
        const requirement = this.requirements.get(id);
        if (!requirement) {
            throw new Error(`Requirement not found: ${id}`);
        }

        const updatedRequirement = {
            ...requirement,
            ...updates,
            updatedAt: new Date().toISOString()
        };

        this.requirements.set(id, updatedRequirement);
        await this.saveData();

        await this.statusManager.updateTask(id, {
            status: updatedRequirement.status,
            priority: updatedRequirement.priority
        });

        return updatedRequirement;
    }

    async makeDecision(decisionData) {
        const decision = {
            id: uuidv4(),
            title: decisionData.title,
            description: decisionData.description,
            context: decisionData.context || {},
            options: decisionData.options || [],
            selectedOption: decisionData.selectedOption,
            rationale: decisionData.rationale,
            impact: decisionData.impact || {},
            requirements: decisionData.requirements || [],
            status: 'active',
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
            madeBy: 'openclaw',
            confidence: decisionData.confidence || 'medium'
        };

        this.decisions.set(decision.id, decision);
        await this.saveData();

        await this.statusManager.createTask(decision.id, {
            type: 'decision',
            title: decision.title,
            status: 'active',
            priority: 'high'
        });

        console.log(`Decision made: ${decision.id} - ${decision.title}`);
        return decision;
    }

    async getDecisions(filters = {}) {
        let decisions = Array.from(this.decisions.values());

        if (filters.status) {
            decisions = decisions.filter(dec => dec.status === filters.status);
        }

        if (filters.madeBy) {
            decisions = decisions.filter(dec => dec.madeBy === filters.madeBy);
        }

        return decisions.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    async getDecision(id) {
        return this.decisions.get(id);
    }

    async updateDecision(id, updates) {
        const decision = this.decisions.get(id);
        if (!decision) {
            throw new Error(`Decision not found: ${id}`);
        }

        const updatedDecision = {
            ...decision,
            ...updates,
            updatedAt: new Date().toISOString()
        };

        this.decisions.set(id, updatedDecision);
        await this.saveData();

        await this.statusManager.updateTask(id, {
            status: updatedDecision.status
        });

        return updatedDecision;
    }

    async assignRequirement(requirementId, platformId) {
        const requirement = await this.getRequirement(requirementId);
        if (!requirement) {
            throw new Error(`Requirement not found: ${requirementId}`);
        }

        const updatedRequirement = await this.updateRequirement(requirementId, {
            assignedTo: platformId,
            status: 'assigned'
        });

        return updatedRequirement;
    }

    async getStatus() {
        const requirements = await this.getRequirements();
        const decisions = await this.getDecisions();

        const stats = {
            requirements: {
                total: requirements.length,
                pending: requirements.filter(r => r.status === 'pending').length,
                inProgress: requirements.filter(r => r.status === 'in_progress').length,
                completed: requirements.filter(r => r.status === 'completed').length,
                assigned: requirements.filter(r => r.status === 'assigned').length
            },
            decisions: {
                total: decisions.length,
                active: decisions.filter(d => d.status === 'active').length,
                implemented: decisions.filter(d => d.status === 'implemented').length,
                rejected: decisions.filter(d => d.status === 'rejected').length
            }
        };

        return {
            stats,
            recentRequirements: requirements.slice(0, 10),
            recentDecisions: decisions.slice(0, 10),
            timestamp: new Date().toISOString()
        };
    }

    async getDashboard() {
        const status = await this.getStatus();
        const requirements = await this.getRequirements();
        const decisions = await this.getDecisions();

        return {
            ...status,
            priorityBreakdown: {
                high: requirements.filter(r => r.priority === 'high').length,
                medium: requirements.filter(r => r.priority === 'medium').length,
                low: requirements.filter(r => r.priority === 'low').length
            },
            categoryBreakdown: requirements.reduce((acc, req) => {
                acc[req.category] = (acc[req.category] || 0) + 1;
                return acc;
            }, {}),
            recentActivity: [
                ...requirements.slice(0, 5).map(r => ({ ...r, type: 'requirement' })),
                ...decisions.slice(0, 5).map(d => ({ ...d, type: 'decision' }))
            ].sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)).slice(0, 10)
        };
    }
}

module.exports = OpenClawAdapter;
