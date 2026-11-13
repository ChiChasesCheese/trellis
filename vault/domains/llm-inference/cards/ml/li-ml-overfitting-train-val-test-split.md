---
id: li-ml-overfitting-train-val-test-split
node: ml.overfitting
type: qa
step: 2
---
## Q
训练集、验证集、测试集各有什么用？为什么需要三份而不是两份？k 折交叉验证（k-fold cross-validation）解决什么问题？

## A
**三份数据，三个用途：**
- **训练集（training set）：** 用来调整模型参数（模型里由训练自动调出来的数字）。通常占 70%–80%。
- **验证集（validation set）：** 用来做"人的决定"：选模型结构、调学习率等超参数（人设定的配置）、决定何时停止训练。通常 10%–15%。
- **测试集（test set）：** 所有决定都做完之后，**只用一次**，报告最终表现。通常 10%–15%。

**为什么要三份：** 如果用测试集来挑超参数，试了 50 组配置、挑测试分数最高的那组，这组分数就被"挑"高了，不再代表模型在新数据上的真实表现。验证集承担反复挑选的工作，测试集保持"没被看过"。这和软件测试的道理一样：用来调代码的测试用例，不能再用来证明代码没问题。

**k 折交叉验证：** 数据少时，切出一份验证集太浪费，而且结果受切分方式影响很大。
- 把训练数据分成 k 份（常用 k = 5 或 10）。
- 轮流用其中 1 份当验证集、其余 k − 1 份训练，共训练 k 次。
- 取 k 次验证分数的平均和标准差。
- 代价：训练成本变成 k 倍，大模型基本不用。

```python
from sklearn.model_selection import train_test_split, cross_val_score
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
print(cross_val_score(model, X_tr, y_tr, cv=5).mean())
```

`stratify=y` 让各份里的类别比例保持一致，类别不平衡时必须加。

**时间序列数据不能随机切：** 必须按时间切，用过去训练、用未来验证，否则模型提前"看到了未来"。
