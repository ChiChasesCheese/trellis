---
id: hl-j16-aba-experiment
node: java21.j16-concurrency-primitives
type: qa
step: 33
---
## Q
确定性复现 ABA：初始栈 `A→B→C`，线程 1 读到 `top=A`、`next=B` 后暂停，线程 2 弹 A、弹 B、再压回 A，线程 1 恢复做 `CAS(top, A, B)`。朴素版与 `AtomicStampedReference` 版最终栈各是什么？

## A
- 正确结果应是 `[C]`：A、B 都被弹走过，线程 2 把 A 压回，线程 1 再把 A 弹掉，只剩 C。
- **朴素版**最终栈 `[B C]`：线程 1 的 CAS 看到 `top` 仍是 A 就成功，把 `top` 设成了过期的 B，B 已被线程 2 弹走却又回到栈里。
- **加版本号**最终栈 `[C]`：线程 2 每次改动戳 +1，线程 1 的 CAS 因戳不同失败，重读后得到正确结果。
