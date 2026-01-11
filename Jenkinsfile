pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '992382545251'
        AWS_REGION = 'us-east-1'
        IMAGE_REPO_NAME = 'avishag/calculator'
        PR_ID = "${env.CHANGE_ID ?: 'master'}"
        IMAGE_TAG = "pr-${PR_ID}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build Image') {
            steps {
                sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Test') {
            steps {
                echo 'Running Tests directly on host...'
                sh 'pip install -r requirements.txt --break-system-packages'
                sh 'python -m pytest'
            }
        }

        stage('Push to ECR') {
            when { changeRequest() }
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}
