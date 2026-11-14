---
id: msd-data-sampling-imbalance-methods
node: data.sampling-imbalance
type: qa
step: 1
---
## Q
从海量日志里构造训练集，常用哪几种采样方法？蓄水池采样（reservoir sampling）怎么在不知道总量的数据流上等概率抽样？

## A
**为什么要采样**：每天 100 亿条曝光日志，不可能也没必要全部用来训练；采样决定了模型看到的世界长什么样。

**常用方法：**
- **简单随机采样**：每条以相同概率入选。简单，但少数类和小群体可能被抽得太少。
- **分层采样**（stratified）：先按类别、国家、新老用户分组，每组按比例或保底数量抽。保证小语种用户在训练集和测试集里都有。
- **加权采样 / 重要性采样**（importance sampling）：按权重抽，并在训练时把权重的倒数乘回去，使统计结果仍然无偏。
- **蓄水池采样**：数据流长度事先未知（例如 Kafka 里源源不断的事件），要保持一个大小为 k 的均匀样本。

**蓄水池采样的做法：**
1. 前 k 条直接放进池子。
2. 第 n 条（n > k）以 k/n 的概率入选；入选就随机替换池中一条。
3. 任意时刻，看过的每条数据留在池中的概率都是 k/n。

```python
import random
def reservoir(stream, k):
    pool = []
    for n, item in enumerate(stream, start=1):
        if n <= k:
            pool.append(item)
        elif random.random() < k / n:
            pool[random.randrange(k)] = item
    return pool
```

**直觉验证**：k = 1 时，第 2 条以 1/2 替换第 1 条，第 3 条以 1/3 替换……最后每条留下的概率都是 1/n。

**常见坑**：按用户采样还是按事件采样会改变分布。按事件采样时，重度用户的行为占了大部分样本，模型会更像为重度用户服务；需要的话按用户先抽，再取其事件。
