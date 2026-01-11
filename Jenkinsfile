pipeline {
 pipeline {
    agent {
        docker { 
            image 'python:3.9-slim'
            
        }
    }
 
    environment {
        AWS_ACCOUNT_ID = '992382545251'
        AWS_REGION = 'us-east-1'
        IMAGE_REPO_NAME = 'avishag/calculator'
        IMAGE_TAG = "pr-${env.CHANGE_ID}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker Image...'
                script {
                    sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running Tests...'
                sh 'pip install -r requirements.txt'
                sh 'python -m pytest'
            }
        }

        stage('Push to ECR') {
            when {
                changeRequest() 
            }
            steps {
                echo 'Pushing Image to ECR...'
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}
