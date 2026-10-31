---
id: tlc-product-of-the-last-k-numbers-0-whole
node: p2.product-of-the-last-k-numbers
type: qa
---
## Q
**LC 1352 最后 K 个数的乘积**｜Medium · LC TikTok 近 6 个月热度 50/100（全时段 38）

设计一个接受整数流并能查询最后 `k` 个整数乘积的类 `ProductOfNumbers`：`add(num)` 把 `num` 添加到数字列表末尾；`getProduct(k)` 返回当前列表中最后 `k` 个数字的乘积（保证列表中至少有 `k` 个数字）。任何时候，任意连续数字序列的乘积都在 32 位整数范围内。`0 <= num <= 100`，`1 <= k <= 4 * 10^4`，`add` 与 `getProduct` 合计最多调用 `4 * 10^4` 次。进阶：让 `getProduct` 和 `add` 都是 `O(1)`。例：依次 `add(3)`、`add(0)`、`add(2)`、`add(5)`、`add(4)`，则 `getProduct(2)` 得 `20`，`getProduct(3)` 得 `40`，`getProduct(4)` 得 `0`；再 `add(8)` 后 `getProduct(2)` 得 `32`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前缀积（prefix product）代替前缀和：`prefix[i]` 是前 `i` 个数的乘积，最后 `k` 个数的乘积 = `prefix[-1] // prefix[-1-k]`，查询 `O(1)`。遇到 `0` 就清空前缀列表重新开始；若 `k` 超过了最近一个 `0` 之后的数字个数，说明这 `k` 个数里含 `0`，答案是 `0`。

**识别。** 「数据流」加「频繁查询最后 `k` 个」加「`O(1)`」是**前缀和思想**的设计题。区间和用减法，区间积用除法；除法的唯一障碍是 `0`，所以设计的核心是怎样处理 `0`。调用次数 `4 * 10^4`、`k` 可达 `4 * 10^4`，每次现算乘积 `O(k)` 总共约 `1.6 * 10^9`，超时。

**推导。** 暴力：存下整个列表，`getProduct` 时对最后 `k` 个现乘，`O(k)`。改用前缀积：`prefix = [1, a1, a1*a2, ...]`，区间积 = 两个前缀相除。障碍：数里有 `0` 时，所有后续前缀都是 `0`，除法会 `0 / 0`。办法：遇到 `0`，之前的所有前缀对以后的查询都没用（任何覆盖这个 `0` 的区间乘积都是 `0`），所以直接清空，`prefix = [1]` 重新开始；查询时只要 `k` 超出了清空后的长度，就一定覆盖了最近的 `0`，返回 `0`。

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

运行：按题面依次 `add(3)`、`add(0)`、`add(2)`、`add(5)`、`add(4)` 后，`getProduct(2)` → `20`，`getProduct(3)` → `40`，`getProduct(4)` → `0`；再 `add(8)`，`getProduct(2)` → `32`。

**复杂度。** `add` 与 `getProduct` 都是 `O(1)`；空间 `O(n)`。

**拓展优化。**
- 不清空前缀列表的写法：`0` 当作 `1` 参与前缀积，另记最近一个 `0` 的位置；查询时 `0` 落在最后 `k` 个里就返回 `0`：
```python
class ProductOfNumbersLastZero:
    def __init__(self) -> None:
        self.prefix: list[int] = [1]                # prefix[i]：前 i 个数（0 按 1 计）的乘积
        self.last_zero = 0                          # 最近一个 0 的位置（从 1 数起），0 表示还没有

    def add(self, num: int) -> None:
        if num == 0:
            self.last_zero = len(self.prefix)       # 这个 0 是第 len(prefix) 个数
            self.prefix.append(self.prefix[-1])     # 0 按 1 计，前缀积保持可除
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        n = len(self.prefix) - 1
        if self.last_zero > n - k:                  # 最后 k 个数的位置是 n-k+1..n，0 在其中
            return 0
        return self.prefix[n] // self.prefix[n - k]
```

**易错点。**
- 遇到 `0` 不清空，直接把 `0` 乘进去：之后的前缀全是 `0`，查询时 `0 // 0` 抛 `ZeroDivisionError`。
- 判断“跨过 `0`”的条件是 `k >= len(self.prefix)`：`prefix` 长度比有效数字个数多 `1`（有哨兵 `1`），所以 `k` 等于有效数字个数时（`k == len(prefix) - 1`）仍可除，`k` 再大一点就越过了 `0`。写成 `k > len(prefix)` 会在 `k == len(prefix)` 时下标越界。
- 用 `/` 而不是 `//`：`getProduct(2)` 返回 `20.0`，类型变成浮点，数值再大还会丢精度。前缀积整除是精确的，用 `//`。

**追问。**
- 内存有上限：只需要最近 `K_max + 1` 个前缀积，可以用 `deque(maxlen=K_max + 1)`；列表长度不再表示“最近一个 `0` 之后有多少个数”，要另记一个计数器。
- 求滑动窗口乘积、或者含负数的情形：前缀积加除法同样适用（整数除法在整除时是精确的），只要没有 `0`。

**同模式。** LC 303 区域和检索、LC 238 除自身以外数组的乘积、LC 560 和为 K 的子数组、LC 713 乘积小于 K 的子数组。
