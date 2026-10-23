---
id: hl-hc03-three-escapes
node: problems.hc03-recursive-sum
type: qa
step: 9
---
## Q
Java 里深递归爆栈有哪三条出路？各自的复杂度和取舍是什么？

## A
1. **改成迭代**（`sumToIterative`）：`long acc = 0; for (long i = 1; i <= n; i++) acc = w.add(acc, i);` 时间 O(n)，栈 O(1)，n = 3×10⁸ 约 77 ms。需要「必须用递归」时才继续往下。
2. **Trampoline**：把递归调用变成「返回一个待办」，`run` 用 `while` + 模式匹配 switch 驱动；栈 O(1)，堆上每步一个短命对象，GC 压力 O(n)。比「改写成循环」通用（能处理互递归）。
3. **加大栈** `new Thread(null, r, name, size)`：治标；`-Xss` 影响所有线程，代价是内存。

尾递归写法 `step(n, acc) = n == 0 ? acc : step(n-1, acc+n)` 在 Java 里**仍然叠 n 层栈帧**，不能指望编译器。

**测试要求**：512 KiB 栈上 `sumToRecursive(1_000_000)` 必须抛 `StackOverflowError`；`sumToTrampoline` / `sumToIterative` 必须返回 `Ok(500000500000)`。

**要诚实说的**：栈深度阈值不是常数；`StackOverflowError` 是 `Error`，捕获只用来测量，业务不靠它兜底。
