---
id: aie-product-defensibility-planning
node: t02.ai-product-defensibility-milestone-planning-main
type: qa
step: 1
tags: [摘要]
---
## Q
**AI 产品 · 护城河、里程碑与维护**｜摘要 · 追问

创业团队做了一个套在 foundation model 上的 PDF 解析应用，两周就做出来了。投资人问：「谷歌用三个工程师两周就能复制，你凭什么活？」你怎么回答，之后又怎么规划？

## A
**入门门槛低是福也是祸：** 你容易做，对手也容易做；模型自己变强，你这一层可能被吞掉（假设「模型解析不了 PDF」一旦不成立，产品就没理由了）。

| 护城河 | 判断 |
|---|---|
| technology | 大家用同样的底座模型，通常差异小 |
| distribution | 大公司占优 |
| data | 最有操作空间：先上线、积累使用数据持续改进 |

即使不能拿用户数据训练，使用信息也能暴露用户行为和产品短板，指导后续数据收集。

**里程碑规划：**
1. 先量化目标，如自动处理 60% 的工单；
2. 先评测现成模型：它已能做 30%，要做的工作就比 0% 少；
3. 评估后目标可能改变：投入大于回报就不做；
4. 按 **last mile** 规划：做 demo 一个周末，做成产品几个月到几年。LinkedIn（2024）一个月做到 80%，又花了四个月才超过 95%。

**维护：**
- 好变化：模型变强、上下文变长、推理变便宜，但每次都要重新做成本收益；自建可能因供应商降价一半而变得更贵。
- 换模型有适配成本：提示词、数据都要调，需要版本管理和评测基础设施。
- 难应对的变化：法规（算力、数据、IP 归属）。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch1 §AI product defensibility、§Milestone Planning、§Maintenance

</details>
