pipeline {
    agent any

    stages {

        stage('Clone Repo (GitHub Token)') {
            steps {
                git credentialsId: 'github-token',
                    url: 'https://github.com/calvinjohnplacio/cicd.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Selenium Test') {
            steps {
                sh '''
                . venv/bin/activate
                python test.py
                '''
            }
        }

        stage('Deploy to Apache') {
            steps {
                sh '''
                sudo cp index.html /var/www/html/index.html
                sudo chown www-data:www-data /var/www/html/index.html
                '''
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
