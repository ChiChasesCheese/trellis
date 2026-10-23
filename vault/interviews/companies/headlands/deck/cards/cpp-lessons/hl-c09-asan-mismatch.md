---
id: hl-c09-asan-mismatch
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 12
---
## Q
```cpp
int* a = new int[8];
delete a;
```
这是什么错误？ASan 怎么报？

## A
- `new[]` 配了 `delete`（缺 `[]`）：**UB**。`new[]` 在分配块里记录元素数，`delete[]` 据此逐个析构，用错不匹配。
- ASan 报：`alloc-dealloc-mismatch (operator new [] vs operator delete)`。
- 配对规则：`new`↔`delete`，`new[]`↔`delete[]`，`malloc`↔`free`，不能交叉。
