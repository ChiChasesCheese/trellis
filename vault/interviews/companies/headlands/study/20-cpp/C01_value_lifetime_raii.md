# C01 · 值语义、对象生命周期与 RAII

> 读者：每天写 Java、C++ 生疏。本课从零讲：C++ 的对象「就是那块内存」，什么时候诞生、什么时候死亡由作用域决定，资源释放靠析构函数（destructor）而不是 GC。

## 1. Java 里是怎样的

* `new Point(1,2)` 永远在堆上；变量 `Point p` 只是**引用**（reference）。`Point b = a;` 复制的是引用，两个变量指向同一个对象。
* 对象什么时候回收由 GC 决定，程序员不知道也不用管；但文件、锁、socket 这类**非内存资源**要自己 `try-with-resources` / `finally` 释放。

## 2. C++ 从零讲起

**值语义（value semantics）**：变量**就是**对象本身。`Point b = a;` 造出第二个独立的 `Point`，改 `b` 不影响 `a`。要得到 Java 那种「同一对象的另一个名字」，必须显式写引用 `Point& r = a;`（引用 = 已有对象的别名，不是新对象）。

**存储期（storage duration）**——对象住在哪、活多久：

| 存储期 | 怎么得到 | 何时销毁 |
|---|---|---|
| 自动（automatic，"栈"） | 局部变量 `Point p;` | 离开所在 `{}` 作用域，**立刻**、确定地销毁 |
| 动态（dynamic，"堆"） | `new` / 智能指针 / `vector` 内部 | 你（或拥有它的对象）释放时 |
| 静态（static） | 全局变量、`static` 局部 | 程序结束 |

**构造/析构（constructor/destructor）**：对象诞生时自动调构造函数，销毁时自动调析构函数。规则只有三条：

1. 局部变量按**声明顺序**构造，按**相反顺序**析构。
2. 成员变量按**声明顺序**构造，按**相反顺序**析构，且在类自己的析构函数体**之后**。
3. 抛异常时，栈展开（stack unwinding）会把已经构造好的局部变量按相反顺序析构掉。

## 3. 例 1：值 vs 引用 vs 布局

```cpp
void demo_copy() {
    Point a{1, 2};
    Point b = a;        // COPY: b is a second, independent Point (Java: both would name one object)
    b.x = 99;
    std::cout << "a.x=" << a.x << " b.x=" << b.x << "\n";            // 1 and 99

    Point& r = a;       // reference = another name for the SAME object (closest to Java's reference)
    r.x = 7;
    std::cout << "a.x=" << a.x << " (changed through r)\n";           // 7
}
```

```cpp
void demo_layout() {
    std::vector<Point> v(4);                       // one contiguous block: 4 * sizeof(Point) bytes
    std::cout << "sizeof(Point)=" << sizeof(Point) << "\n";
    for (int i = 1; i < 4; ++i) {
        auto d = reinterpret_cast<std::uintptr_t>(&v[i]) - reinterpret_cast<std::uintptr_t>(&v[i - 1]);
        std::cout << "&v[" << i << "] - &v[" << i - 1 << "] = " << d << " bytes\n";
    }
    // Java's Point[] holds 4 references; each Point is a separate heap object with a 12-16 byte header.
}
```

```cpp
struct Order {
    std::string symbol;   // the std::string object lives INSIDE Order (its characters may be on the heap)
    Point where;          // Point lives inside Order too: no pointer, no header
    long qty;
};

void demo_nested() {
    Order o{"AAPL", {3, 4}, 100};
    Order copy = o;                  // deep copy by default: symbol is copied, too
    copy.symbol = "MSFT";
    std::cout << o.symbol << " vs " << copy.symbol << "; sizeof(Order)=" << sizeof(Order) << "\n";
}
```

输出：

```text
a.x=1 b.x=99
a.x=7 (changed through r)
sizeof(Point)=8
&v[1] - &v[0] = 8 bytes
&v[2] - &v[1] = 8 bytes
&v[3] - &v[2] = 8 bytes
AAPL vs MSFT; sizeof(Order)=40
```

要点：`vector<Point>` 是**一整块连续内存**，每个元素就是 8 字节的 `Point`；Java 的 `Point[]` 存的是 4 个引用，每个 `Point` 另有对象头，散在堆里。`Order` 里的 `string` 和 `Point` 直接嵌在 `Order` 内部，复制 `Order` 就把它们一起（深）复制。这是后面「为什么 C++ 快」的根。

## 4. 例 2：看得见的生命周期

```cpp
struct Tracer {
    std::string name;
    explicit Tracer(std::string n) : name(std::move(n)) { std::cout << "  ctor " << name << "\n"; }
    Tracer(const Tracer& o) : name(o.name + "'") { std::cout << "  copy " << o.name << " -> " << name << "\n"; }
    ~Tracer() { std::cout << "  dtor " << name << "\n"; }
};
```

