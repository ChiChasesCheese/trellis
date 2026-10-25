---
id: tlc-ip-to-cidr-2-code
node: b.ip-to-cidr
type: qa
step: 2
---
## Q
**LC 751 IP 到 CIDR**｜写出 Python 实现

给起始 IPv4 地址字符串 `ip`（形如 `"a.b.c.d"`）和数量 `n`（`1 <= n <= 1000`），返回用最少 CIDR 块恰好覆盖 `[ip, ip + n - 1]` 的字符串列表，每项形如 `"a.b.c.d/k"`。

## A
**思路。** 先把 `ip` 转成 32 位整数 `x`。循环：对齐上限 `x & -x`（`x = 0` 时视为 `1 << 32`），数量上限是不超过 `n` 的最大 2 的幂，两者取小得 `size`；输出 `x` 对应的地址和前缀长度 `33 - size.bit_length()`，再推进 `x`、减少 `n`。

```python
def ip_to_cidr(ip: str, n: int) -> list[str]:
    def to_int(s: str) -> int:
        a, b, c, d = map(int, s.split("."))
        return a << 24 | b << 16 | c << 8 | d

    def to_ip(x: int) -> str:
        return ".".join(str(x >> sh & 255) for sh in (24, 16, 8, 0))

    x = to_int(ip)
    ans: list[str] = []
    while n > 0:
        low = x & -x or 1 << 32                  # x 的最低位 1：当前地址最多对齐到多大的块（x=0 时不限）
        size = min(low, 1 << (n.bit_length() - 1)) # 又不能超过剩余数量 n 的最大 2 的幂
        ans.append(f"{to_ip(x)}/{33 - size.bit_length()}")
        x += size
        n -= size
    return ans
```

运行：`("255.0.0.7", 10)` → `['255.0.0.7/32', '255.0.0.8/29', '255.0.0.16/32']`；`("117.145.102.62", 8)` → `['117.145.102.62/31', '117.145.102.64/30', '117.145.102.68/31']`；`("0.0.0.0", 1000)` → 六个块 `/23, /24, /25, /26, /27, /29`；`("1.2.3.4", 1)` → `['1.2.3.4/32']`。

**复杂度。** 时间 `O(log n)`：块数不超过约 `2 log2(n)`；空间 `O(log n)`：输出列表。

**写法要点。** `x & -x` 取最低位的 `1`（`lowbit`）；`x & -x or 1 << 32` 利用 `or` 在左值为 `0` 时取右值，一行处理 `x = 0` 的特例；`int.bit_length()` 同时给出「不超过 `n` 的最大 2 的幂」（`1 << (bit_length - 1)`）与前缀长度；`str(x >> sh & 255)` 中移位优先级高于 `&`，不必加括号。
