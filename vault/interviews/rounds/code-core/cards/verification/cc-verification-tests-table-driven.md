---
id: cc-verification-tests-table-driven
node: verification.tests
type: qa
---
## Q
You need ten cases for one function, fast. What structure do you use, and what does it buy you beyond typing speed?

## A
**A table of `(name, input, expected)` and one loop — or `@pytest.mark.parametrize`.**

```python
CASES = [("exact", ["A,2"], ["A"]),
         ("below", ["A,1"], ["NONE"])]
for name, given, want in CASES:
    assert solve(given) == want, name
```

- With `parametrize` each case reports separately, so you learn *which* shapes fail rather than that something did.
- An eleventh case is one line — which is what makes you actually add it under time pressure.
- The names become a checklist you can read straight against the statement's edge-case list.
- Keep every expectation literal; an expectation computed by the code under test reproduces the bug it is meant to catch.

## Q zh
你需要为一个函数快速凑十个用例。用什么结构？除了打字快之外它买到了什么？

## A zh
**一张 `(name, input, expected)` 的表加一个循环 —— 或者 `@pytest.mark.parametrize`。**

```python
CASES = [("exact", ["A,2"], ["A"]),
         ("below", ["A,1"], ["NONE"])]
for name, given, want in CASES:
    assert solve(given) == want, name
```

- 用 `parametrize` 时每个用例单独报告，于是你知道*哪些*形态挂了，而不只是「有东西挂了」。
- 第十一个用例只是一行 —— 而这正是你在时间压力下真的会去加它的原因。
- 这些名字组成一份清单，可以直接对着题面的边界用例列表读。
- 期望值要写死；由被测代码算出来的期望值会复现它本该抓住的那个 bug。
