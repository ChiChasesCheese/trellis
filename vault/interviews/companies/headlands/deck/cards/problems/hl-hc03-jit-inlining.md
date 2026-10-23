---
id: hl-hc03-jit-inlining
node: problems.hc03-recursive-sum
type: qa
step: 10
---
## Q
为什么递归求和比循环慢得多？JIT 的内联（inlining）对递归有什么限制？

## A
实测 n = 10 000 重复 20 000 次（2×10⁸ 步）：递归约 570–650 ms（约 3 ns/步），迭代约 50 ms（约 0.25 ns/步），trampoline 约 460–535 ms（约 2.5 ns/步）。

原因：**内联**把被调方法代码直接贴到调用处，省掉压栈、跳转、返回，并让编译器优化更大范围。C2 对**递归调用**只内联 `MaxRecursiveInlineLevel`（默认 1）层，`-XX:+PrintInlining` 对 `addUp` 的输出是 `@ 14 Inl::addUp inline` 之后 `recursive inlining too deep`。所以每一层仍是真函数调用：压帧、栈检查（stack banging）、返回后才做 `addExact`。循环则能展开、去掉冗余检查，`Math.addExact` 是 intrinsic（一条加法 + 溢出标志跳转，溢出分支走 uncommon trap）。

热方法先被 C1 编译（tier 3，带 profile）再被 C2（tier 4）。副作用：同一递归方法**解释执行**时的栈帧比编译后大几倍，所以「能递归多深」不是常数（冷 17 258 → 热 57 996 层）。

基准做法：预热 + 取多次最小值；单次 `System.nanoTime` 只能说明数量级，不是 JMH。
