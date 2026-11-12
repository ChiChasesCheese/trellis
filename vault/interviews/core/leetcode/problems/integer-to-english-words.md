---
slug: integer-to-english-words
---
## Q
**LC 273 整数转换英文表示**｜Hard

把非负整数 `num`（至多 `2^31-1`）转成英文读法，如 `123` 为 `"One Hundred Twenty Three"`。

## A
**一句话。** 三位一组从低位取，每组读成「百 + 十几/几十几」再接 `Thousand`、`Million`、`Billion`。

```python
ONES = ("One Two Three Four Five Six Seven Eight Nine Ten "
        "Eleven Twelve Thirteen Fourteen Fifteen Sixteen "
        "Seventeen Eighteen Nineteen").split()
TENS = ("Twenty Thirty Forty Fifty Sixty Seventy "
        "Eighty Ninety").split()

def number_to_words(num):
    if num == 0:
        return "Zero"

    def three(n):              # 0 < n < 1000
        w = []
        h, r = divmod(n, 100)
        if h:
            w += [ONES[h - 1], "Hundred"]
        if r >= 20:
            w.append(TENS[r // 10 - 2])
            r %= 10
        if r:
            w.append(ONES[r - 1])
        return w

    parts = []
    for scale in ["", "Thousand", "Million", "Billion"]:
        num, chunk = divmod(num, 1000)
        if chunk:              # 整组为 0 不输出量级词
            w = three(chunk) + ([scale] if scale else [])
            parts.append(" ".join(w))
    return " ".join(reversed(parts))
```

**复杂度。** 时间 `O(log num)`，空间 `O(1)`。

**易错点。**
- 全 0 的组也加量级词：`1000000` 读成 `"One Million Thousand"`，应为 `"One Million"`。
- 13 读成「十位 + 个位」：`rest < 20` 要整体查表，否则得 `"Ten Three"`。
- 字符串到处补空格：先收集单词再 `" ".join`，避免双空格或尾空格。

**追问。**
- 英式读法要加 `and`？：百位非 0 且余数非 0 时，在两者之间插入 `"and"`。
- 数更大怎么办？：量级表末尾继续加 `Trillion` 等，循环不变。

**同模式。** LC 12 整数转罗马数字、LC 13 罗马数字转整数、LC 8 字符串转换整数
