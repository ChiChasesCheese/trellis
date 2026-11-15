---
slug: design-an-atm-machine
---
## Q
**LC 2241 设计一个 ATM 机器**｜Medium

ATM 里有 `20、50、100、200、500` 五种面额的钞票。`deposit(banknotesCount)` 存入各面额的张数；`withdraw(amount)` 取款：优先取大面额，不够再取小面额，不能恰好取出则返回 `[-1]` 且不取钞；成功返回各面额取出的张数。

## A
**一句话。** 取款从大面额往小面额贪心，每种取 `min(amount // 面额, 余额)`，余下金额不为 `0` 就取不出；确认可取后才扣钞。

```python
class ATM:
    VALS = [20, 50, 100, 200, 500]

    def __init__(self):
        self.cnt = [0] * 5

    def deposit(self, banknotes_count):
        for i, c in enumerate(banknotes_count):
            self.cnt[i] += c

    def withdraw(self, amount):
        take = [0] * 5
        for i in range(4, -1, -1):
            v = self.VALS[i]
            take[i] = min(amount // v, self.cnt[i])
            amount -= take[i] * v
        if amount:                        # 取不齐，什么都不动
            return [-1]
        for i in range(5):
            self.cnt[i] -= take[i]
        return take
```

**复杂度。** `deposit`、`withdraw` 均 `O(1)`（面额数固定）。

**易错点。**
- 边算边扣钞：取不齐时已经扣掉了，要先试算、成功再提交。
- 想用"最少张数"的 DP：题目规定的是优先大面额，不是最少张数，直接贪心。

**追问。**
- 面额变成任意的呢？：贪心不再保证能取出，需要 DP 判断，但"优先大面额"的规则仍要按题意实现。

**同模式。** LC 146 LRU 缓存、LC 1396 设计地铁系统、LC 635 设计日志存储系统
