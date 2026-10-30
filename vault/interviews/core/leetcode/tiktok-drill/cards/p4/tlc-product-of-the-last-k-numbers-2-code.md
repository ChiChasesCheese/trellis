---
id: tlc-product-of-the-last-k-numbers-2-code
node: p4.product-of-the-last-k-numbers
type: qa
step: 2
---
## Q
**LC 1352 最后 K 个数的乘积**｜写出 Python 实现

实现类 `ProductOfNumbers`：`add(num)`（`0 <= num <= 100`）把数加到流的末尾，`getProduct(k)`（`1 <= k <= 4 * 10^4`，保证流里至少有 `k` 个数）返回最后 `k` 个数的乘积。调用合计至多 `4 * 10^4` 次，任意连续序列的乘积在 32 位整数内。要求两个操作都是 `O(1)`。

## A
**思路。** 维护前缀积列表 `prefix`，首元素是哨兵 `1`。加入非零数时追加 `prefix[-1] * num`；加入 `0` 时列表重置为 `[1]`。查询时，`k` 不小于列表长度说明跨过了 `0`，返回 `0`；否则用最后一个前缀积整除倒数第 `k + 1` 个。

```python
class ProductOfNumbers:
    def __init__(self) -> None:
        self.prefix: list[int] = [1]        # prefix[i]：最近一个 0 之后前 i 个数的乘积，prefix[0] = 1

    def add(self, num: int) -> None:
        if num == 0:
            self.prefix = [1]               # 遇到 0：之前的前缀全部作废，重新开始
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        if k >= len(self.prefix):           # 最后 k 个数跨过了最近的 0
            return 0
        return self.prefix[-1] // self.prefix[-1 - k]   # 前缀积相除，整除是精确的
```

运行：依次 `add(3)`、`add(0)`、`add(2)`、`add(5)`、`add(4)`，`getProduct(2)` → `20`，`getProduct(3)` → `40`，`getProduct(4)` → `0`；`add(8)` 后 `getProduct(2)` → `32`。

**复杂度。** `add`、`getProduct` 均为 `O(1)`；空间 `O(n)`（流里非零段的前缀积）。

**写法要点。**
- 方法名 `getProduct` 沿用题目的驼峰命名，类的接口要和调用方一致。
- 哨兵 `prefix[0] = 1` 让 `k` 恰好等于有效数字个数时 `prefix[-1 - k]` 取到 `prefix[0]`，不用特判整段乘积。
- 重置用新建列表 `self.prefix = [1]`，旧列表整个被丢弃，比逐个删除快。
- 整数除法 `//` 保持整型；前缀积是后缀乘积的整数倍，所以整除精确。
- `self.prefix[-1 - k]` 用负下标直接从尾部数，和 `len(self.prefix) - 1 - k` 等价。
