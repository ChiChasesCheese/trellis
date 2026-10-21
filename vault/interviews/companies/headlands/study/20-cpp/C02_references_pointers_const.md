# C02 · 引用、指针与 `const`

> Java 只有一种"引用"。C++ 有三种东西承担这个角色：引用（`T&`）、指针（`T*`）、值。本课讲清各自语义、怎么选参数类型、`const` 到底约束什么。

## 1. Java 里是怎样的

* 对象变量都是引用，可以为 `null`，可以重新指向别的对象；方法参数按值传递**引用的拷贝**，所以方法里能改对象内容，但不能让调用者的变量指向别处。
* `final` 只表示**变量**不能重新赋值，不保证对象内容不变。

## 2. C++ 从零讲

| | 值 `T` | 引用 `T&` | 指针 `T*` |
|---|---|---|---|
| 含义 | 对象本身 | 已有对象的**别名** | 存放地址的变量 |
| 能否为空 | 否 | 否（必须初始化） | 可以（`nullptr`） |
| 能否重新绑定 | — | **不能**：`r = b` 是赋值，不是换绑 | 能 |
| 语法 | `p.x` | `r.x` | `p->x`、`*p` |
| 大小 | `sizeof(T)` | 同被引用对象（语言层面） | 8 字节（64 位） |
| 谁负责释放 | 作用域 | 不涉及（不拥有） | 看约定：裸指针**不应**表示所有权 |

**参数传递的选择**（日常 90% 的决策）：

* 小的、廉价可拷贝的类型（`int`、`double`、指针、`string_view`、`span`）：按**值**。
* 只读大对象：`const T&`。
* 要修改调用者的对象：`T&`（或指针，如果"可以没有"）。
* 要取得所有权/存下来：按值接收然后 `std::move` 进成员（`std::move` 把对象标记为"可以被偷走资源"），或用 `unique_ptr<T>`（独占所有权的智能指针）。

## 3. 例 1：参数、`const` 的位置、引用规则

```cpp
struct Big { std::vector<int> data = std::vector<int>(1000, 1); };

void by_value(Big b)         { b.data[0] = 42; }                // copies 4000+ bytes; caller unaffected
void by_ref(Big& b)          { b.data[0] = 42; }                // aliases the caller's object; may mutate
void by_const_ref(const Big& b) { std::cout << "  size=" << b.data.size() << "\n"; }   // read only, no copy
void by_ptr(Big* b)          { if (b) b->data[0] = 43; }        // may be null; reseatable; needs ->
```

```cpp
void const_positions() {
    int x = 1, y = 2;
    const int* p1 = &x;        // pointer to const int: *p1 = 5 is an error, p1 = &y is fine
    int* const p2 = &x;        // const pointer to int: *p2 = 5 is fine, p2 = &y is an error
    const int* const p3 = &x;  // neither can change
    p1 = &y;
    *p2 = 5;
    std::cout << "  *p1=" << *p1 << " *p2=" << *p2 << " *p3=" << *p3 << "\n";
    // Read declarations right-to-left: "p2 is a const pointer to int".
}
```

```cpp
class Counter {
    int n_ = 0;
    mutable int reads_ = 0;               // mutable: bookkeeping that does not change the logical value
public:
    void inc() { ++n_; }
    int get() const { ++reads_; return n_; }   // const member function: promises not to change *this
    int reads() const { return reads_; }
};

void use_const(const Counter& c) {
    // c.inc();                          // would not compile: inc() is not const
    std::cout << "  get=" << c.get() << " reads=" << c.reads() << "\n";
}
```

```cpp
void reference_rules() {
    int a = 1, b = 2;
    int& r = a;          // must be initialised; there is no "null reference"
    r = b;               // NOT rebinding: this assigns b's value to a
    std::cout << "  a=" << a << " b=" << b << " (r still names a)\n";

    std::vector<int> v{1, 2, 3};
    for (auto& e : v) e *= 2;                    // auto& : mutate in place
    long scratch = 0;
    for (auto e : v) { e *= 100; scratch += e; } // auto  : mutates a copy, v unchanged
    for (const auto& e : v) std::cout << "  " << e;
    std::cout << "  (scratch=" << scratch << ")\n";
}
```

输出：

```text
after by_value  data[0]=1
after by_ref    data[0]=42
after by_ptr    data[0]=43
  size=1000
sizeof(Big)=24 sizeof(Big*)=8
  *p1=2 *p2=5 *p3=5
  get=1 reads=1
  a=2 b=2 (r still names a)
  2  4  6  (scratch=1200)
```

### `const` 读法

从右往左读声明：`const int* p` = "p 是指针，指向 const int"（不能通过 p 改值，p 本身可改）；`int* const p` = "p 是 const 指针，指向 int"（p 不能改指向，值可改）。

### const 成员函数

