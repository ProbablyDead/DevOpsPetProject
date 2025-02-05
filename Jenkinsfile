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
                'docker compose build'
            }
        }
        stage('push') {
            steps {
                'docker compose push'
            }
        }
    }
}
