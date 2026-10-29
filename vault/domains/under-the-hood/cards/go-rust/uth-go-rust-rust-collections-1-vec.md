---
id: uth-go-rust-rust-collections-1-vec
node: go-rust.rust-collections
type: qa
step: 1
---
## Q
**Vec 的容量怎样增长**｜Rust · 1.99

Rust 的 `Vec::push` 容量不够时，新容量是多少？

## A
**背景。** 数组要连续才能按下标快速访问，所以满了不能原地接长，只能新开一块更大的，把旧元素搬过去。每次只多开一格，搬运量会涨到 n²；每次翻倍，每个元素平均只搬常数次，`push` 就是均摊 O(1)。例：`Vec<i32>` 容量 4 装满后，再 `push` 一个，容量变成 8。

**结构。** `Vec` 是“指针、长度、容量”三个字段，底下由 `RawVec` 管理一块连续堆内存。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Vec&lt;i32&gt;: 三个字段 + 一块堆内存</text>
<rect x="10" y="26" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="40" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ptr</text>
<rect x="70" y="26" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="100" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">len 3</text>
<rect x="130" y="26" width="60" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="160" y="43.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cap 4</text>
<line x1="40" y1="52" x2="40" y2="78" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="40,78 37.3,72.0 42.7,72.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="10" y="78" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="28" y="94.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="78" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="68" y="94.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="90" y="78" width="36" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="108" y="94.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="130" y="78" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="8" y="124" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">push 时 len == cap: 新容量 = max(旧 × 2, 所需)</text>
<rect x="10" y="132" width="36" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="28" y="147.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="50" y="132" width="36" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="68" y="147.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="90" y="132" width="36" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="108" y="147.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="130" y="132" width="36" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="148" y="147.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="170" y="132" width="36" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="188" y="147.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="210" y="132" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="250" y="132" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="290" y="132" width="36" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="8" y="176" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4 → 8 → 16 → 32 ...: 严格翻倍, 没有逐步降到 1.25 倍</text>
</svg>
```

**细节。**

- 新容量 = `max(旧容量 × 2, 所需容量)`，严格翻倍，没有 Go 那种逐步降到 1.25 倍的缓冲
- 第一次分配的最小容量：元素 1 字节时是 8，元素不超过 1024 字节时是 4，更大的元素是 1
- 实测：`Vec<i32>` 依次为 `4 8 16 32 64 128`，`Vec<u8>` 为 `8 16 32 …`

**为什么。** 翻倍保证均摊 O(1)；给小元素一个最小容量，避免 1、2、4 这样连续的小分配。

**例题：** LC 380 O(1) 时间插入、删除和获取随机元素（同类：LC 155 最小栈）

设计 `RandomizedSet`：`insert`、`remove`、`getRandom`，每个操作平均 O(1)。例：`insert(1)` → `true`，`remove(2)` → `false`，`insert(2)` → `true`，`getRandom()` 返回 1 或 2。数组负责按下标随机取，删除时把末尾元素换到空位，和 `Vec::swap_remove` 一样。

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
