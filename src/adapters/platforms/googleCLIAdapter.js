const { spawn } = require('child_process');
const fs = require('fs-extra');
const path = require('path');

class GoogleCLIAdapter {
    constructor() {
        this.name = 'google-cli';
        this.version = '1.0.0';
        this.config = {};
        this.workingDirectory = path.join(__dirname, '..', '..', '..', 'workspace', 'google-cli');
    }

    async initialize(platform) {
        this.config = platform.config;
        this.platformId = platform.id;
        
        await fs.ensureDir(this.workingDirectory);
        
        console.log(`Google CLI Adapter initialized for platform ${platform.id}`);
        
        if (this.config.auth && this.config.auth.credentials) {
            await this.authenticate();
        }
    }

    async authenticate() {
        try {
            const result = await this.executeCommand('gcloud auth list');
            console.log('Google CLI authentication status:', result);
        } catch (error) {
            console.error('Google CLI authentication failed:', error);
            throw error;
        }
    }

    async assignTask(task) {
        console.log(`Assigning task to Google CLI: ${task.title}`);
        
        try {
            const taskScript = await this.generateTaskScript(task);
            const scriptPath = path.join(this.workingDirectory, `task_${task.id}.sh`);
            
            await fs.writeFile(scriptPath, taskScript);
            await fs.chmod(scriptPath, '755');
            
            return {
                success: true,
                scriptPath: scriptPath,
                message: 'Task assigned to Google CLI successfully'
            };
        } catch (error) {
            console.error('Failed to assign task to Google CLI:', error);
            throw error;
        }
    }

    async generateTaskScript(task) {
        let script = '#!/bin/bash\n';
        script += `# Task: ${task.title}\n`;
        script += `# Task ID: ${task.id}\n`;
        script += `# Created: ${new Date().toISOString()}\n\n`;
        
        script += 'set -e\n\n';
        
        script += 'echo "Starting Google CLI task..."\n';
        script += `echo "Task: ${task.title}"\n\n`;
        
        switch (task.type) {
            case 'deployment':
                script += await this.generateDeploymentScript(task);
                break;
            case 'infrastructure':
                script += await this.generateInfrastructureScript(task);
                break;
            case 'monitoring':
                script += await this.generateMonitoringScript(task);
                break;
            case 'data_processing':
                script += await this.generateDataProcessingScript(task);
                break;
            default:
                script += await this.generateGenericScript(task);
        }
        
        script += '\necho "Task completed successfully"\n';
        
        return script;
    }

    async generateDeploymentScript(task) {
        const config = task.config || {};
        let script = '';
        
        if (config.project) {
            script += `gcloud config set project ${config.project}\n`;
        }
        
        if (config.service) {
            script += `echo "Deploying service: ${config.service}"\n`;
            
            if (config.region) {
                script += `gcloud config set compute/region ${config.region}\n`;
            }
            
            if (config.cluster) {
                script += `gcloud container clusters get-credentials ${config.cluster}\n`;
            }
            
            if (config.image) {
                script += `gcloud builds submit --tag gcr.io/${config.project}/${config.service}\n`;
                script += `kubectl set image deployment/${config.service} ${config.service}=gcr.io/${config.project}/${config.service}\n`;
            }
        }
        
        return script;
    }

    async generateInfrastructureScript(task) {
        const config = task.config || {};
        let script = '';
        
        if (config.project) {
            script += `gcloud config set project ${config.project}\n`;
        }
        
        if (config.resources) {
            for (const resource of config.resources) {
                switch (resource.type) {
                    case 'compute_instance':
                        script += `gcloud compute instances create ${resource.name} \\
                            --machine-type=${resource.machineType || 'e2-medium'} \\
                            --zone=${resource.zone || 'us-central1-a'} \\
                            --image-family=${resource.imageFamily || 'debian-11'} \\
                            --image-project=${resource.imageProject || 'debian-cloud'}\n`;
                        break;
                    case 'storage_bucket':
                        script += `gsutil mb gs://${resource.name}\n`;
                        if (resource.location) {
                            script += `gsutil location -l ${resource.location} gs://${resource.name}\n`;
                        }
                        break;
                    case 'sql_instance':
                        script += `gcloud sql instances create ${resource.name} \\
                            --database-version=${resource.version || 'POSTGRES_13'} \\
                            --tier=${resource.tier || 'db-f1-micro'} \\
                            --region=${resource.region || 'us-central1'}\n`;
                        break;
                }
            }
        }
        
        return script;
    }

