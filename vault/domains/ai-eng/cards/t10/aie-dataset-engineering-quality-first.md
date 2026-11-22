---
id: aie-dataset-engineering-quality-first
node: t10.dataset-engineering
type: qa
step: 1
tags: [摘要]
---
## Q
**Dataset engineering · 质量、覆盖、数量**｜摘要 · 必会

你有 50 万条未清洗的客服对话，另一位同事手写了 1,000 条精标样本。微调用哪个？该准备多少条？

## A
**质量压倒数量：**
- Yi 模型团队发现 1 万条精心设计的指令优于几十万条有噪声的指令；
- LIMA：65B 的 Llama 用 1,000 条精选的 prompt 和回答微调，在 43% 的情况下与 GPT-4 持平或更受人类评判者偏好（但不如产品级模型鲁棒）。

**数据好的六个特征：** relevant、aligned（符合任务要求，不等于「正确」）、consistent、格式正确、sufficiently unique、compliant。**coverage：** 输入的多样性要覆盖用户真实会遇到的情形。

**要多少数据：** 没有固定答案，取决于：

| 因素 | 影响 |
|---|---|
| 微调方法 | 全量微调要的数据比 LoRA 等 PEFT 多几个数量级；几百到几千条用 PEFT |
| 任务复杂度 | 情感分类远少于金融文件问答 |
| 基座模型强度 | 越接近目标，需要的越少（这与预训练相反） |

- 先用 50–100 条小而精的数据试：经验是绝大多数情况下 50–100 条就应当看到提升；没提升再查超参、数据质量、prompt，别急着加数据；
- 画学习曲线：用 25%、50%、100% 的数据各训一次，看斜率：陡说明加数据值得，平说明不值；
- 数据少时可以先在相关性较低的数据上微调（自监督 → 有监督；推文情感 → 产品情感；合成 → 真实）。

**标注一致性：** 两个标注员标同一条，结果不应差太多；要有好的标注指南（同评测 guideline）；Kern 等发现标注会话后半段的质量更低（疲劳）。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch8 §Data Curation（Data Quality、Data Coverage、Data Quantity）、§Clean and Filter Data

</details>
