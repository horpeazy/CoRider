pipeline {

	agent any

    stages {
        stage('Build') {
            steps {
                script {
                    sh 'sudo docker build -t corider:latest .'
                }
            }
        }
        
        stage('Post-Build') {
            steps {
                sh 'sudo mkdir -p /var/www/html/corider/'
                sh 'sudo cp -R static /var/www/html/corider/'
                sh 'sudo cp -R media /var/www/html/corider/'
            }
        }

        stage('Testing') {
            steps {
                sh 'echo "Testing the application..."'
            }
        }

        stage('Deploy') {
            steps {
                
            	sh 'sudo docker-compose -f docker-compose.yaml up -d'
            }
        }
    }

}

