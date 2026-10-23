---
id: hl-j16-visibility-experiment
node: java21.j16-concurrency-primitives
type: qa
step: 4
---
## Q
可见性实验：reader 线程 `while (!plainStop) n++;`，主线程 sleep 300 ms 后设 stop = true。普通字段、`volatile`、`-Xint` 三种情况各是什么结果？这说明并发 bug 的什么特点？

## A
- 普通字段：1 秒后 reader **仍在运行**，没看到 stop 的写入；
- `volatile`：已正常结束；
- 加 `-Xint`（关掉 JIT，只解释执行）：普通字段版也「正常」结束了。

结论：**同一份代码，行为取决于 JIT 是否编译了它**。并发 bug 最阴险处：开发机、单元测试、低负载下全对，上线跑热才出问题。主线程先 sleep 300 ms 是为了让 reader 被 JIT 编译。
