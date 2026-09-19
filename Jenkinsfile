// ===================================================================
// Jenkinsfile  ->  Declarative Pipeline (student project ke liye perfect)
//
// Flow:  Checkout -> Build -> Unit Test -> API Test -> Docker Build
//        -> Docker Push -> Deploy
//
// Jenkins me:  New Item -> Pipeline -> "Pipeline script from SCM" -> Git
//              repo URL do -> Script Path = Jenkinsfile -> Save
// ===================================================================

pipeline {
    agent any

    environment {
        // Credentials (Manage Jenkins -> Credentials me add karna, ID same rakhna)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        APP_NAME              = 'studentdesk'
        IMAGE_TAG             = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(7) ?: 'local'}"
        PYTHON_BIN            = 'python3'
    }

    options {
        timestamps()                       // har line pe time dikhega
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()          // ek saath 2 build nahi
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "=== Stage 1: Code checkout ==="
                checkout scm
                sh 'git log -1 --pretty=format:"Commit: %h | Author: %an | Msg: %s"'
            }
        }

        stage('Setup Python Env') {
            steps {
                echo "=== Stage 2: Virtual environment + dependencies ==="
                sh '''
                    ${PYTHON_BIN} -m venv venv || true
                    . venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt -r requirements-dev.txt
                '''
            }
        }

        stage('Build (Compile Check)') {
            steps {
                echo "=== Stage 3: Syntax / compile check ==="
                sh '''
                    . venv/bin/activate
                    python -m compileall -q app run.py
                    echo "Build SUCCESS - sabhi .py files compile ho gayi"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo "=== Stage 4: pytest (unit + integration + API) ==="
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/test_unit.py -v --junitxml=reports/unit-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/unit-results.xml'
                }
            }
        }

        stage('App & API Tests') {
            steps {
                echo "=== Stage 5: Flask route + REST API tests ==="
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/test_app.py tests/test_api.py -v --junitxml=reports/app-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/app-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "=== Stage 6: Docker image build ==="
                sh '''
                    docker build -t ${APP_NAME}:${IMAGE_TAG} -t ${APP_NAME}:latest .
                    docker images | grep ${APP_NAME}
                '''
            }
        }

        stage('Smoke Test (Container)') {
            steps {
                echo "=== Stage 7: Container ko chala ke /health check karo ==="
                sh '''
                    docker rm -f ${APP_NAME}-smoke || true
                    docker run -d --name ${APP_NAME}-smoke -p 5055:5000 ${APP_NAME}:${IMAGE_TAG}
                    sleep 8
                    for i in $(seq 1 10); do
                      if curl -fsS http://host.docker.internal:5055/health; then
                        echo ""
                        echo "SMOKE TEST PASSED"
                        docker rm -f ${APP_NAME}-smoke
                        exit 0
                      fi
                      sleep 3
                    done
                    docker logs ${APP_NAME}-smoke
                    docker rm -f ${APP_NAME}-smoke
                    echo "SMOKE TEST FAILED"
                    exit 1
                '''
            }
        }

        stage('Docker Push') {
            when { branch 'main' }        // sirf main branch pe push
            steps {
                echo "=== Stage 8: Docker Hub pe push ==="
                sh '''
                    echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                    docker tag ${APP_NAME}:${IMAGE_TAG} ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${IMAGE_TAG}
                    docker tag ${APP_NAME}:latest     ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest
                    docker push ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:${IMAGE_TAG}
                    docker push ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest
                    docker logout
                '''
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                echo "=== Stage 9: Deployment (SSH se VM / cloud pe) ==="
                // Option A: same machine pe redeploy (simplest - college demo ke liye best)
                sh '''
                    docker rm -f ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} --restart unless-stopped \
                      -p 5000:5000 \
                      -e SECRET_KEY="${DOCKER_SECRET_KEY:-jenkins-deploy-secret}" \
                      ${APP_NAME}:${IMAGE_TAG}
                    sleep 5
                    curl -fsS http://host.docker.internal:5000/health && echo " <- DEPLOYED OK"
                '''

                // Option B: remote VM pe deploy karna ho to ye use karo
                // (Manage Jenkins -> Credentials me 'vm-ssh-key' naam se SSH key add karna)
                /*
                sshagent(credentials: ['vm-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@YOUR_VM_IP \
                          "docker pull ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest && \
                           docker rm -f ${APP_NAME} || true && \
                           docker run -d --name ${APP_NAME} --restart unless-stopped -p 5000:5000 \
                             ${DOCKERHUB_CREDENTIALS_USR}/${APP_NAME}:latest"
                    '''
                }
                */
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE SUCCESS — Build #${env.BUILD_NUMBER} deploy ho gaya."
        }
        failure {
            echo "❌ PIPELINE FAILED — Console Output dekho aur error fix karo."
        }
        always {
            echo "=== Cleanup: workspace me test reports archive ==="
            archiveArtifacts artifacts: 'reports/*.xml', allowEmptyArchive: true
            cleanWs(deleteDirs: true, notFailBuild: true)   // Workspace Cleanup plugin chahiye
        }
    }
}
