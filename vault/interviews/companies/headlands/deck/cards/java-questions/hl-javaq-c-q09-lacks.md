---
id: hl-javaq-c-q09-lacks
node: java-questions.c-languages
type: qa
step: 12
---
## Q
和 C++ 相比，Java 没有哪些语言特性，又多了什么？Java 的边界检查会拖慢热循环吗？订单数量累加怎么检测溢出？
Does Java's bounds checking slow down hot loops? How would you detect overflow in an order-quantity accumulation?

## A
- **Java 没有**：指针运算、`const` 正确性、析构函数、多重继承、运算符重载、内联值类型、模板元编程、头文件 / ODR 问题。
- **Java 有**：反射、动态加载、可预测的崩溃（栈追踪）。
- **边界检查会慢吗**：JIT 常把循环里的检查提到循环外消除；剩下的分支预测良好，通常成本很小。不要给具体百分比。
- **订单数量累加防溢出**：`Math.addExact` 抛异常，或用 `long` 加校验。
