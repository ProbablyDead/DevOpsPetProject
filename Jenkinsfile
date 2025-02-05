pipeline {
    stages {
        agent any
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
    stages {
        agent Linux
        stage('verify installation') {
            steps {
                sh '''
                    helmfile -v
                '''
            }
        }
        stage('apply changes') {
            steps {
                sh 'helmfile sync'
            }
        }
    }
}
