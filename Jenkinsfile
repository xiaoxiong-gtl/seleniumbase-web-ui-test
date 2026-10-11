// Jenkins 声明式流水线：每日定时回归
// 与 .github/workflows/regression.yml 等价，两份都保留 ——
// GitHub Actions 负责真跑（面试官在 GitHub 上看得见），Jenkinsfile 佐证 Jenkins 能力。
//
// 使用前提：
//   1. Jenkinsfile 用 Linux 语法（sh）。若 Jenkins 跑在 Windows 节点上，需把 sh 换成 bat。
//   2. 报告展示依赖 HTML Publisher 插件。

pipeline {
    agent any

    triggers {
        // Jenkins 的 cron 与 Linux cron 不同：H 表示"哈希取值"，由 Jenkins 自动散开负载，
        // 避免大量任务挤在同一时刻。这里表示每天凌晨 1 点左右执行一次。
        cron('H 1 * * *')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')          // 超时保护，防止构建挂死
        buildDiscarder(logRotator(numToKeepStr: '14'))
        timestamps()
        disableConcurrentBuilds()
    }

    parameters {
        choice(name: 'BROWSER', choices: ['chrome', 'edge'], description: '执行用例所用的浏览器')
        string(name: 'PYTEST_ARGS', defaultValue: '-n 4', description: '额外的 pytest 参数，如 -n 4 表示四进程并行')
    }

    stages {
        stage('检出代码') {
            steps {
                checkout scm
            }
        }

        stage('准备环境') {
            steps {
                sh '''
                    set -e
                    rm -rf .venv-ci
                    python3 -m venv .venv-ci
                    . .venv-ci/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('执行回归') {
            steps {
                // -o 'addopts=' 用于清空 pytest.ini 中为本地环境写死的 --browser=edge，
                // 避免 CI 节点上没有 Edge 时构建失败。
                sh """
                    set -e
                    . .venv-ci/bin/activate
                    python -m pytest practice/ \\
                      -o 'addopts=' \\
                      --browser=${params.BROWSER} \\
                      --headless \\
                      ${params.PYTEST_ARGS} \\
                      --html=reports/report.html \\
                      --self-contained-html
                """
            }
        }
    }

    post {
        always {
            publishHTML(target: [
                reportName:           '自动化测试报告',
                reportDir:            'reports',
                reportFiles:          'report.html',
                keepAll:              true,
                alwaysLinkToLastBuild: true,
                allowMissing:         true
            ])
            archiveArtifacts(artifacts: 'reports/**', allowEmptyArchive: true)
        }
        success {
            echo '✅ 回归全部通过'
        }
        failure {
            echo '❌ 回归失败，请查看测试报告与失败截图（latest_logs/）'
        }
    }
}
