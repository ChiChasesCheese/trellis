---
id: tlc-integer-to-english-words-0-whole
node: b.integer-to-english-words
type: qa
---
## Q
**LC 273 整数转换英文表示**｜Hard · CodeTop 国内累计 3 次 · 最近 2026-07-02（CodeTop）

把非负整数 `num` 转成英文读法，单词首字母大写、单词之间一个空格。`0 <= num <= 2^31 - 1`。例：`123` → `"One Hundred Twenty Three"`，`12345` → `"Twelve Thousand Three Hundred Forty Five"`，`1234567` → `"One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 英文读数以**三位一组**为单位：每组读成「几 Hundred + 几十几」，再接上量级词 `Thousand / Million / Billion`；从低位每次 `divmod(num, 1000)` 取一组，全 0 的组跳过，最后反转拼接。

**识别。** 这是模拟（simulation）题，难点不在算法而在把规则分解干净：`2^31 - 1` 约 21 亿，最多 4 组；每组内部又只有三种情形（百位、20 及以上的十位 + 个位、1 到 19 的独立单词）。把「组内读法」和「组的量级」拆成两层，各自用查表完成，代码就不会写成一堆特判。

**推导。** 直接按十进制每一位读不行：英语的 11 到 19 是独立单词，十位和个位要合起来看；量级词每三位才出现一次。所以先按 1000 切组（外层只管量级），组内再按 100 和 20 切（内层只管 1 到 999）。两层都只用 `divmod` 和查表，每个单词生成一次，没有浪费。剩下的全是边界：整数 0、全 0 的组、整十、11 到 19。

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

**复杂度。** 时间 `O(log num)`：至多 4 组，每组常数个单词；空间 `O(1)`，输出外只有固定大小的表。

**易错点。**
- 全 0 的组也加量级词：`1000000` 会读成 `"One Million Thousand "`（还多一个末尾空格），正确是 `"One Million"`。必须 `if chunk:` 才输出这一组。
- 11 到 19 按「十位 + 个位」读：`13` 会读成 `"Ten Three"`。`rest < 20` 时整体查 `BELOW_20`。
- 字符串拼接时到处补空格容易出现双空格或尾空格；先收集单词列表，最后 `" ".join`。`"Forty"` 不是 `"Fourty"`。

**追问。**
- 英式读法加 `and`（`One Hundred and Twenty Three`）：在 `below_thousand` 里百位非 0 且余数非 0 时插入 `"and"`。
- 数更大（到 `10^18`）：`SCALES` 末尾加 `"Trillion"`、`"Quadrillion"`、`"Quintillion"`，循环条件不变。
- 反过来把英文转回整数：逐词累加到当前组，遇 `Hundred` 把当前组乘 100，遇量级词把当前组乘量级加进总数并清零。

**同模式。** LC 12 整数转罗马数字、LC 13 罗马数字转整数、LC 8 字符串转换整数、LC 65 有效数字。
