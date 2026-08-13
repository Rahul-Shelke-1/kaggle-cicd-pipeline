# kaggle-cicd-pipeline
An automated, cost-optimized fire-and-forget CI/CD pipeline built with GitHub Actions for Kaggle notebooks. It detects file changes, dynamically injects tracking metadata, and pushes updates using uv. By dispatching remote Kaggle jobs and terminating CI runners immediately, it eliminates idle wait times and maximizes compute savings.
