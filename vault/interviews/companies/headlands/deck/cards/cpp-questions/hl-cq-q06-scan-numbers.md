---
id: hl-cq-q06-scan-numbers
node: cpp-questions.a-why-fast
type: qa
step: 32
---
## Q
对 400 万个 `int` 做一遍求和，`vector<int>`、按顺序分配的 `std::list<int>`、节点在内存里乱序的链表各要多久？第三种代表什么真实场景？

## A
- `vector<int>` 扫描：约 **0.2 ms**。
- `std::list<int>` 扫描：约 **4.4 ms**（节点按顺序分配，大致相邻，仍慢约 20 倍）。
- 节点乱序的指针追逐：约 **28.4 ms**，代表真实世界里“用了很久的链表”，节点已经在内存里四处散开。
