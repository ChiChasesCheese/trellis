---
id: hl-cache-locality-kinds
node: foundations.cpu-cache-locality
type: qa
step: 9
---
## Q
时间局部性（temporal locality）和空间局部性（spatial locality）各指什么？硬件预取器（prefetcher）起什么作用？

## A
- **时间局部性**：刚用过的数据很可能马上再用，缓存留着它。例：循环里反复累加同一个变量。
- **空间局部性**：用了某地址，很可能马上用它旁边的，缓存行把旁边的也搬来。例：顺序遍历数组。

**硬件预取器**检测到顺序（或固定步长）访问，会提前把后面的行取进来，让缓存缺失根本不发生。因此顺序访问最理想。
