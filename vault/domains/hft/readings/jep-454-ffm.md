---
nodes: [java.off-heap, java-at-hft.interop, java.modern]
url: https://openjdk.org/jeps/454
---
# JEP 454：Foreign Function & Memory API

Java 22 正式发布的 API：安全地分配和访问堆外内存，以及不用 JNI 调用本地函数。

**读的时候提取：**
- Arena、MemorySegment、ValueLayout 的作用。
- 与 Unsafe 和 JNI 相比的改进。

%% trellis:begin %%
## Source
[Open the original ↗](https://openjdk.org/jeps/454)

## Archived copy
![[jep-454-ffm-clip]]
%% trellis:end %%
