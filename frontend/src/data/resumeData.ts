export interface Skill {
  id: string;
  name: string;
  category: 'cloud' | 'devops' | 'backend' | 'frontend' | 'database';
  cloud?: 'aws' | 'gcp' | 'azure';
  proficiency: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  usageCount: number;
  evidence?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  technologies: string[];
  awsServices: string[];
  hasCI: boolean;
  hasIaC: boolean;
  evidenceLinks: {
    repo?: string;
    demo?: string;
    pipeline?: string;
    dashboard?: string;
  };
  date: string;
}

export interface ADR {
  id: string;
  title: string;
  decision: string;
  context: string;
  options: string[];
  tradeoffs: string[];
  awsServices: string[];
  date: string;
}

export interface CVVersion {
  version: string;
  date: string;
  changes: string[];
  milestone: string;
}

export const skills: Skill[] = [
  { id: '1', name: 'AWS Lambda', category: 'cloud', cloud: 'aws', proficiency: 'advanced', usageCount: 12, evidence: '/evidence/lambda' },
  { id: '2', name: 'DynamoDB', category: 'database', cloud: 'aws', proficiency: 'advanced', usageCount: 8, evidence: '/evidence/dynamodb' },
  { id: '3', name: 'API Gateway', category: 'cloud', cloud: 'aws', proficiency: 'advanced', usageCount: 10, evidence: '/evidence/api-gateway' },
  { id: '4', name: 'Terraform', category: 'devops', proficiency: 'intermediate', usageCount: 6, evidence: '/evidence/terraform' },
  { id: '5', name: 'GitHub Actions', category: 'devops', proficiency: 'advanced', usageCount: 15, evidence: '/evidence/github-actions' },
  { id: '6', name: 'CloudWatch', category: 'cloud', cloud: 'aws', proficiency: 'intermediate', usageCount: 9, evidence: '/evidence/cloudwatch' },
  { id: '7', name: 'S3', category: 'cloud', cloud: 'aws', proficiency: 'expert', usageCount: 14, evidence: '/evidence/s3' },
  { id: '8', name: 'CloudFront', category: 'cloud', cloud: 'aws', proficiency: 'intermediate', usageCount: 4, evidence: '/evidence/cloudfront' },
  { id: '9', name: 'TypeScript', category: 'backend', proficiency: 'advanced', usageCount: 20, evidence: '/evidence/typescript' },
  { id: '10', name: 'React', category: 'frontend', proficiency: 'advanced', usageCount: 18, evidence: '/evidence/react' },
  { id: '11', name: 'Docker', category: 'devops', proficiency: 'intermediate', usageCount: 7, evidence: '/evidence/docker' },
  { id: '12', name: 'IAM', category: 'cloud', cloud: 'aws', proficiency: 'advanced', usageCount: 11, evidence: '/evidence/iam' },
];

export const projects: Project[] = [
  {
    id: '1',
    name: "Oyin's Journey CV System",
    description: 'Self-documenting, queryable cloud architecture that serves as an engineering resume with CI/CD, IaC, and architectural decision records.',
    technologies: ['TypeScript', 'React', 'Terraform'],
    awsServices: ['Lambda', 'API Gateway', 'DynamoDB', 'S3', 'CloudFront'],
    hasCI: true,
    hasIaC: true,
    evidenceLinks: {
      repo: 'https://github.com/oyintech/oyins-journey',
      demo: 'https://journey.oyintech.dev',
      pipeline: 'https://github.com/oyintech/oyins-journey/actions',
    },
    date: '2024-12',
  },
  {
    id: '2',
    name: 'Serverless Event Processor',
    description: 'Event-driven architecture for processing high-volume data streams with dead letter queues and retry logic.',
    technologies: ['Python', 'AWS SAM'],
    awsServices: ['Lambda', 'SQS', 'SNS', 'CloudWatch'],
    hasCI: true,
    hasIaC: true,
    evidenceLinks: {
      repo: 'https://github.com/oyintech/event-processor',
      dashboard: 'https://cloudwatch.aws.amazon.com/dashboard',
    },
    date: '2024-10',
  },
  {
    id: '3',
    name: 'Cost-Optimized API Gateway',
    description: 'RESTful API with caching, throttling, and usage plans to minimize AWS costs while maintaining performance.',
    technologies: ['Node.js', 'OpenAPI'],
    awsServices: ['API Gateway', 'Lambda', 'ElastiCache'],
    hasCI: true,
    hasIaC: false,
    evidenceLinks: {
      repo: 'https://github.com/oyintech/api-gateway',
      demo: 'https://api.oyintech.dev',
    },
    date: '2024-08',
  },
];

export const adrs: ADR[] = [
  {
    id: '1',
    title: 'Lambda over EC2 for Compute',
    decision: 'Use AWS Lambda for all compute workloads',
    context: 'Needed a compute solution that minimizes operational overhead and stays within AWS Free Tier limits.',
    options: ['EC2 instances', 'ECS Fargate', 'AWS Lambda'],
    tradeoffs: ['Cold starts on infrequent calls', '15-minute execution limit', 'Limited memory (10GB max)'],
    awsServices: ['Lambda', 'CloudWatch'],
    date: '2024-11',
  },
  {
    id: '2',
    title: 'DynamoDB for CV Data Storage',
    decision: 'Use DynamoDB with GSIs for queryable CV data',
    context: 'Required a database that supports flexible querying, scales automatically, and has generous free tier.',
    options: ['RDS PostgreSQL', 'DynamoDB', 'S3 + Athena'],
    tradeoffs: ['Limited query flexibility vs SQL', 'GSI costs at scale', 'Eventually consistent reads by default'],
    awsServices: ['DynamoDB'],
    date: '2024-11',
  },
  {
    id: '3',
    title: 'Terraform for Infrastructure',
    decision: 'Use Terraform over CloudFormation for IaC',
    context: 'Wanted infrastructure as code that is cloud-agnostic and has strong community support.',
    options: ['CloudFormation', 'Terraform', 'Pulumi', 'CDK'],
    tradeoffs: ['State management complexity', 'Learning curve', 'Not native AWS integration'],
    awsServices: ['All'],
    date: '2024-10',
  },
];

export const apiEndpoints = [
  { method: 'GET', path: '/skills', description: 'List all skills with optional filtering', params: ['category', 'cloud', 'minUsage'] },
  { method: 'GET', path: '/skills/:id', description: 'Get detailed skill information', params: [] },
  { method: 'GET', path: '/projects', description: 'List all projects', params: ['hasCI', 'hasIaC'] },
  { method: 'GET', path: '/projects/:id', description: 'Get project details with evidence links', params: [] },
  { method: 'GET', path: '/architecture/decisions', description: 'List all architecture decision records', params: ['service'] },
  { method: 'GET', path: '/architecture/decisions/:id', description: 'Get specific ADR', params: [] },
  { method: 'GET', path: '/experience/timeline', description: 'Get versioned CV history', params: [] },
  { method: 'GET', path: '/health', description: 'System health and metrics', params: [] },
];

export const systemHealth = {
  status: 'healthy',
  uptime: '99.97%',
  lastDeployment: '2024-12-26T10:30:00Z',
  apiLatency: '45ms',
  errorRate: '0.02%',
  version: 'v2.1.0',
};