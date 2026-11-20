---
id: li-basics-training-vs-inference-challenge
node: basics.training-vs-inference
type: qa
step: 4
tags: [挑战]
---
## Q
**挑战。** 团队有一张 24 GB 的显卡，跑 7B 模型（FP16）的推理绰绰有余。产品想"顺手在这张卡上用公司数据把模型全量微调一遍"。行不行？算一下显存和计算量，再给两条出路。

## A
**评分点（答出 3 条算过）：**

1. 推理只存权重：7B × 2 字节 = 14 GB，24 GB 放得下。
2. 训练要同时存参数、梯度和优化器的统计量，约 16 字节每参数：7B 约 112 GB，还没算中间结果，是 24 GB 的近 5 倍。
3. 计算量：训练每个 token 约 6 × 参数量，推理约 2 ×，是 3 倍，而且数据要反复过很多遍。
4. 出路一：冻结原有权重，只训练很少的新增参数（例如 LoRA），梯度和优化器状态只为这一小部分参数保存。
5. 出路二：租多卡的机器做全量微调；或者不训练，用提示和检索把公司数据放进上下文。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 86" font-family="sans-serif" font-size="12">
<text x="4" y="22" fill="currentColor">显卡</text>
<rect x="44" y="10" width="49" height="16" fill="none" stroke="currentColor"/>
<text x="98" y="22" fill="currentColor">24 GB</text>
<text x="4" y="48" fill="currentColor">推理</text>
<rect x="44" y="36" width="29" height="16" stroke="currentColor" fill="currentColor" fill-opacity="0.3"/>
<text x="78" y="48" fill="currentColor">14 GB（每参数 2 字节）</text>
<text x="4" y="74" fill="currentColor">训练</text>
<rect x="44" y="62" width="230" height="16" stroke="currentColor" fill="currentColor" fill-opacity="0.3"/>
<text x="159" y="74" text-anchor="middle" fill="currentColor">每参数约 16 字节</text>
<text x="278" y="74" fill="currentColor">112 GB+</text>
</svg>

<details class="pt"><summary>参考答案</summary>不行。推理时这张卡只需要放 14 GB 的权重，但全量训练要为每个参数同时保存参数、梯度和优化器的统计量，约 16 字节每参数，7B 模型约 112 GB，还不含中间结果，远超 24 GB。计算上，训练每个 token 的运算量约是推理的 3 倍，还要把数据过很多遍。可行的办法是冻结原权重、只训练少量新增参数，或者租多卡机器做全量微调，或者干脆不训练，用检索把公司数据放进提示里。</details>
