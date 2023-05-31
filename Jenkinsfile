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

        stage('Unit Tests & Deploy') {
            steps {
                script {
                    def testFailed = false
                    try {
                    	env.DOCKER_IMAGE_TAG = 'latest'
                        sh 'docker-compose -f docker-compose.yaml up -d'
                        sh 'docker-compose -f docker-compose.yaml logs -f app & sleep 10'
                        sh 'docker-compose -f docker-compose.yaml exec -T app sh -c "cd /corider && python manage.py test"'
                    } catch (Exception err) {
                        testFailed = true
                        echo "Unit tests failed. Performing rollback..."
                    } finally {
                        sh 'docker-compose -f docker-compose.yaml down'
                    }
					env.DOCKER_IMAGE_TAG = 'stable'
                    if (testFailed) {
                        sh 'docker-compose -f docker-compose.yaml up -d'
                    } else {
                        sh 'docker tag corider:latest corider:stable'
                        catchError(buildResult: 'FAILURE', stageResult: 'UNSTABLE') {
                            sh 'docker-compose -f docker-compose.yaml up -d'
                        }
                    }
                }
            }
        }
    }
}

