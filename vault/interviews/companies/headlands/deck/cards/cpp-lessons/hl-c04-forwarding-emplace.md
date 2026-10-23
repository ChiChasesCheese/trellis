---
id: hl-c04-forwarding-emplace
node: cpp-lessons.c04-move-semantics
type: qa
step: 12
---
## Q
转发引用（forwarding reference）和 `std::forward` 做什么？`emplace_back` 为什么能省临时对象？

## A
```cpp
template <class... Args>
void emplace(Args&&... args) {
    items.emplace_back(std::forward<Args>(args)...);
}
```
- 模板里推导出的 `Args&&` 能绑定左值也能绑定右值；`std::forward<Args>(args)...` **原样保持**每个实参"是左值还是右值"。
- `emplace_back(args...)` 靠它把构造参数转发给元素构造函数，**在 `vector` 内存里直接构造**对象，不先造临时对象。
- 注意：`emplace_back(Trade("A",1,1.0))` 传的是已构造的临时对象，仍然先造临时对象再移动；好处只在传**构造参数**时：`emplace_back("A", 1, 1.0)`。
