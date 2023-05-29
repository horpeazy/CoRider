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
                    def appContainer

                    try {
                        appContainer = docker.image('corider:latest').run('-p 8000:8000 -d')

                        script {
                            dir('/corider') {
                                sh 'python manage.py test'
                            }
                        }
                    } finally {
                        if (appContainer != null) {
                            docker.stop(appContainer.id)
                            docker.remove(appContainer.id)
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

