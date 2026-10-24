---
id: pl-cpp-raii-ownership-found-destructor-unwinding
node: cpp.raii-ownership
type: qa
step: 2
---
## Q
C++ 的析构函数（destructor）什么时候被调用？抛出异常时，已经创建的局部对象会怎样？

## A
**析构函数**写作 `~T()`，是随类型绑定的清理代码。编译器在每个**对象生命周期结束的点**自动插入对它的调用：
- 局部变量：离开其所在的花括号。
- 成员对象：外层对象析构时，按成员声明的**逆序**析构。
- 临时对象：完整表达式结束时。

规则：同一作用域内，**后构造的先析构**（栈式逆序）。这样后获取的资源（依赖前面的资源）先被释放。

**异常传播时**：抛出异常后，运行时沿调用栈逐层向外找 `catch`，这个过程叫栈展开（stack unwinding）。每离开一个栈帧，该帧里已构造完成的局部对象都会被析构。所以即使控制流被异常打断，RAII 对象仍会释放资源。实测：

```cpp
void work() { G a("file"); G b("lock"); throw std::runtime_error("boom"); }
```

输出依次是：`acquire file`、`acquire lock`、`release lock`、`release file`、`caught boom`。注意释放发生在 `catch` 执行**之前**，顺序与获取相反。

**对比**：Java 要写 `try-with-resources`、Go 要写 `defer`、Python 要写 `with`，都是在**每个使用点**重新声明释放；C++ 把它写进**类型**，使用点什么都不用写。这是 RAII 的本质优势：释放逻辑只写一次，在资源类里。

**一个限制**：析构函数默认是 `noexcept` 的。如果它在栈展开期间又抛出异常，程序会直接 `std::terminate`（两个异常无法同时处理）。所以析构函数里要吞掉或记录异常，不要抛出。

**要记住的一点**：析构的调用点由编译器插入，所以只要资源被包装进有析构函数的对象，无论函数怎样退出（正常、`return`、异常），都会释放。
