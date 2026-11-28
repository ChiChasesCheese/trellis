---
id: hi-c-sd-temporal-x01-spot-nondeterminism
node: sd.deep-dives.temporal.exam
type: qa
step: 1
---
## Q
**Temporal · 找出 Workflow 里的非确定性**｜考点 · 必会

下面五处写在 Workflow 代码里，哪些会在重放时出问题？怎么改？①`now()` 取当前时间决定分支 ②生成随机数作为幂等键 ③直接 HTTP 调库存服务 ④遍历一个无序集合并依次调用 Activity ⑤调用 Activity 完成后再用其返回值分支。

## A
- **① 有问题：** 重放时时间不同，分支不同。用 SDK 提供的 Workflow 安全时间。
- **② 有问题：** 每次重放随机数不同，幂等键对不上。用 SDK 提供的确定性随机，或把生成放进 Activity 并记录结果。
- **③ 有问题：** 外部调用结果会变，重放时不应再次发出；放进 Activity，由框架记录结果。
- **④ 有风险：** 无序集合的遍历顺序在不同进程里可能不同，Activity 调用顺序与历史不符；先排序，或用有序结构。
- **⑤ 没问题：** Activity 的返回值被记录在历史里，重放返回同一个值，分支一致。
- **规律：** 凡是"每次执行可能得到不同结果"的来源，都要么通过框架（让结果被记录），要么放进 Activity。
