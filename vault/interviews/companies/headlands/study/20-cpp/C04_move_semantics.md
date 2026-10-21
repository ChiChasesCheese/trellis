# C04 · 移动语义、右值引用、Rule of 0/3/5、复制省略

> 目标：说清 `std::move` 到底做了什么、移动构造函数为什么能"O(1) 复制"、什么时候编译器自动生成特殊成员函数、`return std::move(x)` 为什么反而慢。

## 1. Java 里是怎样的

对象变量是引用，`b = a` 只是复制引用（O(1)，共享同一对象）；想要独立副本得显式 `clone()` / 拷贝构造。所以 Java 没有"移动"这个概念——引用拷贝本来就便宜。

## 2. C++ 为什么需要移动

C++ 变量就是对象本身，`b = a` 默认**深拷贝**：`std::string`、`vector` 要分配新内存并逐字节复制。但很多时候源对象马上就要销毁（函数返回的临时对象、`vector` 扩容时搬走的旧元素），复制纯属浪费。**移动（move）**：新对象直接"偷走"源对象的内部资源（指针），把源置为空，O(1)。

## 3. 值类别与右值引用（从零讲）

* **左值（lvalue）**：有名字、能取地址的表达式（变量 `a`）。
* **右值（rvalue）**：临时的、马上销毁的值（`f()` 的返回值、字面量 `5`）。
* **右值引用 `T&&`**：只能绑定到右值的引用。重载 `f(const T&)` 和 `f(T&&)`，传临时对象时选后者——这就是"按是否临时来选择复制或移动"的机制。
* **`std::move(x)` 只是一个类型转换**，把左值 `x` 转成 `T&&`，**本身不移动任何东西**；移动发生在随后选中的移动构造/赋值函数里。`std::move(x)` 之后 `x` 仍然存在，处于"有效但未指定"状态（可以析构、可以赋新值，别读它的值）。

## 4. 例：一个拥有缓冲区的类

```cpp
class Buffer {
    char* data_ = nullptr;
    std::size_t n_ = 0;
public:
    explicit Buffer(std::size_t n) : data_(new char[n]()), n_(n) { std::cout << "  ctor(" << n << ")\n"; }
    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& o) : data_(new char[o.n_]), n_(o.n_) {            // copy: allocate + copy bytes: O(n)
        std::memcpy(data_, o.data_, n_);
        std::cout << "  COPY(" << n_ << ")\n";
    }
    Buffer(Buffer&& o) noexcept : data_(o.data_), n_(o.n_) {              // move: steal the pointer: O(1)
        o.data_ = nullptr; o.n_ = 0;
        std::cout << "  move(" << n_ << ")\n";
    }
    Buffer& operator=(const Buffer& o) {
        if (this != &o) { Buffer tmp(o); swap(tmp); }                      // copy-and-swap: strong guarantee
        return *this;
    }
    Buffer& operator=(Buffer&& o) noexcept {
        if (this != &o) { delete[] data_; data_ = o.data_; n_ = o.n_; o.data_ = nullptr; o.n_ = 0; }
        return *this;
    }
    void swap(Buffer& o) noexcept { std::swap(data_, o.data_); std::swap(n_, o.n_); }
    std::size_t size() const { return n_; }
};
```

```cpp
Buffer a(1 << 20);
Buffer b = a;                       // copy
Buffer c = std::move(a);            // move: a is now empty
std::cout << "  a.size()=" << a.size() << " c.size()=" << c.size() << "\n";
std::vector<Buffer> v;
v.reserve(3);
v.push_back(Buffer(8));             // rvalue argument: moves
v.push_back(b);                     // lvalue argument: copies
v.push_back(std::move(b));          // explicit move
```

```cpp
void moved_from_state() {
    std::string s(40, 'a');
    std::string t = std::move(s);                      // s is "valid but unspecified"
    std::cout << "  t.size()=" << t.size() << "  s.size()=" << s.size() << " (usually empty, but unspecified: do not rely on it)\n";
    s = "reuse is fine";                                // assigning to a moved-from object is always allowed
    std::cout << "  s=" << s << "\n";
}
```

```cpp
// vector growth uses move only if the move constructor is noexcept (otherwise it copies to keep the strong guarantee)
struct Loud {
    Loud() = default;
    Loud(const Loud&) { std::cout << "c"; }
    Loud(Loud&&) noexcept { std::cout << "m"; }
};
struct LoudThrowing {
    LoudThrowing() = default;
    LoudThrowing(const LoudThrowing&) { std::cout << "c"; }
    LoudThrowing(LoudThrowing&&) { std::cout << "m"; }   // NOT noexcept
};
template <class T>
void grow(const char* name) {
    std::vector<T> v;
    std::cout << "  " << name << " growth sequence: ";
    for (int i = 0; i < 4; ++i) v.emplace_back();        // reallocation relocates the old elements
    std::cout << "\n";
}
```

