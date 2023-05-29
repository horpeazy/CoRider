pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'sudo docker build -t corider:latest .'
            }
        }
        
        stage('Testing') {
            steps {
                sh 'echo "Testing the application..."'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'sudo docker-compose -f docker-compose up --build'
            }
        }
    }
    
    post {
    	always {
        	docker.image('jenkins/jenkins:latest').inside('-v /var/www/html/corider:/var/www/html/corider') {
            	sh 'cp -R /var/www/html/corider/static /var/www/html/corider/'
            	sh 'cp -R /var/www/html/corider/media /var/www/html/corider/'
        	}
    	}
    }
}

