---
slug: bulls-and-cows
---
## Q
**LC 299 猜数字游戏**｜Medium

`secret` 和 `guess` 等长数字串，返回 `"xAyB"`：`x` 是位置和数字都对的个数，`y` 是数字对但位置不对、去掉公牛后还能配上的个数。

## A
**一句话。** 先数逐位相等的公牛；剩下没对上的位置，两边各自计数，每个数字取两边次数的最小值之和就是奶牛。

```python
def get_hint(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cs, cg = Counter(), Counter()
    for s, g in zip(secret, guess):
        if s != g:              # 公牛位置不参与配对
            cs[s] += 1
            cg[g] += 1
    cows = sum((cs & cg).values())   # & 逐数字取最小
    return f"{bulls}A{cows}B"
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（只有 10 个数字）。

**易错点。**
- 整串计数取交集当奶牛：公牛也被算进去，`"11","11"` 得 `2A2B`，应为 `2A0B`。
- 只用 `guess` 计数去扣 `secret`：数字在一边多时会多算，要两边取最小。

**追问。**
- 一遍扫完？：一个长度 10 的数组，`secret` 的数字 `+1`、`guess` 的 `-1`；`s` 处计数为负说明之前 `guess` 出现过它，奶牛加一，反之亦然。
- 字母而不是数字？：计数表换成 26 或字典，逻辑不变。

**同模式。** LC 242 有效的字母异位词、LC 383 赎金信、LC 1002 查找共用字符
