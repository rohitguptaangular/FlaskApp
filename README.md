# Flask CI/CD Demo App

A simple Flask web application with CI/CD pipelines set up using both Jenkins and GitHub Actions.

## About the App

A basic Python Flask API with three endpoints:
- `/` - returns welcome message
- `/health` - health check endpoint
- `/about` - app info and version

## Running Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

App runs on http://localhost:5000

## Running Tests

```bash
pytest test_app.py -v
```

---

## Part 1: Jenkins CI/CD Pipeline

### How the Pipeline Works

The `Jenkinsfile` in the repo root defines a three-stage pipeline:

1. **Build** - creates a virtual environment and installs all dependencies from requirements.txt
2. **Test** - runs the test suite using pytest. If any test fails, the pipeline stops here
3. **Deploy** - copies the app to a staging directory on the server and starts it using gunicorn on port 5000

### Jenkins Setup

I used the same Jenkins server from my previous assignment (EC2 instance with Jenkins installed).

Extra setup needed for this pipeline:
- Python 3 installed on the Jenkins server (`sudo yum install python3 python3-pip -y`)
- A pipeline job pointing to this repo's Jenkinsfile
- Email notification configured in Manage Jenkins -> System -> E-mail Notification

### Build Trigger

The pipeline is set to trigger automatically when code is pushed to the main branch. This is done through a GitHub webhook pointing to `http://<JENKINS_IP>:8080/github-webhook/`.

In the Jenkins job settings, "GitHub hook trigger for GITScm polling" is enabled.

### Notifications

Email notifications are sent to my email on both success and failure. This is configured in the `post` block of the Jenkinsfile using the `mail` step.

---

## Part 2: GitHub Actions CI/CD Pipeline

### How the Workflow Works

The workflow file is at `.github/workflows/ci-cd.yml`. It runs different jobs depending on what triggered it:

**On push to main or PR:**
1. **Install Dependencies** - sets up Python 3.11 and installs packages from requirements.txt
2. **Run Tests** - runs pytest to make sure nothing is broken
3. **Build** - verifies the app can start and uploads it as an artifact

**On push to staging branch:**
- All of the above, plus **Deploy to Staging**

**On a version tag (like v1.0.0):**
- All of the above, plus **Deploy to Production**

### Branches

- `main` - primary development branch, runs tests on every push
- `staging` - pushing here triggers deployment to staging environment

### GitHub Secrets

Go to repo Settings -> Secrets and variables -> Actions -> New repository secret

Required secrets:
- `DEPLOY_KEY` - deployment key or token for the server

### Creating a Release (Production Deploy)

To trigger a production deployment:
```bash
git tag v1.0.0
git push origin v1.0.0
```

This creates a version tag which triggers the production deploy job.

### Environments

I set up two environments in the repo (Settings -> Environments):
- **staging** - for staging deployments
- **production** - for production deployments

---

## Screenshots

Screenshots of both pipeline executions are in the `docs/` folder.
# staging trigger
