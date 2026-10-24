---
id: pl-memory-memory-safety-best-practice
node: memory.memory-safety
type: qa
step: 7
---
## Q
在工程实践里，怎样最大化内存安全？各语言的有经验团队分别做什么？

## A
总原则：**默认选内存安全的语言；把不安全的部分缩到最小、封装起来、重点测试。**

1. **选型**：新写的网络服务、解析不可信输入的代码，优先 Go、Java、Rust、Python，而不是 C、C++。这是收益最大的一步，因为它排除了整类漏洞。
2. **隔离不安全代码**：Rust 把 `unsafe` 限制在一个小模块里，对外暴露安全接口，每个 `unsafe` 块写明它依赖的前提（`// SAFETY:` 注释）。Python 的 C 扩展、Java 的 JNI 与 FFM、Go 的 cgo 同理，边界越窄越好。
3. **用工具兜底**：
   - Go：测试与 CI 一律带 `-race`；
   - Rust：对 `unsafe` 代码跑 Miri；
   - C/C++：AddressSanitizer、UndefinedBehaviorSanitizer，加模糊测试（fuzzing）；
   - 所有语言：对处理外部输入的解析器做模糊测试。
4. **并发代码要有专门的策略**：Go 用 channel 转移所有权、锁保护的数据与锁放在同一个结构体里并注明；Java 优先使用不可变对象和 `java.util.concurrent`；Rust 让 `Send`/`Sync` 替你检查。
5. **限制输入**：显式检查长度与范围，即使语言已有边界检查。越界 panic 虽然不会被利用，却是拒绝服务（DoS）的入口。

为什么：内存安全是一个光谱，真实系统的风险集中在边界：FFI、unsafe、并发。把审查和测试资源集中在这几处，比到处撒网有效。

什么时候违反：极端性能或硬件交互场景下确实需要 unsafe 或 C，这时保证它被封装、被审计，而不是被取消。
