---
id: hl-cq-q05-virtual-functions
node: cpp-questions.a-why-fast
type: qa
step: 25
---
## Q
面试题：虚函数是怎么工作的？代价是什么？
How do virtual functions work, and what do they cost?

## A
一句话：每个有虚函数的类有一张**虚表**（vtable），每个对象多一个指向它的**虚指针**（vptr）；虚调用 = 读 vptr → 读表项 → 间接调用。

例：`Shape* p = new Sq(3);`，对象布局是 `[vptr][s=3]`；`p->area()` 就是 load vptr、load slot 0、call indirect。`Sq` 的 vtable 里 slot 0 是 `&Sq::area`，slot 1 是 `&Sq::~Sq`。

代价三条：
- **不能内联**（编译器不知道具体类型）；
- **对象变大**（实测一个 4 字节对象加虚函数后变成 16 字节）；
- **混合类型时间接跳转难预测**。

基类用于多态时，析构函数必须是 `virtual`。
