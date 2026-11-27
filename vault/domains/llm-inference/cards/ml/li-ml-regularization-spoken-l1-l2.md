---
id: li-ml-regularization-spoken-l1-l2
node: ml.regularization
type: qa
step: 4
---
## Q
面试里被问"L1 和 L2 正则的区别是什么？分别在什么场景用？"，怎么答？

## A
按这个顺序说：

- **先说正则化的目的：** 在损失上加一个惩罚权重大小的项，让模型更简单，减少过拟合。L1 加的是 λ 乘权重绝对值之和，L2 加的是 λ 乘权重平方和。
- **核心区别——梯度的形状：** L2 的梯度是 2λw，和权重成正比，权重越小推力越小，所以权重整体变小但很少恰好为 0。L1 的梯度是 λ 乘 w 的符号，大小恒定，小权重也被同样力度推向 0，所以会产生大量恰好为 0 的权重，模型变稀疏。
- **几何解释（加分）：** L1 的约束区域是菱形，角在坐标轴上，最优解容易落在角上；L2 是圆，最优解一般不在轴上。
- **贝叶斯解释（加分）：** L2 相当于假设权重服从高斯先验，L1 相当于拉普拉斯先验，后者在 0 处更尖。
- **场景：** 特征很多、希望自动挑出少数有用的特征，用 L1（Lasso）；特征相关性强、只想稳定模型，用 L2（Ridge），它把相关特征的权重平均分摊，而 L1 可能只留下其中一个、结果不稳定；两者都要可以用 Elastic Net。深度学习里最常见的是 L2 形式的权重衰减，配合 AdamW。
- **补一个实践点：** λ 用验证集选，从 1e-4 到 1 按对数尺度搜索；正则项一般不作用于偏置项。L1 在 0 点不可导，实现上用次梯度或近端方法，把越过 0 的权重直接截成 0。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 184" font-family="sans-serif" font-size="11">
<text x="22" y="12" fill="currentColor">L1：菱形</text>
<text x="182" y="12" fill="currentColor">L2：圆</text>
<line x1="25" y1="105" x2="135" y2="105" stroke="currentColor" stroke-opacity="0.5"/>
<line x1="80" y1="18" x2="80" y2="152" stroke="currentColor" stroke-opacity="0.5"/>
<line x1="185" y1="105" x2="295" y2="105" stroke="currentColor" stroke-opacity="0.5"/>
<line x1="240" y1="18" x2="240" y2="152" stroke="currentColor" stroke-opacity="0.5"/>
<text x="137" y="109" fill="currentColor">w₁</text>
<text x="297" y="109" fill="currentColor">w₁</text>
<polygon points="80,65 120,105 80,145 40,105" fill="currentColor" fill-opacity="0.15" stroke="currentColor"/>
<circle cx="240" cy="105" r="40" fill="currentColor" fill-opacity="0.15" stroke="currentColor"/>
<circle cx="90" cy="40" r="26.9" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
<circle cx="265" cy="45" r="25" fill="none" stroke="currentColor" stroke-dasharray="3 3"/>
<circle cx="90" cy="40" r="1.5" fill="currentColor"/>
<circle cx="265" cy="45" r="1.5" fill="currentColor"/>
<circle cx="80" cy="65" r="3.5" fill="currentColor"/>
<circle cx="255.4" cy="68.1" r="3.5" fill="currentColor"/>
<text x="80" y="164" text-anchor="middle" fill="currentColor">最优解落在角上</text>
<text x="240" y="164" text-anchor="middle" fill="currentColor">最优解不在轴上</text>
<text x="160" y="179" text-anchor="middle" font-size="9" fill="currentColor">虚线：损失的等高线；大圆点：最优解</text>
</svg>
