---
id: quality-test-doubles
node: quality.testability
type: qa
---
## Q
Stub vs mock vs fake — separate the three doubles people actually confuse, by what the test asserts on.

## A
- **Stub**: returns canned answers so the code under test can run (`stubRates.get("EUR") → 1.1`). The test asserts on the **system's output/state** — the stub is scenery.
- **Mock**: records calls and the test **asserts on the interaction itself** — "`emailSender.send()` was called once with X." Use only when the side effect *is* the requirement; over-mocking welds tests to implementation details.
- **Fake**: a real, working, lightweight implementation (in-memory repository, embedded queue). Behaves properly across many calls, so it suits whole-flow tests without a DB.

(Remaining taxonomy: **dummy** — passed but never used; **spy** — a stub that also records, letting you assert afterward instead of setting expectations upfront.)

## Q zh
Stub、mock、fake —— 按"测试断言的是什么"来区分这三个真正被搞混的替身。

## A zh
- **Stub**：返回预设答案，好让被测代码能跑下去（`stubRates.get("EUR") → 1.1`）。测试断言的是**系统的输出/状态** —— stub 只是布景。
- **Mock**：记录调用，测试**断言的是交互本身** —— "`emailSender.send()` 被调用了一次，参数是 X"。只在这个副作用*本身就是需求*时才用；过度 mock 会把测试焊死在实现细节上。
- **Fake**：一个真实可用的轻量实现（内存仓储、嵌入式队列）。多次调用之间行为正确，所以适合不带数据库的全流程测试。

（分类里剩下的两个：**dummy** —— 传进去但从不使用；**spy** —— 会记录的 stub，让你在事后断言，而不必预先设置期望。）
