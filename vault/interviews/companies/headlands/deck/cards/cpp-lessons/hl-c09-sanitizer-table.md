---
id: hl-c09-sanitizer-table
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 11
---
## Q
面试问：`-fsanitize=address`、`undefined`、`thread`、`memory` 分别抓什么？开销多大？怎么选？
Interview question: What do ASan, UBSan, TSan and MSan detect?

## A
- **ASan**（`address`）：越界、use-after-free、double free、栈/全局越界、new/delete 配对错误；开销约 2 倍；**与 TSan 不能同时开**。
- **UBSan**（`undefined`）：有符号溢出、移位、对齐、null、bool/enum 非法值、float→int 溢出等；开销很小。
- **TSan**（`thread`）：数据竞争、锁序问题；开销 5–15 倍；单独构建。
- **MSan**（`memory`）：读未初始化内存；仅 Linux/clang。
- `-Wall -Wextra -Werror`：编译期可发现的问题，开销 0，先把警告清零。

推荐开发命令：`clang++ -std=c++20 -O1 -g -Wall -Wextra -fsanitize=address,undefined`。
