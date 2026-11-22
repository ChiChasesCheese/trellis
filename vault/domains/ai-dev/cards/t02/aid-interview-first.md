---
id: aid-interview-first
node: t02.agent-interview
type: qa
step: 1
tags: [实践]
---
## Q
**先问后做 · 让 agent 访谈你**｜实践 · 必会

你想给公开 API 加限流，但具体怎么限、超限怎么办还没想清楚。直接让 agent 做会怎样？怎么用访谈把它变成 spec？

## A
**直接做的后果：** agent 会替你做选择：按用户还是按 key、超限直接拒绝还是排队。选错了你在 diff 里才发现。

**访谈 prompt（官方示例）：**

```text
I want to add rate limiting to the public API but haven't
thought it through yet. Interview me until you could write
the spec, then write it to SPEC.md.
```

agent 会返回选择题：按用户还是按 key、超限请求怎么处理、什么不在范围内；直到答案凑成一份 spec。

**之后：** 开一个新 session，从 SPEC.md 开始实现——干净的 context 加书面的"完成定义"，之后审查也对照它。

**什么时候用：** 你**不知道自己要什么**时。已经很清楚时，直接写具体 prompt 更快。

**出处：** Claude Code docs《Best practices》（Brainstorm with Claude first）
