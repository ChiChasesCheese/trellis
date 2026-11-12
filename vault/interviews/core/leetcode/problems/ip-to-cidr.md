---
slug: ip-to-cidr
---
## Q
**LC 751 IP 到 CIDR**｜Medium

给起始 IPv4 地址 `ip` 和数量 `n`，用最少的 CIDR 块恰好覆盖 `[ip, ip+n-1]`，返回块列表。

## A
**一句话。** 把 IP 当 32 位整数，贪心每次取「与当前地址对齐、又不超过剩余数量」的最大 2 的幂块。

```python
def ip_to_cidr(ip, n):
    def to_int(s):
        a, b, c, d = map(int, s.split("."))
        return a << 24 | b << 16 | c << 8 | d

    def to_ip(x):
        return ".".join(str(x >> s & 255)
                        for s in (24, 16, 8, 0))

    x, ans = to_int(ip), []
    while n > 0:
        low = x & -x or 1 << 32       # 对齐上限；x=0 时不限
        size = min(low, 1 << (n.bit_length() - 1))
        ans.append(f"{to_ip(x)}/{33 - size.bit_length()}")
        x += size
        n -= size
    return ans
```

**复杂度。** 时间 `O(log n)`，空间 `O(log n)`。

**易错点。**
- 只取不超过 `n` 的最大 2 的幂、忽略对齐：`("255.0.0.7",10)` 得 `/29` 块，实际覆盖 `.0` 到 `.7`，越界到范围外。
- `x=0` 时 `x & -x` 为 `0`，`size` 为 `0`，循环不前进，要特判成不限。
- 前缀长度写成 `32 - size.bit_length()`：`size=1` 应为 `/32`，要 `33 - size.bit_length()`。

**追问。**
- 标准库怎么一步到位？：`ipaddress.summarize_address_range` 返回同样的最短 CIDR 列表。
- 输入是多个 IP 区间？：先排序合并重叠区间，再对每个区间调用本函数。

**同模式。** LC 468 验证 IP 地址、LC 93 复原 IP 地址、LC 191 位 1 的个数、LC 231 2 的幂
