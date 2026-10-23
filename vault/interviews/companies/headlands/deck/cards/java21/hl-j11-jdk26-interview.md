---
id: hl-j11-jdk26-interview
node: java21.j11-structured-concurrency
type: qa
step: 17
---
## Q
JDK 26 的 `StructuredTaskScope` 有哪些小改动？面试里该讲 API 细节还是概念？

## A
**JDK 26** 小改，仍是预览：新增 `Joiner.onTimeout()`；`allSuccessfulOrThrow()` 改为返回结果列表；`anySuccessfulResultOrThrow()` 改名为 `anySuccessfulOrThrow()`。

面试重点讲**概念**，不要背 API 细节：
- 子任务生命周期被词法作用域框住；
- 失败和取消统一处理；
- 取消靠中断。

生产代码用不用，取决于能否接受每次升级 JDK 都改代码。
