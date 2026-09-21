---
id: gil-who-releases
node: concurrency.gil
type: qa
source: python-docs
---
## Q
哪些情况下 GIL 会被主动释放，从而让另一个线程运行？

## A
两类：① 阻塞式系统调用之前，如文件 I/O、网络 I/O、`time.sleep`——线程在发起调用前释放 GIL，等待期间其他线程可执行；② C 扩展在纯 C 计算区域内可显式释放 GIL（如 NumPy 的数值内核、部分正则匹配），只在需要操作 Python 对象时重新获取。这也是线程能有效隐藏 I/O 延迟、但对纯 Python 计算无效的原因。
