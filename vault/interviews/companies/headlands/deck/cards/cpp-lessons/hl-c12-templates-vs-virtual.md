---
id: hl-c12-templates-vs-virtual
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 6
---
## Q
机制三：模板与内联为什么快？对 200 万个形状求面积，虚调用、`variant+visit`、`std::function`、模板各多少 ns/形状？

## A
- 泛型代码在编译期为每个类型生成专门版本，调用点可以**内联**，内联后常量传播、向量化、删除死代码接着发生。
- **虚函数调用是间接调用**，编译器通常看不到目标，无法内联。
- 实测（ns/形状）：虚调用（随机混合）4.04；`variant + visit` 3.70；`std::function` 4.55；**模板，同类型** 0.456。
- 结论：**热路径上用静态多态**（模板、`variant`、按类型分组存放），把虚函数留给冷路径或确实需要运行期扩展的地方。

```cpp
template <class S>
double total_area(const std::vector<S>& v) {
    double t = 0; for (const auto& s : v) t += s.area(); return t;
}
```
