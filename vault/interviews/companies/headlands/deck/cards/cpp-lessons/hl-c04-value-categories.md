---
id: hl-c04-value-categories
node: cpp-lessons.c04-move-semantics
type: qa
step: 2
---
## Q
面试问：C++ 的左值（lvalue）、右值（rvalue）、右值引用 `T&&` 分别是什么？
Interview question: What are lvalues, rvalues and rvalue references?

## A
- **左值**：有名字、能取地址的表达式，如变量 `a`。
- **右值**：临时的、马上销毁的值，如 `f()` 的返回值、字面量 `5`。
- **右值引用 `T&&`**：只能绑定到右值的引用。重载 `f(const T&)` 和 `f(T&&)`，传临时对象时选后者——这就是"按是否临时来选择复制或移动"的机制。
- 注意：具体类型的 `Buffer&&` 是纯右值引用；而 `template<class T> f(T&&)` 里推导出的 `T&&` 或 `auto&&` 才是**转发引用**（forwarding reference），左右值都能绑。