```cpp
struct Holder {
    Tracer first{"member-first"};     // members are built in DECLARATION order ...
    Tracer second{"member-second"};   // ... and destroyed in REVERSE order
    Holder() { std::cout << "  Holder body\n"; }
    ~Holder() { std::cout << "  ~Holder body\n"; }
};

void scope_order() {
    std::cout << "[scope_order]\n";
    Tracer a("a");
    {
        Tracer b("b");
        std::cout << "  inner scope ends\n";
    }                                 // b is destroyed HERE, deterministically (Java: some GC cycle, maybe never)
    Holder h;
    Tracer c("c");
    std::cout << "  function ends\n";
}                                     // destroyed in reverse: c, h (its members reversed), a
```

```cpp
void unwinding() {
    std::cout << "[unwinding]\n";
    try {
        Tracer x("x");
        Tracer y("y");
        throw std::runtime_error("boom");   // stack unwinding destroys y, then x
    } catch (const std::exception& e) {
        std::cout << "  caught " << e.what() << "\n";
    }
}
```

```cpp
void temporaries() {
    std::cout << "[temporaries]\n";
    std::vector<Tracer> v;
    v.reserve(2);
    v.push_back(Tracer("tmp"));       // temporary is built, copied into the vector, destroyed at the ';'
    std::cout << "  after push_back\n";
    const Tracer& r = Tracer("lifetime-extended");   // binding to a const ref extends the temporary's life
    std::cout << "  using " << r.name << "\n";
}
```

输出：

```text
[scope_order]
  ctor a
  ctor b
  inner scope ends
  dtor b
  ctor member-first
  ctor member-second
  Holder body
  ctor c
  function ends
  dtor c
  ~Holder body
  dtor member-second
  dtor member-first
  dtor a
[unwinding]
  ctor x
  ctor y
  dtor y
  dtor x
  caught boom
[temporaries]
  ctor tmp
  copy tmp -> tmp'
  dtor tmp
  after push_back
  ctor lifetime-extended
  using lifetime-extended
  dtor lifetime-extended
  dtor tmp'
```

逐条读：`b` 在内层 `}` 就被销毁；函数结束时按 `c → h（含成员 second、first）→ a` 倒序销毁；`throw` 之后 `y`、`x` 先析构才进 `catch`。`push_back(Tracer("tmp"))` 打印了一次 copy：`Tracer` 自己声明了拷贝构造和析构，编译器就不再自动生成移动构造（移动构造 = 直接"偷走"临时对象的内部资源而不复制），于是临时对象被**复制**进 vector。`const Tracer& r = Tracer(...)` 把临时对象的寿命延长到 `r` 的作用域结束。

## 5. RAII：Resource Acquisition Is Initialization

思想：**把资源的所有权绑到一个对象的生命周期上**——构造函数获取资源，析构函数释放。因为析构函数在**所有**退出路径（return、break、异常）上都会被调用，所以不需要 `finally`，也不会漏释放。Java 的 `try-with-resources` 只是 RAII 的一个特例，C++ 里它适用于**一切**：内存、文件、锁、socket、事务。

```cpp
class File {
    std::FILE* f_;
public:
    File(const char* path, const char* mode) : f_(std::fopen(path, mode)) {
        if (!f_) throw std::runtime_error(std::string("cannot open ") + path);
    }
    ~File() { if (f_) { std::fclose(f_); std::cout << "  file closed\n"; } }
    File(const File&) = delete;                 // two owners of one FILE* would double-close
    File& operator=(const File&) = delete;
    std::FILE* get() const { return f_; }
};
```

```cpp
template <class F>
class ScopeGuard {                              // run an arbitrary cleanup at scope exit (Go: defer)
    F fn_;
    bool active_ = true;
public:
    explicit ScopeGuard(F fn) : fn_(std::move(fn)) {}
    ~ScopeGuard() { if (active_) fn_(); }
    void dismiss() { active_ = false; }         // "commit": cancel the cleanup
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
};
```

```cpp
int read_first_line_length(const char* path) {
    File file(path, "r");                       // throws if missing: nothing to clean up yet
    char buf[256];
    if (!std::fgets(buf, sizeof buf, file.get())) throw std::runtime_error("empty file");
    return static_cast<int>(std::string(buf).size());
}                                               // every return and every throw closes the file

std::mutex m;
int counter = 0;

void locked_increment() {
    std::lock_guard<std::mutex> lock(m);        // Java: synchronized (m) { ... }
    ++counter;
    if (counter > 100) throw std::runtime_error("too big");   // the mutex is still released
}
```

输出：

```text
error: cannot open /definitely/not/here
  file closed
length = 11
  rollback (guard fired)
  committed, guard dismissed
counter = 1
```

