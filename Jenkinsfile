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
                    def appContainerId

                    try {
                        def appContainer = docker.image('corider:latest').run('-d')
                        appContainerId = appContainer.id
                        echo "Container ID: ${appContainerId}"

                        // Wait for the container to start
                        sh "docker wait ${appContainerId}"

                        // Print container information
                        sh "docker ps -a --filter id=${appContainerId}"
						sh "docker logs ${appContainerId}"
                        // Execute the command within the container
                        sh "docker exec ${appContainerId} sh -c 'cd /corider && python manage.py test'"
                        sh "docker logs ${appContainerId}"
                    } finally {
                        if (appContainerId) {
                            // Print container logs
                            sh "docker logs ${appContainerId}"
                            
                            // Stop and remove the container
                            sh "docker stop ${appContainerId}"
                            sh "docker rm ${appContainerId}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker-compose.yaml down'
                sh 'docker-compose -f docker-compose.yaml up -d'
            }
        }
    }
}

