---
id: pl-cpp-stl-ranges-found-string-view-span
node: cpp.stl-ranges
type: qa
step: 6
---
## Q
`std::string_view` 和 `std::span` 是什么？它们解决什么问题，代价是什么？

## A
**问题**：函数要读一段连续数据（一个字符串、一个数组的一部分）。以前有几种接口都不理想：
- `const std::string&`：调用者只有 C 字符串或子串时，必须先构造一个 `std::string`（可能分配堆内存）；
- `const char*` 加长度：两个参数，容易配错；
- `const std::vector<T>&`：数组、子区间都得先拷成 `vector`。

**`std::string_view`**（C++17）：一个**指针 + 长度**的非拥有视图，指向别处存放的字符序列。大小 16 字节，拷贝只复制这两个字，不分配内存。`std::string`、字符串字面量、`char` 数组都可以隐式转换成它。

**`std::span<T>`**（C++20）：同样的想法，用于任意类型的连续序列。`std::span<const int>` 可以从 `vector`、`array`、C 数组构造，是替代"指针 + 长度"的标准方式。`span` 的长度可以在编译期固定（`span<int, 4>`）。

**用法**：函数参数里用它们：

```cpp
bool starts_with_http(std::string_view url);   // 接受 string、字面量、子串，零拷贝
double mean(std::span<const double> xs);        // 接受 vector、array、C 数组
```

**代价：悬垂（dangling）**。视图不拥有数据，一旦底层数据消失，视图就指向已释放的内存。本机实测：

```cpp
std::string_view sv = name();   // name() 返回临时 std::string，语句结束即销毁
println("{}", sv);
```

clang 的编译警告：`object backing the pointer will be destroyed at the end of the full-expression [-Wdangling-gsl]`；运行（ASan）：`heap-use-after-free ... READ of size 53`。更隐蔽的是：把 `string_view` 存成类成员、放进容器、从函数返回，数据来源的生命周期必须长于它。

**对比**：
- **Go 的切片**：同样是"指针 + 长度（+ 容量）"，但有 GC，底层数组不会被释放，不会悬垂，代价是多个切片共享同一数组可能意外别名；
- **Rust 的 `&str`、`&[T]`**：同样的东西，借用检查器保证它不会比底层数据活得久，悬垂是编译错误；
- **Java 的 `String`**：不可变，`substring` 现在是拷贝；
- **Python 的 `memoryview`**：类似，由引用计数保证安全。

**经验规则**：`string_view`/`span` **用作函数参数**，几乎总是安全且高效；**存储、返回、放入长寿对象**时要格外小心，通常应该存拥有数据的 `std::string`/`vector`。

**要记住的一点**：视图是借用，C++ 不会替你检查借期；类型名里的 "view" 提醒你它不拥有数据。
