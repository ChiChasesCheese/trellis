---
id: cc-rules-thr-min-volume-gate
node: rules.thresholds
type: qa
---
## Q
Why does a ratio threshold need a minimum-volume gate, and where exactly does the gate's own boundary sit?

## A
**Because one fraudulent charge out of one is a ratio of 1.0 — without a gate, every new merchant with a single bad charge is flagged.**

```python
if kind == "ratio" and total < min_count:
    return False
```

The gate boundary is itself a tested threshold: `total == min_count` **passes** the gate ("minimum" is inclusive), `min_count - 1` does not. Two further decisions to read out of the statement: the gate applies to ratio thresholds only (count thresholds are volume-free), and the default when no minimum is configured is 0, not 1.

## Q zh
比率阈值为什么需要最小交易量门槛？这个门槛自己的边界又落在哪？

## A zh
**因为 1 笔里有 1 笔欺诈就是 1.0 的比率 —— 没有门槛的话，任何只有一笔坏账的新商户都会被标记。**

```python
if kind == "ratio" and total < min_count:
    return False
```

门槛边界本身就是被测的阈值：`total == min_count` **通过**门槛（「最小」是包含的），`min_count - 1` 不通过。还有两个要从题面读出的决定：门槛只作用于比率阈值（计数阈值与交易量无关）；以及未配置最小值时默认是 0 而不是 1。
