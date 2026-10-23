---
id: hl-cq-q17-deque-list-emplace-growth
node: cpp-questions.d-containers
type: qa
step: 5
---
## Q
三个追问：`vector`、`deque`、`list` 怎么选？`emplace_back` 和 `push_back` 的区别？扩容为什么有 2 倍和 1.5 倍两种选择？

## A
- **选择**：`deque` 在两端 push 时引用保持稳定，但内存是分块的；`list` 迭代器稳定，但局部性很差。
- **`emplace_back`**：用参数在容器内存里原地构造元素。
- **2 倍 vs 1.5 倍**：1.5 倍让释放掉的旧块有机会被之后的增长复用；2 倍增长更快。两者都是均摊 O(1)。