    async generateMonitoringScript(task) {
        const config = task.config || {};
        let script = '';
        
        if (config.project) {
            script += `gcloud config set project ${config.project}\n`;
        }
        
        if (config.metrics) {
            script += 'echo "Collecting metrics..."\n';
            
            for (const metric of config.metrics) {
                switch (metric.type) {
                    case 'compute_instances':
                        script += `gcloud compute instances list --format="table(name,machineType,status,zone)"\n`;
                        break;
                    case 'sql_instances':
                        script += `gcloud sql instances list --format="table(name,databaseVersion,region,state)"\n`;
                        break;
                    case 'storage_buckets':
                        script += `gsutil ls\n`;
                        break;
                    case 'logs':
                        if (metric.filter) {
                            script += `gcloud logging read "${metric.filter}" --limit=50 --format="table(timestamp,severity,textPayload)"\n`;
                        }
                        break;
                }
            }
        }
        
        return script;
    }

    async generateDataProcessingScript(task) {
        const config = task.config || {};
        let script = '';
        
        if (config.project) {
            script += `gcloud config set project ${config.project}\n`;
        }
        
        if (config.dataset) {
            script += `echo "Processing dataset: ${config.dataset}"\n`;
            
            if (config.bigquery) {
                script += `bq query --use_legacy_sql=false "${config.bigquery.query}"\n`;
            }
            
            if (config.dataproc) {
                script += `gcloud dataproc jobs submit spark \\
                    --cluster=${config.dataproc.cluster} \\
                    --region=${config.dataproc.region} \\
                    --class=${config.dataproc.class} \\
                    ${config.dataproc.jar || ''}\n`;
            }
            
            if (config.dataflow) {
                script += `gcloud dataflow jobs run ${config.dataflow.jobName} \\
                    --region=${config.dataflow.region} \\
                    --gcs-location=${config.dataflow.templatePath} \\
                    --parameters=${config.dataflow.parameters || ''}\n`;
            }
        }
        
        return script;
    }

    async generateGenericScript(task) {
        let script = '';
        
        if (task.config && task.config.commands) {
            for (const command of task.config.commands) {
                script += `${command}\n`;
            }
        } else {
            script = `echo "Executing generic task: ${task.title}"\n`;
            script += `echo "Description: ${task.description}"\n`;
        }
        
        return script;
    }

    async executeTask(taskId) {
        const scriptPath = path.join(this.workingDirectory, `task_${taskId}.sh`);
        
        if (!await fs.pathExists(scriptPath)) {
            throw new Error(`Task script not found: ${scriptPath}`);
        }
        
        try {
            const result = await this.executeCommand(`bash ${scriptPath}`);
            return {
                success: true,
                output: result,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async executeCommand(command) {
        return new Promise((resolve, reject) => {
            const child = spawn(command, [], {
                shell: true,
                cwd: this.workingDirectory,
                env: { ...process.env, ...this.config.environment }
            });
            
            let stdout = '';
            let stderr = '';
            
            child.stdout.on('data', (data) => {
                stdout += data.toString();
            });
            
            child.stderr.on('data', (data) => {
                stderr += data.toString();
            });
            
            child.on('close', (code) => {
                if (code === 0) {
                    resolve(stdout);
                } else {
                    reject(new Error(`Command failed with code ${code}: ${stderr}`));
                }
            });
            
            child.on('error', (error) => {
                reject(error);
            });
        });
    }

    async getStatus() {
        try {
            const result = await this.executeCommand('gcloud auth list');
            return {
                authenticated: true,
                details: result,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                authenticated: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    async getCapabilities() {
        return [
            'deployment',
            'infrastructure',
            'monitoring',
            'data_processing',
            'bigquery',
            'compute_engine',
            'storage',
            'sql',
            'container_engine',
            'dataflow',
            'dataproc'
        ];
    }
}

module.exports = GoogleCLIAdapter;
