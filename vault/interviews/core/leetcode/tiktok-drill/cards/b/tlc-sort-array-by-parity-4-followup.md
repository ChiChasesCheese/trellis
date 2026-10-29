---
id: tlc-sort-array-by-parity-4-followup
node: b.sort-array-by-parity
type: qa
step: 4
---
## Q
**LC 905 按奇偶排序数组**｜追问

面试官接着问：（1）要求偶数之间、奇数之间都保持原来的相对顺序？（2）只用一个方向扫描的快慢指针怎么写，和对撞指针比有什么不同？（3）如果要分成三类（比如按 `x % 3`）？

## A
1. **稳定**：Python 的 `sorted` 是稳定排序，`sorted(nums, key=lambda x: x % 2)` 把偶数（键 `0`）排在奇数（键 `1`）前，同键保持原顺序；`[3,1,2,4]` → `[2, 4, 3, 1]`，`O(n log n)`。线性做法是两个列表推导拼接，`O(n)` 时间、`O(n)` 空间。原地且稳定的分区做不到 `O(n)` 时间加 `O(1)` 空间的简单写法，面试里说明这个取舍即可。
2. **快慢指针**：`write` 指向下一个偶数该放的位置，`read` 从左到右扫，遇到偶数就与 `nums[write]` 交换。

```python
def sort_by_parity_writer(nums: list[int]) -> list[int]:
    write = 0                              # nums[:write] 全是偶数
    for read, x in enumerate(nums):
        if x % 2 == 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    return nums
```

运行：`[3,1,2,4]` → `[2, 4, 3, 1]`。偶数部分保持原顺序（奇数部分不保证）；交换次数等于偶数个数；对撞指针只交换放错的那些，交换次数不会更多。这就是 Lomuto 分区，对撞版是 Hoare 分区。
3. **三类**：荷兰国旗问题（LC 75）：`low`、`mid`、`high` 三个指针，`nums[:low]` 是第一类、`nums[high+1:]` 是第三类，`mid` 扫描时按类别与 `low` 或 `high` 交换；与 `high` 交换后 `mid` 不前进，因为换过来的元素还没检查。

**Python 提醒**：`sorted` 返回新列表、`list.sort` 原地排序并返回 `None`；写 `return nums.sort(key=...)` 会返回 `None`。
