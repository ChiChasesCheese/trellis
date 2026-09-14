---
id: leetcode-c-linux-epoll-interest-ready-application
node: topics.uncategorised
type: qa
anki: 1787359913193
tags: [algorithm::doubly-linked-list, algorithm::event-driven-queue, algorithm::red-black-tree, algorithm::state-machine, application, case, case::linux-epoll-interest-ready, category::runtimes-os, leetcode, system::linux-epoll]
---
## Q
Linux epoll 为什么同时需要 red-black tree、ready linked list 和 overflow list？

## A
red-black tree 保存长期 interest set，支持 epoll_ctl 的动态查找和更新；ready FIFO list 只保存当前就绪 fd，让 epoll_wait 不必扫描全部监控对象；扫描 ready list 期间到达的新事件先进入 overflow LIFO，结束后再恢复 FIFO 并回主 ready list，避免丢事件。

**Evidence**

Linux 官方 epoll(7) 区分 interest list 与 ready list；内核 fs/eventpoll.c 定义 rb_root_cached rbr、rdllist 和完整 Ready-list state machine。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fruntimes-os%2FLinux%20epoll%EF%BC%9A%E7%BA%A2%E9%BB%91%E6%A0%91%E7%AE%A1%E7%90%86%E5%85%B3%E6%B3%A8%E9%9B%86%E5%90%88%EF%BC%8C%E9%93%BE%E8%A1%A8%E4%BA%A4%E4%BB%98%E5%B0%B1%E7%BB%AA%E4%BA%8B%E4%BB%B6)
