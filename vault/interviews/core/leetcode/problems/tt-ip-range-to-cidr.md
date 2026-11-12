---
slug: tt-ip-range-to-cidr
---
## Q
**IP 区间转最少 CIDR 列表**｜Medium

给定 IPv4 闭区间 `[start, end]`（点分十进制），输出恰好覆盖它的最短 CIDR 块列表，按地址升序。格式不对或起点大于终点抛 `ValueError`。

## A
**一句话。** 把 IP 当 32 位整数，每步取「起点能对齐的最大块」和「不超过剩余长度的最大 2 的幂」的较小者，输出后前进。

```python
def ip_range_to_cidr(start, end):
    def to_int(ip):
        parts = ip.split(".")
        if len(parts) != 4:
            raise ValueError(ip)
        # 超出 0..255 时 bytes() 抛 ValueError
        return int.from_bytes(bytes(map(int, parts)))

    def to_str(x):
        return ".".join(map(str, x.to_bytes(4)))

    lo, hi = to_int(start), to_int(end)
    if lo > hi:
        raise ValueError("start > end")
    blocks = []
    while lo <= hi:
        align = lo & -lo or 1 << 32   # 起点能对齐的最大块
        left = hi - lo + 1
        fit = 1 << left.bit_length() - 1   # 不超过剩余的 2 的幂
        size = min(align, fit)
        plen = 33 - size.bit_length()
        blocks.append(f"{to_str(lo)}/{plen}")
        lo += size
    return blocks
```

**复杂度。** 时间 `O(32)`，空间 `O(1)`（不含输出）。

**易错点。**
- 前缀长度写成 `32 - size.bit_length()`：`size = 8` 的 `bit_length` 是 `4`，得 `28`，应为 `29`。
- `lo = 0` 时 `lo & -lo` 为 `0`，`lo` 不前进，死循环，要用 `or 1 << 32`。
- 只考虑对齐不考虑剩余长度：`127.0.0.8` 到 `127.0.0.10` 只有 3 个地址，却输出 `/29`，应为 `['127.0.0.8/31','127.0.0.10/32']`。

**追问。**
- 标准库有吗？：`ipaddress.summarize_address_range(first, last)` 结果相同。
- 只要一个能覆盖区间的最小块？：前缀长度是 `32 - (lo ^ hi).bit_length()`。

**同模式。** LC 751 IP 到 CIDR、LC 468 验证IP地址、LC 93 复原 IP 地址、LC 231 2 的幂
