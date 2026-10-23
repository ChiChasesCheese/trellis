---
id: hl-c03-raw-pointer-ok
node: cpp-lessons.c03-smart-pointers
type: qa
step: 12
---
## Q
现代 C++ 里什么时候用裸指针或引用是没问题的？

## A
- **借用**：函数参数、遍历中的临时指针、`get()` 取出给 C API。所有权仍在智能指针手里。
- **非拥有的反向指针**：子对象指向肯定比它活得久的父对象（树的 parent、事件源）。
- 性能关键的内部数据结构（侵入式链表、对象池）里自己管理的指针，但应封装在一个类里。
- 总规则：**裸指针不拥有；拥有就用智能指针；不手写 `new`/`delete`**，用 `make_unique`/`make_shared`。
