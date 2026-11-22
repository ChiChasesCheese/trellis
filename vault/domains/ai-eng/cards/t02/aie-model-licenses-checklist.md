---
id: aie-model-licenses-checklist
node: t02.open-source-open-weights-model-licenses
type: qa
step: 1
tags: [摘要]
---
## Q
**Open weights · 许可证要看什么**｜摘要 · 必会

团队想下载一个「开源」模型自己部署。「开源」二字够用吗？合规上要核对什么？

## A
**术语：**

| 叫法 | 含义 |
|---|---|
| **open weight** | 权重公开，训练数据不公开（目前绝大多数「开源模型」） |
| open model | 权重和训练数据都公开 |

数据不公开，就无法审计训练数据来源，也无法从头重训。

**许可证不是 MIT/Apache 那么简单：** 很多模型用自己的专属许可证（如 Llama 的 Community License），所以每个都要读。书里建议每次都问三件事：

1. **允许商用吗？** 第一代 Llama 是非商用许可。
2. **商用有附加限制吗？** Llama 2 和 Llama 3 规定月活超过 7 亿的应用要另申请许可。
3. **允许用它的输出去训练或改进别的模型吗？** 这关系到 **model distillation**（用大模型的输出训练小模型）和合成数据；Llama 许可至书写作时仍不允许，Mistral 起初不允许、后来改了。

**还有一层法律风险（data lineage）：** 训练数据来源不透明，若模型侵权，被追责的更可能是用它做产品的你，而不是模型开发者；商业模型的合同可能给你一定保护。

**检查清单：** 许可证文本（版本号）→ 商用 → 用户规模门槛 → 输出可否用于训练 → 训练数据披露程度 → 谁来背侵权风险。许可证版本会变，每次升级模型都重读。

**出处：** Huyen《AI Engineering》ch4 §Open source, open weight, and model licenses；§Data lineage and copyright
