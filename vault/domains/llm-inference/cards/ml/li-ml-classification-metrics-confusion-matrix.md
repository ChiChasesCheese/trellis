---
id: li-ml-classification-metrics-confusion-matrix
node: ml.classification-metrics
type: qa
step: 1
---
## Q
什么是混淆矩阵（confusion matrix）？准确率（accuracy）、精确率（precision）、召回率（recall）、F1 怎么从它算出来？手算一个例子。

## A
**场景：** 一个二分类模型（只判断"是"或"否"）判断 100 条模型回答里哪些是"有害内容"。"阳性"（positive）指模型判为有害。

**混淆矩阵：把预测和真实情况交叉成四格。**

| | 真实有害 | 真实无害 |
|---|---|---|
| 预测有害 | **TP（真阳性）= 8** | **FP（假阳性，误报）= 2** |
| 预测无害 | **FN（假阴性，漏报）= 12** | **TN（真阴性）= 78** |

真实有害共 20 条，无害 80 条。

**四个指标：**
- **准确率 = (TP + TN) / 全部** = (8 + 78) / 100 = **0.86**。所有判断里对了多少。
- **精确率 = TP / (TP + FP)** = 8 / 10 = **0.80**。模型说"有害"的那些里，真有害的比例。回答的是"报警可信吗"。
- **召回率 = TP / (TP + FN)** = 8 / 20 = **0.40**。所有真有害的里，被抓到的比例。回答的是"漏了多少"。
- **F1 = 2 × P × R / (P + R)** = 2 × 0.8 × 0.4 / 1.2 ≈ **0.53**。精确率和召回率的调和平均，两者中较低的那个对 F1 影响大。

**这个例子说明的问题：** 准确率 86% 看起来不错，但一半以上的有害内容（12/20）被漏掉了。只看准确率会得出错误结论。

**记忆方法：** 精确率的分母是"预测为阳性"（一行），召回率的分母是"真实为阳性"（一列）。

```python
from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_true, y_pred))
print(classification_report(y_true, y_pred, digits=3))
```

注意 sklearn 的 `confusion_matrix` 行是真实标签、列是预测标签，和上表行列相反，读的时候别弄混。
