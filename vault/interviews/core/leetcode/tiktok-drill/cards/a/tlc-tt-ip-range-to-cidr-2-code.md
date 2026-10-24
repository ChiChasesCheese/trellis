---
id: tlc-tt-ip-range-to-cidr-2-code
node: a.tt-ip-range-to-cidr
type: qa
step: 2
---
## Q
**IP 区间转最少 CIDR 列表**｜写出 Python 实现

函数 `ip_range_to_cidr(start, end)` 接收 IPv4 起止地址（点分十进制，闭区间），返回恰好覆盖该区间、块数最少的 CIDR 列表，按地址升序。起点必须是块大小的整数倍；地址格式不对（不是四段，或某段不在 `0..255`）或起点大于终点时抛 `ValueError`。

## A
**思路。** 地址转 32 位整数。循环：`align = lo & -lo`（起点能对齐的最大块，`lo = 0` 时视为不受限），`fit` 是不超过剩余地址数的最大 `2` 的幂，块大小取两者较小；输出 `地址/(33 - size.bit_length())`，`lo` 前进 `size`。

```python
def ip_range_to_cidr(start: str, end: str) -> list[str]:
    def to_int(ip: str) -> int:
        parts = ip.split(".")
        if len(parts) != 4:
            raise ValueError(f"bad ip {ip!r}")
        return int.from_bytes(bytes(map(int, parts)))        # 四个字节拼成 32 位整数；超出 0..255 时 bytes() 抛 ValueError

    def to_str(x: int) -> str:
        return ".".join(map(str, x.to_bytes(4)))

    lo, hi = to_int(start), to_int(end)
    if lo > hi:
        raise ValueError("start must not exceed end")
    blocks: list[str] = []
    while lo <= hi:
        align = lo & -lo or 1 << 32                          # 起点最低位 1 的值 = 起点处能对齐的最大块；0.0.0.0 不受限
        fit = 1 << (hi - lo + 1).bit_length() - 1            # 不超过剩余地址数的最大 2 的幂
        size = min(align, fit)
        blocks.append(f"{to_str(lo)}/{33 - size.bit_length()}")   # 块大小 2^k 对应前缀长度 32 - k
        lo += size
    return blocks
```

运行：`127.0.0.7` 到 `127.0.0.16` → `['127.0.0.7/32', '127.0.0.8/29', '127.0.0.16/32']`；`0.0.0.0` 到 `255.255.255.255` → `['0.0.0.0/0']`；`10.0.0.0` 到 `10.0.0.0` → `['10.0.0.0/32']`；`192.168.1.0` 到 `192.168.1.255` → `['192.168.1.0/24']`；`0.0.0.1` 到 `0.0.0.2` → `['0.0.0.1/32', '0.0.0.2/32']`；`1.2.3` → `ValueError`；`1.2.3.256` → `ValueError`；起点 `1.2.3.9`、终点 `1.2.3.4` → `ValueError`。

**复杂度。** 循环至多约 `64` 次，时间 `O(1)`；空间 `O(1)`（不含输出）。

**写法要点。** `bytes(map(int, parts))` 把四段整数直接变成 `4` 字节，超出 `0..255` 时自动抛 `ValueError`；`int.from_bytes(..)` 和 `x.to_bytes(4)` 默认大端（Python 3.11 起省略 `byteorder`）；`lo & -lo` 取最低位的 `1`；`1 << (n).bit_length() - 1` 是小于等于 `n` 的最大 `2` 的幂，运算符优先级是先 `-` 再 `<<`；`or 1 << 32` 处理 `lo = 0`，因为 `0 or X` 取 `X`；局部函数 `to_int`、`to_str` 只在这里使用，放进函数内部。
