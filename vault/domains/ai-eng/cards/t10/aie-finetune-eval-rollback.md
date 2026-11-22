---
id: aie-finetune-eval-rollback
node: t10.evaluation-rollback
type: qa
step: 1
tags: [实践]
---
## Q
**微调后的 evaluation 与 rollback · 上线前后**｜实践 · 必会

微调后的模型在你的任务集上得分比基线高 6 点，要不要上线？上线后发现别的功能变差了，怎么办？

## A
**上线前评测：**
1. **对比基线**：基线应包括「最强的现成模型加好的 prompt」，不只是未微调的小模型；书里的建议是先用你负担得起的最强模型探可行性，再拿它当对照；
2. **回归集**：除了目标任务，还要有其他能力的评测（格式、拒答、安全、通用问答），检查 **catastrophic forgetting**（模型学了新任务后忘掉旧任务；序贯微调时尤其容易出现）；
3. **噪声**：6 点是否超出评测噪声（见 statistical power 那张卡）；
4. **成本与延迟**：新模型的单次成本和 TTFT 是否符合预期；
5. **逐切片看**：总分提升可能是少数切片拉高、其他切片下降。

**上线方式：** 走 canary（先放一小部分真实流量给新模型）或 shadow traffic（请求复制给新模型但不返回用户），上线后看线上指标。

**rollback（回滚：切回旧版本）的准备（通用实践）：**
- 保留旧模型或旧 adapter 的版本，并能通过**配置**一键切回，不要靠重新部署；
- LoRA adapter 与基座分开存放时，换版本只需换 adapter，更轻；
- 每条请求的 trace 记录模型版本，才能判断回退是否必要；
- 提前写好回滚条件（格式错误率、拒答率、转人工率等阈值）。

**维护提醒：** 基座模型升级后，微调往往要**重做**；所以保留数据、训练配置和评测集，让重训可复现。

**出处：** Huyen《AI Engineering》ch7 §Finetuning Tactics（Base models）、§Model Merging and Multi-Task Finetuning（catastrophic forgetting）、§Reasons Not to Finetune；rollback 部分为通用发布实践
