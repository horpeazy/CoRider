pipeline {

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build('corider:latest')
                }
            }
        }
        
        stage('Post-Build') {
            steps {
                sh 'mkdir -p /var/www/html/corider/'
                sh 'cp -R static /var/www/html/corider/'
                sh 'cp -R media /var/www/html/corider/'
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

}

