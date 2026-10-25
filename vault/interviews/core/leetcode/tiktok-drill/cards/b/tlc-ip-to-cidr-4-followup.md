---
id: tlc-ip-to-cidr-4-followup
node: b.ip-to-cidr
type: qa
step: 4
---
## Q
**LC 751 IP 到 CIDR**｜追问

面试官接着问：（1）标准库能不能直接做？（2）输入是一批不连续的 IP 区间，要求总块数最少？（3）反过来，给一个 CIDR 块，输出它覆盖的起止地址？（4）换成 IPv6？分别怎么答。

## A
1. **标准库**：

```python
import ipaddress


def cidr_by_stdlib(ip: str, n: int) -> list[str]:
    first = ipaddress.IPv4Address(ip)
    last = ipaddress.IPv4Address(int(first) + n - 1)
    return [str(net) for net in ipaddress.summarize_address_range(first, last)]
```

   `("255.0.0.7", 10)` → `['255.0.0.7/32', '255.0.0.8/29', '255.0.0.16/32']`，与手写结果相同。面试里先手写贪心，说明你理解对齐；再补一句生产代码用标准库。
2. **多个区间**：先按起点排序、合并重叠或首尾相接的区间，再对每个合并后的区间单独调用，块数相加。合并之后各区间互不相邻，不会有可以跨区间合并的块。
3. **CIDR 转起止**：`start = to_int(base) & ~((1 << (32 - k)) - 1)`，`end = start + (1 << (32 - k)) - 1`；`start` 先清掉低 `32 - k` 位，保证基础地址即使写得不规范也能归一。
4. **IPv6**：位宽 `128`，`1 << 32` 换成 `1 << 128`，前缀公式变成 `129 - size.bit_length()`，格式化改成 8 组十六进制；贪心逻辑不变。

**Python 提醒**：`ipaddress.summarize_address_range` 要求起点和终点是同一版本的地址，并且 `first <= last`，否则抛 `TypeError` / `ValueError`；它返回迭代器，需要列表时自己 `list(...)`。
