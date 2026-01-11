pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '992382545251'
        AWS_REGION = 'us-east-1'
        IMAGE_REPO_NAME = 'avishag/calculator'
      
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
       
        PROD_SERVER_IP = '54.236.5.221'
    }

    stages {
        stage('Install & Test') {
            agent {
                docker { 
                    image 'python:3.9-slim' 
                }
            }
            steps {
                echo "Stage 1: Testing the code..."
                sh 'pip install -r requirements.txt'
                sh 'python -m pytest test_app.py'
            }
        }

        stage('Build Image') {
            steps {
                echo "Stage 2: Building Docker Image..."
                sh "docker build -t ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    echo "Stage 3: Pushing Image to AWS ECR..."
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to Production') {
          
            when {
                branch 'main'
            }
            steps {
                echo "Stage 4: Deploying to Production Server..."
                sshagent(['prod-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ec2-user@${PROD_SERVER_IP} "
              
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com &&
                        
                   
                        docker stop calculator || true &&
                        docker rm calculator || true &&
                        
                     
                        docker run -d --name calculator -p 80:5000 ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}
                    "
                    """
                }
            }
        }
    }
}

