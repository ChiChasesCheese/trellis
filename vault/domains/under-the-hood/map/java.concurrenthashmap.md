%% trellis:begin %%
# ConcurrentHashMap：CAS + 桶级锁
*Java 集合与并发工具*

Java 8 起不再分段：空桶用 CAS 放、非空桶锁住桶头；多线程协助扩容；size 用分散计数（LongAdder 思路）。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-java-concurrenthashmap-1-cas-lock]]
2. [[uth-java-concurrenthashmap-2-size]]
3. [[uth-java-concurrenthashmap-3-compound]]
%% trellis:end %%

## Notes
