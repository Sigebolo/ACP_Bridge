const { v4: uuidv4 } = require('uuid');
const fs = require('fs-extra');
const path = require('path');
const crypto = require('crypto');

class ArtifactManager {
    constructor() {
        this.artifacts = new Map();
        this.storagePath = path.join(__dirname, '..', '..', 'artifacts');
        this.dataPath = path.join(__dirname, '..', '..', 'data');
        this.ensureDirectories();
    }

    async ensureDirectories() {
        await fs.ensureDir(this.storagePath);
        await fs.ensureDir(this.dataPath);
        await this.loadData();
    }

    async loadData() {
        try {
            const artifactsPath = path.join(this.dataPath, 'artifacts.json');
            if (await fs.pathExists(artifactsPath)) {
                const artifactsData = await fs.readJson(artifactsPath);
                this.artifacts = new Map(Object.entries(artifactsData));
            }
        } catch (error) {
            console.error('Error loading artifacts data:', error);
        }
    }

    async saveData() {
        try {
            await fs.writeJson(
                path.join(this.dataPath, 'artifacts.json'),
                Object.fromEntries(this.artifacts),
                { spaces: 2 }
            );
        } catch (error) {
            console.error('Error saving artifacts data:', error);
        }
    }

    async saveArtifact(artifactData) {
        const artifactId = artifactData.id || uuidv4();
        const timestamp = new Date().toISOString();
        
        let filePath = null;
        let fileHash = null;
        let fileSize = 0;

        if (artifactData.content) {
            filePath = await this.saveFileContent(artifactId, artifactData.content, artifactData.filename);
            fileHash = this.calculateHash(artifactData.content);
            fileSize = Buffer.byteLength(artifactData.content, 'utf8');
        } else if (artifactData.filePath) {
            const fileInfo = await this.copyExistingFile(artifactId, artifactData.filePath);
            filePath = fileInfo.path;
            fileHash = fileInfo.hash;
            fileSize = fileInfo.size;
        }

        const artifact = {
            id: artifactId,
            name: artifactData.name || `artifact_${artifactId}`,
            description: artifactData.description || '',
            type: artifactData.type || this.detectType(artifactData.filename || artifactData.name),
            filename: artifactData.filename || `artifact_${artifactId}`,
            filePath: filePath,
            fileHash: fileHash,
            fileSize: fileSize,
            taskId: artifactData.taskId || null,
            platformId: artifactData.platformId || null,
            requirementId: artifactData.requirementId || null,
            metadata: artifactData.metadata || {},
            tags: artifactData.tags || [],
            status: 'active',
            createdAt: timestamp,
            updatedAt: timestamp,
            accessedAt: timestamp,
            downloadCount: 0,
            version: artifactData.version || '1.0.0'
        };

        this.artifacts.set(artifactId, artifact);
        await this.saveData();

        console.log(`Artifact saved: ${artifactId} - ${artifact.name}`);
        return artifact;
    }

    async saveFileContent(artifactId, content, filename) {
        const extension = filename ? path.extname(filename) : '.txt';
        const filePath = path.join(this.storagePath, `${artifactId}${extension}`);
        
        await fs.writeFile(filePath, content, 'utf8');
        return filePath;
    }

    async copyExistingFile(artifactId, sourcePath) {
        const extension = path.extname(sourcePath);
        const filePath = path.join(this.storagePath, `${artifactId}${extension}`);
        
        await fs.copy(sourcePath, filePath);
        
        const stats = await fs.stat(filePath);
        const content = await fs.readFile(filePath);
        const hash = this.calculateHash(content);
        
        return {
            path: filePath,
            hash: hash,
            size: stats.size
        };
    }

    calculateHash(content) {
        return crypto.createHash('sha256').update(content).digest('hex');
    }

    detectType(filename) {
        const ext = path.extname(filename).toLowerCase();
        const typeMap = {
            '.txt': 'text',
            '.md': 'markdown',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.csv': 'csv',
            '.log': 'log',
            '.html': 'html',
            '.css': 'css',
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
            '.sql': 'sql',
            '.sh': 'shell',
            '.bat': 'batch',
            '.png': 'image',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.gif': 'image',
            '.svg': 'image',
            '.pdf': 'pdf',
            '.doc': 'document',
            '.docx': 'document',
            '.xls': 'spreadsheet',
            '.xlsx': 'spreadsheet',
            '.zip': 'archive',
            '.tar': 'archive',
            '.gz': 'archive'
        };

        return typeMap[ext] || 'binary';
    }

    async getArtifact(artifactId) {
        const artifact = this.artifacts.get(artifactId);
        if (!artifact) {
            throw new Error(`Artifact not found: ${artifactId}`);
        }

        artifact.accessedAt = new Date().toISOString();
        artifact.downloadCount += 1;
        await this.saveData();

        return artifact;
    }

