pipeline {
    agent any
    triggers {
        githubPush()
        pollSCM('H H * * *')
    }
    options {
        skipStagesAfterUnstable()
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    stages {
        stage('Docker Build') {
            steps {
                sh "docker build --no-cache -t wazoplatform/${JOB_NAME}:latest ."
            }
        }
        stage('Docker publish') {
            steps {
                sh "docker push wazoplatform/${JOB_NAME}:latest"
            }
        }
    }
    post {
        failure {
        mattermostSend color: 'danger', channel: '#dev-failed-tests', message: "xivo-load-tester [failed :nuke:](${JOB_URL})"
        }
    }
}
