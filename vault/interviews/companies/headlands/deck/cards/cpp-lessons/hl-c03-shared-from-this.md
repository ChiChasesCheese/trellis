---
id: hl-c03-shared-from-this
node: cpp-lessons.c03-smart-pointers
type: qa
step: 11
---
## Q
`shared_ptr<T> a(p); shared_ptr<T> b(p);` 和在成员函数里写 `shared_ptr<T>(this)` 各有什么问题？怎么正确做？

## A
- 用**同一个裸指针**造两个 `shared_ptr`，会各建一个控制块，各自计数到 0 时都 `delete` → **双重释放**。永远从已有的 `shared_ptr` 拷贝，或用 `make_shared`。
- 成员函数里 `shared_ptr<T>(this)` 同样错（新建独立控制块）。正确做法：类继承 `std::enable_shared_from_this`，调用 `shared_from_this()`，它返回共享同一个控制块的 `shared_ptr`。

```cpp
struct Session : std::enable_shared_from_this<Session> {
    std::shared_ptr<Session> self() { return shared_from_this(); }
};
```
