---
id: problems-logger-handlers-tuple-and-gil
node: problems.components.logger
type: qa
step: 6
tags: [grown]
---
## Q
日志框架的分发路径（把记录交给本 logger 和所有祖先的 handler）每秒要跑很多次。把 handler 集合存成**元组**、增删时整体替换，为什么能让这条热路径一把锁都不用加？GIL 在这里帮了多少忙？

## A
因为"换一个新元组"是一次单纯的属性赋值：读者要么读到完整的旧元组、要么读到完整的新元组，不存在"遍历到一半列表被别人改了"。存成 `list` 再 `append`/`remove` 就必须给读者也加锁，否则遍历期间被修改会漏掉或重复。

GIL 帮的忙比多数人以为的少：它保证单条字节码不被切开，但 `self._dropped += 1` 是"读—加—写"三条字节码，中间随时可能切线程；`list.append` 恰好是原子的，但"append 之后检查长度再删最旧的"这个组合不是。**凡是"读出来—改—写回去"的复合操作，GIL 都不保护**，该加锁还得加锁。
