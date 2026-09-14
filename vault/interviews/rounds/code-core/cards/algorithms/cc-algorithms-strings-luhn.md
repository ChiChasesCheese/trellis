---
id: cc-algorithms-strings-luhn
node: algorithms.strings
type: qa
---
## Q
Write the Luhn checksum walk and name the two ways it is usually got wrong.

## A
```python
def luhn_ok(num: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(num)):
        d = int(ch)
        if i % 2 == 1:            # every SECOND digit counting from the right
            d *= 2
            if d > 9:
                d -= 9            # 12 -> 3: identical to summing the two digits
        total += d
    return total % 10 == 0
```

- **Wrong #1: doubling from the left.** It agrees with the correct answer only for even-length numbers, and card numbers run 13–19 digits, so the odd-length cases fail.
- **Wrong #2: `d % 9` instead of `d - 9`.** They agree except at `d = 18`, where `% 9` gives 0 instead of 9 — one digit value, one silently rejected card.
- The **length and prefix** check is a separate rule and usually runs *first*: a passing checksum on a 17-digit number is still an unknown network, and the network answer must not depend on the checksum.
- Work on the digit string, not on an `int`: leading zeros are meaningful and a 19-digit number is fine but the string form is what the spec describes.

## Q zh
写出 Luhn 校验的逐位走法，并指出通常出错的两种方式。

## A zh
```python
def luhn_ok(num: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(num)):
        d = int(ch)
        if i % 2 == 1:            # 从右数起每隔一位
            d *= 2
            if d > 9:
                d -= 9            # 12 -> 3：与把两位数字相加等价
        total += d
    return total % 10 == 0
```

- **错法一：从左边开始翻倍。** 它只在偶数长度时与正确答案一致，而卡号长度是 13–19 位，所以奇数长度的用例会挂。
- **错法二：用 `d % 9` 代替 `d - 9`。** 二者只在 `d = 18` 时不同，`% 9` 给出 0 而不是 9 —— 一个数字值之差，一张卡被静默拒绝。
- **长度与前缀**检查是另一条规则，而且通常*先*执行：一个 17 位数字即使校验通过仍是未知卡组织，而卡组织的判定不能依赖校验和。
- 在数字字符串上运算，而不是 `int`：前导零是有意义的，19 位数字也没问题，但 spec 描述的是字符串形态。
