---
id: hl-c09-strict-aliasing
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 9
---
## Q
什么是严格别名（strict aliasing）规则？`float f; int i = *(int*)&f;` 有什么问题？怎么写才对？

## A
- 规则：除少数例外（`char` / `unsigned char` / `std::byte`），通过**不相容类型**的指针读写同一块内存是 UB。
- 编译器因此认为 `int*` 和 `float*` 不会指向同一处，可以不重新读取。实测 `store_both(int* i, float* f)`：先 `*i = 1`，再 `*f = 2.0f`，返回 `*i`——编译器直接返回常量 1，不重新读内存，而字面理解应是 1073741824。
- 正确的按位重解释：

```cpp
std::uint32_t bits_memcpy(float f) { std::uint32_t u; std::memcpy(&u, &f, sizeof u); return u; } // 编译成一条 mov
std::uint32_t bits_cast(float f)   { return std::bit_cast<std::uint32_t>(f); }                  // C++20
```
- `*reinterpret_cast<uint32_t*>(&f)` 是 UB。
