# C03 · 智能指针：`unique_ptr`、`shared_ptr`、`weak_ptr`

> 目标：知道现代 C++ 里**几乎不写 `new`/`delete`**，所有权由类型表达；能回答 `shared_ptr` 的控制块、开销、循环引用，以及什么时候裸指针没问题。

## 1. Java 里是怎样的

所有对象都由 GC 管理，"谁拥有对象"这个问题不存在——引用够多就活着，没人引用就回收。代价是回收时机不可预测，文件、锁等资源释放要另想办法（try-with-resources）。

## 2. C++ 为什么需要智能指针

堆对象不会自动回收。裸指针 `T*` 看不出：这个指针是**拥有**对象（要负责 `delete`），还是只是**借用**？谁释放、释放几次？答错就是泄漏或双重释放。智能指针把所有权写进类型，用 RAII（资源绑定到对象寿命，析构函数自动释放）自动释放：

| 类型 | 所有权 | 大小 | 拷贝 | 典型场景 |
|---|---|---|---|---|
| `unique_ptr<T>` | 唯一拥有者 | 一个指针（零额外开销） | **禁止**，只能移动 | 默认选择；工厂返回；容器里放多态对象 |
| `shared_ptr<T>` | 多个共同拥有，引用计数归零时释放 | 两个指针（对象 + 控制块） | 原子加 1 | 真的有多个拥有者、生命周期不好确定 |
| `weak_ptr<T>` | 不拥有，只观察 `shared_ptr` | 两个指针 | 弱计数加 1 | 打破循环引用、缓存、观察者 |
| `T*` / `T&` | **不拥有**，只借用 | 一个指针 | 随便 | 函数参数、非拥有的反向指针 |

## 3. `unique_ptr`

```cpp
std::unique_ptr<Order> make_order(int id) {          // returning transfers ownership to the caller
    return std::make_unique<Order>(id);              // make_unique: one expression, exception safe
}

void inspect(const Order* o) {                       // raw pointer = "borrowing, I do not own it, may be null"
    std::cout << "  inspecting " << (o ? o->id : -1) << "\n";
}
void inspect_ref(const Order& o) { std::cout << "  inspecting ref " << o.id << "\n"; }   // better: cannot be null
void consume(std::unique_ptr<Order> o) {             // by value = "I take ownership"
    std::cout << "  consuming " << o->id << "\n";
}                                                    // destroyed here
```

```cpp
void sizes() {
    std::cout << "  sizeof(Order*)=" << sizeof(Order*) << " sizeof(unique_ptr<Order>)=" << sizeof(std::unique_ptr<Order>)
              << " sizeof(shared_ptr<Order>)=" << sizeof(std::shared_ptr<Order>) << "\n";
}
```

```cpp
struct FileCloser { void operator()(std::FILE* f) const { if (f) std::fclose(f); } };
using FilePtr = std::unique_ptr<std::FILE, FileCloser>;   // custom deleter in the type: still pointer-sized
```

```cpp
struct Shape { virtual ~Shape() = default; virtual double area() const = 0; };   // virtual dtor is REQUIRED
struct Sq : Shape { double s; explicit Sq(double x) : s(x) {} double area() const override { return s * s; } };
struct Circ : Shape { double r; explicit Circ(double x) : r(x) {} double area() const override { return 3.14159 * r * r; } };
```

所有权的转移（`std::move` 之后 `a` 为空）：

```cpp
auto a = make_order(1);
inspect(a.get());            // get() hands out the raw pointer; the unique_ptr keeps ownership
inspect_ref(*a);
// auto b = a;               // does not compile: copying would mean two owners
auto b = std::move(a);       // ownership moves; a is now empty
std::cout << "  a is " << (a ? "full" : "null") << ", b->id=" << b->id << "\n";
consume(std::move(b));
```

输出：

```text
[ownership]
  Order 1 created
  inspecting 1
  inspecting ref 1
  a is null, b->id=1
  consuming 1
  Order 1 destroyed
[after consume]
[container of owners]
  Order 10 created
  Order 11 created
  Order 10 destroyed
  left: 1
[sizes]
  sizeof(Order*)=8 sizeof(unique_ptr<Order>)=8 sizeof(shared_ptr<Order>)=16
[custom deleter]
[polymorphism]
  total area 7.14159
[end of main]
  Order 11 destroyed
```

* 函数**返回** `unique_ptr` = 把所有权交给调用者；函数**按值接收** `unique_ptr` = 取得所有权（调用者要 `std::move`）；**只想用一下**就传 `const T&`/`const T*`，不要传 `unique_ptr`。
* 拷贝被删除，所以「两个拥有者」在编译期就报错。移动后源对象为空。
* 自定义删除器（deleter）放在类型里，能管理任何需要特殊释放的资源（`FILE*`、句柄）。
* 多态：基类必须有**虚析构函数**，否则通过基类指针删除派生对象是 UB。

