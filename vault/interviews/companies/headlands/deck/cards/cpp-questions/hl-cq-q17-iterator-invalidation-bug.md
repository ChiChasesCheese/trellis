---
id: hl-cq-q17-iterator-invalidation-bug
node: cpp-questions.d-containers
type: qa
step: 3
---
## Q
下面这段代码错在哪里？AddressSanitizer 会报什么？

```cpp
std::vector<int> v{1, 2, 3};     // capacity 3
auto first = v.begin();
v.push_back(4);
std::printf("%d\n", *first);
```

## A
- `push_back(4)` 时容量已满（3 → 重新分配），旧缓冲区被释放，`first` 成了**悬空迭代器**，`*first` 读的是已释放的内存。
- AddressSanitizer 报 **`heap-use-after-free`**，直接指向重新分配的路径。
- 规则：重新分配的 `push_back` 使所有迭代器、指针、引用失效；`erase` 使被删位置及之后的失效，并返回下一个有效迭代器；`insert` 同理。
