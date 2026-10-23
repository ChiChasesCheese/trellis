---
id: hl-c11-copy-nontrivial
node: cpp-lessons.c11-copy-vs-memcpy
type: qa
step: 6
---
## Q
```cpp
std::vector<std::string> src{...}, dst(2);
std::copy(src.begin(), src.end(), dst.begin());
std::memcpy(dst.data(), src.data(), 2 * sizeof(std::string));
```
这两行各是什么结果？为什么？

## A
- `std::copy`：**正确**。对每个元素调用 `std::string::operator=`，目标得到独立副本，`src` 不变。
- `memcpy`：**错**。把两个 `string` 内部的指针按位复制，两个字符串共享同一堆缓冲区；各自析构时都 `free` → **double free**。
- AddressSanitizer 报：`attempting double-free`。
- 对 `std::vector<T>`、`std::string` 对象本身 `memcpy`，拷贝的只是它们内部的指针。
