---
id: hl-cache-calc-line-ints
node: foundations.cpu-cache-locality
type: qa
step: 39
---
## Q
Apple 芯片缓存行 128 字节。`int[]` 一个缓存行装多少个 `int`？顺序遍历平均每多少次访问加载一次新行？1000 万个元素的 `ArrayList<Long>` 与 `long[]` 各占多少内存？

## A
- 128 / 4 = **32 个** `int`。顺序遍历每 32 次访问加载一次新行（硬件预取会提前加载，程序感觉不到等待）。
- `ArrayList<Long>`：10⁷ × 28 B ≈ **280 MB**；`long[]`：10⁷ × 8 B = **80 MB**。
