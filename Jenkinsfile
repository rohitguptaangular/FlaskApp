pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/opt/flask-staging'
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        SNS_TOPIC = 'arn:aws:sns:ap-south-1:859666866036:streaming-app-notifications'
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
                echo 'App deployed to staging on port 5000'
            }
        }
    }

    post {
        success {
            sh '''
                aws sns publish \
                    --topic-arn $SNS_TOPIC \
                    --subject "BUILD SUCCESS - FlaskApp" \
                    --message "Flask app build #${BUILD_NUMBER} succeeded. App deployed to staging." \
                    --region ap-south-1
            '''
        }
        failure {
            sh '''
                aws sns publish \
                    --topic-arn $SNS_TOPIC \
                    --subject "BUILD FAILED - FlaskApp" \
                    --message "Flask app build #${BUILD_NUMBER} failed. Check Jenkins for details." \
                    --region ap-south-1
            '''
        }
    }
}
