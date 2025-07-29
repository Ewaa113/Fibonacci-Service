pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "fibonacci-app"
        HEROKU_API_KEY = credentials('HEROKU_API_KEY')
        AZURE_PUBLISH_PROFILE = credentials('AZURE_PUBLISH_PROFILE')
        AZURE_APP_NAME = "the-azure-app-name"
        AZURE_RESOURCE_GROUP = "the-azure-resource-group"
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY')
        AWS_REGION = "us-east-1"
        AWS_EB_APP_NAME = "the-eb-app-name"
        AWS_EB_ENV_NAME = "the-eb-env-name"
        GCP_PROJECT = "the-gcp-project"
        GCP_SA_KEY = credentials('GCP_SA_KEY')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build & Test') {
            steps {
                dir('python') {
                    sh 'pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                    sh 'pytest'
                    sh 'docker build -t fibonacci-app .'
                }
            }
        }
        stage('Deploy to Heroku') {
            when { branch 'main' }
            steps {
                sh '''
                    curl https://cli-assets.heroku.com/install.sh | sh
                    heroku container:login
                    heroku create fibonacci-app-${BUILD_NUMBER}
                    heroku container:push web -a fibonacci-app-${BUILD_NUMBER}
                    heroku container:release web -a fibonacci-app-${BUILD_NUMBER}
                '''
            }
        }
        stage('Deploy to Azure Web App') {
            when { branch 'main' }
            steps {
                sh '''
                    echo "$AZURE_PUBLISH_PROFILE" > azure_publish_profile
                    az webapp deploy --name $AZURE_APP_NAME --resource-group $AZURE_RESOURCE_GROUP --src-path python/Dockerfile
                '''
            }
        }
        stage('Deploy to AWS Elastic Beanstalk') {
            when { branch 'main' }
            steps {
                sh '''
                    pip install awsebcli
                    eb init -p docker $AWS_EB_APP_NAME --region $AWS_REGION
                    eb create $AWS_EB_ENV_NAME
                    eb deploy
                '''
            }
        }
        stage('Deploy to Google Cloud Run') {
            when { branch 'main' }
            steps {
                sh '''
                    echo "$GCP_SA_KEY" > gcp-key.json
                    gcloud auth activate-service-account --key-file=gcp-key.json
                    gcloud config set project $GCP_PROJECT
                    gcloud builds submit --tag gcr.io/$GCP_PROJECT/$DOCKER_IMAGE python
                    gcloud run deploy $DOCKER_IMAGE --image gcr.io/$GCP_PROJECT/$DOCKER_IMAGE --platform managed --region us-central1 --allow-unauthenticated
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}


// How this Jenkins CI/CD Pipeline Works
// Pipeline Stages

// The pipeline is divided into these stages: Build & Test, and one deploy stage for each cloud provider (Deploy to Heroku, Deploy to Azure Web App, Deploy to AWS Elastic Beanstalk, Deploy to Google Cloud Run).
// Build & Test Stage

// Installs Python dependencies inside the python directory.
// Runs the unit tests using pytest to ensure the code works as expected.
// Builds a Docker image for the application using the Dockerfile in the python directory.
// Deploy Stages

// Each deploy stage deploys the Docker image to a different cloud provider:
// Heroku: Uses the Heroku CLI to push and release the Docker image.
// Azure: Uses the Azure CLI to deploy the Docker image to Azure Web App.
// AWS: Uses the AWS EB CLI to deploy the Docker image to AWS Elastic Beanstalk.
// GCP: Uses the Google Cloud CLI to deploy the Docker image to Google Cloud Run.
// By default, these deploy stages are set to run only on the main branch.

// How to Use This Pipeline
// Set Up Jenkins Credentials

// In the Jenkins instance, add the required secrets as credentials:
// HEROKU_API_KEY, AZURE_PUBLISH_PROFILE, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, GCP_SA_KEY, etc.
// Update the Jenkinsfile environment variables with the actual app/environment names.
// Push to Main Branch

// Push the code to the main branch to trigger the pipeline.
// Monitor the Pipeline

// By default, all deploy stages run automatically after a successful build and test on the main branch.
// You can add when or input steps in the Jenkinsfile if you want to require manual approval for deployments.