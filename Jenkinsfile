pipeline {
    agent any

    environment {
        GIT_REPO_URL = 'https://github.com/calvinjohnplacio/cicd.git'
        GIT_CREDENTIALS_ID = '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'  // Correct credential ID
        GIT_BRANCH = 'main'  // Explicitly setting branch to 'main'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    // Checkout the correct branch (main)
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: [[name: "refs/heads/${env.GIT_BRANCH}"]],
                        userRemoteConfigs: [[url: "${env.GIT_REPO_URL}", credentialsId: "${env.GIT_CREDENTIALS_ID}"]]
                    ]
                }
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Create and activate virtual environment
                    sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Selenium Test') {
            steps {
                script {
                    // Activate the virtual environment and run the tests
                    sh '''
                    . venv/bin/activate
                    python test.py
                    '''
                }
            }
        }

        stage('Deploy to Apache') {
            steps {
                script {
                    // Deploy to Apache and handle permissions
                    sh '''
                    sudo cp index.html /var/www/html/index.html
                    sudo chown www-data:www-data /var/www/html/index.html
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "CI/CD SUCCESS ✔ Deployed"
        }
        failure {
            echo "CI/CD FAILED ❌ Check logs"
        }
    }
}
