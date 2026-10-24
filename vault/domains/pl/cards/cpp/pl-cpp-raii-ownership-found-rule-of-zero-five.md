---
id: pl-cpp-raii-ownership-found-rule-of-zero-five
node: cpp.raii-ownership
type: qa
step: 3
---
## Q
零法则（rule of zero）、三法则（rule of three）、五法则（rule of five）各是什么？一个直接管理 `new[]` 内存的类忘了写拷贝函数会怎样？

## A
**背景**：编译器会自动生成 5 个特殊成员函数：析构、拷贝构造、拷贝赋值、移动构造、移动赋值。自动生成的拷贝是**逐成员拷贝**。如果成员是一个裸指针，拷贝的只是指针值，不是它指向的内存。

**最小复现**：

```cpp
struct Name {
  char* s;
  explicit Name(const char* t) : s(new char[strlen(t) + 1]) { strcpy(s, t); }
  ~Name() { delete[] s; }
};
Name a("alice"); Name b = a;   // 两个对象的 s 指向同一块内存
```

作用域结束时 `b` 和 `a` 各自 `delete[] s`。带 ASan 运行的真实报错：`AddressSanitizer: attempting double-free on 0x602000000910`。

**三个法则**：
1. **三法则**（C++98）：如果一个类需要自定义析构函数、拷贝构造函数、拷贝赋值之一，通常**三个都需要**。因为自定义析构意味着它持有需要手动释放的资源，拷贝就必须决定怎样复制（深拷贝）或禁止。
2. **五法则**（C++11）：再加上移动构造和移动赋值。只写拷贝不写移动，对象永远只能拷贝，性能退化。
3. **零法则**：**尽量不写其中任何一个**。成员全用 `std::string`、`std::vector`、`std::unique_ptr` 这类自己管理资源的类型，编译器自动生成的 5 个函数就是正确的。上例只要把 `char*` 换成 `std::string` 就修好了，还少了 8 行代码。

**如何选**：
- 业务类：零法则。
- 封装一个裸资源（文件描述符、GPU 句柄、C 库对象）的小类：五法则，只写这一个小类，其他类依旧遵守零法则。
- 不想允许拷贝：`= delete` 拷贝函数。

**要记住的一点**：好的 C++ 代码里，手写析构函数的类很少，它们是“资源包装器”，数量越少越好。
