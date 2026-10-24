%% trellis:begin %%
# 用户态线程：goroutine 与虚拟线程
*并发与并行*

M:N 调度：Go 的 GMP 调度器与可增长栈、Java 21 虚拟线程；为什么能开几十万个、阻塞调用怎么处理。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/concurrency.os-threads|操作系统线程（1:1 模型）]]

**Unlocks:** [[domains/pl/map/concurrency.async-await|async/await 与函数着色]], [[domains/pl/map/concurrency.channels-csp|通道与 CSP]], [[domains/pl/map/concurrency.structured-concurrency|结构化并发]], [[domains/pl/map/signatures.go|Go 的独到之处]]

## Cards (10)
1. [[pl-conc-green-threads-principle]]
2. [[pl-conc-green-threads-found-goroutine]]
3. [[pl-conc-green-threads-found-gmp]]
4. [[pl-conc-green-threads-found-virtual]]
5. [[pl-conc-green-threads-mechanism-blocking]]
6. [[pl-conc-green-threads-table]]
7. [[pl-conc-green-threads-unique-preempt]]
8. [[pl-conc-green-threads-best-practice]]
9. [[pl-conc-green-threads-pitfall-leak]]
10. [[pl-conc-green-threads-evolution]]
%% trellis:end %%

## Notes
