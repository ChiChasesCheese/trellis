---
id: tlc-python-recursion-memo-1-cache-search
node: python.recursion-memo
type: qa
step: 1
---
## Q
**Python 递归｜用 `@cache` 写记忆化搜索**

把编辑距离（LC 72）写成「递归 + `@cache`」，状态怎么选、复杂度怎么算？这样写比自底向上的 DP 好在哪里，代价是什么？

## A
先写**不带缓存的递归**（只看「当前状态」怎么由更小的状态得到），再加 `@cache`，就把指数级的重复计算压成「状态数 × 单次转移」。

```python
from functools import cache
def edit_distance(a: str, b: str) -> int:
    @cache
    def dp(i: int, j: int) -> int:          # a 的前 i 个字符变成 b 的前 j 个字符的最少步数
        if i == 0:
            return j                        # 只能插入 j 个字符
        if j == 0:
            return i                        # 只能删除 i 个字符
        if a[i - 1] == b[j - 1]:
            return dp(i - 1, j - 1)         # 末尾相同，不用操作
        return 1 + min(dp(i - 1, j),        # 删除 a 的末尾
                       dp(i, j - 1),        # 插入
                       dp(i - 1, j - 1))    # 替换
    return dp(len(a), len(b))
print(edit_distance("horse", "ros"), edit_distance("intention", "execution"), edit_distance("", "a"))
# 3 5 1
```

- 状态数 `(len(a)+1) * (len(b)+1)`，每个状态转移 `O(1)` → 时间、空间都是 `O(mn)`。
- 好处：转移方程直接翻译成代码，不用想遍历顺序、不用想初值数组下标；只会计算**被用到的**状态（有些题大量状态不可达，比自底向上省）。
- 代价：函数调用开销大（常数约是循环版的 3 到 5 倍）；递归深度等于状态链的长度，LC 72 在 `m, n` 到几百时深度约 `m + n`，可以；一维 DP 到 `10^4` 以上就会 `RecursionError`。
- 把 `@cache` 放在**内层函数**上：`a`、`b` 作为闭包变量，不进缓存键（键只含 `i`、`j`），且每次调用外层函数后缓存随函数一起释放。
- 注意：缓存键必须可哈希，传下标，不传子串或列表。
