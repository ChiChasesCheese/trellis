---
id: tr-ci-pipeline-design-github-actions
node: ci.pipeline-design
type: qa
step: 2
---
## Q
GitHub Actions 的核心概念有哪些（workflow、job、step、runner、trigger、artifact、cache）？写一个"PR 上跑测试、硬件测试跑在自建机器上"的最小配置。

## A
- **workflow**：`.github/workflows/*.yml` 里的一个流水线文件，"流水线即代码"，和代码一起评审、一起版本化。
- **trigger（`on:`）**：什么事件触发。常见：`pull_request`（PR 更新时，测的是 PR 与目标分支的合并结果）、`push`、`schedule`（cron，做夜间作业）、`workflow_dispatch`（手动）、`merge_group`（合并队列）。
- **job**：一组步骤，在同一台 runner 上执行；不同 job 默认并行，`needs:` 声明依赖顺序。
- **step**：job 里的一条命令或一个复用的 action。
- **runner**：执行 job 的机器。GitHub 托管的，或自建的（self-hosted），用标签选择：`runs-on: [self-hosted, hw-a]`。自建 runner 主动向 GitHub 长轮询领取任务，所以实验室机器不需要开放入站端口。
- **artifact**：job 之间或运行之后要保留的文件，`actions/upload-artifact` / `download-artifact`。
- **cache**：跨运行复用的依赖目录，`actions/cache`，按 key 命中，可能不命中。

```yaml
on: [pull_request]
concurrency: {group: "pr-${{ github.ref }}", cancel-in-progress: true}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: uv build
      - uses: actions/upload-artifact@v4
        with: {name: dist, path: dist/}
  hw-test:
    needs: build
    runs-on: [self-hosted, hw-a]
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with: {name: dist, path: dist/}
      - run: uv run pytest -m hardware --junitxml=report.xml
```

`concurrency` 让同一个 PR 推了新提交时取消旧的运行，省下稀缺的硬件 runner；`needs: build` 保证硬件测试用的是同一份构建产物。
