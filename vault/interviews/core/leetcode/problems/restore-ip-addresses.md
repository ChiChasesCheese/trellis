---
slug: restore-ip-addresses
---
## Q
**LC 93 复原 IP 地址**｜Medium

在纯数字字符串 `s` 中插入三个 `.`，返回所有有效 IP（四段，每段 `0..255` 且无前导零）。

## A
**一句话。** 回溯逐段切，每段 1 到 3 位，无前导零且不超过 255，剩余长度不在 `[剩余段数, 3倍]` 就剪枝。

```python
def restore_ip_addresses(s):
    n = len(s)
    res, parts = [], []
    def dfs(start):
        left = 4 - len(parts)    # 还要切几段
        if left == 0:
            if start == n:       # 必须恰好用完
                res.append(".".join(parts))
            return
        if not left <= n - start <= 3 * left:
            return
        for end in range(start + 1, min(start + 3, n) + 1):
            seg = s[start:end]
            if len(seg) > 1 and seg[0] == "0":
                break            # 前导零，更长也不行
            if int(seg) > 255:
                break
            parts.append(seg)
            dfs(end)
            parts.pop()
    dfs(0)
    return res
```

**复杂度。** 时间 `O(3^4)`，即常数，空间 `O(1)`。

**易错点。**
- 不判前导零：`"101023"` 多出 `"1.0.1.023"` 等。
- 把单独的 `"0"` 也当前导零：`"0000"` 得空，应为 `["0.0.0.0"]`；条件是 `len(seg) > 1 and seg[0] == "0"`。
- 切满四段不查是否用完：`"11111"` 会多出只用前 4 位的地址。

**追问。**
- 不想递归？：`combinations(range(1, n), 3)` 枚举三个切点，逐段验证。
- 只验证一个地址（LC 468）？：按 `.` 切成四段，逐段查长度、前导零、范围。

**同模式。** LC 131 分割回文串、LC 468 验证 IP 地址、LC 165 比较版本号、LC 17 电话号码的字母组合
