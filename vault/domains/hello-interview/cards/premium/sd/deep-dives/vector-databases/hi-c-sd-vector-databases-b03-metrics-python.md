---
id: hi-c-sd-vector-databases-b03-metrics-python
node: sd.deep-dives.vector-databases.beyond
type: qa
step: 3
---
## Q
**向量数据库 · 归一化后三种度量等价，以及 top-K 的实现**｜拓展 · 加分

为什么多数嵌入用余弦、点积、欧氏距离结果一样？暴力 top-K 在代码里怎样做才不浪费？

## A
**模式。** 部分选择（partial selection）：只需要前 K 个，就不要对 n 个分数全排序。
```python
import numpy as np

rng = np.random.default_rng(0)
x = rng.standard_normal((100_000, 128)).astype(np.float32)
x /= np.linalg.norm(x, axis=1, keepdims=True)   # 归一化：每个向量长度为 1
q = x[0] + 0.1 * rng.standard_normal(128).astype(np.float32)
q /= np.linalg.norm(q)

def topk(scores: np.ndarray, k: int) -> list[int]:
    # argpartition 是 O(n) 的选择，只对 k 个候选排序，而不是 O(n log n) 全排序
    idx = np.argpartition(-scores, k)[:k]
    return idx[np.argsort(-scores[idx])].tolist()

dot = x @ q                                      # 一次矩阵乘法算出所有点积
l2 = np.linalg.norm(x - q, axis=1)
print(topk(dot, 5) == topk(-l2, 5))              # True：点积越大 = 距离越小
```
- **等价的原因：** 单位向量下 ‖x − q‖² = 2 − 2·(x·q)，所以距离越小等价于点积越大，也等价于余弦越大；排序完全一致。
- **推论：** 嵌入已归一化时，可以直接用最快的点积，不必再除以长度。
- **未归一化时：** 点积会偏向长度大的向量，余弦与欧氏距离不再等价，必须按模型训练时的度量来选。
- **向量化的意义：** 一次矩阵乘法（`x @ q`）借助 SIMD 和 BLAS 同时算所有分数，比逐个 Python 循环快几个数量级；精确 KNN 在几十万向量以内常常够用，不一定要建索引。