输出：

```text
[copy vs move]
  ctor(1048576)
  COPY(1048576)
  move(1048576)
  a.size()=0 c.size()=1048576
  ctor(8)
  move(8)
  COPY(1048576)
  move(1048576)
[moved-from std::string]
  t.size()=40  s.size()=0 (usually empty, but unspecified: do not rely on it)
  s=reuse is fine
[relocation on growth: c = copy, m = move]
  noexcept move    growth sequence: mmm
  throwing move    growth sequence: ccc
```

逐条读：

* `Buffer b = a;` 打印 `COPY`；`std::move(a)` 之后 `a.size()` 为 0。
* `push_back(Buffer(8))`（右值）走 `move`，`push_back(b)`（左值）走 `COPY`，`push_back(std::move(b))` 走 `move`。
* **`noexcept` 很重要**：`vector` 扩容要把旧元素搬到新内存。如果移动构造可能抛异常，搬到一半失败就无法恢复原状；所以 `vector` 只在移动构造 `noexcept` 时才移动，否则**退回到拷贝**（输出 `mmm` vs `ccc`）。自己写的移动操作务必标 `noexcept`。
* 赋值版本写成 copy-and-swap：先拷贝出临时对象再 `swap`，天然处理自赋值且异常安全。

## 5. Rule of 0 / 3 / 5

**特殊成员函数**：析构、拷贝构造、拷贝赋值、移动构造、移动赋值。

* **Rule of 0（首选）**：类的成员本身都会自己管理资源（`string`、`vector`、`unique_ptr`），那就**一个都不写**，编译器生成的全是对的。
* **Rule of 3**：只要手写了析构/拷贝构造/拷贝赋值**中的一个**（说明你在管理原始资源），其余两个也几乎一定要写。
* **Rule of 5**：现代版本加上移动构造和移动赋值。
* 编译器生成规则：你声明了析构或拷贝操作，**不会**再自动生成移动操作（一个声明了析构函数和拷贝构造的 `Tracer` 类，放进 `vector` 时只会被复制，不会被移动）；你声明了移动操作，拷贝操作被**删除**。

```cpp
// Rule of zero: every member already manages itself, so write NO special member functions.
struct Account {
    std::string name;
    std::vector<int> history;
    std::unique_ptr<int> secret = std::make_unique<int>(7);     // makes the class move-only automatically
};
static_assert(std::is_nothrow_move_constructible_v<Account>);
static_assert(!std::is_copy_constructible_v<Account>);          // unique_ptr member deletes the copy
```

`Account` 一个特殊成员都没写：因为 `unique_ptr` 成员，它自动成为只能移动的类型，且移动不抛异常；`static_assert` 在编译期验证。

### 参数风格：sink 参数与完美转发

```cpp
class Person {
    std::string name_;
public:
    explicit Person(std::string name) : name_(std::move(name)) {}   // sink: by value, then move. One move for rvalues,
                                                                    // one copy + one move for lvalues. Simple and fast enough.
    const std::string& name() const { return name_; }
};
```

```cpp
template <class T>
struct Recorder {
    std::vector<T> items;
    template <class... Args>
    void emplace(Args&&... args) {                       // Args&& here is a FORWARDING reference
        items.emplace_back(std::forward<Args>(args)...); // keeps lvalue-ness / rvalue-ness of each argument
    }
};

struct Trade {
    std::string sym; int qty; double px;
    Trade(std::string s, int q, double p) : sym(std::move(s)), qty(q), px(p) { std::cout << "  Trade built in place\n"; }
    Trade(const Trade&) { std::cout << "  Trade COPY\n"; }
    Trade(Trade&&) noexcept { std::cout << "  Trade move\n"; }
};
```

```text
moved Account holds secret=7, source secret is null
alice alice n.size() after move: 0
emplace with constructor arguments:
  Trade built in place
push_back(Trade(...)) temporary:
  Trade built in place
  Trade move
emplace_back(Trade(...)) still builds a temporary first:
  Trade built in place
  Trade move
```

* **sink 参数**：构造函数要存下字符串，就**按值接收然后 `std::move` 进成员**。传右值：1 次移动；传左值：1 次拷贝 + 1 次移动。简单且足够快。
* **转发引用（forwarding reference）**：模板里的 `Args&&` 能绑定左值也能绑定右值；`std::forward<Args>(args)...` 原样保持"是左值还是右值"。`emplace_back(args...)` 就靠它**在 vector 内存里直接构造**对象，省掉临时对象。注意输出：`emplace_back(Trade(...))` 仍然先造了临时对象再移动——`emplace` 的好处只在传**构造参数**时。

## 6. 复制省略（copy elision）

编译器可以（部分情形必须）直接把对象构造在最终位置，**根本不调用拷贝/移动构造**。

