---
id: pl-cpp-modern-practice-found-intent-keywords
node: cpp.modern-practice
type: qa
step: 3
---
## Q
`enum class`、`override`、`final`、`nullptr`、`explicit`、`= delete`、`[[nodiscard]]` 各把哪种"写在注释里的意图"变成了编译器检查？

## A
这些特性共同点：**多写一个词，把意图交给编译器验证**，全部零运行时成本。

**1. `enum class`（作用域枚举）**。老 `enum` 的枚举值泄漏进外层作用域，并隐式转成整数；`enum class` 不会：

```cpp
enum Color { Red, Green };   int c = Green;      // 编译通过，c == 1
enum class Level { Low, High };  int l = Level::High;
// error: cannot initialize a variable of type 'int' with an rvalue of type 'Level'
```

**2. `override`**。重写虚函数时写了错的参数类型，老写法静默成了一个**新函数**，基类的函数没被重写。写 `override` 后编译器核对：

```cpp
struct Base { virtual void run(int) const; };
struct D : Base { void run(long) const override {} };
// error: non-virtual member function marked 'override' hides virtual member function
```

**3. `final`**：禁止继续派生或重写。`struct G : F {}` 而 `F` 是 `final`：`error: base 'F' is marked 'final'`。也帮助编译器去虚化优化。

**4. `nullptr`**。老写法 `NULL` 是整数 0，会匹配 `int` 重载：本机实测 `f(0)` 调 `f(int)`，`f(nullptr)` 调 `f(char*)`。`nullptr` 有自己的类型，只转成指针。

**5. `explicit`**：禁止单参数构造函数被用于隐式转换，防止 `walk(3)` 悄悄变成 `walk(Meters(3))`。

**6. `= delete`**：显式禁用某个函数，如不可拷贝的类型 `T(const T&) = delete;`，或禁止某个危险重载。使用时报错 `use of deleted function`，比链接错误清楚。

**7. `[[nodiscard]]`**：函数返回值不该被忽略（错误码、`expected`、资源句柄）。忽略时 `warning: ignoring return value of function declared with 'nodiscard' attribute`。标准库的 `std::async`、`std::vector::empty` 已经标了。

**8. `const` 和 `noexcept`**：`const` 成员函数承诺不改对象，`noexcept` 承诺不抛异常。都让接口更精确，并向编译器暴露优化机会。

**对比**：Rust 的 `match` 必须穷尽、`#[must_use]`、默认不可变，是同一思路但**默认开启**；C++ 因为兼容性，这些都是**可选**的，需要你主动写。所以团队规范里常有"所有重写必须标 `override`"，用 `-Wsuggest-override` 或 `clang-tidy` 强制。

**要记住的一点**：在 C++ 里，意图要写出来才有效；凡是能表达意图的关键字都应该默认写上。
