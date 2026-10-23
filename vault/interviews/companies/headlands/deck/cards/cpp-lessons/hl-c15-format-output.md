---
id: hl-c15-format-output
node: cpp-lessons.c15-io-performance
type: qa
step: 8
---
## Q
面试问：怎么把输出格式化为两位小数、左右对齐的列？`setprecision` 和 `setw` 的作用范围有何不同？
Interview question: How do you format output to two decimal places?

## A
```cpp
std::cout << std::fixed << std::setprecision(2);
for (const auto& [sym, pos] : net)
    std::cout << std::left << std::setw(6) << sym
              << std::right << std::setw(6) << pos
              << std::setw(12) << notional[sym] << '\n';
```
- `std::fixed << std::setprecision(2)` 控制小数位，对 `cout` **持续生效**；`std::setw` **只作用于下一个输出**。
- 其他写法：`printf("%.2f")`、`std::format("{:.2f}", x)`（C++20）、`snprintf`。
- 注意 `std::to_string` 对 `double` 固定 6 位。
- 例：输出 `AAPL      65    34715.00`。
