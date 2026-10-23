---
id: hl-cq-q13-make-shared-allocs
node: cpp-questions.c-memory-ownership
type: qa
step: 13
---
## Q
`std::shared_ptr<int>(new int)` 和 `std::make_shared<int>()` 各做几次堆分配？为什么？两个 `shared_ptr` 指向同一对象时 `use_count` 是多少？全部 reset 后 `weak_ptr` 的状态是什么？

## A
- `shared_ptr(new int)`：**2 次**分配（对象一次，控制块一次）。
- `make_shared`：**1 次**分配（对象和控制块放在一起）。
- 两个 `shared_ptr` 共享时 `use_count = 2`。
- 全部 reset 后，`weak_ptr` 已**过期**（`expired = 1`），`lock()` 返回空指针。
