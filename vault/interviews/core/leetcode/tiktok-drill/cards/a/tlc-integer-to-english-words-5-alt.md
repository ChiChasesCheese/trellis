---
id: tlc-integer-to-english-words-5-alt
node: a.integer-to-english-words
type: qa
step: 5
---
## Q
**LC 273 整数转换英文表示**｜另一种解法

不按三位一组切，能不能用一张「数值 → 单词」的降序表，像整数转罗马数字那样递归地写？

## A
**思路。** 把所有会独立出现的单词按数值降序列成表：`Billion, Million, Thousand, Hundred, 90, 80, …, 20, 19, …, 1`。读 `n` 时找表里第一个 `<= n` 的单位：
- 单位 `>= 100`（量级词或 Hundred）：前面要读倍数，结果是「读 `n // 单位`」+ 单位词 +「读 `n % 单位`」。
- 单位 `< 100`：直接是这个单词，再接「读 `n - 单位`」。

```python
UNITS: list[tuple[int, str]] = [
    (10**9, "Billion"), (10**6, "Million"), (1000, "Thousand"), (100, "Hundred"),
    (90, "Ninety"), (80, "Eighty"), (70, "Seventy"), (60, "Sixty"), (50, "Fifty"), (40, "Forty"),
    (30, "Thirty"), (20, "Twenty"), (19, "Nineteen"), (18, "Eighteen"), (17, "Seventeen"),
    (16, "Sixteen"), (15, "Fifteen"), (14, "Fourteen"), (13, "Thirteen"), (12, "Twelve"),
    (11, "Eleven"), (10, "Ten"), (9, "Nine"), (8, "Eight"), (7, "Seven"), (6, "Six"),
    (5, "Five"), (4, "Four"), (3, "Three"), (2, "Two"), (1, "One"),
]


def number_to_words_table(num: int) -> str:
    if num == 0:
        return "Zero"

    def words(n: int) -> list[str]:
        for value, name in UNITS:                    # 找最大的、不超过 n 的单位
            if n >= value:
                if value >= 100:                     # 量级词和 Hundred：前面还要读出倍数
                    q, r = divmod(n, value)
                    return words(q) + [name] + words(r)
                return [name] + words(n - value)     # 20..90 与 1..19：单词 + 余数
        return []                                    # n == 0：什么都不读

    return " ".join(words(num))
```

运行：`1234567` → `"One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"`，`1000010` → `"One Million Ten"`，`0` → `"Zero"`，`2147483647` 的输出与三位一组的写法相同。

**为什么对。** 降序表保证每次取到的是当前最高位的读法；`words(0)` 返回空列表，全 0 的部分自然不发音，不需要单独判断「全 0 组」。递归深度只和单位层数有关（至多十几层）。

**取舍。** 表驱动版更短，边界由「`n == 0` 返回空」统一处理，适合白板快速写；三位一组版结构更贴近读法规则，改英式 `and` 或扩量级时只动一处，面试中更容易边写边解释。两者都是 `O(log num)`。
