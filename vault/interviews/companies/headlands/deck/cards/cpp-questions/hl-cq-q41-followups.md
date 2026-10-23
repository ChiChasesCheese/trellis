---
id: hl-cq-q41-followups
node: cpp-questions.j-cross-language
type: qa
step: 13
---
## Q
三个追问：C++ 里什么时候会隐式发生拷贝？构造函数上的 `explicit` 做什么？`const T&` 参数绑定到临时对象会怎样？

## A
- **隐式拷贝**：按值传参、按值返回（除非被省略）、赋值、用左值向容器插入、lambda 按值捕获。
- **`explicit`**：禁止通过该构造函数发生隐式转换。
- **`const T&` 绑到临时对象**：允许，并且把临时对象的寿命延长到调用结束。
