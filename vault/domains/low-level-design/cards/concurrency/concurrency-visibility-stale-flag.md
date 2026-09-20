---
id: concurrency-visibility-stale-flag
node: concurrency.model
type: qa
---
## Q
线程 A 把 `running` 设成了 false，但那个在 `while (running) {}` 上循环的工作线程永远不停 —— 没有崩溃，也没有异常。为什么会这样，有哪两种修法？

## A
这个写和那些读之间**没有 happens-before 边**：写可能还压在 store buffer 里，而 JIT 甚至可能把这次读整个提到循环外面（它"证明"了 `running` 在本线程内不会变）。

- 修法一：把这个标志声明为 `volatile` / 原子类型 —— 每次读都能看到最新的写。
- 修法二：在**同一把锁**下读写它（释放锁 → 获取锁 建立了顺序关系）。

关键：这是一个**可见性** bug，不是原子性 bug —— 那次写确实发生了，只是不保证被看见。
