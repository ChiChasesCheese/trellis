---
id: aie-online-evals-drift
node: t05.online-evals-production-monitoring-sampled-scori
type: qa
step: 2
tags: [考点]
---
## Q
**Online evals · 离线好 ≠ 线上好，以及漂移**｜考点 · 必会

离线评测一直 90%，但线上"平均回答长度"这两个月缓慢下降，用户满意度也在掉。没改过代码。可能是什么原因？

## A
**三类漂移（drift）：**

| 漂移 | 例子 | 怎么发现 |
|---|---|---|
| **System prompt 变化** | 模板被更新；同事修了个错别字 | 对 system prompt 做简单的变更检测 |
| **User behavior 变化** | 用户学会了写"请简短回答"，回答长度缓慢变短 | 光看指标看不出，要**调查根因** |
| **Underlying model 变化** | API 没变，背后的模型被供应商更新了 | 固定一组回归样本定期跑，对比版本 |

**数字（用于说明模型变化的影响）：** Chen et al.（2023）观察到 GPT-4 / GPT-3.5 在 2023 年 3 月与 6 月版本的基准分数差别明显；Voiceflow 报告从 GPT-3.5-turbo-0301 换到 1106 后性能下降 10%。

**回到题目：** 先看长度下降是不是用户行为变了（用户自己要求简短），再对比用户满意度的变化；同时跑回归样本，排除模型被悄悄更新。

**监控的健康度（DevOps 三个指标）：**
- **MTTD** 出事后多久发现；
- **MTTR** 发现后多久解决；
- **CFR（change failure rate）** 有多少比例的改动导致故障或回滚。

CFR 高，要回头改评测流程，让坏改动在上线前被抓住。

**出处：** Huyen《AI Engineering》ch10 §Monitoring and Observability（MTTD、MTTR、CFR）、§Drift detection
