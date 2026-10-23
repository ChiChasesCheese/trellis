---
id: hl-j17-thread-shared-cost
node: java21.j17-ffm-api
type: qa
step: 19
---
## Q
什么时候该用 `Arena.ofShared()` 而不是 `ofConfined()`？`ofShared().close()` 有什么代价？

## A
- `ofConfined` 的 segment 被别的线程访问抛 `WrongThreadException`。测试框架换线程时（如 JUnit 超时断言在别的线程运行）、或多个线程要共享同一块堆外内存时，用 `ofShared`。
- 代价：`ofShared().close()` 比较慢，关闭时需保证没有其他线程正在访问，JVM 要握手（类似安全点）。**别在热路径反复开关 shared arena**。`ofConfined` 略快。
