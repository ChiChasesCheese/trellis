---
id: hl-c15-mix-cin-getline
node: cpp-lessons.c15-io-performance
type: qa
step: 9
---
## Q
`cin >> n; getline(cin, line);` 读到什么？怎么修？

## A
- `>>` 读完 `n` 后会把**换行留在流里**，下一个 `getline` 立刻读到这个换行，`line` 是**空串**。
- 修法：先 `cin >> std::ws` 或 `cin.ignore()` 吃掉换行，或者统一都用 `getline` 再解析。
- 另一个相关坑：`getline` 读到的行可能带 `\r`（Windows 换行）。
