---
id: s13-closed-intervals-offbyone
node: stripe.time
type: qa
---

## Q
为什么 BIN 区间、部署窗口、营业时段这类题的唯一难点是端点？闭区间 vs 半开区间该怎么处理才能不翻车？

## A
这类题全都是区间题，逻辑本身不难，**端点处理是唯一的难点**。

**做法**：在函数顶端用注释**声明区间惯例**，然后全程只用这一种：

```python
# 全文件惯例：[lo, hi] 闭区间，整数域
```

**闭区间的三个基本操作**：

```python
overlap  = a.lo <= b.hi and b.lo <= a.hi
adjacent = a.hi + 1 == b.lo            # 整数域才有"相邻"
merged   = (min(a.lo, b.lo), max(a.hi, b.hi))
gap      = (a.hi + 1, b.lo - 1)        # 仅当 a.hi + 1 <= b.lo - 1
```

半开区间 `[lo, hi)` 的对应式子里没有 `+1`，这就是为什么必须先声明惯例——两种表示不能混用。

**典型翻车**：`merge` 时用了 `a.hi < b.lo` 判断"不重叠"，但整数域里 `[1,3]` 和 `[4,6]` 其实是相邻的，应该合并成 `[1,6]`。
