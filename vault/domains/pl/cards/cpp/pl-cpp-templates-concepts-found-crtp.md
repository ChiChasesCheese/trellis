---
id: pl-cpp-templates-concepts-found-crtp
node: cpp.templates-concepts
type: qa
step: 5
---
## Q
CRTP 是什么？它怎样用模板实现"静态多态"（static polymorphism），与虚函数相比换来什么？C++23 的 `deducing this` 又改变了什么？

## A
**多态的两种实现**：
- **动态多态**：基类声明 `virtual` 函数，对象带一个虚表指针（vptr），调用在运行时通过虚表间接跳转。
- **静态多态**：在编译期决定调用哪个函数，没有间接跳转，可以被内联。

**CRTP**（Curiously Recurring Template Pattern，奇异递归模板模式）：派生类把**自己**作为模板实参传给基类，基类就能在编译期静态转换成派生类，调用派生类的函数：

```cpp
template <class D> struct ShapeC {
  double area() const { return static_cast<const D*>(this)->area_impl(); }
};
struct SqC : ShapeC<SqC> { double s; double area_impl() const { return s * s; } };
```

调用 `SqC{}.area()` 时，`ShapeC<SqC>::area` 直接调用 `SqC::area_impl`，这个调用在编译期解析，可内联。

**换来什么**（本机实测）：
1. **没有虚表指针**：含一个 `double` 的虚函数版本 `sizeof` 为 16 字节，CRTP 版本为 8 字节。
2. **没有间接调用**：可以内联，后续优化（向量化、常量折叠）才有机会。
3. 缺点：**无法放进同一个 `vector<Base*>` 混用**，因为 `ShapeC<SqC>` 与 `ShapeC<CiC>` 是毫无关系的不同类型；编译时间和代码体积增加。

**`deducing this`（C++23）**：成员函数可以显式声明"调用者本身"的类型参数：

```cpp
struct Base { template <class Self> double area(this Self&& self) { return self.impl(); } };
struct Sq : Base { double impl() const { return 4.0; } };   // Sq{}.area() 输出 4
```

不再需要把派生类作为模板实参传给基类，CRTP 的大部分用途被一个普通继承加显式 `this` 参数取代，写法更直白，错误信息也更清楚。

**选哪个**：需要在运行时存放异构对象（插件、UI 控件树）用虚函数；性能关键、类型在编译期已知（数值库、容器适配器）用静态多态。

**要记住的一点**：静态多态把"选哪个实现"这件事挪到编译期，代价是失去运行时的异构性。
