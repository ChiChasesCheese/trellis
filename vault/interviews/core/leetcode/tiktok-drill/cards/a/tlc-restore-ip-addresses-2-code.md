---
id: tlc-restore-ip-addresses-2-code
node: a.restore-ip-addresses
type: qa
step: 2
---
## Q
**LC 93 复原 IP 地址**｜写出 Python 实现

只含数字的字符串 `s`（长度 `1..20`）。通过插入 `'.'` 把它切成四段，每段是 `0..255` 的整数且没有前导零，返回所有可能的有效 IP 地址，不能重排或删除数字。用回溯实现。

## A
**思路。** `dfs(start)` 表示从下标 `start` 开始切下一段，`parts` 里是已经切好的段。若已有 `4` 段，当 `start == n` 时收集答案。否则先用长度范围剪枝；再依次尝试长度 `1`、`2`、`3` 的段，遇到前导零或数值超过 `255` 就 `break`，合法就加入 `parts`、递归、再撤销。

```python
def restore_ip_addresses(s: str) -> list[str]:
    n = len(s)
    res: list[str] = []
    parts: list[str] = []

    def dfs(start: int) -> None:
        left = 4 - len(parts)           # 还要切出几段
        if left == 0:
            if start == n:              # 恰好用完所有字符
                res.append(".".join(parts))
            return
        if not left <= n - start <= 3 * left:   # 每段 1~3 位：剩余字符数不在范围内就剪枝
            return
        for end in range(start + 1, min(start + 3, n) + 1):
            seg = s[start:end]
            if len(seg) > 1 and seg[0] == "0":  # 前导零：更长的段同样非法，直接 break
                break
            if int(seg) > 255:                  # 更长的段只会更大
                break
            parts.append(seg)
            dfs(end)
            parts.pop()

    dfs(0)
    return res
```

运行：`"25525511135"` → `['255.255.11.135', '255.255.111.35']`，`"0000"` → `['0.0.0.0']`，`"101023"` → `['1.0.10.23', '1.0.102.3', '10.1.0.23', '10.10.2.3', '101.0.2.3']`，`"1"` → `[]`，`"1111"` → `['1.1.1.1']`，`20` 个 `"2"` → `[]`（太长，最多 `12` 位）。

**复杂度。** 时间 `O(3^4)`，即常数；空间 `O(1)`：递归深度 `4`，`parts` 至多 `4` 项。

**写法要点。** `".".join(parts)` 一步把四段拼成地址；`min(start + 3, n)` 保证切片不越界，`range(start + 1, …)` 的右端是切片的结束下标，所以长度是 `1..3`；链式比较 `left <= n - start <= 3 * left` 一次写出长度范围；`seg[0] == "0"` 与 `len(seg) > 1` 联合，保留单独的 `"0"`；`int(seg)` 只对长度不超过 `3` 的数字串调用，没有溢出问题；`break` 利用「更长的段更糟」，比 `continue` 少试几次。
