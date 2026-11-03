---
id: hi-pt-coding-contest-platform-3-async-flow
node: qb.sd.coding-contest-platform.points
type: qa
step: 3
---
## Q
**在线判题与编程竞赛平台 · 异步提交流程**｜必会 · 出自：在线判题与编程竞赛平台 › 整体设计

提交代码后系统内部怎么走？为什么用队列而不是 API 同步直连容器？

## A
**流程。** API 校验后把代码写对象存储，插入状态 QUEUED 的提交记录，向队列投只含 submission_id 的消息并立即返回；按语言分池的 worker 拉取、沙箱里编译并逐点运行，条件更新写回结果，再更新排行榜。
**为什么队列。** 削峰、重试、比赛优先于练习的分队列、worker 独立伸缩；worker 崩溃消息重新可见，被别的 worker 重判，不丢提交。
