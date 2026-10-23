---
id: hl-cq-q39-followups
node: cpp-questions.i-low-latency
type: qa
step: 19
---
## Q
两个追问：C++ 的异常安全保证有哪几级？为什么启用异常会让二进制变大？

## A
- **异常安全保证**：基本保证（basic）——不变量保持、不泄漏；强保证（strong）——提交或回滚；不抛保证（no-throw）——`noexcept`。
- **二进制变大**：每个有析构函数要运行的函数都带展开表（unwind tables）和着陆点（landing pads）。
