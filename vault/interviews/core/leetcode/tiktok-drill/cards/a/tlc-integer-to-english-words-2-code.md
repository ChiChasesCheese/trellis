---
id: tlc-integer-to-english-words-2-code
node: a.integer-to-english-words
type: qa
step: 2
---
## Q
**LC 273 整数转换英文表示**｜写出 Python 实现

把 `0 <= num <= 2^31 - 1` 转成英文读法：单词首字母大写、单词之间恰好一个空格，`0` 读作 `"Zero"`。

## A
**思路。** 从低位每次 `divmod(num, 1000)` 取一组三位数，配上 `""`、`Thousand`、`Million`、`Billion`。组内：百位读「几 Hundred」，余数 `>= 20` 读「整十 + 个位」，`1` 到 `19` 直接查表。全 0 的组跳过，各组读完后反转拼接。

```python
BELOW_20 = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
            "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen",
            "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
SCALES = ["", "Thousand", "Million", "Billion"]


def number_to_words(num: int) -> str:
    if num == 0:
        return "Zero"

    def below_thousand(n: int) -> list[str]:        # 0 < n < 1000 的英文单词列表
        words: list[str] = []
        hundreds, rest = divmod(n, 100)
        if hundreds:
            words += [BELOW_20[hundreds], "Hundred"]
        if rest >= 20:
            tens, ones = divmod(rest, 10)
            words.append(TENS[tens])
            if ones:
                words.append(BELOW_20[ones])
        elif rest:                                   # 1..19 有各自的单词
            words.append(BELOW_20[rest])
        return words

    parts: list[str] = []
    for scale in SCALES:                             # 从低位的三位一组开始取
        num, chunk = divmod(num, 1000)
        if chunk:                                    # 整组为 0（如 1,000,000 的中间组）不输出
            words = below_thousand(chunk)
            if scale:
                words.append(scale)
            parts.append(" ".join(words))
        if num == 0:
            break
    return " ".join(reversed(parts))
```


运行：`123` → `"One Hundred Twenty Three"`，`12345` → `"Twelve Thousand Three Hundred Forty Five"`，`1234567` → `"One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"`，`0` → `"Zero"`，`1000010` → `"One Million Ten"`，`2147483647` → `"Two Billion One Hundred Forty Seven Million Four Hundred Eighty Three Thousand Six Hundred Forty Seven"`。

**复杂度。** 时间 `O(log num)`，至多 4 组、每组常数个单词；空间 `O(1)`。

**写法要点。** `divmod` 一次拿到商和余数，组间（1000）和组内（100、10）用同一个动作；`BELOW_20[0]` 和 `TENS[0]`、`TENS[1]` 留空串占位，让下标等于数值，查表不用减偏移；每组先收集成单词列表再 `" ".join`，从结构上杜绝双空格和尾空格。
