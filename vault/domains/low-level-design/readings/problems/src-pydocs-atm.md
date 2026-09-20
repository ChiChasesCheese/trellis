---
nodes: [problems.machines.atm]
url: https://docs.python.org/3/library/math.html#math.gcd
---
# math.gcd — Python 标准库

值得读：一行文档，却撑起 ATM 这道题里最容易被忽略的一种失败。`NOTE_STEP = math.gcd(*面额)`
把"这笔金额有没有可能被钞票表达"从一串 `if` 变成一个常量：任何不是 `NOTE_STEP` 整数倍的金额，
**无论钞箱装多满**都吐不出来，它和"库存凑不出"是两种不同的错误，屏幕上该说的下一步也不同。
附带的好处是新增面额（比如 5 元）时 `NOT_REPRESENTABLE` 的判据自动跟着变，没有任何一处
判断要改。同页的 `math.isqrt`、`math.prod` 在别的题里也常用，但这里只需要 `gcd` 这一个。
