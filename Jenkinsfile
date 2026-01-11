pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '992382545251'
        AWS_REGION = 'us-east-1'
        IMAGE_REPO_NAME = 'avishag/calculator'
        IMAGE_TAG = "PR-${env.CHANGE_ID ?: 'main'}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Install & Test') {
            agent {
                docker { 
                    image 'python:3.9-slim' 
                }
            }
            steps {
                echo "Running tests for Branch: ${env.BRANCH_NAME}"
                sh 'pip install -r requirements.txt'
          
                sh 'python -m pytest test_app.py || echo "No specific test file found, running general pytest"'
                sh 'python -m pytest'
            }
        }

        stage('Build Image') {
            steps {
                sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}
