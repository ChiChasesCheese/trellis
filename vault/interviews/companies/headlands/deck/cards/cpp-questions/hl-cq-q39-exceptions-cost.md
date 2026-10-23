---
id: hl-cq-q39-exceptions-cost
node: cpp-questions.i-low-latency
type: qa
step: 16
---
## Q
面试题：异常、错误码、`std::optional` / `std::expected`，它们的成本是什么？交易系统通常怎么做？
Exceptions vs error codes vs `std::optional`/`std::expected`: what do they cost, and what do trading systems do?

## A
- C++ 异常在**不抛**时几乎零成本（“零开销模型”：靠表查找，正常路径上不做检查），但**抛出很贵**（微秒级，要栈展开和查表）。
- 所以异常只用于真正的异常情况；**可预期的失败**（解析失败、找不到）用返回值：错误码（加 `[[nodiscard]]`）、`optional`（不需要原因）、`expected`（需要原因）。
- 交易系统：热路径不抛异常——校验失败返回状态码 / 枚举；初始化、配置解析这类冷路径可以抛；很多代码库整个关掉异常（`-fno-exceptions`，有的再加 `-fno-rtti`）。
