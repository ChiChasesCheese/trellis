---
id: tlc-generate-parentheses-4-followup
node: p3.generate-parentheses
type: qa
step: 4
---
## Q
**LC 22 括号生成**｜追问

面试官接着问：（1）只要有效括号的**个数**，不要列出？（2）有没有不用回溯的生成方法？（3）`n` 很大，结果装不下内存，怎么一个一个地给出？

## A
1. **只要个数**：个数是卡特兰数。直接用公式 `math.comb(2 * n, n) // (n + 1)`，`O(n)`；或者用递推 `C(n) = Σ C(i) · C(n - 1 - i)`，`O(n^2)`。`n = 8` 得到 `1430`。
2. **闭包数法**：任何有效串都可以唯一地写成 `"(" + A + ")" + B`，其中 `A` 是 `k` 对、`B` 是 `n - 1 - k` 对的有效串（`0 <= k <= n - 1`）。递归地把所有 `k` 下的组合列出，等价于动态规划按对数 `0..n` 逐层构造，不需要回溯，也不会有无效串。

```python
from functools import cache


@cache
def closure(n: int) -> tuple[str, ...]:
    if n == 0:
        return ("",)
    return tuple("(" + a + ")" + b
                 for k in range(n)
                 for a in closure(k)
                 for b in closure(n - 1 - k))
```

   `closure(3)` 与回溯得到的集合相同，只是顺序不同。
3. **逐个产出**：把回溯改成生成器：在叶子处 `yield "".join(path)`，递归调用前加 `yield from`。内存只和递归深度有关，调用者可以边取边处理。

**Python 提醒**：用 `@cache` 的函数参数必须可哈希，返回值缓存的是同一个对象，所以返回不可变的 `tuple` 而不是 `list`，避免调用者修改后污染缓存。`str` 拼接 `"(" + a + ")" + b` 每次生成新字符串，对 `n <= 8` 没有问题。
