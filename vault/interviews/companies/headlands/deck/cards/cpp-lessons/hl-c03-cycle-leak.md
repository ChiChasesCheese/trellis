---
id: hl-c03-cycle-leak
node: cpp-lessons.c03-smart-pointers
type: qa
step: 9
---
## Q
两个类互相持有 `shared_ptr` 会怎样？怎么修？和 Java 有什么区别？

## A
- 两个对象互相持有 `shared_ptr`，强计数永远到不了 0，**泄漏**（实测作用域结束后两个节点仍存活）。
- Java 的 tracing GC 能回收环，这是 C++ 的区别。
- 修法：把"向上/反向"的一边改成 `weak_ptr`。

```cpp
struct NodeGood {
    std::shared_ptr<NodeGood> child;   // 父拥有子
    std::weak_ptr<NodeGood> parent;    // 子只观察父
};
```
- 这样作用域结束后新泄漏数为 0。
- 循环引用只能靠设计避免，泄漏检测工具可以报告。
