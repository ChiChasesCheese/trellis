---
id: pl-cpp-errors-found-exceptions
node: cpp.errors
type: qa
step: 2
---
## Q
C++ 的异常（exception）怎样抛出和捕获？按值捕获为什么是错的，`throw;` 又是什么？

## A
**基础**：`throw 表达式` 抛出任意类型的对象（实践中几乎总是 `std::exception` 的派生类，如 `std::runtime_error`）。`try { ... } catch (类型 变量) { ... }` 捕获。抛出后，控制流跳出当前函数，沿调用栈向外逐层展开，每层的局部对象被析构，直到遇到类型匹配的 `catch`；一路上没有匹配的，调用 `std::terminate`，程序终止。

**异常对象是被拷贝出来的**：`throw MyErr("disk full")` 会在专用内存里构造一个异常对象，`catch` 引用到它。`catch` 按声明顺序匹配，**第一个能接受的就生效**，所以要把派生类放在基类前面。

**按值捕获会"切片"**。本机实测：

```cpp
struct MyErr : std::runtime_error { using std::runtime_error::runtime_error; int code = 7; };
try { f(); } catch (std::exception e)       { /* 按值 */ }
try { f(); } catch (const std::exception& e) { /* 按引用 */ }
```

按值捕获时 `e.what()` 打印的是 `std::exception`，原来的消息 `disk full` 丢了，动态类型也丢了（只剩基类部分）；按 `const&` 捕获时，`what()` 得到 `disk full`，`dynamic_cast<const MyErr*>(&e)` 成功。**规则：永远按 `const&` 捕获。**

**`throw;`（不带表达式）**：在 `catch` 块里重新抛出**同一个**异常对象，保留动态类型。实测：

```cpp
try { try { f(); } catch (...) { log("rethrow"); throw; } }
catch (const MyErr& e) { /* e.code == 7 */ }
```

外层仍能捕获 `MyErr`，`code` 为 7。如果写 `throw e;` 则会拷贝并按静态类型抛出，同样发生切片。

**与其他语言的对应**：
- Java 用 `try/finally`、`try-with-resources` 清理资源；C++ 不需要 `finally`，清理写在析构函数里；
- Python 的 `try/except/finally` 同样需要显式清理；
- Go 和 Rust 的 `Result` 不用栈展开。

**要记住的一点**：C++ 异常的清理靠析构函数，所以"异常安全"其实就是"资源都被 RAII 对象持有"；捕获永远用 `const&`。
