---
id: hl-c08-cpp20-library
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 12
---
## Q
C++20 标准库新增了哪些常用组件？指定初始化、模板 lambda 又是什么？

## A
- `std::span`：非拥有视图；`std::format`：类型安全格式化。
- `<bit>`：`popcount`、`bit_width`、`countl_zero`、`bit_ceil`（`bit_ceil(100)` = 128）、`bit_cast`。
- 并发：`jthread` / `stop_token`（可取消线程）、`latch`/`barrier`/`semaphore`、`atomic::wait`。
- `erase_if`：容器删除一行搞定。
- 语言：**指定初始化** `Config{.threads = 8}`；**模板 lambda**；`using enum`——可读性。
- 例：`popcount(0b1011)` = 3，`bit_width(255)` = 8。
