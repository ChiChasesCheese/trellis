---
id: hl-c01-temporary-lifetime
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 6
---
## Q
临时对象（temporary）什么时候销毁？`const T& r = T(...)` 会怎样？`v.push_back(Tracer("tmp"))` 为什么会多打印一次 copy？

## A
- 临时对象默认在**完整表达式结束（`;`）**时销毁。
- 把临时对象绑定到 `const T&` 局部引用，其寿命被**延长**到该引用的作用域结束。
- `push_back(Tracer("tmp"))` 打印了 `copy tmp -> tmp'`：类 `Tracer` **自己声明了拷贝构造和析构函数**，编译器就不再自动生成移动构造（移动 = 直接"偷走"临时对象的内部资源而不复制）。于是临时对象被**复制**进 `vector`，然后原临时对象在 `;` 处析构。
- 引用和视图都不会延长普通对象的寿命，只有「临时对象绑到 const 引用」这个特例会。