```cpp
Pinned make_pinned() { return Pinned(7); }       // C++17: guaranteed elision, so a non-movable type can be returned
Heavy make_prvalue() { return Heavy("prvalue"); }            // no copy, no move: constructed in the caller's slot
Heavy make_nrvo() { Heavy h("nrvo"); return h; }             // named return: NRVO (optional, but every compiler does it here)
Heavy make_pessimized() { Heavy h("pessimized"); return std::move(h); }   // BAD: blocks NRVO, forces a move
Heavy make_two_paths(bool f) {                               // two different locals: NRVO is impossible -> move (implicit)
    Heavy a("path-a"), b("path-b");
    if (f) return a;
    return b;
}
```

```text
  guaranteed elision, non-movable type:
    Pinned ctor
    p.v=7
  prvalue:
    ctor prvalue
  NRVO:
    ctor nrvo
  return std::move(local):
    ctor pessimized
    move
  two candidate locals:
    ctor path-a
    ctor path-b
    move
```

* **C++17 起保证省略**：用纯右值（`return Pinned(7);`、`Heavy h = make();`）初始化对象时，不存在临时对象，所以连"不可拷贝不可移动"的类型也能这样返回。
* **NRVO**（具名返回值优化）：返回局部变量 `h`，编译器通常直接把 `h` 构造在调用者的位置；允许但不保证。
* `return std::move(h);` 是**反模式**：它把表达式变成右值，阻止 NRVO，强制多一次移动；编译器会警告 `-Wpessimizing-move`：

```text
$ c04_copy_elision
  guaranteed elision, non-movable type:
    Pinned ctor
```

* 有两个不同局部变量可能被返回时无法 NRVO，但 `return a;` 会自动按右值处理（隐式移动），也不要手写 `std::move`。

## 7. 坑

1. **用了被移动后的对象**：`std::move(s)` 之后读 `s` 的值是逻辑错误（不是 UB，但内容未指定）。
2. **给 `const` 对象 `std::move`**：`const T&&` 绑不上移动构造，静默退化为拷贝。
3. **移动操作忘记 `noexcept`**：容器扩容退回拷贝（见上例）。
4. **移动赋值不处理自赋值**：`a = std::move(a)` 可能先释放自己再读自己。
5. **对基础类型 `std::move` 没有意义**：`int` 移动 = 拷贝。
6. 手写资源管理类而不是组合标准库类型——Rule of 0 能避免上面全部。

## 8. 面试官接着会问

**Q：`std::move` 做了什么？**
要点：只是 `static_cast<T&&>`，不移动；让重载决议选中移动构造/赋值。

**Q：左值、右值、`T&&`、转发引用？**
要点：见第 3 节；`T&&` 在**推导出的**模板参数上（`template<class T> f(T&&)`）或 `auto&&` 才是转发引用，具体类型 `Buffer&&` 是纯右值引用。

**Q：Rule of 5 是什么？什么时候用 Rule of 0？**
要点：见第 5 节；优先 0。

**Q：为什么 `vector` 扩容时有时拷贝有时移动？**
要点：`move_if_noexcept`：移动构造 `noexcept` 才移动，否则为了强异常保证拷贝。

**Q：`return std::move(x)` 好不好？**
要点：不好，阻止 NRVO，且 C++11 起返回局部变量本来就是隐式移动。

**Q：与 Java 对比？**
要点：Java 引用拷贝天然廉价，C++ 值语义要靠移动达到同样的"转移所有权"；移动让值语义既保留布局优势又避免深拷贝。

**口述版**："Copying a vector duplicates its heap buffer; moving just steals the pointer and leaves the source empty, which is O(1). `std::move` is only a cast to an rvalue reference - the move constructor does the stealing. I mark moves `noexcept`, otherwise `vector` falls back to copying on reallocation, and I prefer the rule of zero so the compiler generates all of it."

## 9. 自测

1. `std::string t = std::move(s);` 之后能对 `s` 做什么？
2. 为什么 `const std::string s; auto t = std::move(s);` 仍然是拷贝？
3. 一个类有手写析构函数，编译器还会自动生成移动构造吗？
4. `emplace_back(Trade("A",1,1.0))` 比 `push_back(Trade("A",1,1.0))` 快吗？

<details><summary>答案</summary>

1. 析构、赋新值都可以；不要依赖它的内容（通常为空）。
2. `std::move(s)` 得到 `const std::string&&`，移动构造需要非 const 的 `string&&`，只能匹配拷贝构造 `const string&`。
3. 不会；声明析构函数会抑制隐式移动操作，拷贝仍会生成（所以 `Tracer` 只能被复制）。
4. 没有区别：两者都先构造临时 `Trade` 再移动；要省掉临时对象应写 `emplace_back("A", 1, 1.0)`。

</details>
