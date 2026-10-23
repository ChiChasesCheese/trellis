---
id: hl-cq-q14-script
node: cpp-questions.c-memory-ownership
type: qa
step: 25
---
## Q
用英文 60 秒回答：What is move semantics? What does `std::move` really do? When does the compiler elide copies?

## A
结构：移动 = 偷资源，moved-from 有效但未指定 → `move` 只是转型，对 `const` 退化为拷贝 → `noexcept` 与 `vector` 扩容（7 次移动对 7 次拷贝）→ 不要 `return std::move(x)`、C++17 保证省略 → 零法则/五法则。

- **Move semantics** transfer a resource from a temporary or dying object instead of copying: the move constructor steals the pointer and nulls the source. Moved-from objects are **valid but unspecified**.
- **`std::move` is just a cast to an rvalue reference** - it moves nothing itself. Moving from a `const` object silently falls back to a copy; I checked: the source stayed full.
- Mark move operations **`noexcept`**: `vector` growth only moves if the move can't throw, otherwise it copies. In my test it was 7 moves versus 7 copies for 8 elements.
- Return locals **by value without `std::move`**: since C++17, returning a temporary involves no copy at all, and `return std::move(x)` actually blocks elision - the compiler warns about it.
- Rule of Zero where possible, Rule of Five when I own a resource.
