---
id: hl-c16-error-syntax-include
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 9
---
## Q
编译器报 `expected ';' after struct` 和 `no member named 'accumulate' in namespace 'std'` 分别说明什么？

## A
- `error: expected ';' after struct`：**类/结构体定义后缺分号**（`struct Point { int x, y; }` 末尾要 `;`）。
- `error: no member named 'accumulate' in namespace 'std'`：几乎一定是**缺头文件**，这里要 `#include <numeric>`。
- 同理：`setw` → `<iomanip>`，`sort` → `<algorithm>`。
