---
id: hl-c15-eof-bug
node: cpp-lessons.c15-io-performance
type: qa
step: 12
---
## Q
为什么 `while (!cin.eof()) { cin >> x; ... }` 是 bug？正确写法是什么？

## A
- EOF 标志只在一次读取**失败**之后才设置，最后一次读取失败后，循环体还会被执行一遍，处理到一个无效的 `x`。
- 正确写法：`while (cin >> x)`；读行用 `while (std::getline(std::cin, line))`。
- 相关：`int` 读入大数溢出时流进入错误状态，后续读取全部失败；用 `long long`，必要时检查 `cin.fail()`。
