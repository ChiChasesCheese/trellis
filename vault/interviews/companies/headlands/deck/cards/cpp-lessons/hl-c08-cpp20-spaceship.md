---
id: hl-c08-cpp20-spaceship
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 11
---
## Q
C++20 的三路比较 `<=>`（spaceship）怎么用？写出让 `Version` 结构体拥有全部比较运算符的一行代码。

## A
```cpp
struct Version {
    int major, minor, patch;
    auto operator<=>(const Version&) const = default;
};
```
- 这一行按成员**字典序**生成 `<`、`<=`、`>`、`>=`、`==`、`!=` 六个运算符。
- 例：`Version{1,2,3} < Version{1,10,0}` 为 true，`==` 为 false。
- 解决的痛点：比较运算符样板。
