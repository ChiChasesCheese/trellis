---
id: hl-cq-q14-move-from-const
node: cpp-questions.c-memory-ownership
type: qa
step: 20
---
## Q
对一个 `const` 对象调用 `std::move` 再初始化新对象，会移动还是拷贝？为什么？

## A
- **会拷贝。** `std::move` 只是转型，`const` 对象转出来是 `const` 右值引用，移动构造函数需要非 const 引用，绑不上，只能退回拷贝构造。
- 实测：从 `const` 移动后 `c.size()=40`，源对象仍然是满的，说明它被拷贝了。
