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
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error('Unit tests failed!')
                    } finally {
                        sh 'docker-compose -f docker-compose.yaml down'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker-compose.yaml up -d'
                archiveArtifacts artifacts: 'docker-compose.yaml', fingerprint: true
            }
        }

        stage('Rollback') {
    when {
        expression {
            currentBuild.result != 'SUCCESS'
        }
    }
    steps {
        script {
            def buildInfo = currentBuild.rawBuild.getBuildVariables()
            def previousBuildNumber = buildInfo['BUILD_NUMBER'].toInteger() - 1
            def previousBuild = Jenkins.instance.getBuildByNumber(previousBuildNumber)
            while (previousBuild != null) {
                def buildArtifacts = previousBuild.artifacts
                if (buildArtifacts.find { it.fileName == 'docker-compose.yaml' }) {
                    sh 'docker-compose -f docker-compose.yaml down'
                    sh "docker-compose -f docker-compose.yaml up -d --build --no-deps ${buildArtifacts.find { it.fileName == 'docker-compose.yaml' }.getUrlName()}"
                    break
                }
                previousBuild = previousBuild.previousBuild
            }
        }
    }
}

    }
}

