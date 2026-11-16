---
id: lcp-rate-limiter-first-instruction-to-agent
node: lcproject.lcp-rate-limiter
type: qa
step: 3
tags: [作答]
---
## Q
你在 IDE 里打开 LLM 网关限流器项目，已经读完合同，旁边有一个编程智能体面板。你给它的第一条指令写什么？哪些决定你自己留着？怎么验证它的改动？

## A
**评分点**
- 说出指令带着合同和数字例子：返回口径、截断、被拒不留痕，而不是一句写个限流器
- 说出拆成小步：先滑动窗口并只给一个失败用例，再令牌桶、统计、并发，每次只改一件事
- 说出自己留着的决定：锁的范围、remaining 口径、时间用整数纳秒还是浮点
- 说出每次改动之后点 Run 跑公开测试，再跑自己写的合同数字测试和屏障并发测试
- 说出读 diff：确认它没有改测试、没有悄悄改公开签名（HTTP 服务端依赖这些签名）
- 说出让它解释锁罩住了哪些步骤，对不上就自己改

<details class="pt"><summary>参考答案</summary>

第一条指令：贴上合同的六条规则和三个数字例子，说明"只实现滑动窗口，先让这个失败用例通过，不要动签名和测试"。锁的范围、`remaining` 口径、时间表示由我定，智能体只负责按我的决定写。每次改完点 Run，再跑自己的数字测试；读 diff，看它有没有改测试、扩大范围；让它说出锁罩住哪几步。通过后再给下一条。

</details>

**知识点：** 写清任务（Specifying the Task）、拆成可验证的小步（Decomposition）、该交给 AI 还是自己写（When to Delegate）、验证输出（Verification）
