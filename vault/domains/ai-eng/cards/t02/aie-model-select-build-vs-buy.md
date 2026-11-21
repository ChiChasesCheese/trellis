---
id: aie-model-select-build-vs-buy
node: t02.model-selection-build-vs-buy
type: qa
step: 2
tags: [考点]
---
## Q
**Build vs buy · 用 API 还是自己托管**｜考点 · 必会

一家公司的合规政策规定客户数据不得出境。另一家公司只是做内部摘要，流量很大，API 账单一个月比一个月高。各自该怎么在 model API 和自托管开源模型之间选？

## A
**书里列了七条轴：**

| 轴 | 要点 |
|---|---|
| Data privacy | 严格隐私政策下，外部托管的 API 直接排除；还要担心 API 方的条款变化（Zoom 2023 年 8 月悄悄改了服务条款，允许用用户数据训练模型） |
| Data lineage、copyright | 模型训练数据不透明，IP 法律仍在演变；商业合同有时能转移部分风险 |
| Performance | 开源与闭源的差距在缩小，但最强的模型通常放在 API 后面；很多场景不需要最强的 |
| Functionality | API 开箱提供 scalability、function calling（让模型调用外部工具）、structured outputs、guardrails；但可能没有 logprobs（模型给每个 token 的概率）或 finetuning |
| Cost | API 按用量计费，量大会很贵；自托管要工程投入，"工程可能更贵" |
| Control、access、transparency | 开源的组件更好改动，企业看重控制与可定制 |
| On-device | 需要在设备上跑时只能选可本地部署的模型 |

**回到题目：**
- **数据不得出境的公司：** 外部 API 出局；选自托管或部署在私有网络里的方案。这是 hard attribute。
- **流量大的摘要应用：** 到一定规模，API 费用值得与自托管比较，但要把自己团队的运维、优化、guardrails 工程成本一起算进去，用评测确认开源模型质量够用。

**别忘了：** 无论选哪边，都用**标准化的 API**，方便以后换模型；换 API 或换提供商后，要重新评测，因为同一模型在不同 API 上表现可能有细微差别。

**出处：** Huyen《AI Engineering》ch4 §Model Build Versus Buy（Open source models versus model APIs 七条轴）
