pipeline {
    agent any

    environment {
        APP_NAME  = 'gesturex-system'
        IMAGE_TAG = "${env.BUILD_NUMBER ?: 'v1.0.0'}"
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('1. SCM Checkout') {
            steps {
                echo '==> [SCM Checkout] Checking out repository source...'
                checkout scm
            }
        }

        stage('2. Docker Build') {
            steps {
                echo "==> [Docker Build] Building Docker image ${APP_NAME}:latest and ${APP_NAME}:${IMAGE_TAG}..."
                sh "docker build -t ${APP_NAME}:latest -t ${APP_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('3. In-Container Syntax Validation') {
            steps {
                echo '==> [Syntax Validation] Validating Python syntax inside container...'
                sh "docker run --rm ${APP_NAME}:latest python -m py_compile app.py actions.py config.py gesture_utils.py"
            }
        }

        stage('4. Run Automated Unit Tests') {
            steps {
                echo '==> [Testing] Running pytest test suite inside container...'
                sh "docker run --rm ${APP_NAME}:latest pytest -v tests/"
            }
        }

        stage('5. Container Smoke Test') {
            steps {
                echo '==> [Smoke Test] Verifying Streamlit container health...'
                sh """
                    docker rm -f gesturex_smoke_test 2>/dev/null || true
                    docker run -d --name gesturex_smoke_test -p 8502:8501 ${APP_NAME}:latest
                    sleep 8
                    docker exec gesturex_smoke_test curl -f http://localhost:8501/_stcore/health || exit 1
                    docker rm -f gesturex_smoke_test
                """
            }
        }

        stage('6. Deploy Container') {
            steps {
                echo '==> [Deploy] Launching GestureX service container...'
                sh """
                    docker rm -f gesturex_container 2>/dev/null || true
                    docker run -d --name gesturex_container -p 8501:8501 --restart unless-stopped ${APP_NAME}:latest
                    echo "==> GestureX deployed successfully and accessible at http://localhost:8501"
                """
            }
        }
    }

    post {
        always {
            sh 'docker rm -f gesturex_smoke_test 2>/dev/null || true'
            echo '==> Pipeline execution completed.'
        }
        success {
            echo '=========================================================='
            echo " SUCCESS: GestureX Build #${env.BUILD_NUMBER} passed successfully!"
            echo '=========================================================='
        }
        failure {
            echo '=========================================================='
            echo ' FAILURE: Pipeline encountered errors. Check stage logs.'
            echo '=========================================================='
        }
    }
}
