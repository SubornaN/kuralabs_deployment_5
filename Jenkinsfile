pipeline {
    agent any
    stages {
        stage ('Build') {
            steps {
                sh '''#!/bin/bash
                python3 -m venv test3
                source test3/bin/activate
                pip install pip --upgrade
                pip install -r requirements.txt
                export FLASK_APP=application
                flask run &
                '''
            }
        }
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                source test3/bin/activate
                py.test --verbose --junit-xml test-reports/results.xml
                ''' 
            }
            post{
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage ('CreateContainer') {
            agent{label 'agentDocker'}
            steps {
                sh '''#!/bin/bash
                docker build -t url-shortner:v1 .
                docker run -d --name web_app -p 8081:8081 url-shortner:v1
                '''
            }
        }  
    }
}