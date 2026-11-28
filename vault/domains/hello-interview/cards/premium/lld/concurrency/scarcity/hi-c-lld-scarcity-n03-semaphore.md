---
id: hi-c-lld-scarcity-n03-semaphore
node: lld.concurrency.scarcity.notes
type: qa
step: 3
---
## Q
**并发稀缺资源 · 信号量**｜摘要 · 必会

信号量怎么工作？什么场景下它是首选，面试里怎么说？

## A
- **机制：** 带许可数 N 的计数器；`acquire` 减一，`release` 加一，为零时下一个 `acquire` 阻塞
- **类比：** 夜店容量 100，保安手上 100 个令牌，拿到才能进，离开时归还
- **场景：** 没有真实资源对象，只需保证最多 N 个操作同时进行，例如外部接口最多 5 个并发请求
- **Python：** `with self._semaphore:` 进入获取、退出释放，异常也释放
- **被问怎么阻塞：** 用操作系统原语让线程睡眠，释放时唤醒；不用自己实现
