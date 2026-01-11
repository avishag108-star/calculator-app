pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock -u root'
        }
    }

    environment {
        AWS_ACCOUNT_ID = '992382545251'
        AWS_REGION = 'us-east-1'
        IMAGE_REPO_NAME = 'avishag/calculator'
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Install & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m pytest'
            }
        }

        stage('Build & Push') {
            steps {
                sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
                sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
            }
        }
    }
}
