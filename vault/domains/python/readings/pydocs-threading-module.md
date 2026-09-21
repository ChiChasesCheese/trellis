---
nodes:
- concurrency.threads
- concurrency.locks-races
- concurrency.gil
title: threading 模块：线程、锁与同步原语
corpus: python-docs
section: 22-threading
url: https://docs.python.org/3/library/threading.html
tags:
- canonical
---

# threading 模块：线程、锁与同步原语

threading 模块的官方参考，重点在两处：一是 GIL 与性能考量一节直接讨论了在有 GIL 的构建下，多线程能有效隐藏 I/O 等待延迟，但对 CPU 密集型代码几乎没有加速甚至因为锁争用而变慢；二是完整的同步原语家族，Lock（互斥锁）、RLock（可重入锁，同一线程可重复获取）、Condition（配合锁实现等待/通知，典型用于生产者消费者模式）、Semaphore（限制同时访问资源的数量）、Event（一次性广播信号）、Barrier（等待固定数量线程都到达某点再一起放行）。文档强调这些同步对象都支持 with 语句自动获取/释放，减少忘记 release() 导致死锁的风险。读完能准确区分该用哪种同步原语，而不是所有场景都无脑用一把 Lock。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/threading.html)

## Archived copy
![[pydocs-threading-module-clip]]
%% trellis:end %%
