---
id: hl-hc03-trampoline
node: problems.hc03-recursive-sum
type: qa
step: 8
---
## Q
Trampoline（蹦床）怎么把递归的栈换成堆？写出 `Trampoline`、`step` 和 `run`，并说清楚它的代价。

## A
思路：函数不直接调用下一步，而**返回一个描述「下一步做什么」的对象**；外层 `while` 循环不断取出执行直到拿到答案。每步立刻返回（栈帧立刻弹出），待办放在**堆**上，栈深恒定。

```java
sealed interface Trampoline<T> permits Done, More {}
record Done<T>(T value) implements Trampoline<T> {}
record More<T>(Supplier<Trampoline<T>> next) implements Trampoline<T> {}

static Trampoline<Long> step(long n, long acc, Width w) {
    return n == 0 ? new Done<>(acc)
                  : new More<>(() -> step(n - 1, w.add(acc, n), w));
}
static <T> T run(Trampoline<T> start) {
    var cur = start;
    while (true) switch (cur) {
        case Done<T>(var v)    -> { return v; }
        case More<T>(var next) -> cur = next.get();
    }
}
```
关键：`w.add(acc, n)` 写在 **lambda 里**，延迟到 `run` 循环才执行；写成急切求值就把递归又写回栈上。溢出时 `w.add` 抛 `ArithmeticException`，抛到入口转成 `Overflow`。

**代价**：每步在堆上分配一个 `More` + 一个 lambda（逃逸分析救不了，它们被 `Supplier` 返回出去）。n = 5×10⁶ 约 14 ms，约 2.5 ns/步，比循环慢约 10 倍，与递归同量级。**trampoline 解决「不爆栈」，不解决「更快」。**

互递归 `isEven(n) = n==0 ? true : isOdd(n-1)` / `isOdd` 连 `@tailrec` 都不处理，trampoline 可以：两个函数都返回 `Trampoline<Boolean>`，512 KiB 栈上能跑到 n = 200 万。
