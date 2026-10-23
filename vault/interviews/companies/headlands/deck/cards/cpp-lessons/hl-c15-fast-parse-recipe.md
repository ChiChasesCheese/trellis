---
id: hl-c15-fast-parse-recipe
node: cpp-lessons.c15-io-performance
type: qa
step: 11
---
## Q
面试问：怎么最快地解析大文本里的数字？
Interview question: How do you parse numbers from large input as fast as possible?

## A
- **一次读入缓冲区**：`std::istreambuf_iterator<char>` 构造 `string`，或循环 `fread` 到缓冲区。
- 用 `from_chars` 或手写状态机解析。
- 避免流、`string` 分配、locale。
- 用 `string_view` 切分。
- 输出：先 `std::string out; out.reserve(n);` 拼接，最后写一次。
- 复杂度提醒：`string` 的 `+` 在循环里拼接是 O(n²)；`+=` / `append` 摊销 O(1)。
