---
id: cc-rules-thr-count-vs-ratio
node: rules.thresholds
type: qa
---
## Q
One category's tolerance is `3`, another's is `0.25`, a third's is `1.0`. State the three rules these produce.

## A
**A literal without a decimal point is a count; with one it is a ratio — including `1.0`, which means "100% of charges must be fraudulent".**

- `3` → flagged when `fraud_count >= 3`, regardless of volume.
- `0.25` → flagged when `fraud_count / total >= 1/4`, subject to any minimum-volume gate.
- `1.0` → a ratio of one, satisfied only by an all-fraud merchant. `1` would instead flag on the first fraudulent charge.

The shape of the literal is the type tag, so branch on the string before converting, and never let `float()` erase the difference. See [[cc-input-num-literal-shape]].

## Q zh
一个类别的容忍度是 `3`，另一个是 `0.25`，第三个是 `1.0`。说出这三者各自的规则。

## A zh
**不带小数点的字面量是计数；带小数点的是比率 —— 包括 `1.0`，它表示"扣款必须 100% 是欺诈"。**

- `3` → `fraud_count >= 3` 时标记，与交易量无关。
- `0.25` → `fraud_count / total >= 1/4` 时标记，还要受最小交易量门槛约束。
- `1.0` → 比率为 1，只有全部欺诈的商户才满足。而 `1` 会在第一笔欺诈扣款就标记。

字面量的形状就是类型标签，所以要在转换之前对字符串分支，绝不要让 `float()` 抹掉这个区别。见 [[cc-input-num-literal-shape]]。
