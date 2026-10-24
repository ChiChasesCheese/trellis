---
id: pl-rt-jit-evolution
node: runtime.jit
type: qa
step: 10
---
## Q
JIT 技术是怎么发展的？今天 JIT 与 AOT 正在走向怎样的融合？

## A
**起源**：自适应优化来自 Self 语言和 Smalltalk 的研究（1980–90 年代）：在动态语言上做类型反馈和去优化。Self 团队的核心人员后来创建了 HotSpot（Java 1.3，2000 年前后成为默认），把这些思想带入主流；V8（Chrome，2008）把它用于 JavaScript，让动态语言的性能提升了一个数量级。

**路线分化**：
- **方法 JIT + 分层**：HotSpot、V8、.NET。
- **追踪 JIT**：LuaJIT 与 PyPy，对热循环极有效；但实现复杂，对非循环、分支多的代码收益有限。
- **元追踪**：PyPy 的 RPython 框架，语言实现者写解释器，工具链自动生成 JIT；GraalVM / Truffle 走“部分求值”路线。
- **轻量级 JIT**：CPython 3.13 起的 copy-and-patch JIT（PEP 744），目标是低复杂度、低维护成本，先拿到小收益，再逐步改进；3.14 中仍是实验性、默认关闭。

**趋势：JIT 与 AOT 互相借鉴**：
1. JIT 语言想要 AOT 的启动速度：Java 的 CDS、AOT 缓存（Leyden 项目）、GraalVM Native Image；.NET 的 ReadyToRun 与 Native AOT。
2. AOT 语言想要 JIT 的运行时信息：PGO（Go 1.21 起正式支持、Rust、C++），用线上 profile 指导内联与布局，BOLT 之类的后链接优化。
3. 云原生场景下，“冷启动 + 低内存”重新抬高了 AOT 的价值，而长期运行的大型后端服务仍然靠 JIT 的稳态性能。
4. WebAssembly 作为可移植的 AOT/JIT 通用目标，把“字节码 + 运行时编译”的思路带到浏览器之外。

判断依据始终是工作负载：长期运行、热点集中、类型动态 → JIT 价值大；短命、对启动与内存敏感、行为可预测 → AOT 更合适。
