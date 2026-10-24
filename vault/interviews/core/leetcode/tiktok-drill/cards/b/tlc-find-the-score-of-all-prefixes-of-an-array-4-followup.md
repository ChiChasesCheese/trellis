---
id: tlc-find-the-score-of-all-prefixes-of-an-array-4-followup
node: b.find-the-score-of-all-prefixes-of-an-array
type: qa
step: 4
---
## Q
**LC 2640 一个数组所有前缀的分数**｜追问

面试官接着问：（1）数据是逐个到来的流，不能存下整个数组，怎么办？（2）要求除答案外 `O(1)` 额外空间怎么写？（3）数值很大，Java / C++ 要注意什么？

## A
1. **流式。** 只需要「当前最大值」和「累计分数」两个变量，每来一个元素就更新并吐出一个答案，用生成器最自然：

```python
from collections.abc import Iterable, Iterator


def prefix_scores_stream(nums: Iterable[int]) -> Iterator[int]:
    run_max = total = 0                  # 元素都是正数，0 可以当 run_max 的初值
    for x in nums:
        run_max = max(run_max, x)
        total += x + run_max
        yield total
```

2. **原地。** 同一个循环里把 `nums[i]` 直接覆盖成 `total`，不再新建列表；如果输入允许被修改，额外空间就是两个变量。
3. **溢出。** 每个转换值最大 `2 * 10^9`，最多 `10^5` 项累加，答案最大 `2 * 10^14`：超出 32 位整数，要用 `long` / `int64`，但不需要大数。

**Python 提醒**：若元素可以是负数，`run_max` 的初值不能写 `0`，要用 `float("-inf")` 或第一个元素；`accumulate(nums, max)` 没有这个问题，因为它用第一个元素当起点。
