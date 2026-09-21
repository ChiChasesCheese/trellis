---
id: threads-local-vs-slots
node: concurrency.threads
type: qa
source: python-docs
---
## Q
`threading.local` 提供“线程局部存储”，为什么给它的子类加上 `__slots__` 会破坏这个隔离？

## A
`threading.local` 的隔离机制作用在实例的 `__dict__` 上：每个线程访问同一个 `local` 对象时看到的是自己独立的属性字典。但 `__slots__` 定义的属性不经过 `__dict__`，而是直接存储在对象本身，因此这些槽位属性是所有线程共享的普通属性，对它们的并发读写不再具有线程隔离，反而可能引入竞态。
