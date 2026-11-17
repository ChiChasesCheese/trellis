---
id: parsing-io-tokenizer-integer
node: parsing-io.tokenizer
type: qa
step: 4
---
## Q
整数的语法是 `-?(0|[1-9][0-9]*)`，要求 `-0` 接受，`01`、`+1`、`1.5`、`1e3` 拒绝，并限制在 64 位有符号范围内。读数字 token 时，为什么「正则匹配成功」还不够？

## A
**匹配之后还要看后一个字符，再查范围**

- **只吃合法前缀**：正则对 `01` 会匹配前面的 `0` 成功，剩下一个 `1`；`1.5` 会匹配 `1`，剩下 `.5`；不看后一个字符，数字被悄悄截成两段；
- **后继检查**：数字之后若紧跟数字、`.`、`e`、`E`，整个 token 非法；
- **`+1`**：正则不匹配，直接拒绝；`-0` 匹配，接受；
- **范围**：先看位数，超过十九位一定溢出，不交给 `int()`；再转换并比较 -2^63 到 2^63-1；
- **溢出是语法错**：不是「值太大」的请求错，评估阶段永远看不到它。

```python
import re
INT = re.compile(r"-?(?:0|[1-9][0-9]*)")
def read_int(s: str, i: int):
    m = INT.match(s, i)
    if not m: raise ValueError("invalid_json")
    j = m.end()
    if j < len(s) and s[j] in "0123456789.eE": raise ValueError("invalid_json")
    if len(m.group().lstrip("-")) > 19 or not -2**63 <= int(m.group()) < 2**63:
        raise ValueError("invalid_json")
    return int(m.group()), j
for text in ("-0,", "9223372036854775807]", "01", "1.5", "9223372036854775808", "+1"):
    try: print(text, read_int(text, 0))
    except ValueError: print(text, "invalid_json")
```

**知识点：**词法分析（Tokenizer）
