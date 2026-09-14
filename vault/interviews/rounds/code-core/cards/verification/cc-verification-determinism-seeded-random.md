---
id: cc-verification-determinism-seeded-random
node: verification.determinism
type: qa
---
## Q
Your randomized cross-check found a bug yesterday and passes today. What went wrong, and what is the discipline?

## A
**Unseeded randomness makes a failure unreproducible** — you cannot debug what you cannot re-run.

```python
rng = random.Random(0)      # an instance, not random.seed(0)
```

- Use an **instance**: the module-level generator is global state that any import or other test can advance, so two files silently interfere and neither is repeatable.
- Attach the failing case to the assertion message so a red run carries its own reproduction.
- When one fails, shrink it by hand to the smallest input that still fails before debugging: a 4-record counterexample is a fix, a 40-record one is an afternoon.

## Q zh
你的随机交叉验证昨天抓到了一个 bug，今天却通过了。哪里出了问题？纪律是什么？

## A zh
**没有种子的随机让失败无法复现** —— 你没法调试一个跑不回来的东西。

```python
rng = random.Random(0)      # 用实例，不是 random.seed(0)
```

- 用**实例**：模块级生成器是全局状态，任何 import 或别的测试都能推进它，于是两个文件互相干扰、谁也不可重复。
- 把失败用例挂进断言信息里，让一次变红的运行自带复现方式。
- 一旦有用例失败，先手工把它缩到仍然失败的最小输入再调试：4 条记录的反例是一次修复，40 条的是一个下午。
