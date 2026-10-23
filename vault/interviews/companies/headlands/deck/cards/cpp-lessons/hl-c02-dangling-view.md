---
id: hl-c02-dangling-view
node: cpp-lessons.c02-references-pointers-const
type: qa
step: 11
---
## Q
```cpp
std::string make_name();              // 返回很长的 string
std::string_view sv = make_name();
std::cout << sv.size();
```
这段代码错在哪？AddressSanitizer 会报什么？

## A
- `make_name()` 返回的临时 `std::string` 在 `;` 处就销毁了，`sv` 指向**已释放的堆内存**，之后读 `sv` 是 use-after-free，Java 不可能出现这种 bug。
- 视图和引用都**不延长**被引用对象的寿命（只有"临时对象绑到 const 引用"才被延长，`string_view` 不算）。
- AddressSanitizer 报：`heap-use-after-free`，`READ of size 1`，并给出 `freed by thread T0 here` 和 `previously allocated by thread T0 here` 两处栈。编译器本身也会警告。
- 修法：用 `std::string s = make_name();` 持有数据，再取视图。
