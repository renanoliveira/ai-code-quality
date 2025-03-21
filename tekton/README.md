# Tekton CI/CD Integration

This directory contains Tekton pipeline configurations for running AI-powered code reviews in your CI/CD workflow.

## Structure

```
tekton/
├── pipelines/
│   └── code-review-pipeline.yaml  # Main pipeline definition
├── tasks/
│   └── code-review-task.yaml      # Task for running code reviews
└── README.md                      # This file
```

## Setup

1. Create required secrets:

```bash
# Create namespace
kubectl create namespace ai-quality-ci

# Create secrets
kubectl create secret generic ai-secrets \
  --namespace ai-quality-ci \
  --from-literal=openai-key='your-openai-key' \
  --from-literal=azure-key='your-azure-key' \
  --from-literal=azure-endpoint='your-azure-endpoint'

kubectl create secret generic github-secret \
  --namespace ai-quality-ci \
  --from-literal=token='your-github-token'
```

2. Build and push the Docker image:

```bash
# Build image
docker build -t your-registry/ai-quality-ci:latest .

# Push to registry
docker push your-registry/ai-quality-ci:latest
```

3. Apply Tekton resources:

```bash
# Apply task and pipeline
kubectl apply -f tekton/tasks/code-review-task.yaml
kubectl apply -f tekton/pipelines/code-review-pipeline.yaml
```

## Usage

Create a PipelineRun to analyze your code:

```yaml
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  name: code-review-run
spec:
  pipelineRef:
    name: ai-code-review-pipeline
  params:
    - name: repo-url
      value: "https://github.com/username/repo.git"
    - name: path
      value: "src/*.py"
    - name: provider
      value: "openai"
    - name: model
      value: "gpt-4"
    - name: auto-apply
      value: "true"
```

Apply the PipelineRun:

```bash
kubectl apply -f pipeline-run.yaml
```

## Parameters

| Parameter    | Description              | Default |
|-------------|-------------------------|---------|
| repo-url    | Git repository URL      | -       |
| branch-name | Branch to analyze       | main    |
| path        | Files to analyze        | .       |
| provider    | AI provider to use      | openai  |
| model       | AI model to use         | gpt-4   |
| language    | Output language         | en      |
| auto-apply  | Auto-apply fixes       | false   |

## Security Notes

1. Always use Kubernetes secrets for API keys
2. Use specific versions for production deployments
3. Consider network policies for API access
4. Review auto-applied changes before merging
