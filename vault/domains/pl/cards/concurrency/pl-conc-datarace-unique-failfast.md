---
id: pl-conc-datarace-unique-failfast
node: concurrency.data-race-freedom
type: qa
step: 7
---
## Q
4 个线程同时往一个普通的 Java `HashMap` 或 Go `map` 里写入，两门语言的反应有何不同？这反映了怎样的“出错哲学”？

## A
Java：
```java
Map<Integer,Integer> m = new HashMap<>();
Map<Integer,Integer> c = new ConcurrentHashMap<>();
// 4 threads, thread g writes keys g*100000 .. g*100000+99999
```
输出（两次运行都是这样，数字每次不同）：
```
HashMap size = 198457 (expected 400000)
ConcurrentHashMap size = 400000 (expected 400000)
```
`HashMap` 没有任何提示，悄悄丢了一半数据，遍历时还可能抛出异常；`ConcurrentHashMap` 用 CAS 加每个桶一把的锁，结果正确。

Go：
```go
m := map[int]int{}
for g := 0; g < 4; g++ {
    wg.Go(func() { for i := 0; i < 100000; i++ { m[i] = i } })
}
wg.Wait()
```
输出：`fatal error: concurrent map writes`，进程直接崩溃（不是 panic，无法 `recover`）。Go 的 map 里有一个写标志位，写入开始和结束时检查，发现另一个写者同时在写就立刻终止：宁可崩溃也不让带损坏的数据继续运行。这个检测是尽力而为的（best effort），不是保证，仍应使用 `sync.Mutex` 或 `sync.Map`。

哲学对比：Java 让错误悄悄发生（偶尔在迭代时抛 `ConcurrentModificationException`），数据坏了但程序继续跑；Go 选择快速失败（fail fast），宁可崩溃也不让坏数据扩散。对生产系统，崩溃加重启往往比悄悄返回错误数据好：前者被监控发现，后者可能几周后才被客户发现。Python 的 `dict` 在 GIL 保护下不会损坏结构，但多步骤的读-改-写仍需要锁。
