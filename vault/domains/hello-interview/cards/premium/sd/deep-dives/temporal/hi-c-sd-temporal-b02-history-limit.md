---
id: hi-c-sd-temporal-b02-history-limit
node: sd.deep-dives.temporal.beyond
type: qa
step: 2
---
## Q
**Temporal · 事件历史越来越长怎么办：continue-as-new**｜拓展 · 加分

一个"每分钟检查一次"的 Workflow 要跑一年，历史会无限增长吗？

## A
- **会的：** 每个 Activity、计时器、Signal 都往事件历史里加事件。历史有上限（51,200 个事件或 50 MB，约 1 万个事件或 10 MB 起就有警告），而且重放时间随历史变长而增加。
- **continue-as-new：** Workflow 主动结束当前执行，并以相同的 Workflow ID 启动一个新的执行，把必要的状态作为参数传过去，历史从零开始。
- **何时用：** 无限循环或超长生命周期的 Workflow（定时轮询、订阅计费）定期调用，比如每处理一批或每过一段时间。
- **对比粘性缓存：** 缓存减轻每次重放的成本；continue-as-new 把重放的上界压住。
- **设计习惯：** 估计一个 Workflow 的事件数，大于几千就要考虑拆分为子 Workflow 或 continue-as-new。
