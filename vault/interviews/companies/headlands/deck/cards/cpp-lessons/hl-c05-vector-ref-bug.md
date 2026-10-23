---
id: hl-c05-vector-ref-bug
node: cpp-lessons.c05-stl-containers
type: qa
step: 11
---
## Q
```cpp
std::vector<int> v{1, 2, 3};
int& first = v[0];
auto it = v.begin();
v.push_back(4);
std::cout << first << *it;
```
这段代码错在哪？AddressSanitizer 怎么报？怎么避免？

## A
- `v` 容量是 3，`push_back(4)` **重分配**，旧缓冲区被释放；`first` 和 `it` 指向已释放内存 → 读它们是 use-after-free，UB。
- AddressSanitizer 报：`heap-use-after-free`，`READ of size 4`，`0 bytes inside of 12-byte region`，并给出 freed / previously allocated 两处栈。
- 避免：先 `reserve` 够再取引用；换用 `deque`/`list`；或者只存**下标**而不是引用/迭代器。
