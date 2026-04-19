pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/opt/flask-staging'
    }

    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_app.py -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    sudo mkdir -p ${DEPLOY_DIR}
                    sudo cp app.py ${DEPLOY_DIR}/
                    sudo cp requirements.txt ${DEPLOY_DIR}/
                    cd ${DEPLOY_DIR}
                    sudo python3 -m venv venv
                    sudo ${DEPLOY_DIR}/venv/bin/pip install -r requirements.txt
                    sudo pkill -f "gunicorn.*5000" || true
                    sudo nohup ${DEPLOY_DIR}/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app --chdir ${DEPLOY_DIR} --daemon
                '''
                echo "App deployed to staging at http://${env.JENKINS_URL}:5000"
            }
        }
    }

    post {
        success {
            mail to: 'eiron.rohit@gmail.com',
                 subject: "BUILD SUCCESS - FlaskApp #${env.BUILD_NUMBER}",
                 body: "Flask app build and deployment succeeded.\nCheck Jenkins: ${env.BUILD_URL}"
        }
        failure {
            mail to: 'eiron.rohit@gmail.com',
                 subject: "BUILD FAILED - FlaskApp #${env.BUILD_NUMBER}",
                 body: "Flask app build failed.\nCheck Jenkins: ${env.BUILD_URL}"
        }
    }
}
