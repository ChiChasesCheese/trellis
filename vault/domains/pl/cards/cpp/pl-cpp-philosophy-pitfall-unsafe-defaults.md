---
id: pl-cpp-philosophy-pitfall-unsafe-defaults
node: cpp.philosophy
type: qa
step: 9
---
## Q
C++ 的“默认值”在哪些地方偏向危险？一个带单参数构造函数的类会引发什么意外，应该怎么修？

## A
C++ 的默认值多半是“尽量允许”：向后兼容、也尽量少给程序员添麻烦，结果是**不显式声明就得到最宽松的行为**。典型默认项：
1. 单参数构造函数默认可用于**隐式转换**。
2. 局部变量默认**不初始化**，读取它是未定义行为。
3. 函数参数默认**按值拷贝**，大对象的拷贝悄悄发生。
4. `[]` 访问默认不检查越界。

**第一项的最小复现**：

```cpp
struct Meters { Meters(double v) : v(v) {} double v; };
void walk(Meters) {}
int main() {
  walk(3);       // 编译通过：3 被悄悄转换成 Meters
  int x{3.9};    // 花括号初始化拒绝窄化
}
```

`walk(3)` 通过编译，意图是“3 米”还是“3 步”完全由读代码的人猜。花括号初始化则会拒绝窄化，真实报错：`type 'double' cannot be narrowed to 'int' in initializer list`。

**修法**：
1. 单参数构造函数一律写 `explicit`，需要隐式转换才显式去掉；
2. 初始化统一用花括号 `{}`，窄化直接变成编译错误；
3. 用强类型代替裸 `double`（如 `std::chrono::seconds` 这类单位类型）。

**更一般的做法**：在项目里给“必须显式”的东西加规则，并让工具检查——`clang-tidy` 的 `google-explicit-constructor`、`-Wconversion`、`[[nodiscard]]`。

**根因**：这些默认值是为兼容 C 或 C++98 保留下来的，委员会不能改默认，只能让新写法更好用。所以资深 C++ 工程师的习惯是：**凡是语言默认放宽的地方，主动收紧**。
