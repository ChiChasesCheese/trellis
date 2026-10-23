---
id: hl-j16-x86-vs-arm
node: java21.j16-concurrency-primitives
type: qa
step: 30
---
## Q
x86 与 ARM 的内存模型有何不同？为什么「在我机器上没问题」不是并发正确的证据？该怎么真正验证？

## A
- **x86 是较强的内存模型（TSO）**，只允许 StoreLoad 重排，volatile 写补一个 StoreLoad 栅栏。
- **ARM 更弱**，允许四种重排，没保护的代码更容易现形（重排实验里 98% 就是这么来的）。**x86 开发机「测不出来」的 bug，部署到 ARM（Graviton、Apple Silicon）服务器可能当场爆。**
- 同理：JIT 未编译比已编译宽容，低负载比高负载宽容。
- 验证：用 `jcstress`（OpenJDK 并发压力测试工具）才算验证。
