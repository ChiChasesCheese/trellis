---
id: aid-spec-review-prompt
node: t02.spec-first-spec-driven-development
type: qa
step: 2
tags: [实践]
---
## Q
**Spec-first · 对照 spec 审查**｜实践 · 追问

实现完成了。你想让另一个 reviewer 对照 SPEC.md 检查，prompt 怎么写？为什么要加"跳过风格"？

## A
```text
review the rate limiter diff against SPEC.md.
check every requirement is implemented and the listed edge cases have tests.
report gaps that affect correctness and skip style.
```

**为什么要有"skip style"：** 被要求"找问题"的 reviewer 一定会找到点什么。如果你把每条都修掉，最终得到的是多余的抽象层和给不可能出现的情况写的测试。

| 好的审查问题 | 差的审查问题 |
|---|---|
| 每条需求都实现了吗？ | 代码质量怎么样？ |
| 列出的边界都有测试吗？ | 有什么可以改进的？ |
| 有没有影响正确性的缺口？ | 请全面检查 |

**做：** 审查的依据是 spec，输出限定为"影响正确性的缺口"。
**别做：** 开放式"找所有问题"。

**出处：** Claude Code docs《Best practices》（Review against your spec）
