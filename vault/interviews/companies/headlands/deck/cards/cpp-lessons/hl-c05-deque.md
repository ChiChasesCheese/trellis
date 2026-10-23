---
id: hl-c05-deque
node: cpp-lessons.c05-stl-containers
type: qa
step: 20
---
## Q
面试问：`std::deque` 是什么？它和 `vector` 比有什么取舍？
Interview question: What is a `std::deque`?

## A
- 内部是**分块数组**（固定大小块的数组）。
- 两端插入摊销 O(1)，随机访问 O(1)（需要两次间接寻址）。
- 元素**不连续**。
- 两端插入使**迭代器**失效，但**引用/指针不失效**（实测连续 `push_back` 1000 次，首元素地址不变）。
- 对应 Java 的 `ArrayDeque`。
