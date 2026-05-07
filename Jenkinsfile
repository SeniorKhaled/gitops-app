pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "seniorkhaled"
        APP_NAME = "gitops-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/${APP_NAME}"
        CONFIG_REPO = "https://github.com/SeniorKhaled/gitops-config.git"
    }

    stages {

        stage('Clone App Repo') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/SeniorKhaled/gitops-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh "docker login -u $USER -p $PASS"
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Update Config Repo') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-credentials',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh """
                        rm -rf gitops-config
                        git clone https://${GIT_USER}:${GIT_PASS}@github.com/SeniorKhaled/gitops-config.git
                        sed -i 's|image: seniorkhaled/gitops-app:.*|image: seniorkhaled/gitops-app:${IMAGE_TAG}|g' gitops-config/deployment.yaml
                        git -C gitops-config config user.email "jenkins@gitops.com"
                        git -C gitops-config config user.name "Jenkins"
                        git -C gitops-config add deployment.yaml
                        git -C gitops-config commit -m "Update image tag to ${IMAGE_TAG}"
                        git -C gitops-config push
                    """
                }
            }
        }
    }
}