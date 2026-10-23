---
id: hl-c03-virtual-dtor-poly
node: cpp-lessons.c03-smart-pointers
type: qa
step: 5
---
## Q
用 `std::vector<std::unique_ptr<Shape>>` 存多态对象时，`Shape` 基类必须满足什么？为什么？写出基类骨架。

## A
基类必须有**虚析构函数**。否则通过基类指针删除派生对象是**未定义行为**（只调用基类析构，派生部分的资源不释放）。

```cpp
struct Shape {
    virtual ~Shape() = default;
    virtual double area() const = 0;
};
struct Sq : Shape {
    double s;
    explicit Sq(double x) : s(x) {}
    double area() const override { return s * s; }
};
```
- `unique_ptr<Shape>` 能装 `make_unique<Sq>(2)`，容器里放的是指针，所有权清晰。
- `unique_ptr` 不可拷贝，所以 `vector<unique_ptr<T>>` 只能移动：用 `push_back(std::make_unique<T>())` 或 `push_back(std::move(p))`。
