---
id: cc-python-portability-integer-division
node: python.portability
type: qa
---
## Q
Your hour-bucket code is `t // 3600` and passes every test. You port it to Java. What breaks, and where else does the same difference bite?

## A
**Python's `//` floors toward −∞; Java, Go, C and C# truncate toward zero.** For a negative `t` — a timestamp shifted by a negative UTC offset, an offset before an epoch — `-1 // 3600` is `-1` in Python and `0` in Java, so the bucket index moves by one.

- Java: `Math.floorDiv(a, b)` and `Math.floorMod(a, b)` reproduce Python exactly; Go has no built-in, so hand-roll it.
- JavaScript has no integer division at all: `Math.floor(a / b)` for Python's behaviour, `Math.trunc` for C's.
- `%` follows the same split: Python's result takes the **divisor's** sign, Java's takes the **dividend's** ([[cc-python-pitfalls-negative-floordiv]]).

## Q zh
你的小时分桶代码是 `t // 3600`，所有测试都过。你把它移植到 Java。什么坏了？同样的差异还会在哪里咬人？

## A zh
**Python 的 `//` 朝负无穷向下取整；Java、Go、C、C# 朝零截断。** 对负的 `t` —— 被负 UTC 偏移平移过的时间戳、纪元之前的偏移 —— `-1 // 3600` 在 Python 里是 `-1`，在 Java 里是 `0`，于是桶下标错一位。

- Java：`Math.floorDiv(a, b)` 和 `Math.floorMod(a, b)` 精确复现 Python；Go 没有内置，得自己写。
- JavaScript 根本没有整数除法：要 Python 的行为用 `Math.floor(a / b)`，要 C 的行为用 `Math.trunc`。
- `%` 也是同一条分界：Python 的结果取**除数**的符号，Java 的取**被除数**的（[[cc-python-pitfalls-negative-floordiv]]）。
