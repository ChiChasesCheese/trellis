---
id: uth-ai-sampling-3-partial-sort
node: ai.sampling
type: qa
step: 3
---
## Q
**词表十几万，不用整个排序**｜llama.cpp · vLLM

top-k 和 top-p 都要用到「从大到小」。词表有十几万个词，每生成一个字就全排一遍太慢，实际怎样省？

## A
**背景。** 全排序是 O(V log V)，V 是词表大小。可只有前几十名会被留下，而这一步每生成一个字都要做一次。

**结构。** 只排需要的部分：部分排序（partial sort）把最大的几个排好就停，后面的不管；或者干脆不排，只找一个「门槛分数」，高于它的留下。

**细节。**

- llama.cpp 的 top-k：`k` 不超过 128 用 `std::partial_sort`；更大时先把词按分数分进 128 个桶，只排够 `k` 个的那几个高分桶
- llama.cpp 的 top-p：词数超过 1024 时先只排前 256 名并累加，加到 `p` 就停；没加到才扩大到整个词表
- vLLM 0.11 的 PyTorch 版：只用 top-k 时取前 `k` 名，第 `k` 名的分数当门槛；开了 top-p 就整行排序
- vLLM 0.32 的 GPU 内核：不排序，在分数范围里反复试门槛值、数一数高于它的有几个，直到刚好留下 `k` 个

**为什么。** 概率集中在头部，绝大多数时候前 256 名就够累加到 `p`，尾巴永远不用排。

**坑。** 排序版的 top-p 比 top-k 贵：累加必须有序。

**例题：** LC 215 数组中的第 K 个最大元素（同类：LC 347 前 K 个高频元素）

给整数数组 `nums` 和整数 `k`，返回排序后的第 `k` 个最大元素，要求期望 `O(n)`。例：`nums = [3,2,1,5,6,4]`、`k = 2` → `5`。快速选择拿一个 pivot 把数组分堆，只钻进答案所在的那一堆，不把整个数组排好，和「只排前几名、或只找门槛」是同一个想法。

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 答案在比 pivot 大的那一堆里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在 pivot 自己这一段
            return pivot
        else:                                      # 答案在比 pivot 小的那一堆里
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```
