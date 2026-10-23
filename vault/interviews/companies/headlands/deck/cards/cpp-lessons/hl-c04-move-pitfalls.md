---
id: hl-c04-move-pitfalls
node: cpp-lessons.c04-move-semantics
type: qa
step: 16
---
## Q
C++ 移动语义有哪六个常见的坑？

## A
1. **使用被移动后的对象**：`std::move(s)` 之后读 `s` 的值是逻辑错误（不是 UB，但内容未指定）。
2. **给 `const` 对象 `std::move`**：绑不上移动构造，静默退化为拷贝。
3. **移动操作忘记 `noexcept`**：`vector` 扩容退回拷贝。
4. **移动赋值不处理自赋值**：`a = std::move(a)` 可能先释放自己再读自己。
5. **对基础类型 `std::move` 没有意义**：`int` 移动 = 拷贝。
6. **手写资源管理类**而不是组合标准库类型；Rule of 0 能避免上面全部。
