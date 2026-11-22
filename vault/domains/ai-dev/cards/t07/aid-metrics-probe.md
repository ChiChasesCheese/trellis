---
id: aid-metrics-probe
node: t07.cycle-time-change-failure-rate-recovery-time-rew
type: qa
step: 2
tags: [考点]
---
## Q
**度量 · 一个季度后的数据**｜考点 · 必会

试点一个季度：cycle time 缩短 25%，change failure rate 从 8% 升到 12%，rework 上升。管理层说"成功"。你怎么回应？

## A
| 数字 | 解读 |
|---|---|
| cycle time −25% | 变快了 |
| change failure rate 8% → 12% | 失败的变更多了一半（12/8 = 1.5） |
| rework 上升 | 一部分"变快"是把返工推后 |

**回应：** 这是吞吐上升、稳定性下降的典型形态（和 DORA 2025 的整体发现一致）。要问：多出来的失败来自哪些变更？是不是**审查跟不上**？先补验证（t04）再扩大，而不是庆祝。

**别做：** 只汇报 cycle time。
**注意：** 这里的 25%、8%、12% 是题目设定的例子数字，不是任何研究的结果。

<details class="pt" markdown="1"><summary>出处</summary>

DORA《2025 State of AI-assisted Software Development》（Google Cloud 博客）

</details>
