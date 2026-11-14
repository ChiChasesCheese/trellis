---
id: msd-data-collection-labeling-weak-active
node: data.collection-labeling
type: qa
step: 4
---
## Q
标注预算很少时，弱监督（weak supervision）、主动学习（active learning）和用大模型自动标注分别怎么做？怎么选？

## A
**弱监督**：写很多条"标注函数"，每条是一个粗糙的规则，可以投"是 / 否 / 弃权"，再合并它们的投票。
```python
SPAM, HAM, ABSTAIN = 1, 0, -1
def lf_has_link(c):    return SPAM if "http" in c.text else ABSTAIN
def lf_new_account(c): return SPAM if c.account_age_days < 1 else ABSTAIN
def lf_long_reply(c):  return HAM if len(c.text) > 200 else ABSTAIN
```
开源工具 Snorkel 会估计每条规则的准确率和规则之间的相关性，给每条样本一个概率标签。优点：一个人一天能写几十条规则，覆盖几百万条数据；规则改了全量重新打标签。缺点：规则覆盖不到的模式模型也学不到。

**主动学习**：先用少量标签训练一个模型，让它挑出"最拿不准"的样本（例如预测概率接近 0.5 的），只把这些送去人工标注，标完再训练，循环。同样标 1 万条，挑出来的比随机抽的信息量大得多。缺点：需要标注和训练的闭环工具；挑出的样本分布有偏，不能直接当测试集。

**大模型自动标注**：把标注指南写进提示词（prompt），让大语言模型给每条数据打标签。速度快、成本低，适合文本分类。必须先用几百条人工标签测它的准确率和 kappa（扣除碰巧一致后的一致性），只在它达标的类别上使用。

**怎么选：**
- 领域规则清楚（关键词、黑名单）：弱监督起步。
- 有标注团队但预算紧：主动学习，把预算花在难样本上。
- 文本任务、标准容易用文字讲清：大模型标注 + 人工抽检。
- **无论哪种**，测试集都要用人工精标，否则评估本身就有偏差。
