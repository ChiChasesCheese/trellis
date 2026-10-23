---
id: hl-javaq-f-q32-follow-ups
node: java-questions.f-concurrency
type: qa
step: 26
---
## Q
线程池怎么做背压（back-pressure）？为什么服务端用 `parallelStream()` 有风险？
How would you implement back-pressure? Why is `parallelStream()` risky in a server?

## A
- **背压**：有界队列 + `CallerRunsPolicy`（让提交者自己执行，自然放慢），或用信号量限制在途任务，或直接拒绝并返回错误。
- **`parallelStream()` 的风险**：共享 `commonPool`，阻塞任务会饿死其他使用者。
