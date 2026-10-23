---
id: hl-cq-q41-value-semantics
node: cpp-questions.j-cross-language
type: qa
step: 9
---
## Q
面试题：C++ 里 `Order b = a;` 做了什么？什么是切片（slicing）？什么是悬空引用？
Value semantics: what does `Order b = a;` do in C++? What is slicing? What's a dangling reference?

## A
- `Order b = a;` **复制**出一个新对象（Java 里是两个名字指同一个对象）；要“别名”得用引用 `Order& r = a`。
- 按值传参会拷贝，所以大对象用 `const T&`。
- **切片**：把派生类对象按值存进基类类型的变量，会丢掉派生部分和多态。
- **悬空**：返回局部变量的引用或指针。
