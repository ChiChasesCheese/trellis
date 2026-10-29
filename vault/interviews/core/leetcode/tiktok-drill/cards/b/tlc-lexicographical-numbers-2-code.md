---
id: tlc-lexicographical-numbers-2-code
node: b.lexicographical-numbers
type: qa
step: 2
---
## Q
**LC 386 字典序排数**｜写出 Python 实现

给整数 `n`（`1 <= n <= 5 * 10^4`），按字典序返回 `[1, n]` 内的所有整数，要求时间 `O(n)`、额外空间 `O(1)`。

## A
**思路。** 把数字看成十叉树做先序遍历，只用一个变量 `cur`。如果 `cur * 10 <= n` 就下沉；否则先回退（末位是 9 或 `cur + 1 > n` 时 `cur //= 10`）直到可以右移，再 `cur += 1`。循环恰好 `n` 次。

```python
def lexical_order(n: int) -> list[int]:
    result: list[int] = []
    cur = 1
    for _ in range(n):                       # 恰好生成 n 个数
        result.append(cur)
        if cur * 10 <= n:
            cur *= 10                        # 往下走：进入最左的孩子
        else:
            while cur % 10 == 9 or cur + 1 > n:
                cur //= 10                   # 这一层走完了：回退到父亲
            cur += 1                         # 换到右边的兄弟
    return result
```

运行：`13` → `[1,10,11,12,13,2,3,4,5,6,7,8,9]`，`2` → `[1,2]`，`1` → `[1]`，`25 的前 14 个` → `[1,10,11,12,13,14,15,16,17,18,19,2,20,21]`，`50000 的前 5 个` → `[1,10,100,1000,10000]`，`50000 的最后 3 个` → `[9997,9998,9999]`。

**复杂度。** 时间 `O(n)`，回退的总次数不超过 `n`；额外空间 `O(1)`。

**写法要点。** `for _ in range(n)` 明确「生成 n 个」；`while` 的条件把两种回退合在一起：`cur % 10 == 9 or cur + 1 > n`；整数除法 `//=` 去掉最后一位，比转字符串更省；一边生成一边 `append`，没有任何排序。
