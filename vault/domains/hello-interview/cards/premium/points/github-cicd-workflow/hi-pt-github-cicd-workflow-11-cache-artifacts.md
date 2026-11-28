---
id: hi-pt-github-cicd-workflow-11-cache-artifacts
node: qb.sd.github-cicd-workflow.points
type: qa
step: 11
---
## Q
**CI/CD 平台 · 缓存与产物**｜加分 · 出自：CI/CD 平台 › 深入 7

CI/CD 平台里，很多任务反复下载同样的依赖。怎样加速？

## A
**做法。** 依赖缓存按 (repo, key) 存对象存储，任务开始时恢复、结束时保存；构件（artifact）设保留期；执行镜像预热到暖池节点，减少冷启动。
