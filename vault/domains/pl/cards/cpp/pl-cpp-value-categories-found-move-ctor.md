---
id: pl-cpp-value-categories-found-move-ctor
node: cpp.value-categories
type: qa
step: 4
---
## Q
一个持有堆内存的类，移动构造函数里具体做什么？为什么移动的成本与对象大小无关？

## A
**移动构造函数**接收一个右值引用，把源对象内部的资源（指针、句柄）**转交**给新对象，再把源对象留在一个能安全析构的状态（通常是空指针）。没有分配，没有逐字节复制。

```cpp
struct Buf {
  char* p; size_t n;
  Buf(const Buf& o) : p(new char[o.n]), n(o.n) { memcpy(p, o.p, n); }
  Buf(Buf&& o) noexcept
    : p(std::exchange(o.p, nullptr)), n(std::exchange(o.n, 0)) {}
  ~Buf() { delete[] p; }
};
```

运行 `Buf b = a;` 会打印 `copy 1000000 bytes`（分配 1 MB 并复制）；`Buf c = std::move(a);` 只打印 `move: steal pointer`，之后 `a.p == nullptr`、`c.n == 1000000`。

**为什么成本与大小无关**：移动只复制两个机器字（指针与长度），不管缓冲区是 1 KB 还是 1 GB。拷贝则是 O(n) 的分配加复制。

**为什么要把源对象置空**：源对象之后仍会被析构。如果两个对象都指向同一块内存，两次 `delete[]` 就是 double free。`delete[] nullptr` 是安全的空操作，所以“置空”就是让源对象析构时什么也不做。

**哪些类型的移动不便宜**：没有堆资源的类型，移动和拷贝一样（`int` 的移动就是拷贝）；`std::array<int, 1000>` 的数据直接在对象里，移动是逐元素复制，仍是 O(n)；`std::vector` 和 `std::string`（超过小串优化阈值）的移动是 O(1)。

**要记住的一点**：移动语义的收益来自“资源在堆上、对象里只有句柄”这一结构；对象里直接内嵌大数据的类型，移动不会更快。
