---
id: amz-file-watcher-common-mistake-sleep-tests-and-first-scan-events
node: amazon.amz-file-watcher
type: qa
step: 9
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，常见的两个错误是什么？一个出在测试，一个出在第一次扫描。

## A
测试：创建真实文件再 `time.sleep(1)` 后断言，慢且偶尔失败；改为注入假文件系统（测试直接写每个文件的 mtime 与 size）并显式调用 `poll()`，线程测试用 `Event` 等「回调被调用了」。第一次扫描：把目录里已有的文件全报成 CREATED，订阅者被淹没；应让第一次 `poll()` 只建基线，监听开始前就存在的文件不算新建。
