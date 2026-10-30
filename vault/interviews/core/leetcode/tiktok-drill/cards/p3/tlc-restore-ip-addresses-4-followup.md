---
id: tlc-restore-ip-addresses-4-followup
node: p3.restore-ip-addresses
type: qa
step: 4
---
## Q
**LC 93 复原 IP 地址**｜追问

面试官接着问：（1）不想写递归，能不能直接枚举切点？（2）改成**验证**一个字符串是不是有效的 IPv4 地址（LC 468）？（3）段数 `k` 和每段的取值范围都是参数时怎么推广？

## A
1. **枚举切点**：IP 有 `4` 段，就有 `3` 个切点，从 `1..n-1` 里选出，用 `itertools.combinations` 一行生成，再检查四段是否合法。结果顺序与回溯相同。

```python
from itertools import combinations


def restore_ip_addresses_comb(s: str) -> list[str]:
    res: list[str] = []
    for a, b, c in combinations(range(1, len(s)), 3):
        parts = [s[:a], s[a:b], s[b:c], s[c:]]
        if all(len(p) <= 3 and int(p) <= 255 and (p == "0" or p[0] != "0") for p in parts):
            res.append(".".join(parts))
    return res
```

   `n = 20` 时有 `C(19, 3) = 969` 个切法，每个检查四段，速度也完全够用。回溯的优势是可以提前剪枝，并且对「段数是参数」的推广更自然。
2. **验证 IPv4**：`s.split(".")` 必须正好得到 `4` 段；每段非空、全是数字、长度 `1..3`、没有前导零、数值 `<= 255`。注意 `str.isdigit()` 会接受某些 Unicode 数字，严格校验时要限定 `0-9`。
3. **推广**：把 `4` 换成参数 `k`，把 `3` 与 `255` 换成各段的位数上限和数值上限；剪枝里的 `3 * left` 换成各段上限之和。IPv6 每段是 `1..4` 位十六进制，规则不同，但回溯框架不变。

**Python 提醒**：`int("0123")` 返回 `123`，不会报错，也不会告诉你有前导零，所以前导零必须在转换前用字符串判断。`".".join(parts)` 要求 `parts` 全是 `str`，不能放整数。
