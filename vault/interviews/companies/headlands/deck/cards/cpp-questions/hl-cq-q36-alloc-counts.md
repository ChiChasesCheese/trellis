---
id: hl-cq-q36-alloc-counts
node: cpp-questions.i-low-latency
type: qa
step: 2
---
## Q
怎么数一段代码做了多少次堆分配？1000 次 `push_back` 不 `reserve`、`reserve(1000)`、`std::list` 1000 个节点、`pmr` 竞技场各是多少次分配？2000 次构建 1000 节点链表，`malloc` 和竞技场各多少毫秒？

## A
- 数法：替换全局 `operator new` 做计数。
- `vector push_back ×1000`，不 `reserve`：**11 次**。
- `vector` 先 `reserve(1000)`：**1 次**。
- `std::list ×1000`：**1000 次**。
- `pmr list` + 100 个 `pmr string` 放在竞技场上：**0 次**（全从栈上缓冲区切）。
- 2000 次构建 1000 节点链表：`malloc` 约 **19 ms**，竞技场约 **6 ms**（约 3 倍）。
