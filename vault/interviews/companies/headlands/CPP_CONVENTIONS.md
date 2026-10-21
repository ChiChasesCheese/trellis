# C++20 题集用法

Headlands 日常写 C++，面试官可以指定语言，所以高频题除了 Java 版还有 C++20 版（同样的 Part、同样的测试用例，外加 C++ 特有的边界）。

## 目录

```
loop/rounds/<轮次>/<id>/cpp/
  reference.hpp   参考实现（单头文件，命名空间里）
  starter.hpp     起点：类型和签名已给，函数体 throw std::logic_error("TODO")
  work.hpp        你的工作副本（start 命令从 starter.hpp 复制）
  test.cpp        测试，用 #include IMPL_HEADER 选择实现
  main.cpp        只有 stdin→stdout 的题有
  cases/*.in|out  main.cpp 的端到端样例
```

目前有 C++ 版的：`oa01_job_chain`、`hc02_merge_k_streams`、`hc03_recursive_sum`、`hc04_queue_mean_snapshot`、`hc05_market_order_book`、`hc07_ticker_hash_map`。

## 命令（在 kit 根目录跑）

```bash
python3 tools/cpptest.py start  loop/rounds/01_video/hc03_recursive_sum            # starter.hpp → work.hpp
python3 tools/cpptest.py run    loop/rounds/01_video/hc03_recursive_sum --tag part1  # 默认 --impl work
python3 tools/cpptest.py run    loop/rounds/01_video/hc03_recursive_sum --impl reference --exclude-tag perf -q
python3 tools/cpptest.py main   loop/rounds/00_oa/oa01_job_chain --impl reference < input.txt
python3 tools/cpptest.py verify "loop/rounds/*/*"   # 验收：reference 全绿，starter 编译且至少一个测试红
```

## 编译参数

`clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined -fno-sanitize-recover=undefined`。

* 最后一项让 UBSan 一发现未定义行为（比如有符号溢出）就终止进程；默认只打印、测试照样"绿"。
* 带 `perf` 标签的测试不在 sanitizer 版里跑（慢几倍，限时没意义）；工具另编一个 `-O2` 无 sanitizer 的二进制只跑它们。
* reference 用 `-Werror` 编译，starter / work 的警告只提示。
* 没有额外依赖：测试框架是 `tools/cpp/minitest.hpp`。

## 测试写法

```cpp
TEST(my_case, "part1,edge") {          // 第二个参数是逗号分隔的标签：partN / edge / fmt / io / conc / perf / cpp
    CHECK_EQ(f(1), 2);                 // 非致命；REQUIRE / REQUIRE_EQ 失败即终止该测试
    CHECK_THROWS_AS(f(-1), std::invalid_argument);
    CHECK_WITHIN_MS(2000, heavy(););   // 限时，放在 perf 测试里
}
MT_MAIN()
```

* 标签 `cpp` 标记只有 C++ 才有的边界（UB、移动后状态、悬空引用、from_chars 严格性……）。
* 测试里逗号会被宏拆开：`CHECK_EQ((Chain{1, 2, 3, 4}).x, 1)` 要多加一层括号。
* 栈溢出是信号不是异常：用 `mt::child_survives(fn)` 在子进程里验证；用 `mt::run_on_stack(bytes, fn)` 指定线程栈大小。
* `mt::i128("123…")` 解析十进制字符串，`mt::to_string(__int128)` 输出（libc++ 没有 `__int128` 的 `operator<<`）。

## 起点文件约定

* 公共类型与签名已给出，函数体抛 `std::logic_error("TODO")`；未使用的参数不写名字，免得警告。
* 异常类型（`std::out_of_range`、`std::invalid_argument`、各题自定义的异常）是接口的一部分，测试按类型检查。
