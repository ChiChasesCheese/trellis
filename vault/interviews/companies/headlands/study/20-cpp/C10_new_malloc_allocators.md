# C10 · `new`/`delete` vs `malloc`/`free`、placement new、分配器与内存池

> 面试原题：*malloc vs new*。目标：说清两者差别，并知道 placement new、自定义分配器、内存池为什么存在（低延迟系统避免热路径上 `malloc`）。

## 1. Java 对照

Java 的 `new Foo()` = 在线程私有分配缓冲区（TLAB）里"指针碰撞"分配 + 跑构造函数，分配极快，回收交给 GC。你无法决定对象放在哪里，也无法单独释放。
C++ 把"拿内存"和"造对象"拆开，并让你完全控制。

## 2. `malloc` vs `new`

| | `malloc` / `free`（C） | `new` / `delete`（C++） |
|---|---|---|
| 做什么 | 只分配**未初始化的字节** | 分配内存（`operator new`）**并调用构造函数** |
| 释放 | `free`：只还内存 | `delete`：先调**析构函数**再还内存 |
| 返回类型 | `void*`，要强转 | 带类型的指针 |
| 大小 | 你算字节数 | 编译器按类型算 |
| 失败 | 返回 `NULL`，必须检查 | 抛 `std::bad_alloc`（`new(std::nothrow)` 返回 `nullptr`） |
| 数组 | 手动 | `new[]` / `delete[]`（记录元素个数以便逐个析构） |
| 可重载 | 否 | `operator new` 可以全局或按类替换 |

要点：`malloc` 出来的内存里**没有对象**，对非平凡类型（`std::string`）使用它是 UB；`free` 不会调析构函数，持有的资源泄漏。**配对规则**：`new`↔`delete`，`new[]`↔`delete[]`，`malloc`↔`free`，不能交叉。

```cpp
std::cout << "[malloc]\n";
void* raw = std::malloc(sizeof(Widget));        // raw bytes only: NO constructor ran
std::cout << "  malloc returned " << (raw ? "non-null" : "null") << ", no ctor message above\n";
// Widget* bad = static_cast<Widget*>(raw); bad->name.size();   // UB: no Widget exists there, name is garbage
std::free(raw);                                 // no destructor either
```

```cpp
std::cout << "[new / delete]\n";
Widget* w = new Widget;                         // operator new(sizeof(Widget)), then Widget::Widget()
std::cout << "  name length " << w->name.size() << "\n";
delete w;                                       // Widget::~Widget(), then operator delete
```

```cpp
std::cout << "[new[] / delete[]]\n";
Widget* arr = new Widget[2];                    // two constructors; the count is remembered for delete[]
delete[] arr;                                   // two destructors (plain delete here would be UB)
```

```cpp
std::cout << "[failure behaviour]\n";
std::size_t huge = static_cast<std::size_t>(-1) / 2;          // about 8 EiB: no machine has it
void* volatile sink = nullptr;                  // storing into a volatile stops the optimiser from deleting the allocation
void* m = std::malloc(huge);
sink = m;
std::cout << "  malloc(8 EiB) -> " << (m ? "non-null" : "NULL (you must check)") << "\n";
try { char* c = new char[huge]; sink = c; delete[] c; std::cout << "  new succeeded?\n"; }
catch (const std::bad_alloc&) { std::cout << "  new char[8 EiB] -> threw std::bad_alloc\n"; }
char* nt = new (std::nothrow) char[huge];                     // nothrow form: returns nullptr like malloc
sink = nt;
void* seen = sink;                                            // read it back so the volatile is used
(void)seen;
std::cout << "  new(std::nothrow) -> " << (nt ? "non-null" : "nullptr") << "\n";
```

```text
WARNING: AddressSanitizer failed to allocate 0x… bytes
WARNING: AddressSanitizer failed to allocate 0x… bytes
[malloc]
  malloc returned non-null, no ctor message above
[new / delete]
  Widget ctor
  name length 35
  Widget dtor
[new[] / delete[]]
  Widget ctor
  Widget ctor
  Widget dtor
  Widget dtor
[failure behaviour]
  malloc(8 EiB) -> NULL (you must check)
  new char[8 EiB] -> threw std::bad_alloc
  new(std::nothrow) -> nullptr
```

（失败演示里替换了全局 `operator new` 来模拟"内存耗尽"：）

```cpp
// operator new is an ordinary replaceable function. Here: refuse absurd sizes the way a real out-of-memory would
// (the sanitizer's own allocator would abort instead of throwing, and we want to show the standard behaviour).
void* operator new(std::size_t n) {
    if (n > (static_cast<std::size_t>(1) << 40)) throw std::bad_alloc();
    if (void* p = std::malloc(n)) return p;
    throw std::bad_alloc();
}
void* operator new[](std::size_t n) { return operator new(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
```

配对错误会被 ASan 抓到：