* `File` 删除了拷贝：两个对象各自 `fclose` 同一个 `FILE*` 会双重释放。**拥有资源的类必须想清楚拷贝语义**：要么像这样禁止拷贝，要么实现深拷贝，要么把资源交给标准库成员类型去管理。
* `lock_guard` 就是 Java `synchronized` 的 RAII 版；`ScopeGuard` 相当于 Go 的 `defer`。
* 标准库里的 RAII 类型：`vector`/`string`（内存）、`unique_ptr`/`shared_ptr`（对象）、`lock_guard`/`unique_lock`/`scoped_lock`（锁）、`fstream`（文件）、`jthread`（线程）。

## 6. 例 3：构造函数抛异常、切片

```cpp
struct Part {
    std::string n;
    explicit Part(std::string name) : n(std::move(name)) { std::cout << "  Part " << n << " built\n"; }
    ~Part() { std::cout << "  Part " << n << " destroyed\n"; }
};

struct Machine {
    Part a{"a"};
    Part b{"b"};
    Machine(bool fail) {
        std::cout << "  Machine body starts\n";
        if (fail) throw std::runtime_error("constructor failed");
    }
    ~Machine() { std::cout << "  ~Machine runs\n"; }
};
```

```cpp
struct Animal { virtual std::string name() const { return "animal"; } virtual ~Animal() = default; };
struct Dog : Animal { std::string name() const override { return "dog"; } int tricks = 3; };

std::string by_value(Animal a) { return a.name(); }          // copies only the Animal part: Dog is "sliced" off
std::string by_ref(const Animal& a) { return a.name(); }     // no copy: virtual dispatch works
```

```text
[constructor throws]
  Part a built
  Part b built
  Machine body starts
  Part b destroyed
  Part a destroyed
  caught: constructor failed
[slicing]
  by_value: animal, by_ref: dog
  through base pointer: dog
```

* 构造函数抛异常：**已经构造好的成员会被析构，对象自己的析构函数不会运行**（对象从未"完整存在"）。这就是为什么资源要放在成员对象里（RAII），而不是在构造函数里裸 `new`：裸指针成员在这种情况下会泄漏。
* 切片（slicing）：按**值**接收基类参数会把派生类部分切掉，多态失效。多态对象用引用/指针传递。

## 7. 坑

1. **析构函数里抛异常**：析构默认 `noexcept`，异常逃出去直接 `std::terminate`。析构里吞掉或记录异常。
2. **悬空引用**：返回局部变量的引用/指针：函数返回后局部变量已销毁，引用指向无效内存。
3. **静态初始化顺序**：不同源文件里的全局对象构造顺序不确定；全局对象依赖另一个全局对象是经典 bug。用函数内 `static` 局部变量（首次调用时初始化，线程安全）。
4. **以为 `delete` 之后指针会变空**：不会，指针还在，成了悬空指针。所以现代 C++ 不手写 `delete`，用智能指针让对象的所有者在析构时自动释放。
5. **按值传大对象**：每次调用都深拷贝。

## 8. 面试官接着会问

**Q：什么是 RAII？为什么 C++ 没有 `finally`？**
要点：资源绑定对象寿命；析构函数在所有出口自动运行（含异常）；比 `finally` 好在「写一次，处处生效」且不会忘；Java 的 try-with-resources 是同一思想但要调用者记得写。

**Q：栈和堆的区别？栈对象一定快吗？**
要点：自动存储 = 指针移动，不碰分配器，缓存友好；堆分配要走 `malloc`（找空闲块、可能加锁）。但「栈上」是对象所在位置，`vector` 对象在栈上而元素在堆上。栈空间小（默认几 MB），大数组放栈会栈溢出。

**Q：构造函数里抛异常会怎样？**
要点：如上；已构造的子对象被析构，自己的析构不执行；所以用成员 RAII 对象。

**Q：C++ 的值语义对性能有什么影响？**
要点：连续布局、没有对象头和间接寻址、复制成本显式（需要用移动/引用避免）。

**一句话版（口述）**："In C++ an object's lifetime is tied to its scope, and its destructor runs deterministically at every exit path, including exceptions. That's RAII: I put every resource - memory, file, lock - in an object, so cleanup is automatic and there's no finally to forget."

## 9. 自测

1. 局部变量 `A a; B b;` 的析构顺序？成员 `X x; Y y;` 呢？
2. 构造函数在第二个成员构造完后抛异常，哪些析构函数会运行？
3. 为什么 `File` 要 `= delete` 拷贝构造？
4. `void f(Animal a)` 传入 `Dog` 会发生什么？

<details><summary>答案</summary>

1. 先 `b` 后 `a`；成员先 `y` 后 `x`（都是声明顺序的逆序），且成员的析构发生在类自己析构函数体之后。
2. 两个已构造成员的析构函数运行；类自己的析构函数不运行。
3. 拷贝会得到两个指向同一 `FILE*` 的对象，各自析构时 `fclose` 两次 = 双重释放。
4. 切片：只复制 `Animal` 子对象，`Dog` 的字段和虚函数覆盖丢失，`a.name()` 返回基类版本。

</details>
