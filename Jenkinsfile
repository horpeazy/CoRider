pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'docker build -t corider:latest .'
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
                    try {
                        sh 'docker-compose -f docker-compose.yaml up -d'
                        sh 'docker-compose -f docker-compose.yaml logs -f app & sleep 10'
                        sh 'docker-compose -f docker-compose.yaml exec -T app sh -c "cd /corider && python manage.py test"'
                    } finally {
                        sh 'docker-compose -f docker-compose.yaml down'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker-compose.yaml up -d'
            }
        }
    }
}

