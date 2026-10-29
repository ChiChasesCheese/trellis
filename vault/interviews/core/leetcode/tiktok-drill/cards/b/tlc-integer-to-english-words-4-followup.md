---
id: tlc-integer-to-english-words-4-followup
node: b.integer-to-english-words
type: qa
step: 4
---
## Q
**LC 273 整数转换英文表示**｜追问

面试官接着问：（1）要支持英式读法 `"One Hundred and Twenty Three"`？（2）数的范围扩到 `10^18`？（3）反过来，把英文读法转回整数？

## A
1. **英式 `and`**：只影响组内：百位非 0 且余数非 0 时，在 `"Hundred"` 后插入 `"and"`。改 `below_thousand` 一处即可，外层不动，这正是两层拆分的好处。
2. **更大的数**：`SCALES` 末尾追加 `"Trillion"`（`10^12`）、`"Quadrillion"`（`10^15`）、`"Quintillion"`（`10^18`），循环和组内逻辑不变；Python 整数无上限，不需要改类型。
3. **英文转整数**：维护 `total`（已封口的高位）和 `group`（当前组）。数字词加到 `group`，`Hundred` 让 `group *= 100`，量级词让 `total += group * 量级` 并清零 `group`，最后返回 `total + group`。

```python
WORD_VALUE = {w: i for i, w in enumerate(["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
              "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
              "Sixteen", "Seventeen", "Eighteen", "Nineteen"])}
WORD_VALUE |= {w: 10 * i for i, w in enumerate(["Twenty", "Thirty", "Forty", "Fifty", "Sixty",
               "Seventy", "Eighty", "Ninety"], 2)}
SCALE_VALUE = {"Thousand": 10**3, "Million": 10**6, "Billion": 10**9}


def words_to_number(text: str) -> int:
    total = group = 0                        # total：已封口的高位；group：当前三位一组
    for w in text.split():
        if w == "Hundred":
            group *= 100
        elif w in SCALE_VALUE:
            total += group * SCALE_VALUE[w]  # 遇到量级词：当前组乘上量级后封口
            group = 0
        else:
            group += WORD_VALUE[w]
    return total + group
```

`"One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"` → `1234567`。

**Python 提醒**：`dict |= other` 是 3.9 起的原地合并；`enumerate(seq, 2)` 的第二个参数是起始编号，用来让 `"Twenty"` 对上 `2`。
