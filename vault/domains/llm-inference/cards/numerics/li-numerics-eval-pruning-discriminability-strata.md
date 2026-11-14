---
id: li-numerics-eval-pruning-discriminability-strata
node: numerics.eval-pruning
type: qa
step: 2
---
## Q
压缩大模型评测集时，怎样用"区分度"和"难度分层"挑题？写出选题和估分的代码，并说明它的偏差。

## A
**输入：** 一个"题 × 模型"的得分矩阵。大模型（LLM，读入文字、预测后续文字的程序）每做一道题得 0 或 1（写代码题在沙箱跑测试），或 0–1 之间的分（另一个大模型当评委打分）。

**两个量：**
- **难度：** 一道题在所有模型上的平均分。三个模型都对 = 1.0，都错 = 0.0。
- **区分度（discriminability）：** 同一道题上各模型分数差多大，最简单的算法是方差。三个模型 1/1/1 或 0/0/0 时方差为 0，不提供任何比较信息；1/0/0 或 1/1/0 时方差 = 2/9 ≈ 0.22。

**为什么分层用题目自己的标签：** 只有三个模型时，难度只能取 0、1/3、2/3、1 四个值，太粗，也完全取决于这三个模型。写代码题通常自带"简单 / 中等 / 困难"标签，长上下文题有文档长度，这些不依赖任何模型，换新模型也不变。

```python
def spread(v):                                   # 区分度：模型间方差
    m = sum(v) / len(v)
    return sum((x - m) ** 2 for x in v) / len(v)

def select(scores, strata, budget):
    # scores: {题号: [模型1分, 模型2分, ...]}；strata: {题号: "easy"/"medium"/"hard"}
    groups, n = {}, len(strata)
    for item, s in strata.items():
        groups.setdefault(s, []).append(item)
    chosen, weight = [], {}
    for s, items in groups.items():
        k = max(2, round(budget * len(items) / n))       # 名额按全集比例分
        items.sort(key=lambda i: (-spread(scores[i]), i))  # 区分度高的优先，题号定序
        chosen += items[:k]
        weight[s] = len(items) / n                        # 层权重，用于估全集分
    return chosen, weight

def estimate(one_model, chosen, strata, weight):
    per = {}
    for i in chosen:
        per.setdefault(strata[i], []).append(one_model[i])
    return sum(weight[s] * sum(v) / len(v) for s, v in per.items())
```

**要点：**
- **按比例分名额：** 剪完后简单、中等、困难的比例和全集一样，估出的总分才能和全集分数对照。
- **分层加权估分：** 子集分数 = Σ 层权重 × 层内平均分，而不是子集的直接平均。
- **固定排序：** 同分按题号排，同样的输入永远选出同样的题，结果可复现。
- **偏差：** 区分度高的题都是"有人对有人错"的中等题，层内平均分会被拉向中间，绝对分数有偏。排名和放行结论用它最灵敏；如果还要报绝对分，每层再留一小部分随机题，专门用来估绝对分，并用全量数据量出误差。
