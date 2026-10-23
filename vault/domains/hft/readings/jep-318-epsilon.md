---
nodes: [java.gc-choices, java.garbage-free]
url: https://openjdk.org/jeps/318
---
# JEP 318：Epsilon 无操作收集器

只分配不回收的 GC：用于性能测试、极短任务和完全无垃圾的程序。

**读的时候提取：**
- Epsilon 适用的场景。
- 堆用尽时会发生什么。

%% trellis:begin %%
## Source
[Open the original ↗](https://openjdk.org/jeps/318)

## Archived copy
![[jep-318-epsilon-clip]]
%% trellis:end %%
