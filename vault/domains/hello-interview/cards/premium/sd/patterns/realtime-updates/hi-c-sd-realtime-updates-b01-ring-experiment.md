---
id: hi-c-sd-realtime-updates-b01-ring-experiment
node: sd.patterns.realtime-updates.beyond
type: qa
step: 2
---
## Q
**实时更新 · 一致性哈希的搬迁量，用代码量一下**｜拓展 · 加分

"一致性哈希只搬一小部分"是真的吗？取模哈希和带虚拟节点的哈希环，扩容一台各搬多少？

## A
**模式。** 哈希环（consistent hash ring）加虚拟节点：把"哈希值取模"换成"在环上找顺时针第一个点"。

```python
import bisect
import hashlib


def h(s: str) -> int:
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")   # 稳定哈希，不用内置 hash()（每次启动种子不同）


class Ring:
    def __init__(self, servers: list[str], vnodes: int = 100) -> None:
        # 每台服务器在环上放 vnodes 个虚拟点，让负载更均匀，且增删一台时被影响的区段分散
        self._pts = sorted((h(f"{s}#{i}"), s) for s in servers for i in range(vnodes))
        self._keys = [p for p, _ in self._pts]

    def owner(self, user: str) -> str:
        i = bisect.bisect(self._keys, h(user)) % len(self._pts)   # 顺时针第一个点；越过末尾回到开头
        return self._pts[i][1]


users = [f"user{i}" for i in range(20000)]
old = [f"s{i}" for i in range(10)]
new = old + ["s10"]                                           # 扩容一台

mod_moved = sum(h(u) % 10 != h(u) % 11 for u in users) / len(users)   # 简单取模：N 从 10 变 11
r1, r2 = Ring(old), Ring(new)
ring_moved = sum(r1.owner(u) != r2.owner(u) for u in users) / len(users)
print(f"modulo moved {mod_moved:.0%}, ring moved {ring_moved:.0%}, ideal {1/11:.0%}")
```
- **结果：** 10 台扩到 11 台，取模搬走约 91% 的用户，哈希环约 10%，接近理想值 1/11（约 9%）；数字随点数略有浮动。
- **为什么用稳定哈希：** Python 内置 `hash()` 对字符串每次启动都会换种子，两台机器算出的结果不同，路由必须用 MD5 之类的稳定哈希。
- **虚拟节点的作用：** 每台服务器在环上放很多个点，让各机负担更均匀（少了就可能一台占掉大段环），也让一台下线时它的用户分散给多台而不是全压给下一台。
- **查找：** 点按哈希排序，用二分查找（`bisect`）找后继，O(log n)。
- **何时不用：** 服务器几乎不变、连接无状态且可以随便重连时，取模或随机分配就够了。
