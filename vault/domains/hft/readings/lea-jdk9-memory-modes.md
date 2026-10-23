---
nodes: [java.memory-model, cpp.atomics]
url: https://gee.cs.oswego.edu/dl/html/j9mm.html
---
# Using JDK 9 Memory Order Modes

VarHandle 的 plain、opaque、release/acquire、volatile 四种模式各保证什么、何时用。

**读的时候提取：**
- 四种模式由弱到强的保证。
- release/acquire 足以实现单生产者消息传递。

%% trellis:begin %%
## Source
[Open the original ↗](https://gee.cs.oswego.edu/dl/html/j9mm.html)

## Archived copy
![[lea-jdk9-memory-modes-clip]]
%% trellis:end %%
