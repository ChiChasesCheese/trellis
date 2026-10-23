---
id: hl-c07-function-template
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 2
---
## Q
写出一个函数模板 `clamp_to(v, lo, hi)`。编译器怎么确定 `T`？推导不出时怎么办？模板的定义为什么必须放在头文件里？

## A
```cpp
template <typename T>
T clamp_to(T v, T lo, T hi) { return v < lo ? lo : (v > hi ? hi : v); }
```
- 编译器根据实参**推导** `T`：`clamp_to(15, 0, 10)` → `T=int`。
- 推导不出（实参类型不一致）时**显式指定**：`clamp_to<long>(3, 5, 9)`。
- 每个用到的类型实例化一份。
- **模板定义必须在头文件/同一个文件里**，因为实例化时编译器要看到完整代码；这也是模板的定义要对所有使用它的翻译单元可见（ODR/头文件）的原因。
