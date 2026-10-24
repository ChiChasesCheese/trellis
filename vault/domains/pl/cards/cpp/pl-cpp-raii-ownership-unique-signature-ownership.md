---
id: pl-cpp-raii-ownership-unique-signature-ownership
node: cpp.raii-ownership
type: qa
step: 9
---
## Q
在 C++ 的函数签名里，参数类型怎样表达所有权？`T*`、`T&`、`unique_ptr<T>`、`shared_ptr<T>` 各自向调用者承诺什么？

## A
C++ 没有生命周期标注，所有权信息只能写进**参数和返回值的类型**，靠约定被所有人理解。常见的分工：

| 签名 | 含义 |
|---|---|
| `void f(const T&)` / `void f(T&)` | 借用，非空，调用期间有效；不存、不释放 |
| `void f(T*)` | 借用，**可以为空**，不拥有；"可选的借用" |
| `void f(std::unique_ptr<T>)` | 调用者把独占所有权**交给**函数（sink） |
| `std::unique_ptr<T> f()` | 函数把独占所有权**交给**调用者（工厂） |
| `void f(std::shared_ptr<T>)` | 函数要**共享**所有权，存下一份 |

**读法**：看到 `T*` 就默认不拥有、不 `delete`，需要所有权时用 `unique_ptr`。这套约定来自 Core Guidelines（R 与 F 章节）：裸指针和引用永远表示"非拥有"。

**例子**：
```cpp
void render(const Scene& s);              // 只看一眼
void attach(std::unique_ptr<Plugin> p);   // 接管 p
Widget* find(const Name& n);              // 可能没有；不要 delete 返回值
```
`attach(std::move(p))` 在调用点就能看到"所有权被交出去了"；`attach(p)` 编译不过，因为 `unique_ptr` 不能拷贝。

**与 Rust 对比**：Rust 的 `&T`、`&mut T`、`Box<T>`、`Rc<T>` 与上表一一对应，且 Rust 还有生命周期标注，编译器**强制**：函数声称借用，就不能存起来、也不能返回给更长寿命的地方。C++ 的同一规则靠约定，`f(T*)` 里拿着指针存进成员变量，编译器不会说话。

**哲学**：C++ 把"契约写在类型里"当作文档兼工具链基础，但**不强制**。这既是灵活（旧接口可以逐步重构），也是风险（旧代码里的裸指针语义不明）。

**要记住的一点**：阅读和审查 C++ 代码时，先看签名里每个指针/引用的所有权含义；新代码里把含义写进类型，不要留给注释。
