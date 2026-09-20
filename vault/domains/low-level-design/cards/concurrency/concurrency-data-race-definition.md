---
id: concurrency-data-race-definition
node: concurrency.model
type: cloze
---
**data race（数据竞争）** 指两个线程访问同一个内存位置，其中{{c1::至少有一个访问是写}}，并且{{c2::没有任何同步（happens-before 边）为这两次访问定序}}。有 race 的程序不只是"偶尔读到旧值"——编译器和 CPU 可以自由地{{c3::重排并缓存这些访问}}，所以行为是未定义的、任意的，而不只是陈旧。
