---
id: aie-retrieval-eval-calc
node: t03.retrieval-evaluation-recall-k-precision-mrr-ndcg
type: qa
step: 2
tags: [考点]
---
## Q
**Retrieval evaluation · 算一算**｜考点 · 必会

两个测试 query，库里分别有 4 个、2 个相关文档。retriever 取回 top-5：

| | 取回的 5 个（✓ 相关 / ✗ 不相关，按名次） |
|---|---|
| Query 1（库里 4 个相关） | ✓ ✗ ✓ ✗ ✗ |
| Query 2（库里 2 个相关） | ✗ ✗ ✓ ✓ ✗ |

求每个 query 的 precision@5、recall@5，以及两个 query 的 MRR。第一个 query 的 recall 低说明什么？

## A
| | 相关取回数 | precision@5 | recall@5 | 第一个相关的名次 | 倒数 |
|---|---|---|---|---|---|
| Query 1 | 2 | 2/5 = 0.40 | 2/4 = 0.50 | 1 | 1 |
| Query 2 | 2 | 2/5 = 0.40 | 2/2 = 1.00 | 3 | 1/3 |

**MRR** = (1 + 1/3) ÷ 2 ≈ **0.67**。

**解读：**
- Query 1 的 recall 是 0.5：4 个相关文档只找回 2 个。可能原因：k 太小、chunk 把答案切散、关键词/embedding 没匹配上。**应该改召回**（加大 k、hybrid search、改 chunking），再看。
- Query 2 的 recall 满分，但相关文档排在第 3、4 名，MRR 把它扣下来了。**应该改排序**（reranking）。
- precision 低（0.4）意味着放进 context 的 5 个里有 3 个是噪声，会占 token、干扰模型。

**这两个指标在回答什么问题：** recall = "该找的找到没有"，precision = "找到的有多少是对的"，MRR = "第一个对的有多靠前"。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch6 §Comparing retrieval algorithms（指标定义）；表中数据为出题用的例子

</details>