```cpp
// C10: pairing rules: new/delete, new[]/delete[], malloc/free. Crossing them is UB.
#include <cstdlib>
#include <iostream>

int main() {
    int* a = new int[8];
    delete a;                       // should be delete[] : ASan "alloc-dealloc-mismatch"
    std::cout << "survived the mismatched delete\n";
}
```

```text
ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x…
0x… is located 0 bytes inside of 32-byte region [0x…,0x…)
SUMMARY: AddressSanitizer: alloc-dealloc-mismatch (c10_alloc_mismatch_ub:arm64+0x…) in main+0x1c
```

## 3. `operator new` 与构造的分离：placement new

`new T(args)` 其实是两步：`operator new(sizeof(T))` 取原始内存，然后在那块内存上调用构造函数。**placement new** 只做第二步：`new (地址) T(args)`，在你给的内存上构造对象，**不分配**。对应地，要手动调用析构函数 `p->~T()`（或 C++20 `std::destroy_at`），内存本身由你另行管理。

用途：`vector` 预留容量里在尾部构造元素；`optional`/`variant` 的内部存储；对象池；共享内存里构造对象。

```cpp
class Slot {                                         // a minimal std::optional<Order>
    alignas(Order) unsigned char storage_[sizeof(Order)];   // raw, correctly aligned bytes
    bool live_ = false;
public:
    template <class... A> Order& emplace(A&&... a) {
        Order* p = new (storage_) Order(std::forward<A>(a)...);   // placement new: construct AT this address, no allocation
        live_ = true;
        return *p;
    }
    void reset() {
        if (live_) { std::launder(reinterpret_cast<Order*>(storage_))->~Order(); live_ = false; }   // call the destructor by hand
    }
    Order& get() { return *std::launder(reinterpret_cast<Order*>(storage_)); }
    ~Slot() { reset(); }
};
```

```text
[slot]
  construct 1
  AAPL
  destroy 1
  construct 2
[uninitialized_* algorithms and construct_at]
  construct 10
  construct 11
  destroy 11
  destroy 10
  alignof(Order)=8 sizeof(Order)=32
  destroy 2
```

* 存储必须对齐：`alignas(Order) unsigned char storage_[sizeof(Order)]`。
* 用 `std::launder` 读取（编译器可能假设该地址上的旧对象信息），或保存 `new` 返回的指针。
* `std::construct_at` / `std::destroy_at` 是 C++20 的无裸语法版本。

## 4. 分配器（Allocator）模型

标准容器的第二个模板参数就是分配器：容器所有的内存申请经由 `allocate(n)` / `deallocate(p, n)`。换分配器就能改变内存来源（栈缓冲、arena、共享内存、统计）而不改容器代码。

```cpp
template <class T>
struct CountingAlloc {
    using value_type = T;
    CountingAlloc() = default;
    template <class U> CountingAlloc(const CountingAlloc<U>&) {}       // rebind: node containers allocate other types
    T* allocate(std::size_t n) {
        ++g_allocs; g_bytes += n * sizeof(T);
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) noexcept { ++g_frees; ::operator delete(p); }
    template <class U> bool operator==(const CountingAlloc<U>&) const { return true; }
    template <class U> bool operator!=(const CountingAlloc<U>&) const { return false; }
};
```

```text
vector of 1000 push_backs: 11 allocations, 8188 bytes requested in total
after destruction: allocs=11 frees=11
list of 1000 push_backs  : 1000 allocations (one per node), 24000 bytes
vector with reserve(1000): 1 allocation
```

输出直接解释了「为什么 `reserve` 重要」和「为什么 `list` 慢」：`vector` 1000 次 `push_back` 只做了 11 次分配，`list` 做了 1000 次（每节点一次）。

C++17 的 `std::pmr`（polymorphic memory resources）：分配器类型固定为 `polymorphic_allocator`，运行期选择 `memory_resource`（如 `monotonic_buffer_resource` 使用给定缓冲区）。

## 5. 内存池与 arena

`malloc` 通用但有代价：找合适的空闲块、元数据、多线程时的锁或线程缓存、碎片化，延迟不稳定。交易系统的热路径常常**根本不调用 `malloc`**，而是启动时一次性分配，然后：

* **Arena / bump allocator**：分配 = 指针前移；不单独释放；`reset()` 一次性回收全部。适合"一个请求/一个批次"生命周期一致的对象。
* **固定大小对象池（free list）**：预先切成相同大小的槽，空闲槽用自己的存储串成链表；分配/释放都是 O(1)，无碎片，满了就明确失败（由调用者决定），不会悄悄去 `malloc`。

