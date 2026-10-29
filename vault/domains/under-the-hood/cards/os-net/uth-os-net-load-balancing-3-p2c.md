---
id: uth-os-net-load-balancing-3-p2c
node: os-net.load-balancing
type: qa
step: 3
---
## Q
**随机挑两个，选闲的那个**｜Envoy · least request

有 1000 台后端时，“选当前请求数最少的”要扫 O(n)，有没有又便宜又接近的办法？

## A
**背景。** 想把请求发给最闲的后端。1000 台时每次扫一遍找最少，是 O(n)；而且许多负载均衡器会同时看到同一台最闲的机器，一起涌向它（羊群效应，herding），反而把它压垮。P2C（power of two choices，两次选择的威力）的办法：随机挑 2 台，选其中活跃请求少的那台。

**结构。** Envoy 的 least request 在各主机权重相同时就是 P2C，挑选个数默认 2，复杂度 O(1)。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 204">
<text x="20" y="16" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">各后端的活跃请求数</text>
<rect x="40" y="90" width="24" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="52" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">1</text>
<rect x="76" y="115" width="24" height="35" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">2</text>
<rect x="112" y="70" width="24" height="80" rx="2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="124" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">3</text>
<rect x="148" y="125" width="24" height="25" rx="2" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="160" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">4</text>
<rect x="184" y="80" width="24" height="70" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="196" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">5</text>
<rect x="220" y="105" width="24" height="45" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="232" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">6</text>
<rect x="256" y="60" width="24" height="90" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">7</text>
<rect x="292" y="95" width="24" height="55" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="304" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">8</text>
<text x="124" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">忙</text>
<text x="160" y="117" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">选</text>
<line x1="30" y1="150" x2="330" y2="150" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">随机挑 2 台 取请求少的那台</text>
</svg>
```

**细节。**

- 文档引用 Mitzenmacher 等人的结论：几乎和 O(n) 的全扫一样好
- 全扫的毛病正是羊群效应：所有均衡器同时涌向那台“最闲”的机器
- 权重不等时改用加权轮询，权重按 `weight / (active_requests + 1)^bias` 动态计算（`bias` 是可配置的指数）

**为什么。** 多看一个随机样本，就能避开最忙的机器，又不必掌握全局状态。

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素（同类：LC 528 按权重随机选择）

实现 `RandomizedSet`：`insert(val)`、`remove(val)`、`getRandom()`（每个现有元素被返回的概率相同），每个操作平均 O(1)。

```python
import random


class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```
