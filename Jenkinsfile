pipeline {
    agent any
    
    stages {
        
        stage('Pre-build') {
            steps {
                sh 'cp -R static /var/www/html/corider/'
                sh 'cp -R media /var/www/html/corider/'
                sh 'cd /corider/'
            }
        }
        
        stage('Build') {
            steps {
                sh 'sudo docker build -t corider:latest .'
            }
        }
        
        stage('Build') {
            steps {
                sh 'testing the application'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'sudo docker-compose -f docker-compose up --build'
            }
        }
    }
}

