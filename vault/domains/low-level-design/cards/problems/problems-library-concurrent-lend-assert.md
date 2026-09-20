---
id: problems-library-concurrent-lend-assert
node: problems.booking.library
type: qa
step: 8
tags: [grown]
---
## Q
图书馆管理（Library Management）里，十个读者同时借一个有三本副本的书目。并发测试该断言什么？只断言「恰好三笔借阅」够吗？

## A
**不够。**「恰好三笔」挡不住同一本副本被借出两次——那也是三笔。必须同时断言**三个条码互不相同**：

```python
assert len(loans) == 3, f"over-lent: {loans}"
assert len(set(loans)) == 3, f"same copy lent twice: {loans}"
assert desk.library.availability("T1") == 0
```

写法上用真线程 + `threading.Barrier` 让所有线程在同一时刻起跑，把竞态放大到可复现；断言的是**不变量**，不是时序，所以不会 flaky。

根因在于「算出空闲副本 + 写入借阅记录」是一个**复合操作**。Python 的 GIL 只保证单条字节码不被切开，`dict` 的一次读写是原子的，但这几百条字节码中间随时会切换线程——所以必须自己加锁，把查与占放进同一个临界区。
