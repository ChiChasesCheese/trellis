---
id: hl-j15-ceildiv-floormod-use
node: java21.j15-math-string-utils
type: qa
step: 6
---
## Q
`Math.ceilDiv` 和 `Math.floorMod` 各用在什么场景？为什么比手写好？

## A
- `Math.ceilDiv(a, b)`（Java 18）：向上取整除法，「需要几页/几批/几块」的标准写法。103 条记录每页 25 条 → `Math.ceilDiv(103, 25) = 5`。旧写法 `(a + b - 1) / b` 在 `a` 接近 `MAX` 时自己会溢出。数组分块常见：`Math.ceilDiv((long) data.length, chunks)`。
- `Math.floorMod(x, n)`：结果永远在 `[0, n)`。环形缓冲区、哈希桶下标用它，因为 `x % n` 对负 `x` 会得到**负下标**。
