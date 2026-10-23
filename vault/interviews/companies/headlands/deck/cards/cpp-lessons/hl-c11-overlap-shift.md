---
id: hl-c11-overlap-shift
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 5
---
## Q
对 `{1,2,3,4,5,6,7,8}` 要把前 5 个元素右移 2 位、以及把 `[2,n)` 左移 2 位，分别用什么？结果是什么？

## A
```cpp
std::memmove(v.data() + 2, v.data(), 5 * sizeof(int));       // 右移，重叠安全
std::copy_backward(w.begin(), w.begin() + 5, w.begin() + 7); // 右移，目标在源之后
std::copy(u.begin() + 2, u.end(), u.begin());                // 左移，目标在源之前
```
- 右移后两者都得 `1 2 1 2 3 4 5 8`；左移后得 `3 4 5 6 7 8 7 8`。
- 规则：`std::copy` 要求 `d_first` 不在 `[first, last)` 内：**目标在源之前**用 `std::copy`，**目标在源之后且重叠**用 `copy_backward`，否则是 UB。
