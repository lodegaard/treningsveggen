pipeline {
  agent any
  stages {
    stage('Clone') {
      steps {
        git(url: 'https://github.com/lodegaard/treningsveggen.git', branch: 'master', changelog: true)
        node(label: 'yocto')
      }
    }
  }
}