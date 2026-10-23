---
id: hft-java-modern-vector-api
node: java.modern
type: qa
step: 3
---
## Q
Vector API 是什么？在什么情况下对交易相关的数值计算有帮助？

## A
Vector API（`jdk.incubator.vector`，仍是孵化中的 API，需要 `--add-modules`）让 Java 代码显式使用 **SIMD**（单指令多数据：一条 CPU 指令同时处理多个数）。例如 AVX2 的 256 位寄存器一次能处理 4 个 `double` 或 8 个 `float`，对大数组做求和、点积、归一化时，理论上最多能快数倍。

适合：研究平台里对大数组的数值运算（协方差、特征计算、批量定价）、批量编解码这类数据量大且分支少的循环。

不适合：每条消息分支很多、数据量很小的热路径逻辑，向量化的收益很容易被装载和分支抵消。JIT 本身也会对简单循环做自动向量化，Vector API 用在你需要明确控制、而自动向量化做不到的地方。因为 API 仍在孵化，可能变动，上生产前要评估。
