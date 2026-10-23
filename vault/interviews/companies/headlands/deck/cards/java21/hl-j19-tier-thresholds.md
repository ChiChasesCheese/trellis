---
id: hl-j19-tier-thresholds
node: java21.j19-runtime-zgc-jit
type: qa
step: 19
---
## Q
分层编译的默认阈值是多少？面试里怎么说？

## A
默认：`Tier3InvocationThreshold = 200`（调用 200 次进 C1）、`Tier4InvocationThreshold = 5000`（再调用 5000 次进 C2）；循环回边另有 `Tier3BackEdgeThreshold = 60000`、`Tier4BackEdgeThreshold = 40000`。

触发逻辑比这复杂，面试说「**几百次进 C1，几千次进 C2**」即可。
