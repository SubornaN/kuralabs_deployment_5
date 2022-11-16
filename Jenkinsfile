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
                docker run -d --name web_app -p 8081:5000 url-shortner:v1
                '''
            }
        }  
        stage ('DockerhubImage') {
            agent{label 'agentDocker'}
            steps {
                sh '''
                docker commit web_app web_app:v1
                docker tag web_app:v1 suborna/web_app:v1
                docker push suborna/web_app:v1
                docker stop web_app
                docker rm web_app
                '''
            }
        }
        stage('Init') {
            agent{label 'agentTerraform'}
            steps {
                withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                    string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                        dir('intTerraform') {
                            sh 'terraform init' 
                        }
                    }
            }
        }
        stage('Plan') {
            agent{label 'agentTerraform'}
            steps {
                withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                    string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                        dir('intTerraform') {
                            sh 'terraform plan -out plan.tfplan -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key"' 
                        }
                    }
            }
        }
        stage('Apply') {
            agent{label 'agentTerraform'}
            steps {
                withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'), 
                    string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
                        dir('intTerraform') {
                            sh 'terraform apply plan.tfplan' 
                        }
                    }
            }
        }
        // stage('Destroy') {
        //     agent{label 'agentTerraform'}
        //     steps {
        //         withCredentials([string(credentialsId: 'AWS_ACCESS_KEY', variable: 'aws_access_key'),
        //             string(credentialsId: 'AWS_SECRET_KEY', variable: 'aws_secret_key')]) {
        //                 dir('intTerraform') {
        //                     sh 'terraform destroy -auto-approve -var="aws_access_key=$aws_access_key" -var="aws_secret_key=$aws_secret_key"'
        //                 }
        //             }
        //     }
        // }  

    }
}