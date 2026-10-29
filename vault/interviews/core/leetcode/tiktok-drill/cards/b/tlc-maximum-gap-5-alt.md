---
id: tlc-maximum-gap-5-alt
node: b.maximum-gap
type: qa
step: 5
---
## Q
**LC 164 最大间距**｜另一种解法

不用桶，能不能用基数排序（radix sort）达到线性？它和桶 + 鸽巢的方案相比，各自适合什么场合？

## A
**思路。** 基数排序（LSD，最低位优先）是非比较排序：每一趟按某一段二进制位把数分到 `256` 个桶，按桶顺序稳定地收集；`nums[i] < 2^30`，每趟处理 `8` 位，共 `4` 趟，就得到完整的有序数组，再扫描相邻差。总时间 `O(n * d)`，`d = 4` 是常数。

```python
from itertools import pairwise


def maximum_gap_radix(nums: list[int]) -> int:
    if len(nums) < 2:
        return 0
    arr = list(nums)
    shift, top = 0, max(arr)
    while top >> shift:                         # LSD 基数排序：每趟按 8 位分 256 个桶，稳定地收集
        buckets: list[list[int]] = [[] for _ in range(256)]
        for x in arr:
            buckets[(x >> shift) & 255].append(x)
        arr = [x for bucket in buckets for x in bucket]
        shift += 8
    return max(b - a for a, b in pairwise(arr))
```

运行：`[3,6,9,1]` → `3`，`[10]` → `0`，`[1,2,100,101]` → `98`，`[0,1000000000]` → `1000000000`。

**为什么对。** 每一趟只按当前 `8` 位排序，但分桶时同桶内保持原有顺序（稳定），所以低位的顺序在高位趟里保留下来；`4` 趟之后整个数按全部位有序。循环条件 `top >> shift` 在最大值所有高位处理完后停止，数组全为 `0` 时一趟也不跑。

**取舍。** 基数排序思路直接（先排序再取相邻差），不用想鸽巢原理，不易出错，`d` 与数值位数有关；桶 + 鸽巢的方案只做常数遍扫描，不依赖位数，且更能体现思考。若只关心 Python 的实际速度，`sorted` + `pairwise` 往往最快；面试里先给桶方案，被问到「不用想这个性质」时给基数排序。