    async getArtifacts(filters = {}) {
        let artifacts = Array.from(this.artifacts.values());

        if (filters.type) {
            artifacts = artifacts.filter(a => a.type === filters.type);
        }

        if (filters.taskId) {
            artifacts = artifacts.filter(a => a.taskId === filters.taskId);
        }

        if (filters.platformId) {
            artifacts = artifacts.filter(a => a.platformId === filters.platformId);
        }

        if (filters.requirementId) {
            artifacts = artifacts.filter(a => a.requirementId === filters.requirementId);
        }

        if (filters.status) {
            artifacts = artifacts.filter(a => a.status === filters.status);
        }

        if (filters.tags && filters.tags.length > 0) {
            artifacts = artifacts.filter(a => 
                filters.tags.some(tag => a.tags.includes(tag))
            );
        }

        if (filters.createdAfter) {
            const afterDate = new Date(filters.createdAfter);
            artifacts = artifacts.filter(a => new Date(a.createdAt) > afterDate);
        }

        if (filters.createdBefore) {
            const beforeDate = new Date(filters.createdBefore);
            artifacts = artifacts.filter(a => new Date(a.createdAt) < beforeDate);
        }

        if (filters.search) {
            const searchTerm = filters.search.toLowerCase();
            artifacts = artifacts.filter(a => 
                a.name.toLowerCase().includes(searchTerm) ||
                a.description.toLowerCase().includes(searchTerm)
            );
        }

        return artifacts.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    async getArtifactPath(artifactId) {
        const artifact = await this.getArtifact(artifactId);
        if (!artifact.filePath) {
            throw new Error(`Artifact ${artifactId} has no file path`);
        }

        if (!await fs.pathExists(artifact.filePath)) {
            throw new Error(`Artifact file not found: ${artifact.filePath}`);
        }

        return artifact.filePath;
    }

    async getArtifactContent(artifactId) {
        const filePath = await this.getArtifactPath(artifactId);
        return await fs.readFile(filePath, 'utf8');
    }

    async updateArtifact(artifactId, updates) {
        const artifact = this.artifacts.get(artifactId);
        if (!artifact) {
            throw new Error(`Artifact not found: ${artifactId}`);
        }

        const updatedArtifact = {
            ...artifact,
            ...updates,
            updatedAt: new Date().toISOString()
        };

        if (updates.content) {
            const filePath = await this.saveFileContent(artifactId, updates.content, artifact.filename);
            updatedArtifact.filePath = filePath;
            updatedArtifact.fileHash = this.calculateHash(updates.content);
            updatedArtifact.fileSize = Buffer.byteLength(updates.content, 'utf8');
        }

        this.artifacts.set(artifactId, updatedArtifact);
        await this.saveData();

        return updatedArtifact;
    }

    async deleteArtifact(artifactId) {
        const artifact = this.artifacts.get(artifactId);
        if (!artifact) {
            throw new Error(`Artifact not found: ${artifactId}`);
        }

        if (artifact.filePath && await fs.pathExists(artifact.filePath)) {
            await fs.remove(artifact.filePath);
        }

        this.artifacts.delete(artifactId);
        await this.saveData();

        return true;
    }

    async getArtifactsByTask(taskId) {
        return await this.getArtifacts({ taskId });
    }

    async getArtifactsByPlatform(platformId) {
        return await this.getArtifacts({ platformId });
    }

    async getArtifactsByRequirement(requirementId) {
        return await this.getArtifacts({ requirementId });
    }

    async getArtifactStatistics() {
        const artifacts = Array.from(this.artifacts.values());
        
        const stats = {
            total: artifacts.length,
            byType: {},
            byPlatform: {},
            byTask: {},
            totalSize: 0,
            averageSize: 0,
            downloadCounts: {
                total: 0,
                average: 0
            }
        };

        artifacts.forEach(artifact => {
            stats.byType[artifact.type] = (stats.byType[artifact.type] || 0) + 1;
            stats.totalSize += artifact.fileSize || 0;
            stats.downloadCounts.total += artifact.downloadCount || 0;
            
            if (artifact.platformId) {
                stats.byPlatform[artifact.platformId] = (stats.byPlatform[artifact.platformId] || 0) + 1;
            }
            
            if (artifact.taskId) {
                stats.byTask[artifact.taskId] = (stats.byTask[artifact.taskId] || 0) + 1;
            }
        });

        if (artifacts.length > 0) {
            stats.averageSize = stats.totalSize / artifacts.length;
            stats.downloadCounts.average = stats.downloadCounts.total / artifacts.length;
        }

        return stats;
    }

    async searchArtifacts(query) {
        const artifacts = await this.getArtifacts({ search: query });
        return artifacts;
    }

    async createArtifactBundle(artifactIds, bundleName) {
        const bundleId = uuidv4();
        const artifacts = [];
        
        for (const artifactId of artifactIds) {
            const artifact = await this.getArtifact(artifactId);
            artifacts.push(artifact);
        }

        const bundle = {
            id: bundleId,
            name: bundleName || `bundle_${bundleId}`,
            description: `Bundle containing ${artifacts.length} artifacts`,
            artifacts: artifacts.map(a => a.id),
            createdAt: new Date().toISOString(),
            totalSize: artifacts.reduce((sum, a) => sum + (a.fileSize || 0), 0),
            metadata: {
                artifactCount: artifacts.length,
                types: [...new Set(artifacts.map(a => a.type))]
            }
        };

        await this.saveArtifact({
            ...bundle,
            type: 'bundle',
            content: JSON.stringify(bundle, null, 2),
            filename: `${bundle.name}.json`
        });

        return bundle;
    }

    async validateArtifact(artifactId) {
        const artifact = await this.getArtifact(artifactId);
        
        if (!artifact.filePath) {
            return { valid: false, error: 'No file path' };
        }

        if (!await fs.pathExists(artifact.filePath)) {
            return { valid: false, error: 'File not found' };
        }

        try {
            const content = await fs.readFile(artifact.filePath);
            const currentHash = this.calculateHash(content);
            
            if (currentHash !== artifact.fileHash) {
                return { valid: false, error: 'File hash mismatch' };
            }

            return { valid: true };
        } catch (error) {
            return { valid: false, error: error.message };
        }
    }
}

module.exports = ArtifactManager;
