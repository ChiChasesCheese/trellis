---
id: tlc-kth-missing-positive-number-4-followup
node: b.kth-missing-positive-number
type: qa
step: 4
---
## Q
**LC 1539 第 k 个缺失的正整数**｜追问

面试官接着问：（1）有没有更短的 `O(n)` 写法？（2）数组不保证有序、可能有重复？（3）`k` 非常大，比如 `10^18`？

## A
1. **`O(n)` 的线性写法**：遍历数组，只要 `x <= k`，说明答案前面有一个位置被数组元素占掉了，`k` 后移一位；遇到 `x > k` 就停。

```python
def find_kth_positive_linear(arr: list[int], k: int) -> int:
    for x in arr:
        if x <= k:
            k += 1
        else:
            break
    return k
```

   `([2,3,4,7,11], 5)` → `9`，`([1,2,3,4], 2)` → `6`。这是最短的正确解法，二分版是进阶要求；先写它可以保证有一个正确答案。
2. **无序或有重复**：先 `sorted(set(arr))`，去重并排序，`O(n log n)`，之后用同样的二分或线性写法。如果只做一次，也可以建集合后从 `1` 数起：`O(max + k)`。
3. **`k` 极大**：二分的复杂度只与 `n` 有关，`k = 10^18` 也是 `O(log n)`；答案最大是 `k + n`。Python 的整数不会溢出，别的语言要用 64 位。

**Python 提醒**：`bisect_left` 的 `key` 参数（3.10+）可以让你在 `range(len(arr))` 上二分而不构造列表：`k + bisect_left(range(len(arr)), k, key=lambda i: arr[i] - i - 1)`。老版本没有 `key`，要自己写循环，或者先构造 `[arr[i] - i - 1 for i in range(n)]` 再 `bisect_left`（多一份 `O(n)` 空间）。
