pipeline {
    agent { docker { image 'golang:1.23.5-alpine3.21' } }
    stages {
        stage('build') {
            steps {
                sh 'go version'
            }
        }
    }
}
