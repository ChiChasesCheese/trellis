---
id: pl-sig-cpp-pitfall-silent-surprises
node: signatures.cpp
type: qa
step: 9
---
## Q
新手与有经验的工程师在 C++ 里最常见的陷阱是什么？这些陷阱有什么共同的结构？

## A
**陷阱一：未定义行为静默通过**。越界读 `v[10]` 在本机普通构建里输出 `0`，没有崩溃；`x + 1 > x` 在 `-O0` 为 `false`、`-O2` 为 `true`；检查溢出的 `x + 1 < x` 在 `-O2` 下被编译成 `return false`。**对策**：sanitizer、加固库、事前检查。

**陷阱二：悬垂的借用**。`std::string_view sv = name();` 指向即将销毁的临时字符串；容器扩容后旧迭代器；lambda 按引用捕获局部变量后逃出函数，本机 `-Wall -Wextra` 无警告，运行时随优化级别打印 `42` 或 `2`。**对策**：视图只在局部使用，逃逸的 lambda 按值捕获，ASan 加 `detect_stack_use_after_return=1`。

**陷阱三：看似只读的操作其实在修改**。

```cpp
std::map<std::string, int> stock{{"apple", 3}};
if (stock["pear"] == 0) { /* 缺货 */ }     // [] 在键不存在时插入
```

实测之后 `stock.size()` 是 2：**读取悄悄插入了一个键**。要只读查找用 `find` 或 `contains`。

**陷阱四：有符号与无符号混合比较**。

```cpp
int i = -1; std::vector<int> v{1, 2, 3};
println("{}", i < v.size());     // 输出 false
```

`i` 被转成无符号的 `size_t`，变成巨大的数。编译器警告：`comparison of integers of different signs [-Wsign-compare]`。**对策**：开 `-Wall -Wextra`，用同号类型或显式转换。

**陷阱五：拷贝与移动的静默代价**。`auto x = v[0]` 拷贝；`for (auto s : strings)` 每次拷贝；没有 `noexcept` 的移动构造让 `vector` 扩容改为拷贝，实测慢约 2 倍。

**陷阱六：构建与链接的静默问题**。同名 `inline` 函数在不同文件定义不同，`-O0` 与 `-O2` 结果不同，没有报错；静态初始化顺序跨文件不确定，链接顺序一变结果就变。

**陷阱七：并发中的隐形竞争**。把 `release/acquire` 改成 `relaxed`，本机 2 万轮测试全部通过，TSan 却报 `data race`。

**共同的结构**：它们都是**编译器接受、程序能运行、结果看似合理，但依赖未写明的假设**（范围、寿命、符号、定义）。C++ 默认信任你，而你的假设不总是对的。

**防御的统一框架**：
1. 警告全开并当作错误；
2. 在 CI 里把 ASan/UBSan/TSan 变成常规任务；
3. 用类型表达约束（`span`、`optional`、强类型、`explicit`、`[[nodiscard]]`）；
4. 代码评审时按“范围、寿命、符号、定义”四项检查。

**要记住的一点**：在 C++ 里，“能运行”和“正确”之间的距离，比其他语言长得多；工具链是你缩短这段距离的主要手段。