## 4. `shared_ptr` 的内部：控制块（control block）

`shared_ptr` 由两个指针构成：一个指向对象，一个指向**控制块**——堆上一小块，存放**强引用计数**、**弱引用计数**、删除器和（`make_shared` 时）对象本身。拷贝 `shared_ptr` = 对强计数做**原子**加 1，析构 = 原子减 1，减到 0 才销毁对象。

```cpp
void count_allocations() {
    int before = g_allocs;
    { std::shared_ptr<Payload> p(new Payload{}); }              // 1: the Payload, 2: the control block
    std::cout << "  shared_ptr(new T):  " << g_allocs - before << " allocations\n";
    before = g_allocs;
    { auto p = std::make_shared<Payload>(); }                   // object and control block in ONE block
    std::cout << "  make_shared<T>():   " << g_allocs - before << " allocation\n";
    before = g_allocs;
    { auto p = std::make_unique<Payload>(); }
    std::cout << "  make_unique<T>():   " << g_allocs - before << " allocation, no control block\n";
}
```

```cpp
void use_counts() {
    auto sp = std::make_shared<std::string>("quote");
    std::weak_ptr<std::string> wp = sp;                         // observes; does not keep it alive
    std::cout << "  use_count=" << sp.use_count() << " weak expired=" << wp.expired() << "\n";
    {
        auto sp2 = sp;                                          // atomic increment of the strong count
        std::cout << "  use_count=" << sp.use_count() << "\n";
    }
    if (auto locked = wp.lock()) std::cout << "  lock() ok: " << *locked << "\n";   // upgrade, atomically
    sp.reset();
    std::cout << "  after reset: expired=" << wp.expired() << ", lock() null=" << (wp.lock() == nullptr) << "\n";
}
```

```text
sizeof(shared_ptr<Payload>)=16 (object pointer + control-block pointer)
[allocations]
  shared_ptr(new T):  2 allocations
  make_shared<T>():   1 allocation
  make_unique<T>():   1 allocation, no control block
[counts]
  use_count=1 weak expired=0
  use_count=2
  lock() ok: quote
  after reset: expired=1, lock() null=1
[cycles]
  cycle with shared_ptr both ways: alive after scope = 2 (leaked)
  with weak_ptr back-pointer: newly leaked = 0
[enable_shared_from_this] use_count=1 before, same object: 1
```

* `make_shared<T>()` 把对象和控制块放在**一次**分配里（更快、更省、缓存更友好）；`shared_ptr<T>(new T)` 是两次分配。缺点：只要还有 `weak_ptr`，整块内存（包括已析构的对象占的空间）不能回收。
* 计数是原子的，所以引用计数本身线程安全；**指向的对象**不会因此线程安全。

### 开销

```cpp
struct Session : std::enable_shared_from_this<Session> {       // hand out shared_ptr to *this safely
    std::shared_ptr<Session> self() { return shared_from_this(); }
};
```

拷贝一个 `shared_ptr` 是一次原子操作；多个线程拷贝同一个 `shared_ptr` 会争抢同一条缓存线上的计数器：

```text
single thread:
  raw pointer          : 0.882377 ns/op
  shared_ptr const&    : 0.882196 ns/op
  shared_ptr by value  : 3.07456 ns/op
4 threads copying the SAME shared_ptr (one control block, contended atomic counter):
  total wall 501.093 ms for 20000000 copies (100.219 ns per copy per thread)
(sink=80000000)
```

读法：传 `const shared_ptr&` 与传裸指针几乎一样快；**按值传**（每次一对原子加减）慢了几倍；多线程争抢同一个控制块时每次拷贝可达上百纳秒。结论：`shared_ptr` 作参数时传 `const&`，或者干脆传 `T&`；热路径避免到处拷贝 `shared_ptr`。

## 5. `weak_ptr` 与循环引用

两个对象互相持有 `shared_ptr`，计数永远到不了 0——泄漏。（Java 的 GC 能回收环，这是 C++ 的区别。）把"向上/反向"的一边改成 `weak_ptr`：

```cpp
static int g_alive = 0;
struct NodeBad {                       // parent <-> child both shared_ptr: a cycle nobody can free
    std::shared_ptr<NodeBad> other;
    NodeBad() { ++g_alive; }
    ~NodeBad() { --g_alive; }
};
struct NodeGood {                      // child holds a weak_ptr back to its parent
    std::shared_ptr<NodeGood> child;
    std::weak_ptr<NodeGood> parent;
    NodeGood() { ++g_alive; }
    ~NodeGood() { --g_alive; }
};

void cycles() {
    {
        auto a = std::make_shared<NodeBad>();
        auto b = std::make_shared<NodeBad>();
        a->other = b; b->other = a;
    }
    std::cout << "  cycle with shared_ptr both ways: alive after scope = " << g_alive << " (leaked)\n";
    int leaked = g_alive;
    {
        auto p = std::make_shared<NodeGood>();
        p->child = std::make_shared<NodeGood>();
        p->child->parent = p;          // weak back-pointer
    }
    std::cout << "  with weak_ptr back-pointer: newly leaked = " << g_alive - leaked << "\n";
}
```

