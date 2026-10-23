---
id: hl-bs-s7-followups
node: behavioral.stories
type: qa
step: 40
---
## Q
被追问 S7：两个会话抢同一个 slot 怎么办？会话崩溃占着 slot 怎么办？你怎么信任 AI 写的代码？为什么直接推 main？
Two sessions grab the same slot? Session crashes holding a slot? Why direct-push to main?

## A
- **Two sessions grab the same slot?** 【待补：真实的借用/归还机制】
- **Session crashes holding a slot?** 【待补：泄漏回收】
- **How do you trust AI-written code?** 与 agent **一起做计划**，每个阶段 **TDD**，用 **CI 和监控的门**；盯**门和阈值**，不盯行；涉及钱的代码**读每个 diff**。
- **Why direct-push to main?** **个人仓库**，不碰团队代码。
