---
id: hl-c16-trap-size-t
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 13
---
## Q
`for (size_t i = n - 1; i >= 0; --i)` 错在哪？空 vector 的 `v.size() - 1` 是多少？写出安全的倒序循环。

## A
- `size_t` 是**无符号**：`i >= 0` 永远为真；`i` 减到 0 之后回绕到 2^64-1，死循环/越界。`n == 0` 时 `n - 1` 也回绕。
- 空 `vector` 的 `empty.size() - 1` = **18446744073709551615**，不是 -1；转成 `int` 才是 -1。
- 安全倒序：

```cpp
for (std::size_t i = v.size(); i-- > 0;) std::cout << v[i] << ' ';
```
