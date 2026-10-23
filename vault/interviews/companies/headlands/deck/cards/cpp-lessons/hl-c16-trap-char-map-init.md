---
id: hl-c16-trap-char-map-init
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 15
---
## Q
`'a' + 1`、`s + 'c'`（`s` 是 `std::string`）的类型分别是什么？`map` 的 `m["x"]` 查询有什么副作用？`vector<int>(3,7)` 与 `vector<int>{3,7}` 的区别？未初始化的 `int` 呢？

## A
- `'a' + 1` 是 **`int`**（98）；要得到字符用 `static_cast<char>('a' + 1)`。`s + 'c'` 才是字符串拼接得 `"abc"`。`'7' - '0'` 得数字 7。
- `m["x"] == 0` 会**插入**键，`size()` 变 1；只查用 `find` / `count` / `contains`。
- `vector<int> a(3, 7)`：3 个元素，都是 7；`vector<int> b{3, 7}`：2 个元素 3 和 7（花括号优先选 `initializer_list` 构造）。
- `int uninit;` 值不确定，读它是 UB；`int zero{};` 值初始化为 0。