`int get() const` 承诺不修改 `*this`；`const` 对象只能调用 `const` 成员函数。`mutable` 成员例外，用于缓存、计数这类**逻辑上不改变对象值**的内部状态。**const-correctness**：凡是不修改的参数、成员函数都写 `const`，编译器帮你查错——这是 C++ 用类型表达"只读"的方式（Java 没有）。

### `auto` 与引用

`for (auto e : v)` 复制每个元素；`for (auto& e : v)` 修改原元素；`for (const auto& e : v)` 只读且不复制。**拿不准就写 `const auto&`**。

## 4. 例 2：非拥有视图 `string_view` / `span`

视图（view）= 一个指针 + 一个长度，不拥有数据。作函数参数很理想：能接受字面量、`string`、`vector`、数组，不分配内存。

```cpp
// Java: a String parameter is a cheap reference. C++: std::string by value copies; const std::string& forces
// a std::string to exist; std::string_view accepts literals, std::string, char arrays with no allocation.
int count_char(std::string_view s, char c) {
    int n = 0;
    for (char ch : s) n += (ch == c);
    return n;
}

std::string_view first_token(std::string_view s) {
    auto pos = s.find(' ');
    return s.substr(0, pos);                    // O(1): same bytes, new (pointer, length)
}
```

```cpp
long sum(std::span<const int> xs) {             // works for vector, array, C array, sub-ranges
    return std::accumulate(xs.begin(), xs.end(), 0L);
}
```

```text
4 2
first token: BUY (3 chars, no allocation)
21 60 12
sizeof(string_view)=16 sizeof(span<int>)=16 (a pointer and a length)
```

## 5. 坑：视图和引用的悬空

视图和引用都**不延长**被引用对象的寿命。下面的 `string_view` 指向一个已经销毁的临时 `string`：

```cpp
// C02: the hazard of views. The view outlives the string it points into: use-after-free that Java cannot have.
#include <iostream>
#include <string>
#include <string_view>

std::string make_name() { return std::string(64, 'x') + " (a name too long for the small-string buffer)"; }

int main() {
    std::string_view sv = make_name();   // the temporary std::string dies at the ';' -> sv dangles
    std::cout << sv.size() << "\n";      // reads freed heap memory: AddressSanitizer stops us
    std::cout << sv[0] << "\n";
}
```

编译器本身就警告了；AddressSanitizer 在运行时报告：

```text
ERROR: AddressSanitizer: heap-use-after-free on address 0x… at pc 0x… bp 0x… sp 0x…
READ of size 1 at 0x… thread T0
0x… is located 0 bytes inside of 144-byte region [0x…,0x…)
freed by thread T0 here:
previously allocated by thread T0 here:
SUMMARY: AddressSanitizer: heap-use-after-free (c02_dangling_view_ub:arm64+0x…) in main+0x204
```

规则：视图/引用可以当**参数**；当**成员变量或返回值**时，必须确保被引用对象活得更久。

其他坑：

1. 返回局部变量的引用或指针 = 悬空。
2. `const_cast` 去掉 const 再写入原本就是 const 的对象 = UB。
3. 引用成员使类不可赋值（引用不能换绑）。
4. 指针算术越界不会报错，访问越界内存是未定义行为。
5. 指向 `vector` 元素的引用/指针，在 `vector` 扩容重新分配内存后会失效。

## 6. 面试官接着会问

**Q：引用和指针的区别？**
要点：表中各行；引用不能为空、不能重新绑定、语法上像值；指针可空、可重绑、可做算术；引用通常由编译器用指针实现，但语言不保证 `sizeof`/存储。用引用表达"一定有"，指针表达"可能没有"或需要重绑/算术。

**Q：`const int*`、`int* const`、`const int* const`？**
要点：右往左读。

**Q：为什么参数常写 `const std::string&`，现在又推荐 `string_view`？**
要点：`const string&` 避免复制但只接受 `string`（传字面量会临时构造一个 `string`，可能分配）；`string_view` 接受任何字符序列，零分配；代价是不能保证以 `\0` 结尾、不拥有数据、悬空风险。

**Q：`mutable` 的用途？**
要点：const 成员函数里可以改的成员，如懒计算缓存、互斥量（`mutable std::mutex`）。

**Q：返回引用安全吗？**
要点：只有被引用对象在函数返回后仍存在（成员、静态、参数引用）才安全；局部变量不行。

## 7. 自测

1. `int& r = a; r = b;` 之后 `r` 指向谁？
2. `void f(const std::vector<int> v)` 有什么问题？
3. 什么时候用指针参数而不是引用？
4. `for (auto x : vec) x *= 2;` 能改 `vec` 吗？

<details><summary>答案</summary>

1. 仍然是 `a`：这是把 `b` 的值赋给 `a`，引用永远绑定初始对象。
2. 按值传，会复制整个 vector；`const` 又只约束函数内部，应写 `const std::vector<int>&`。
3. 参数"可以没有"（`nullptr` 表示没有）、需要在函数里重新指向、或与 C API 交互。
4. 不能：`auto` 是副本。要改写 `auto&`。

</details>
