pipeline {
  agent {
    dockerfile true
  }
  stages {
    stage('Test') {
      steps {
        sh 'make test'
      }
    }
  }
  post {
    always {
      junit testResults: 'reports/pytest.xml', skipPublishingChecks: true
      recordIssues tool: pyLint(pattern: 'reports/pylint.log'), enabledForFailure: true, skipPublishingChecks: true
      cleanWs()
    }
  }
}
