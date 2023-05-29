pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'sudo docker build -t corider:latest .'
            }
        }
        
        stage('Post-Build') {
            steps {
                sh 'sudo mkdir -p /var/www/html/corider/'
                sh 'sudo cp -R static /var/www/html/corider/'
                sh 'sudo cp -R media /var/www/html/corider/'
            }
        }

        stage('Unit Tests') {
            steps {
                script {
                    docker.image('corider:latest').withRun('-p 8000:8000') { container ->
                        dir('/corider') {
                            sh 'sudo docker exec ${container.id} python manage.py test'
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
            	sh 'sudo docker-compose -f docker-compose.yaml down'
                sh 'sudo docker-compose -f docker-compose.yaml up -d'
            }
        }
    }
}

