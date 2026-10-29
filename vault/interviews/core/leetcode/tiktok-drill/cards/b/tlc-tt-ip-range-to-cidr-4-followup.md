---
id: tlc-tt-ip-range-to-cidr-4-followup
node: b.tt-ip-range-to-cidr
type: qa
step: 4
---
## Q
**IP 区间转最少 CIDR 列表**｜追问

面试官接着问：（1）标准库里有没有现成的；（2）只要一个能覆盖整个区间的最小 CIDR 块（允许多覆盖），怎么算；（3）IPv6 怎么办。

## A
1. **标准库**：`ipaddress.summarize_address_range(first, last)` 返回同样的最少块序列，参数是 `ipaddress.IPv4Address`，结果可以 `str()` 得到 `a.b.c.d/k`。手写的版本与它在任意区间上给出相同的列表；反方向用 `ipaddress.collapse_addresses` 把一堆 CIDR 合并成最少的块。
2. **单个最小覆盖块**：起止地址按位异或，最高的不同位决定块要有多大；前缀长度是 `32 - (lo ^ hi).bit_length()`，起点是把 `lo` 的低位清零。

```python
def cover_cidr(start: str, end: str) -> str:
    lo = int.from_bytes(bytes(map(int, start.split("."))))
    hi = int.from_bytes(bytes(map(int, end.split("."))))
    bits = (lo ^ hi).bit_length()                      # 起止地址不同的最高位决定块的大小
    base = lo >> bits << bits                          # 清掉低 bits 位，得到块的起点
    return f"{'.'.join(map(str, base.to_bytes(4)))}/{32 - bits}"
```

`127.0.0.7` 到 `127.0.0.16` → `127.0.0.0/27`（覆盖 `.0` 到 `.31`）；单个地址 `10.0.0.5` 到 `10.0.0.5` → `10.0.0.5/32`；`0.0.0.0` 到 `255.255.255.255` → `0.0.0.0/0`。
3. **IPv6**：思路完全一样，整数换成 `128` 位，前缀长度的基数从 `32` 换成 `128`，`to_bytes(16)`；`ipaddress.IPv6Address` 和 `summarize_address_range` 同样可用。Python 整数没有位数上限，不需要特殊处理。

**Python 提醒**：`int.from_bytes` 和 `int.to_bytes` 的 `byteorder` 参数从 Python 3.11 起默认为 `"big"`，旧版本必须显式写；`bytes([...])` 在元素超出 `0..255` 时抛 `ValueError`，可以直接当作地址段的范围检查。
