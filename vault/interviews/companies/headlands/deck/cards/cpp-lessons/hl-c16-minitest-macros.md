---
id: hl-c16-minitest-macros
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 23
---
## Q
这套 C++ 题的测试怎么写？`TEST` 的标签、`CHECK_EQ` 与 `REQUIRE_EQ`、`CHECK_THROWS_AS`、`CHECK_WITHIN_MS` 各是什么？

## A
```cpp
TEST(my_case, "part1,edge") {          // 第二个参数是逗号分隔的标签
    CHECK_EQ(f(1), 2);                 // 非致命
    CHECK_THROWS_AS(f(-1), std::invalid_argument);
    CHECK_WITHIN_MS(2000, heavy(););   // 限时，放在 perf 测试里
}
MT_MAIN()
```
- 标签：`partN` / `edge` / `fmt` / `io` / `conc` / `perf` / `cpp`；`cpp` 标记只有 C++ 才有的边界（UB、移动后状态、悬空引用、`from_chars` 严格性……）。
- `CHECK_*` 非致命；`REQUIRE` / `REQUIRE_EQ` 失败即终止该测试。
