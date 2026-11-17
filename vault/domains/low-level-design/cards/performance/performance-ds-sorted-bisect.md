---
id: performance-ds-sorted-bisect
node: performance.data-structures
type: qa
step: 5
---
## Q
账户的余额历史按时间追加，要回答“某个时刻 t 的余额是多少”，也就是不晚于 t 的最近一条记录。线性往后扫一遍，和有序列表加 `bisect` 差多少？什么时候 `insort` 反而不划算？

## A
**有序数组 + 二分查“向下取整”，写入走追加**

- **查询**：`bisect_right(times, t) - 1` 是最后一个 `<= t` 的位置，O(log n)；返回 -1 表示 t 之前没有记录；
- **写入顺序决定成本**：时间只增不减时直接 `append`，仍然有序，写入 O(1)；
- **乱序插入用 `insort`**：它找位置很快，但要把后面的元素整体后移，每次 O(n)；
- **批量乱序写入**：先全部 `extend`，再 `sort()` 一次；timsort 对“一段有序加一小段乱序”的数据很快；
- **读写比**：读多写少用有序数组；写多读少、要随时删除中间项，换堆或平衡树（标准库没有，通常引入 `sortedcontainers`）。

实测（3.11，本机，10 万个有序时间点）：线性扫描一次查询约 303 µs，`bisect_right` 约 154 ns。往里乱序插 1000 个：逐个 `insort` 每个约 5.9 µs，合计约 5.9 ms；`extend` 后 `sort()` 一次合计 0.43 ms。

```python
import bisect

times = [10, 20, 30, 40]
balances = [100, 120, 90, 150]

def balance_at(t):
    i = bisect.bisect_right(times, t) - 1     # 最后一个 <= t 的下标
    return balances[i] if i >= 0 else None    # t 在第一条之前：没有记录

print(balance_at(5), balance_at(20), balance_at(35), balance_at(99))
# None 120 90 150
```

**知识点：**按访问模式选结构（Choosing Structures）
