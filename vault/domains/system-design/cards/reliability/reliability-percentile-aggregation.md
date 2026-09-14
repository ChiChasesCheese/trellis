---
id: reliability-percentile-aggregation
node: reliability.observability
type: qa
---
## Q
Each of 50 hosts reports its own p99 latency. Why can't you average (or max) them to get the service p99, and what should hosts export instead?

## A
**Percentiles don't compose** — a percentile is a point on a distribution, and you can't reconstruct the merged distribution from per-host points. Averaging p99s systematically understates the true p99 (traffic is uneven; the worst host's tail dominates), and max overstates it.

Fix: hosts export **histograms** (fixed buckets or mergeable sketches like DDSketch/t-digest); buckets are just counters that **sum across hosts and time windows**, and the backend computes any percentile from the merged histogram at query time. Same reason latency SLIs use threshold-ratio form — [[reliability-latency-sli-form]].

## Q zh
每个 50 个主机报告其自己的 p99 延迟。为什么你不能平均（或最大）它们以获得服务 p99，主机应该导出什么？

## A zh
**百分位不组合** ——百分位是分布上的一个点，你无法从每主机点重建合并分布。平均 p99 系统地低估真实 p99（流量不均匀；最坏主机的尾巴主导），最大夸大。

修复：主机导出**直方图**（固定桶或可合并的草图，如 DDSketch/t-digest）；桶只是跨主机和时间窗口**相加**的计数器，后端在查询时从合并直方图计算任何百分位。相同原因延迟 SLI 使用阈值比率形式——[[reliability-latency-sli-form]]。
