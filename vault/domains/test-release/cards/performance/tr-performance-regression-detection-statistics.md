---
id: tr-performance-regression-detection-statistics
node: performance.regression-detection
type: qa
step: 2
---
## Q
两组性能数据（基线 10 次、新版本 10 次），怎么判断新版本是否真的变慢？为什么不能只比较平均值差了几个百分点？

## A
**只比较平均值的问题**：
- 不知道差异是否超过噪声。噪声变异系数（标准差 ÷ 均值）是 5% 时，两组均值差 3% 很可能只是运气；
- 平均值被一两次离群运行（例如那次机器上有别的进程）拖偏。

**两个条件同时满足才报回归**：
1. **效应足够大**：中位数的相对变化超过"最小有意义变化"，例如 3%。小于这个值即使统计显著，也不值得处理。
2. **统计显著**：用不假设正态分布的检验，例如 Mann–Whitney U 检验；或者用自助法（bootstrap）估计"中位数之比"的置信区间，区间不包含 1.0 才算显著。

```python
from scipy.stats import mannwhitneyu
import numpy as np

def is_regression(base, new, min_effect=0.03, alpha=0.01):
    ratio = np.median(new) / np.median(base)   # 延迟类指标，越大越差
    p = mannwhitneyu(new, base, alternative="greater").pvalue
    return ratio > 1 + min_effect and p < alpha, ratio, p
```

**多重比较陷阱**：每晚检测 200 个基准配置，每个用 `alpha=0.05`，即使什么都没变，平均也会有约 10 个误报。办法：降低 alpha（例如 0.01）、要求连续两次检测都超阈值、或者复测确认后再告警。

**重复次数怎么定**：先对同一构建跑 30 次左右测出噪声；想检测的最小变化越接近噪声，需要的重复次数越多。粗略地说，标准误差随 √n 下降，噪声 5%、想稳定检测 3% 的变化，每组需要十几到几十次。
