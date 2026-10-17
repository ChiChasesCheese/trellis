---
nodes: [amazon.amz-file-watcher, patterns.observer, concurrency.primitives]
tags: [problem]
---
# Drill：文件监听器（File Watcher）

监听一个目录：里面的文件被新建、修改或删除时，调用你登记的回调；可以后台一直跑，也可以停。规模很小，但每一关都在检验同一件事：读磁盘、比对变化、通知订阅者是不是三件分开的事，能不能不靠睡眠就测试。
（报告里只有题名；以下各关全部是重建。）

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：`poll()` 拍一次目录快照，和上次比对，报告新建 / 修改 / 删除。第一次调用只建立基线。想清楚：指纹用什么（为什么不只是修改时间）、改名怎么算。
- 第 2 关（约 15 分钟）：多个订阅者、按事件种类订阅、可取消订阅；递归与否；按文件名过滤。读文件系统要藏在一个接口后面，测试里换成内存假实现。
- 第 3 关（约 15 分钟）：去抖（写到一半的文件不要报半截事件）；一个订阅者的回调抛异常，不能影响别人和下一轮监听。
- 第 4 关（选做）：`start(interval)` 开后台线程，`stop()` 停止；回调很慢、回调里调用 `stop()` 分别会怎样。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-file-watcher/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-file-watcher -q`。

**评分点**
- 开场问了通知还是轮询、递归与过滤、改名与半截文件（[[amz-file-watcher-how-asked-and-three-questions]]）。
- 读磁盘、比对、回调各有归属，比对是纯函数（[[amz-file-watcher-objects-and-their-jobs]]）。
- 第一次 `poll()` 只建基线（[[amz-file-watcher-stage1-poll-and-diff-in-code]]）。
- 指纹带上 size 并说得出剩余盲区（[[amz-file-watcher-snapshot-diff-mtime-and-size]]）。
- 选轮询并留出换成系统通知的接口（[[amz-file-watcher-decision-polling-vs-os-notification]]）。
- 去抖不用时钟（[[amz-file-watcher-followup-debounce-by-stability]]）。
- 回调在锁外、异常被隔离、失败记录有上限（[[amz-file-watcher-edge-callback-failure-isolation]]）。
- 用 `Event` 停线程，回调里 `stop()` 不 join 自己（[[amz-file-watcher-concurrency-callback-thread-and-stop]]）。
- 测试不靠睡眠（[[amz-file-watcher-common-mistake-sleep-tests-and-first-scan-events]]）。

**题解**：[[solution-amz-file-watcher]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
