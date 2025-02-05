pipeline {
    agent any
    stages {
        stage('verify docker installation') {
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
        stage('verify helmfile installation') {
            agent { label 'Linux' }
            steps {
                sh 'helmfile -v'
            }
        }
        stage('apply changes') {
            agent { label 'Linux' }
            steps {
                withCredentials([file(credentialsId: 'gpg_key', variable: 'signingKey')]) {
                    sh 'cat $signingKey > $WORKSPACE/signkey.gpg'
                    sh 'gpg --allow-secret-key-import --import $WORKSPACE/signkey.gpg'
                }
                sh 'helmfile sync'
            }
        }
    }
}