`weak_ptr` 用前必须 `lock()`：返回 `shared_ptr`（对象还在）或空（已销毁），检查与提升是原子的，所以不会出现"检查时还在、使用时没了"。

## 6. 什么时候裸指针 / 引用没问题

* **借用**：函数参数、遍历中的临时指针、`get()` 取出给 C API。所有权仍在智能指针手里。
* **非拥有的反向指针**：子对象指向肯定比它活得久的父对象（树的 parent、事件源）。
* 性能关键的内部数据结构（侵入式链表、对象池）里自己管理的指针，但应被封装在一个类里。
* 规则：**裸指针不拥有；拥有就用智能指针；不手写 `new`/`delete`**（用 `make_unique`/`make_shared`）。

## 7. 坑

1. `shared_ptr<T> a(p); shared_ptr<T> b(p);` 用同一个裸指针造两个，会各建一个控制块 → 双重释放。永远从已有的 `shared_ptr` 拷贝，或用 `make_shared`。
2. 在成员函数里 `shared_ptr<T>(this)` 同样错；继承 `enable_shared_from_this` 并调 `shared_from_this()`。
3. 把 `shared_ptr` 当默认选择：引起不必要的原子操作、不明确的生命周期。**默认 `unique_ptr`**，需要共享再升级（`unique_ptr` 能直接转成 `shared_ptr`）。
4. 在同一个表达式里 `f(shared_ptr<A>(new A), g())` 旧标准下 `g()` 抛异常可能泄漏：用 `make_shared`。
5. `shared_ptr` 数组、`unique_ptr<T[]>` 的区别：`unique_ptr<T[]>` 用 `delete[]`；其余用 `vector`。
6. 循环引用只能靠设计避免（`weak_ptr`），泄漏检测工具能报告。

## 8. 面试官接着会问

**Q：`unique_ptr`、`shared_ptr`、`weak_ptr` 各自什么时候用？**
要点：见第 2 节表格；默认 `unique_ptr`；共享所有权才用 `shared_ptr`；`weak_ptr` 观察/打破环。

**Q：`shared_ptr` 怎么实现？拷贝要多少成本？线程安全吗？**
要点：对象指针 + 控制块指针（强/弱计数、删除器、分配器）；拷贝 = 原子 inc；计数线程安全，对象本身不安全；同一个 `shared_ptr` **变量**被多线程读写需要同步（或用 `atomic<shared_ptr>`），不同线程各自持有副本才安全。

**Q：`make_shared` 的好处？**
要点：一次分配（对象+控制块），异常安全；坏处：自定义删除器不能用、`weak_ptr` 存活时内存不能提前归还。

**Q：`unique_ptr` 为什么零开销？**
要点：只含一个指针，析构内联成 `delete`；默认删除器是空类，利用空基类优化不占空间。

**Q：Java 里对应什么？**
要点：Java 的引用 ≈ 无限 `shared_ptr` 但由 tracing GC 回收（能回收环）；`WeakReference` ≈ `weak_ptr`；try-with-resources ≈ `unique_ptr` + 自定义删除器。

**Q：为什么说"不应该写 `new`"？**
要点：裸 `new`/`delete` 在异常、提前 return 时易泄漏；智能指针让所有权可读、可编译期检查。

## 9. 自测

1. `unique_ptr` 能放进 `vector` 吗？怎么放？
2. 为什么 `weak_ptr` 要 `lock()` 而不是直接解引用？
3. `sizeof(unique_ptr<int>)` 和 `sizeof(shared_ptr<int>)` 各是多少？为什么？
4. 两个类互相持有 `shared_ptr` 会怎样？

<details><summary>答案</summary>

1. 可以：`push_back(std::make_unique<T>())` 或 `push_back(std::move(p))`；vector 的拷贝因此被禁用，只能移动。
2. 对象可能在你检查之后被另一线程销毁；`lock()` 原子地检查并提升为 `shared_ptr`，持有期间对象不会消失。
3. 8 和 16（64 位）：`unique_ptr` 只有对象指针；`shared_ptr` 多一个控制块指针。
4. 强计数都到不了 0，两个对象永远不释放（泄漏）；把一方改为 `weak_ptr`。

</details>
