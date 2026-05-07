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
                        cd gitops-config
                        sed -i 's|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g' deployment.yaml
                        sed -i 's|image: ${IMAGE_NAME}:.*|image: ${IMAGE_NAME}:${IMAGE_TAG}|g' service.yaml
                        git config user.email "jenkins@gitops.com"
                        git config user.name "Jenkins"
                        git add deployment.yaml
                        git add service.yaml
                        git commit -m "Update image tag to ${IMAGE_TAG}"
                        git push
                    """
                }
            }
        }

    }
}