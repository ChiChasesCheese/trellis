---
id: pl-cpp-undefined-behavior-best-practice
node: cpp.undefined-behavior
type: qa
step: 7
---
## Q
资深 C++ 工程师怎样系统地对付 UB？编译选项、写法与测试各该做什么，什么时候用 `-fwrapv`？

## A
**防御分四层**：

1. **编译选项**：`-Wall -Wextra -Wconversion -Wshadow`，把警告当错误；`-D_GLIBCXX_ASSERTIONS` 或 libc++ 的加固模式，让容器的 `operator[]` 在越界时终止程序；生产构建可加 `-fstack-protector-strong`、`-D_FORTIFY_SOURCE=2`。
2. **写法**：
   - 变量一律就地初始化：`int x = 0;`，不要先声明后赋值；
   - 容器与 `std::span` 代替裸指针加长度；需要检查的地方用 `.at()`，或自己写显式判断；
   - 类型转换用 `static_cast`，不要用 C 风格 `(int)x`；
   - 算术检查用**事前条件**：`if (x == INT_MAX)`，而不是事后 `x + 1 < x`（后者会被优化器删除）；
   - 类型双关用 `std::bit_cast` 或 `memcpy`，不用指针强转；
   - 构造函数里不要抛异常到半构造的状态；
3. **测试**：CI 里至少一轮 `-fsanitize=address,undefined`，另一轮 `-fsanitize=thread`；用 libFuzzer 对解析输入的代码做模糊测试；
4. **设计**：校验放在系统边界，内部用 `assert` 表示前置条件（调试构建启用）。

**`-fwrapv` 什么时候用**：它让有符号溢出变成回绕（有定义），去掉相关优化假设。适合：遗留代码里大量依赖溢出回绕，无法一时清理；或安全敏感程序，宁可慢一点也要确定行为（Linux 内核和一些大型代码库就这么做）。**代价**：丢掉有符号循环变量的部分优化，常见影响很小（常见是百分之几以内）；但它让 UB 变成 bug，而不是消除 bug，仍需修正。

**什么时候打破规则**：热路径上的越界检查可能影响性能，此时先用 sanitizer 证明代码在测试中从不触发，再对该处去掉检查，并留下注释说明依据的不变量。

**为什么这样**：UB 无法靠"小心"消除，只能靠多层机器检查叠加；每一层都不完整，叠起来才够用。
