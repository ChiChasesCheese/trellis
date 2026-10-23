---
id: hl-bs-s7-hook
node: behavioral.stories
type: qa
step: 35
---
## Q
schema pool 故事 S7 的钩子句是什么？用来回答哪些问题？开口先说什么边界？有哪些数字？

## A
钩子："**Nobody assigned it: two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of two-second zero-copy clones.**"

用于：**something you built unasked**、**curiosity about internals**、**a design you rewrote**、**how you use AI**。

先说：**"it's my personal repo, not the team toolchain."**

数字：一次克隆约 **2 秒**；**23 次提交**，全部直推 main（个人仓库）；**3 篇 ADR**；最不稳的一块（仅生产存在的依赖用结构空壳 stub）一天内约 **10 次提交**才收敛。
