---
id: pl-cpp-errors-pitfall-throwing-destructor
node: cpp.errors
type: qa
step: 10
---
## Q
C++ 异常处理在生产里最危险的陷阱是什么？析构函数抛异常、异常逃出 `noexcept`、吞掉异常，分别会发生什么？

## A
**陷阱一：析构函数抛出异常，直接终止进程**。析构函数默认就是 `noexcept` 的，在里面抛出且没有在内部捕获，会终止进程。本机真实输出：

```cpp
struct Bad2 { ~Bad2() { throw std::runtime_error("from dtor"); } };
int main() { try { Bad2 b; } catch (...) { println("caught"); } }
```

编译器警告：`'~Bad2' has a non-throwing exception specification but can still throw`。运行时输出：`libc++abi: terminating due to uncaught exception of type std::runtime_error: from dtor`，`catch (...)` 没有机会运行。即使把析构函数标成 `noexcept(false)`，**在栈展开过程中**又从析构函数抛出，也会终止（同时存在两个异常，C++ 无法处理）。**对策**：析构函数里只做不会失败的事，失败就记录日志或吞掉；需要报告失败的清理，提供单独的 `close()` 函数。

**陷阱二：异常逃出 `noexcept` 函数**：直接终止，外层的 `catch` 没有机会运行。症状是线上进程突然消失，只留下一行终止信息。

**陷阱三：`catch (...) {}` 吞掉所有异常**。错误悄悄消失，程序继续在损坏的状态上运行。**对策**：只捕获你能处理的具体类型；在边界处捕获后必须记录日志。

**陷阱四：按值捕获造成切片**：`catch (std::exception e)` 丢失派生类的消息（`what()` 变成 `std::exception`）。**对策**：永远 `const&`。

**陷阱五：异常跨越线程或 C 边界**：线程函数里未捕获的异常会终止整个进程；C 回调里抛出是未定义行为。**对策**：在每个线程入口和每个回调外层写 `try/catch`，把异常转换成错误码或 `std::exception_ptr` 传回。

**陷阱六：忽略返回值**：错误码和 `expected` 没有被检查。**对策**：`[[nodiscard]]`。

**共同的根因**：异常是隐式的控制流，错误处理代码的位置和执行条件不在被审查的那一行附近。

**要记住的一点**：C++ 里"异常安全"是整个代码库的属性，一个违反规则的析构函数就足以让整个进程终止。
