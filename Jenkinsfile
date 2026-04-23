pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/calvinjohnplacio/cicd.git'
        GIT_CREDENTIALS_ID = 'github-pat'   // ✔ Use Jenkins credentials, NOT raw PAT
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
                    def changes = sh(
                        script: "git diff --name-only HEAD~1 HEAD || true",
                        returnStdout: true
                    ).trim()

                    echo "Changed files:\n${changes}"

                    env.HAS_PHP_CHANGES = changes =~ /.*\\.php/
                    env.HAS_TEST_CHANGES = changes =~ /(test\\.py|requirements\\.txt)/
                }
            }
        }

        stage('Setup Python Environment') {
            when {
                expression { return env.HAS_TEST_CHANGES }
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
                expression { return env.HAS_TEST_CHANGES }
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
