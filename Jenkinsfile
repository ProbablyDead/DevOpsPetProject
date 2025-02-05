pipeline {
    agent any
    stages {
        stage('verify installation') {
            steps {
                sh '''
                    docker version
                    docker info
                    docker compose version
                '''
            }
        }
        stage('build') {
            steps {
                sh 'docker compose build'
            }
        }
        stage('push') {
            steps {
                sh 'docker compose push'
            }
        }
    }
}
