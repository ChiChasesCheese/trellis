---
id: tlc-rotate-array-4-followup
node: p3.rotate-array
type: qa
step: 4
---
## Q
**LC 189 轮转数组**｜追问

面试官接着问：（1）不用翻转，还有别的 `O(1)` 空间的原地做法吗？（2）改成向**左**轮转 `k` 位？（3）数组是一个很长的流/文件，不能整体放进内存？

## A
1. **环状替换**（cyclic replacement）：元素 `i` 的目的地是 `(i + k) % n`，沿这条链把元素逐个放到目的地，被挤掉的元素带在手里继续放。链的个数是 `gcd(n, k)`，每条链长 `n / gcd(n, k)`，总共恰好搬 `n` 次。
```python
from math import gcd

def rotate_cyclic(nums: list[int], k: int) -> None:
    n = len(nums)
    k %= n
    for start in range(gcd(n, k)):
        i, carry = start, nums[start]
        while True:
            i = (i + k) % n
            nums[i], carry = carry, nums[i]    # 放下手里的，拿起被挤掉的
            if i == start:
                break
```
   `k == 0` 时 `gcd(n, 0) = n`，每个环长度为 1，什么都不改，结果仍然正确。
2. **向左轮转 `k` 位**：等价于向右轮转 `n - k`；或把三次翻转改成「翻转前 `k` 个、翻转后 `n-k` 个、再整体翻转」。
3. **数据流/文件**：右移 `k` 位就是把末尾 `k` 个元素搬到开头。用 `collections.deque(maxlen=k)` 扫一遍留下末尾 `k` 个，输出时先写它们再写其余，内存 `O(k)`；或直接记录偏移量 `offset`，读第 `i` 个元素时返回 `(i - k) % n` 处的值，根本不移动数据。

**Python 提醒**：`collections.deque.rotate(k)` 就是原地向右轮转 `k` 位，`O(k)`；但 `deque` 随机访问中间元素是 `O(n)`，题目给的是 `list`，转成 `deque` 再转回来要 `O(n)` 额外空间，不符合 `O(1)` 要求。
