---
id: hl-c15-selftest
node: cpp-lessons.c15-io-performance
type: qa
step: 14
---
## Q
自测：`std::from_chars` 返回什么？如何判断整个字符串都被解析？`cout << x << endl;` 与 `cout << x << '\n';` 的区别？

## A
- `from_chars` 返回 `from_chars_result{ptr, ec}`；整个字符串被解析的条件是 `ec == std::errc{}` **且** `ptr == last`。
- `endl` 比 `'\n'` 多一次**强制刷新**。
