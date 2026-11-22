---
id: aie-evaluation-criteria-four-buckets
node: t05.evaluation-criteria-domain-capability-generation
type: qa
step: 1
tags: [摘要]
---
## Q
**Evaluation criteria · 评什么**｜摘要 · 必会

你要做合同摘要功能，团队说「评一下质量」。「质量」怎么拆成可测的几项？

## A
**四类 criteria（先定义，再建应用，即 evaluation-driven development）：**

| 类别 | 问什么 | 合同摘要的例子 |
|---|---|---|
| **domain-specific capability** | 模型懂这个领域吗 | 能否理解合同条款 |
| **generation capability** | 生成的内容好不好：流畅、连贯、事实一致、安全 | 摘要是否忠实于原文 |
| **instruction-following capability** | 是否遵守格式和约束 | 是否在长度限制内、按要求的结构 |
| **cost & latency** | 花多少钱、等多久 | 单份合同成本、TTFT、总耗时 |

**怎么用：**
- 每一类至少定一个可测指标，并写明**硬要求**和**理想值**；先按不可妥协的（如延迟）过滤，再在剩下里选最好的；
- 示例（选型表）：cost per output token、TPM、TTFT 的 P90、总耗时的 P90、事实一致性分数等，都有「硬要求」和「理想」两列；
- 关于延迟：问用户想不想更快，没人说不想；要区分必须有和锦上添花；
- 为什么先定 criteria：部署了却无法评估的应用，比没部署的更糟，维护有成本，下线成本可能更高。

**评测先行的局限：** 只做可评测的应用容易「在路灯下找钥匙」，漏掉难评测但价值高的方向。所以要同时投资评测能力本身。

**出处：** Huyen《AI Engineering》ch4 §Evaluation Criteria、§Evaluation-Driven Development、§Cost and Latency（Table 4-3）
