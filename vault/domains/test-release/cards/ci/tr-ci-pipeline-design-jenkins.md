---
id: tr-ci-pipeline-design-jenkins
node: ci.pipeline-design
type: qa
step: 3
---
## Q
Jenkins 的核心概念（controller、agent、Jenkinsfile、stage、`post`）是什么？和 GitHub Actions 相比，它在硬件测试场景下有什么优缺点？

## A
- **controller**：Jenkins 主服务，保存作业配置和历史、调度构建、提供界面。
- **agent**（旧称 slave / node）：真正执行构建的机器，用标签（label）区分，例如 `hw-a`、`linux`。
- **Jenkinsfile**：放在仓库里的流水线定义（Groovy 语法）。声明式写法：

```groovy
pipeline {
  agent none
  stages {
    stage('Build') {
      agent { label 'linux' }
      steps { sh 'make build'; stash name: 'dist', includes: 'dist/**' }
    }
    stage('HW test') {
      agent { label 'hw-a' }
      options { timeout(time: 60, unit: 'MINUTES') }
      steps { unstash 'dist'; sh 'pytest -m hardware --junitxml=report.xml' }
    }
  }
  post { always { junit '**/report.xml' } }
}
```

- **stage / steps**：阶段和命令；`stash` / `unstash` 在同一次运行的不同机器之间传文件，`archiveArtifacts` 长期保存。
- **post**：`always`、`failure`、`success` 等条件下的收尾，例如无论成败都收集 JUnit 报告。
- **插件**：几乎所有能力都来自插件，例如 Lockable Resources 的 `lock(label: 'hw-a', quantity: 2)` 实现稀缺设备的排队。

**和 GitHub Actions 比**：
- **Jenkins 的优点**：完全自建，适合内网实验室和特殊硬件；插件多，资源锁、复杂调度、参数化构建都成熟；可以长期运行、手工触发、带参数的发布作业。
- **Jenkins 的缺点**：controller 要自己运维、升级、备份；插件版本互相冲突是常见故障；配置容易散落在界面里，不在代码中。
- **GitHub Actions 的优点**：和代码评审天然集成，托管 runner 免运维，配置全部在仓库里。
- **GitHub Actions 的缺点**：复杂的资源调度、长时间作业、内网硬件需要自建 runner 和额外工具。

很多团队两者并用：代码评审相关的快速检查放 GitHub Actions，硬件实验室和发布流水线放 Jenkins。
