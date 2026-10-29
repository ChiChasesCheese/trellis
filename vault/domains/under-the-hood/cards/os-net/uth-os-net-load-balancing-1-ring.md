---
id: uth-os-net-load-balancing-1-ring
node: os-net.load-balancing
type: qa
step: 1
---
## Q
**一致性哈希环**｜Nginx · upstream hash consistent · 1.31

加一台后端时，怎样只搬走一小部分 key，而不像 `hash % N` 那样几乎全部重新洗牌？

## A
**背景。** N 台缓存服务器，最直接的分法是 `hash(key) % N`。可一旦加一台或坏一台，N 变了，几乎每个 key 的余数都变，缓存全部失效。一致性哈希的办法：把哈希值首尾相接成一个环，服务器也按哈希放到环上，key 沿顺时针走到的第一台服务器就是它的主人。加一台，只会接管它前面那一小段。

**结构。** Nginx 的做法：每台服务器按权重在 2^32 的环上放 `160 × weight` 个点（虚拟节点；对主机、端口和上一个点的哈希做 crc32），点排成有序数组。请求取 crc32 后在数组里二分，找第一个不小于它的点。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<circle cx="170" cy="100" r="70" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="182.155" cy="31.0635" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="184.76" y="20.2913" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<circle cx="223.623" cy="55.0049" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235.114" y="49.3631" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<circle cx="240" cy="100" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="255" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<circle cx="223.623" cy="144.995" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235.114" y="158.637" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<circle cx="193.941" cy="165.778" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="199.072" y="183.874" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<circle cx="157.845" cy="168.937" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="155.24" y="187.709" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<circle cx="104.222" cy="123.941" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="90.1261" y="133.072" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<circle cx="109.378" cy="65" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="96.3878" y="61.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<circle cx="135" cy="39.3782" r="5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="127.5" y="30.3878" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<circle cx="237.615" cy="118.117" r="4" stroke="currentColor" stroke-width="1.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<path d="M237.6,118.1 A70,70 0 0 1 222.2,142.1" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="210.364" y="116.423" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">key</text>
<text x="150" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">顺时针</text>
<text x="150" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">第一个点</text>
</svg>
```

**细节。**

- 查找是二分，O(log 点数)
- 增删一台，只有它相邻区间的 key 换主，约 1/N 的 key 受影响
- 每台机器放很多个点，地盘被切成许多小段，分布更均匀

**为什么。** `hash % N` 在 N 变化时几乎所有 key 都要重新映射；环把变动限制在被增删节点附近。

**例题：** LC 981 基于时间的键值存储（同类：LC 35 搜索插入位置）

设计 `TimeMap`：`set(key, value, timestamp)` 存值（时间戳严格递增）；`get(key, timestamp)` 返回满足 `timestamp_prev <= timestamp` 的最大时间戳对应的值，没有则返回 `""`。例：`set("foo","bar",1)`，`get("foo",3)` → `"bar"`。

```python
from bisect import bisect_right
from collections import defaultdict


class TimeMap:
    def __init__(self) -> None:
        self.times: defaultdict[str, list[int]] = defaultdict(list)    # key -> 递增的时间戳
        self.values: defaultdict[str, list[str]] = defaultdict(list)   # key -> 与 times 同下标的值

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times[key].append(timestamp)       # 时间戳严格递增：直接 append 就是有序的
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        times = self.times.get(key)             # 用 .get：defaultdict 的 [] 会凭空造出空列表
        if not times:
            return ""
        i = bisect_right(times, timestamp)      # 第一个 > timestamp 的位置，i-1 就是最后一个 <= timestamp 的
        return self.values[key][i - 1] if i else ""
```
