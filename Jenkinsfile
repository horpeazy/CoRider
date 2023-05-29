pipeline {
    agent {
        docker {
            image 'jenkins/jenkins:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build('corider:latest')
                }
            }
        }

        stage('Testing') {
            steps {
                sh 'echo "Testing the application..."'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('', 'docker-credentials') {
                        sh 'docker-compose -f docker-compose.yaml up --build'
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                sh '''
                cp -R static /var/www/html/corider/
                cp -R media /var/www/html/corider/
                '''
            }
        }
    }
}

