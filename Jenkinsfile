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
                        def appContainer = docker.image('corider:latest').run('-p 8000:8000 -d')
                        appContainerId = appContainer.id

                        // Wait for the container to start
                        sh "docker wait ${appContainer.id}"

                        // Execute the command within the container
                        sh "docker exec ${appContainer.id} sh -c 'cd /corider && python manage.py test'"
                    } finally {
                        if (appContainerId) {
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

