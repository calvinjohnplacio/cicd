pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/calvinjohnplacio/cicd.git'
        GIT_CREDENTIALS_ID = 'github-pat'
        GIT_BRANCH = 'main'
    }

    options {
        skipDefaultCheckout(true)
    }

    stages {

        stage('Checkout SCM') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${env.GIT_BRANCH}"]],
                    userRemoteConfigs: [[
                        url: "${env.GIT_REPO_URL}",
                        credentialsId: "${env.GIT_CREDENTIALS_ID}"
                    ]]
                ])
            }
        }

        stage('Detect Changes') {
            steps {
                script {
                    // safer diff fallback (fixes HEAD~1 issue)
                    def changes = sh(
                        script: """
                        git fetch origin ${env.GIT_BRANCH}
                        git diff --name-only origin/${env.GIT_BRANCH} HEAD || true
                        """,
                        returnStdout: true
                    ).trim()

                    echo "Changed files:\n${changes}"

                    // FIX: convert to proper boolean strings
                    env.HAS_PHP_CHANGES = changes.contains('.php') ? 'true' : 'false'
                    env.HAS_TEST_CHANGES = (changes.contains('test.py') || changes.contains('requirements.txt')) ? 'true' : 'false'
                }
            }
        }

        stage('Setup Python Environment') {
            when {
                expression { return env.HAS_TEST_CHANGES == 'true' }
            }
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Tests') {
            when {
                expression { return env.HAS_TEST_CHANGES == 'true' }
            }
            steps {
                sh '''
                . venv/bin/activate
                python test.py
                '''
            }
        }

        stage('Deploy to Apache') {
            when {
                expression { return env.HAS_PHP_CHANGES == 'true' }
            }
            steps {
                sh '''
                echo "Deploying PHP files to Apache..."

                sudo rsync -av --delete ./ /var/www/html/

                sudo chown -R www-data:www-data /var/www/html/
                '''
            }
        }
    }

    post {
        success {
            echo "CI/CD SUCCESS ✔ Deployment completed"
        }
        failure {
            echo "CI/CD FAILED ❌ Check logs"
        }
        always {
            cleanWs()
        }
    }
}
