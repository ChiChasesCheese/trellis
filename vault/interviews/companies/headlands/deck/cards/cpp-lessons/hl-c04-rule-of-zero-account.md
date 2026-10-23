---
id: hl-c04-rule-of-zero-account
node: cpp-lessons.c04-move-semantics
type: qa
step: 10
---
## Q
```cpp
struct Account {
    std::string name;
    std::vector<int> history;
    std::unique_ptr<int> secret = std::make_unique<int>(7);
};
```
这个类没写任何特殊成员函数，它能拷贝吗？能移动吗？怎么在编译期验证？

## A
- **不能拷贝**：`unique_ptr` 成员删除了拷贝，整个类自动成为只能移动（move-only）的类型。
- **能移动，且不抛异常**：每个成员的移动都是 `noexcept`。
- 验证：
```cpp
static_assert(std::is_nothrow_move_constructible_v<Account>);
static_assert(!std::is_copy_constructible_v<Account>);
```
- 这是 Rule of 0 的样板：成员各自管理自己，编译器生成的全是对的。
