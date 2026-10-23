---
id: hl-c16-check-macro
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 3
---
## Q
写出自测用的 `CHECK` 和 `CHECK_EQ` 宏。为什么自己写而不用 `assert`？

## A
```cpp
#define CHECK(cond) do { if (!(cond)) { \
    std::cerr << "FAILED line " << __LINE__ << ": " #cond "\n"; std::exit(1); } } while (0)
#define CHECK_EQ(a, b) do { auto va = (a); auto vb = (b); if (!(va == vb)) { \
    std::cerr << "FAILED line " << __LINE__ << ": " #a " == " #b \
              "  (" << va << " vs " << vb << ")\n"; std::exit(1); } } while (0)
```
- `assert` 在定义了 `NDEBUG`（常见于 release/`-O2` 构建配置）时**整个消失**，测试就成了空操作。
- 自己的宏**总是执行**，并且能打印行号和表达式（`__LINE__`、`#cond`）。
