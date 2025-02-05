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
                withCredentials([file(credentialsId: gpg_key, variable: 'signingKey')])
                {
                    sh ('cat $signingKey > $WORKSPACE/signkey.gpg')
                    sh ('gpg --allow-secret-key-import --import signkey.gpg')
                }
                sh 'helmfile sync'
            }
        }
    }
}
