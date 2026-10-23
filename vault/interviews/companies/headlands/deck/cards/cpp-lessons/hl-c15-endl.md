---
id: hl-c15-endl
node: cpp-lessons.c15-io-performance
type: qa
step: 3
---
## Q
面试问：`std::endl` 和 `'\n'` 有什么区别？
Interview question: What is the difference between `std::endl` and `'\n'`?

## A
- `std::endl` = `'\n'` + **强制刷新**（flush）；刷新是系统调用级别的慢操作。
- 输出很多行时用 `'\n'`；用 `endl` 输出 10 万行是常见坑。
- `cerr` 不缓冲、写 stderr；调试信息放这里，别污染标准输出。
