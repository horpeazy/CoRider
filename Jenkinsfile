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
                        sh 'docker-compose -f docker-compose.staging.yaml up -d'
                        sh 'docker-compose -f docker-compose.staging.yaml logs -f test_app & sleep 5'
                        sh 'docker-compose -f docker-compose.staging.yaml exec -T test_app sh -c "cd /corider && python manage.py test"'
                        sh 'docker tag corider:latest corider:stable'
                    } catch (Exception err) {
                        currentBuild.result = 'FAILURE'
                        echo "Unit tests failed. Performing rollback..."
                        sh 'docker-compose -f docker-compose.staging.yaml down'
                        error("Unit tests failed. Deployment rollback performed.")
                    } finally {
                        sh 'docker-compose -f docker-compose.staging.yaml down'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'UNSTABLE') {
                    sh 'docker-compose -f docker-compose.yaml up -d'
                }
            }
        }
    }
}

