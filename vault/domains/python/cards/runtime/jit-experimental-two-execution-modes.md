---
id: jit-experimental-two-execution-modes
node: runtime.adaptive-jit
type: qa
source: cpython-internals
---
## Q
实验性 JIT 默认是开启的吗？打开之后它执行 trace 有几种方式？

## A
默认不开启：需要用 `--enable-experimental-jit`（或 `--enable-experimental-jit=interpreter`）这样的编译期配置显式打开，属于实验特性。打开后有两种执行方式：①uop 解释器——对微操作序列再做一次类似 tier 1 的 switch-case 解释执行，主要用于调试和分析；②完整 JIT——用 copy-and-patch 技术，把每个微操作对应的预编译机器码「模板」（stencil）在运行时拼接、打补丁成一段可直接执行的机器码函数，跳过解释开销。
