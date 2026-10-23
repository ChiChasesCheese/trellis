---
id: hl-c01-value-semantics-perf
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 15
---
## Q
面试问：C++ 的值语义对性能有什么影响？
Interview question: How does value semantics affect performance in C++?

## A
要点：
- **连续布局**：成员和数组元素直接嵌在一起，遍历对缓存友好。
- **没有对象头和间接寻址**：不像 Java 每个对象有 12–16 字节头、通过引用跳转。
- **复制成本是显式的**：按值传大对象会深拷贝，需要用 `const T&`、移动（move）或指针避免；这是代价，也是可控性。
- 对象销毁确定，无 GC 停顿。
