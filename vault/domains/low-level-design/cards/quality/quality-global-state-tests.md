---
id: quality-global-state-tests
node: quality.testability
type: qa
---
## Q
Name the two distinct ways static/global state breaks tests, and the standard fix for nondeterministic dependencies like time.

## A
Two failure modes:

- **No substitution point**: `Payment.process()` as a static call (or `Singleton.getInstance()`) can't be replaced — every test drags the real implementation along.
- **State leaks between tests**: a mutable global survives across test methods, so tests pass alone and fail in suite (or in parallel) depending on **order** — the worst kind of flake.

Fix for time (the canonical case): never call `LocalDateTime.now()` in domain logic — inject a `Clock`; tests pass `Clock.fixed(...)` and can step time deterministically. Same recipe for randomness (`Random` seed/interface) and UUIDs (injected `IdGenerator`). Legacy escape hatch: wrap the static in an instance class you can inject — then migrate.

## Q zh
说出静态/全局状态破坏测试的两种不同方式，以及对时间这类不确定依赖的标准修法。

## A zh
两种失败模式：

- **没有可替换点**：`Payment.process()` 这样的静态调用（或 `Singleton.getInstance()`）无法被替换 —— 每个测试都被迫拖着真实实现一起跑。
- **状态在测试之间泄漏**：可变的全局变量跨测试方法存活，于是测试单独跑能过、进了套件（或并行）就挂，取决于**执行顺序** —— 最难缠的一类 flaky。

时间的修法（最典型的例子）：领域逻辑里永远不要调用 `LocalDateTime.now()` —— 注入一个 `Clock`；测试传 `Clock.fixed(...)`，还能确定性地推进时间。随机性（`Random` 种子或接口）和 UUID（注入 `IdGenerator`）是同一套配方。遗留代码的逃生口：把静态调用包进一个可注入的实例类里 —— 然后再迁移。
