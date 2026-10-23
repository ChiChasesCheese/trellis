---
id: hl-cache-line-corollaries
node: foundations.cpu-cache-locality
type: qa
step: 8
---
## Q
缓存行机制带来哪三条必须记住的推论？什么是冲突缺失（conflict miss）？

## A
1. 读 `a[0]` 之后，`int` 数组的 `a[1]`…`a[15]`（64 B 行）**已免费在缓存里**。
2. 相距 ≥ 64 字节（Apple 为 128）的两次访问，几乎一定是两次不同的缓存行读取。
3. 缓存按组映射，两个地址 `set` 相同会互相竞争，称冲突缺失；数组步长恰为 2 的大幂（如 4096 字节）时，访问反复落在同一组，互相挤掉。
