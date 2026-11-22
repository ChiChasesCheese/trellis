---
id: aie-model-merging-multitask
node: t10.model-merging-multi-task-finetuning
type: qa
step: 1
tags: [摘要]
---
## Q
**Model merging 与 multi-task finetuning · 多个任务一个模型**｜摘要 · 追问

要让一个模型同时会摘要、分类、抽取三件事。是一起微调、依次微调，还是分别微调后合并？

## A
| 方式 | 做法 | 问题 |
|---|---|---|
| simultaneous finetuning | 所有任务的数据混在一起训 | 同时学多个技能更难，通常要更多数据和训练 |
| sequential finetuning | 一个任务接一个任务 | **catastrophic forgetting**：学新任务时忘旧任务，旧任务性能明显下降 |
| **model merging** | 各任务**分别并行**微调，再把模型合并 | 每个任务单独学得更好，没有序贯学习，遗忘风险小 |

**model merging：** 把多个模型的参数合并成一个新模型（通常不需要 GPU，除非之后还要微调）。价值：
- 合并后可能比任何一个都好（一个模型会前 60% 的题，另一个会后 60%，合并后也许能到 80%，这是书里的示意）；
- 减少内存：一个模型做多件事，参数更少，对手机、车载等**设备端部署**尤其有吸引力；
- 在同一基座上用 LoRA 微调的多个 adapter 可以合并成一个。

**三类做法：** summing（线性组合、SLERP、剪掉冗余的任务参数）、layer stacking（把不同模型的层堆起来）、concatenation（拼接参数）。很多技术还在实验阶段，可能会过时。

**和 ensembling 的区别：** ensembling 保持各模型不变，只合并输出（多数投票），每次请求要多次推理，成本更高；merging 合并参数，推理成本不变。

**什么时候用：** 有多个任务、各自已有微调模型、部署内存紧张。合并后要重新评测每个任务，别假设合并无损。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch7 §Model Merging and Multi-Task Finetuning

</details>
