%% trellis:begin %%
# 延迟是一个分布：百分位与尾部
*测量与性能分析*

平均值掩盖问题，要看 p50 / p99 / p99.9 / max；尾延迟在交易中最重要，因为行情最忙时正是赚钱时。

**Unlocks:** [[domains/hft/map/measurement.histograms|HdrHistogram]], [[domains/hft/map/measurement.coordinated-omission|coordinated omission（协同遗漏）]], [[domains/hft/map/measurement.budget-method|延迟预算与排查方法]]

## Readings
- [[hdrhistogram|HdrHistogram]]
- [[scylla-coordinated-omission|On Coordinated Omission]]

## Drills
- [[measurement-coordinated-omission|练习：一份漂亮的延迟报告，凭什么不能信]]

## Cards (4)
1. [[hft-measurement-distributions-mean-hides]]
2. [[hft-measurement-distributions-tail-amplification]]
3. [[hft-measurement-distributions-busy-time]]
4. [[hft-measurement-distributions-no-averaging-percentiles]]
%% trellis:end %%

## Notes
