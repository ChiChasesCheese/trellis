---
id: pl-bench-pitfall-warmup
node: engineering.benchmarking
type: qa
step: 10
---
## Q
在 Java 里手写 `System.nanoTime()` 循环做基准，为什么会得到错误的数字？

## A
因为 JVM 的速度随运行时间变化。下面这段代码把同一个函数连续测 8 轮，每轮 200 万次调用：

```java
for (int round = 1; round <= 8; round++) {
    long t = System.nanoTime();
    for (int i = 0; i < 2_000_000; i++) s += mix(i);
    System.out.printf("round %d: %.2f ns/op%n", round, (System.nanoTime() - t) / 2e6);
}
```

输出（本机一次运行）：

```text
round 1: 1.00 ns/op
round 2: 1.13 ns/op
round 3: 0.40 ns/op
round 4: 0.39 ns/op
...
round 8: 0.39 ns/op
```

前两轮是解释执行和 C1 编译的代码，约慢 2.5 到 3 倍；从第 3 轮起 C2 编译完成，数字稳定在 0.4 ns 左右（第 5 到 7 轮同为 0.39，此处省略）。热循环就写在 `main` 里，JVM 靠栈上替换（OSR）在循环中途切换到编译后的代码，所以前两轮是混合状态。

后果：只跑一轮会高估约 2.5 倍；如果跑「一个总循环再除以总次数」，结果取决于总共跑了多久，因为预热期被平均进去了，改变迭代次数就会改变结论。

**怎么办**：用 JMH（它把预热轮和测量轮分开）。如果只能手写，至少要：预热到数字稳定再计时，多轮测量，输出每轮的数字而不是只给一个平均值，并让结果被使用（累加后打印），防止计算被删除。
