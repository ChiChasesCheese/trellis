---
id: li-ml-classification-metrics-roc-auc
node: ml.classification-metrics
type: qa
step: 3
---
## Q
ROC 曲线和 AUC 是什么？AUC = 0.9 是什么意思？它和 PR 曲线该怎么选？

## A
**前提：** 分类模型输出一个分数，再用阈值切成"是/否"。换一个阈值，混淆矩阵（真阳性、假阳性、真阴性、假阴性四格计数）就变一次。

**ROC 曲线（receiver operating characteristic）：** 把阈值从 1 扫到 0，每个阈值下算两个比例，画成一条曲线：
- 纵轴 **TPR（真阳性率）** = TP / (TP + FN)，就是召回率：真阳性里被抓到的比例；
- 横轴 **FPR（假阳性率）** = FP / (FP + TN)：真阴性里被误报的比例。
- 阈值很高时两者都接近 0（左下角），阈值很低时都接近 1（右上角）。
- 随机猜测是一条对角线；完美模型经过左上角（TPR = 1，FPR = 0）。

**AUC（area under curve）：ROC 曲线下的面积，0.5 是随机，1.0 是完美。**
- **直观含义：** 随机抽一个真阳性样本和一个真阴性样本，模型给阳性样本的分数更高的概率。AUC = 0.9 就是 90% 的情况下排序正确。
- **优点：** 不依赖某一个阈值，衡量的是"排序能力"。

**手算一个小例子：** 2 个阳性分数 `[0.9, 0.4]`，2 个阴性分数 `[0.6, 0.2]`。四种阳性—阴性配对中，(0.9, 0.6)、(0.9, 0.2)、(0.4, 0.2) 排序正确，(0.4, 0.6) 错误，AUC = 3/4 = **0.75**。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 212" font-family="sans-serif" font-size="11">
<polygon points="50,180 50,100 130,100 130,20 210,20 210,180" fill="currentColor" fill-opacity="0.15"/>
<line x1="50" y1="180" x2="210" y2="180" stroke="currentColor"/>
<line x1="50" y1="180" x2="50" y2="20" stroke="currentColor"/>
<line x1="50" y1="180" x2="210" y2="20" stroke="currentColor" stroke-dasharray="4 3"/>
<polyline points="50,180 50,100 130,100 130,20 210,20" fill="none" stroke="currentColor" stroke-width="2.5"/>
<circle cx="50" cy="100" r="3" fill="currentColor"/>
<circle cx="130" cy="100" r="3" fill="currentColor"/>
<circle cx="130" cy="20" r="3" fill="currentColor"/>
<text x="46" y="184" text-anchor="end" fill="currentColor">0</text>
<text x="46" y="104" text-anchor="end" fill="currentColor">0.5</text>
<text x="46" y="24" text-anchor="end" fill="currentColor">1</text>
<text x="130" y="194" text-anchor="middle" fill="currentColor">0.5</text>
<text x="210" y="194" text-anchor="middle" fill="currentColor">1</text>
<text x="130" y="208" text-anchor="middle" fill="currentColor">FPR</text>
<text x="12" y="64" fill="currentColor">TPR</text>
<text x="170" y="120" text-anchor="middle" fill="currentColor">面积 0.75</text>
<text x="222" y="60" fill="currentColor">粗线：例子的 ROC</text>
<text x="222" y="78" fill="currentColor">虚线：随机猜测</text>
</svg>

```python
from sklearn.metrics import roc_auc_score, average_precision_score
print(roc_auc_score([1, 1, 0, 0], [0.9, 0.4, 0.6, 0.2]))           # 0.75
print(average_precision_score([1, 1, 0, 0], [0.9, 0.4, 0.6, 0.2]))  # PR 曲线下面积的近似
```

**ROC 还是 PR：**
- 类别大致平衡：ROC-AUC 直观、通用。
- 严重不平衡（阳性 1% 以下）：FPR 的分母是庞大的阴性数，误报多了 FPR 也几乎不动，ROC 曲线显得很好看。PR 曲线的精确率会直接暴露误报问题，这时看 PR-AUC。
- AUC 只看排序，不说明阈值该放哪，上线前仍要按业务成本选定阈值。
