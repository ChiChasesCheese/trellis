---
slug: fizz-buzz
---
## Q
**LC 412 Fizz Buzz**｜Easy

对 `1..n`：3 的倍数输出 `"Fizz"`，5 的倍数输出 `"Buzz"`，两者皆是输出 `"FizzBuzz"`，否则输出数字字符串。

## A
**一句话。** 3 的倍数拼 `"Fizz"`、5 的倍数拼 `"Buzz"`，拼出空串就用数字本身。

```python
def fizz_buzz(n):
    ans = []
    for i in range(1, n + 1):
        word = ("Fizz" if i % 3 == 0 else "") + \
               ("Buzz" if i % 5 == 0 else "")
        ans.append(word or str(i))
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`（不计输出）。

**易错点。**
- `elif` 链里 15 的分支放在 3、5 后面：`n=15` 最后一项成了 `"Fizz"`。
- `range(n)` 从 0 开始：第一项成了 `"FizzBuzz"`，应为 `"1"`。

**追问。**
- 规则要可扩展（加 7 → `"Jazz"`）？：用 `[(3, "Fizz"), (5, "Buzz")]` 规则表循环拼接，顺序决定拼接次序。

**同模式。** LC 12 整数转罗马数字、LC 13 罗马数字转整数、LC 168 Excel 表列名称、LC 17 电话号码的字母组合
