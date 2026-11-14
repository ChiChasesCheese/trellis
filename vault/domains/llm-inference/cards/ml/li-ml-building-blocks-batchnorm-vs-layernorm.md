---
id: li-ml-building-blocks-batchnorm-vs-layernorm
node: ml.building-blocks
type: qa
step: 2
---
## Q
BatchNorm 和 LayerNorm（以及 RMSNorm）有什么区别？为什么 Transformer 和大语言模型都用 LayerNorm 一类而不用 BatchNorm？

## A
**归一化（normalization）：** 把一组数减去均值、除以标准差，变成均值 0、方差 1 的分布，再乘、加两个可学习的参数。目的是让每层的输入数值范围稳定，训练更快更稳。区别在于**在哪个方向上算均值和方差**。

**以一个形状 `[批大小 B, 特征数 D]` 的张量为例：**
- **BatchNorm：** 对每个特征，沿批方向（B 个样本）算均值和方差。一个样本的归一化结果依赖于同一批里的其他样本。
- **LayerNorm：** 对每个样本，沿特征方向（D 个数）算均值和方差。每个样本独立处理，与批里有谁无关。
- **RMSNorm：** LayerNorm 的简化，不减均值，只除以均方根 `sqrt(mean(x²) + ε)`。计算更省，效果相当，Llama 系列使用。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150" font-family="sans-serif" font-size="11">
<text x="75" y="14" text-anchor="middle" fill="currentColor">BatchNorm</text>
<text x="245" y="14" text-anchor="middle" fill="currentColor">LayerNorm</text>
<text x="30" y="30" fill="currentColor">D 个特征 →</text>
<text x="200" y="30" fill="currentColor">D 个特征 →</text>
<text x="4" y="74" fill="currentColor">B ↓</text>
<text x="174" y="74" fill="currentColor">B ↓</text>
<rect x="30" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="48" y="34" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="66" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="84" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="102" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="30" y="52" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="48" y="52" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="66" y="52" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="84" y="52" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="102" y="52" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="30" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="48" y="70" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="66" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="84" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="102" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="30" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="48" y="88" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="66" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="84" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="102" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="200" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="218" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="236" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="254" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="272" y="34" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="200" y="52" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="218" y="52" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="236" y="52" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="254" y="52" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="272" y="52" width="18" height="18" stroke="currentColor" fill="currentColor" fill-opacity="0.35"/>
<rect x="200" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="218" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="236" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="254" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="272" y="70" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="200" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="218" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="236" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="254" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<rect x="272" y="88" width="18" height="18" fill="none" stroke="currentColor"/>
<text x="75" y="126" text-anchor="middle" fill="currentColor">每个特征沿批算</text>
<text x="75" y="142" text-anchor="middle" fill="currentColor">依赖同批其他样本</text>
<text x="245" y="126" text-anchor="middle" fill="currentColor">每个样本沿特征算</text>
<text x="245" y="142" text-anchor="middle" fill="currentColor">与批里有谁无关</text>
</svg>
```

**BatchNorm 的麻烦：**
- **训练和推理行为不同：** 训练时用当前批的统计量；推理时用训练期间累计的"滑动平均"统计量（`running_mean`、`running_var`）。忘了 `model.eval()`，推理就会用当前批的统计量，结果随批的组成变化。
- **批很小时不稳定：** 批大小为 1 时方差无法估计。
- **变长序列：** 文本长短不一，补齐的位置会污染统计量。

**为什么大语言模型用 LayerNorm 或 RMSNorm：**
- 每个 token 独立归一化，不受批大小和序列长度影响。
- 训练和推理完全同一种计算，没有滑动统计量。
- **对推理服务尤其重要：** 服务会把不同用户的请求凑在一起算，批的组成随时在变。如果用 BatchNorm，你的回答会受到同批其他人的影响；LayerNorm 从设计上避免了这一点。

BatchNorm 在卷积网络（图像）里仍然很常用，因为那里批大、输入尺寸固定。
