---
id: cc-verification-invariant-brute-force-oracle
node: verification.invariants
type: qa
---
## Q
Your optimized solution passes every worked example. How do you get evidence that it is right on the inputs you did not think of?

## A
**Cross-check against a slow, obviously-correct reference on random inputs.**

```python
rng = random.Random(0)
for _ in range(2000):
    case = gen(rng)
    assert fast(case) == slow(case), case
```

- The oracle must be written **from the statement**, not from your fast solution — a brute force derived from the same misreading agrees with it perfectly and proves nothing.
- Keep the generated cases tiny (5–10 records): small inputs hit boundaries far more densely than large ones, and a failure stays readable.
- Print the failing case and shrink it by hand before debugging ([[cc-verification-determinism-seeded-random]]).

## Q zh
你优化过的方案通过了所有样例。你怎样拿到「它在你没想到的输入上也对」的证据？

## A zh
**在随机输入上与一个慢但显然正确的参考实现做交叉验证。**

```python
rng = random.Random(0)
for _ in range(2000):
    case = gen(rng)
    assert fast(case) == slow(case), case
```

- 那个 oracle 必须**照题面写**，而不是照你的快解写 —— 从同一处误读派生出的暴力解会与它完美一致，什么也证明不了。
- 生成的用例要小（5–10 条记录）：小输入命中边界的密度远高于大输入，失败也仍然可读。
- 打印失败用例，先手工缩小再调试（[[cc-verification-determinism-seeded-random]]）。
