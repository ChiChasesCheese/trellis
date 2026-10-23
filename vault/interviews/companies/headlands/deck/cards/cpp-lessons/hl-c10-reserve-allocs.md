---
id: hl-c10-reserve-allocs
node: cpp-lessons.c10-new-malloc-allocators
type: qa
step: 9
---
## Q
用计数分配器实测：`vector` 做 1000 次 `push_back`、`list` 做 1000 次 `push_back`、`vector` 先 `reserve(1000)` 各发生多少次分配？这说明什么？

## A
- `vector` 1000 次 `push_back`：**11 次**分配，共请求 8188 字节（容量 1、2、4…1024 翻倍增长）。
- `list` 1000 次 `push_back`：**1000 次**分配（每节点一次），24000 字节。
- `vector` 先 `reserve(1000)`：**1 次**分配。
- 说明：这直接解释了「为什么 `reserve` 重要」和「为什么 `list` 慢」。销毁后分配次数 = 释放次数（11 = 11），没有泄漏。
