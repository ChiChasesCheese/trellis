---
id: cc-rules-thr-band-edges
node: rules.thresholds
type: qa
---
## Q
A rule adds a penalty for hours 12–17, subtracts for 9–11 and 18–21, and does nothing otherwise. Which inputs do you test?

## A
**Both sides of all four joints: 8/9, 11/12, 17/18, 21/22.**

```python
if 12 <= hour <= 17:   score += penalty
elif 9 <= hour <= 11 or 18 <= hour <= 21: score -= penalty
```

Chained comparisons keep both ends visible and inclusive, which is what a written band ("12 to 17") means unless the statement says otherwise. The mistakes this catches: a band written as `hour > 11 and hour < 18` (fine) versus `hour > 12` (loses 12), and an `else` that silently absorbs hours 0–8 and 22–23 into a branch that should do nothing.

## Q zh
一条规则对 9–11 点和 18–21 点扣分、对 12–17 点加分，其余时段不做任何事。你测哪些输入？

## A zh
**四个接缝的两侧全测：8/9、11/12、17/18、21/22。**

```python
if 12 <= hour <= 17:   score += penalty
elif 9 <= hour <= 11 or 18 <= hour <= 21: score -= penalty
```

链式比较让两端都可见且包含，而这正是文字区间（「12 到 17」）在没有特别说明时的含义。它能抓到的错误：把区间写成 `hour > 11 and hour < 18`（正确）与写成 `hour > 12`（丢掉 12）的区别；以及一个 `else` 悄悄把 0–8 和 22–23 点吸进了本该什么都不做的分支。
