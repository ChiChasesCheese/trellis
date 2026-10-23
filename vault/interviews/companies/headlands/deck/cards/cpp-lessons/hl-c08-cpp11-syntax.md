---
id: hl-c08-cpp11-syntax
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 2
---
## Q
C++11 加了哪些语法层面的特性？各解决什么问题？

## A
- `auto`、范围 `for`、`nullptr`、`enum class`、`using` 别名：少写样板；**`nullptr` 修复 `0`/`NULL` 的重载歧义**；强类型枚举不泄漏名字、不隐式转 `int`；`using` 别名还能模板化。
- 统一初始化 `{}`、`initializer_list`：统一构造语法，**禁止窄化**。
- `override` / `final`、`= default` / `= delete`：让编译器检查重写；显式控制特殊成员函数。
- 可变参数模板、`static_assert`、`constexpr`（单语句）：通用库（`tuple`、`make_shared`）、编译期检查。
- lambda：就地写回调/谓词，配合算法。
- 用户定义字面量、原始字符串字面量：单位、正则。

```cpp
enum class Side : char { Buy, Sell };
template <class T> using Vec = std::vector<T>;   // alias template，typedef 做不到
struct Derived final : Base { int f() const override { return 2; } };
```