```cpp
// Bump allocator: allocation = move a pointer; free = nothing; reset() = free everything at once.
class Arena {
    unsigned char* base_;
    std::size_t cap_, used_ = 0;
public:
    explicit Arena(std::size_t cap) : base_(static_cast<unsigned char*>(std::malloc(cap))), cap_(cap) {}
    ~Arena() { std::free(base_); }
    Arena(const Arena&) = delete;
    Arena& operator=(const Arena&) = delete;
    void* allocate(std::size_t n, std::size_t align = alignof(std::max_align_t)) {
        std::size_t p = (used_ + align - 1) & ~(align - 1);            // round up to the alignment
        if (p + n > cap_) return nullptr;                              // a real arena would chain another block
        used_ = p + n;
        return base_ + p;
    }
    void reset() { used_ = 0; }
};
```

```cpp
// Fixed-size pool: slots threaded into a free list stored INSIDE the free slots. O(1) alloc/free, no fragmentation.
template <class T, std::size_t N>
class Pool {
    union Slot { Slot* next; alignas(T) unsigned char bytes[sizeof(T)]; };
    Slot slots_[N];
    Slot* free_ = nullptr;
public:
    Pool() { for (std::size_t i = N; i-- > 0;) { slots_[i].next = free_; free_ = &slots_[i]; } }
    template <class... A> T* create(A&&... a) {
        if (!free_) return nullptr;                                    // pool exhausted: caller decides (no hidden malloc)
        Slot* s = free_; free_ = s->next;
        return new (s->bytes) T{std::forward<A>(a)...};
    }
    void destroy(T* p) {
        p->~T();
        Slot* s = reinterpret_cast<Slot*>(p);
        s->next = free_; free_ = s;
    }
};
```

对一批 256 个 64 字节订单的创建/销毁（每个对象的耗时）：

```text
create and destroy 256 Orders per round, 200000 rounds
  new / delete          : 6.81861 ns per create+destroy (sink 0)
  fixed pool (free list): 1.77473 ns per create+destroy (sink 0)
  bump arena + reset    : 0.767253 ns per create+destroy (sink 0)
  pmr monotonic + vector: 2.09299 ns per create+destroy (sink 0)
```

读法：热缓存、单线程下 `new/delete` 已经只要几纳秒，池再快 3–4 倍，arena 最快（释放是 O(1) 的一次 `reset`）；真正的收益在**尾部延迟**（没有偶发的慢分配/系统调用）、**多线程无争用**和**缓存局部性**（对象紧挨着）。

## 6. 坑

1. `new[]` 配 `delete`（缺 `[]`）= UB。
2. 手动 `delete` 后继续用指针 / 再次 `delete`（置 `nullptr` 只缓解）；所以用智能指针。
3. 在 `malloc` 的内存上直接当对象用（没有构造）。
4. placement new 用未对齐的缓冲区。
5. 忘记调用析构函数导致资源泄漏。
6. `new` 抛异常时构造函数部分完成的对象：成员 RAII 保证无泄漏。
7. 池/arena 中对象的指针在 `reset` 后悬空。
8. 自定义分配器要满足 rebind 和相等性比较。

## 7. 面试官接着会问

**Q：`malloc` 和 `new` 的区别？**
要点：第 2 节表格；核心一句：`new` = 分配 + 构造，`delete` = 析构 + 释放；`malloc` 只管字节。

**Q：`new` 失败怎么办？**
要点：抛 `bad_alloc`；`nothrow` 版本返回空；可设置 `new_handler`；工业代码常在启动时预分配、运行期不分配。

**Q：`delete` 和 `delete[]` 的区别？**
要点：`new[]` 在分配块里记录元素数，`delete[]` 据此逐个析构；用错 UB。

**Q：placement new 是什么？什么时候用？**
要点：在已有内存上构造对象，不分配；容器内部、池、共享内存；需要手动析构和对齐。

**Q：为什么低延迟系统不用 `malloc`？**
要点：延迟不确定、可能锁/系统调用（`mmap`/缺页）、碎片、缓存局部性差；用预分配的池/arena，分配 O(1) 且可预测。

**Q：`operator new` 能自定义吗？**
要点：可全局替换或为某个类重载，常用于统计/池化/调试。

**Q：与 Java 对比？**
要点：Java 分配快（TLAB 指针碰撞）、回收由 GC；代价在 GC 暂停与对象头/指针；C++ 分配可以更慢但完全可控，也能完全避免。

## 8. 自测

1. 对 `std::string` 用 `malloc(sizeof(std::string))` 然后 `s->append("x")` 会怎样？
2. `delete` 做哪两件事，顺序是什么？
3. 为什么池在满时返回 `nullptr` 而不是去 `malloc`？
4. placement new 创建的对象，谁来调用析构函数？

<details><summary>答案</summary>

1. UB：没有构造，`string` 内部指针/长度是垃圾。
2. 先调析构函数，再 `operator delete` 归还内存。
3. 热路径不允许出现不可预测的延迟；容量不足是需要调用者显式处理的状态（背压/丢弃/告警）。
4. 你自己（`p->~T()` 或 `std::destroy_at`），内存也由你管理。

</details>
