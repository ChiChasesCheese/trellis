---
id: hl-c15-io-pitfalls
node: cpp-lessons.c15-io-performance
type: qa
step: 13
---
## Q
C++ 编程题 I/O 方面还有哪些常见的坑？

## A
1. `sync_with_stdio(false)` 之后混用 `printf` 和 `cout` → 输出顺序错乱。
2. `int` 读入大数溢出（读失败后流进入错误状态，后续读取全部失败）。
3. `stoi` 对 `"12abc"` 返回 12 且不报错；`from_chars` + 检查 `ptr == end` 才严格。
4. `getline` 读到的行可能带 `\r`。
5. 对 `unordered_map<string,...>` 用 `string_view` 做 key 时，要保证原字符串活着；不确定就存 `string`。
6. 用 `endl` 输出 10 万行。
