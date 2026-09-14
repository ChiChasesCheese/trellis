---
id: cc-round-reading-later-part-flips-a-rule
node: round.reading
type: qa
---
## Q
Part 2 says a new subscription start *replaces* the old one; Part 3 says a start on a still-active subscription *extends* it from the current expiry. You notice this at minute 3. How do you structure the code?

## A
**One `simulate()` with a mode, not two copied loops.** The later part flips a rule rather than adding one, so write the rule once and parameterize it:

```python
expiry = t + d if mode == "replace" else max(expiry, t) + d
```

Two copies drift on every later fix, and you will fix the one the current part is testing. Reading all parts first is what lets you see the flip before you have written the first version — a flipped rule discovered late is the most common cause of "Part 3 broke Part 2". See [[cc-round-ambiguity-one-flag-away]].

## Q zh
Part 2 说新的 subscription start **替换**旧的；Part 3 说在仍然有效的订阅上 start 会从当前到期时间**延长**。你在第 3 分钟就看到了这点。代码怎么组织？

## A zh
**一个带 mode 的 `simulate()`，而不是两份复制的循环。** 后一部分是翻转规则而不是新增规则，所以规则只写一次并参数化：

```python
expiry = t + d if mode == "replace" else max(expiry, t) + d
```

两份副本会在后续每次修改时漂移，而你只会改当前正在测的那一份。先读完所有部分，才能在写出第一版之前看到这个翻转 —— 太晚发现规则被翻转，是"Part 3 弄坏了 Part 2"的最常见原因。见 [[cc-round-ambiguity-one-flag-away]]。
