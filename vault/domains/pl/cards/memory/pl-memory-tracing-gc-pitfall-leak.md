---
id: pl-memory-tracing-gc-pitfall-leak
node: memory.tracing-gc
type: qa
step: 10
---
## Q
有 GC 的语言还会内存泄漏吗？为什么，该怎么排查？

## A
会。GC 回收的是「不可达」的对象，而不是「不再需要」的对象。一个对象只要还被某个根间接引用着，哪怕程序永远不会再用它，也不会被回收。

典型成因：
1. 静态集合当缓存却从不淘汰。
2. 注册了监听器或回调却忘了取消注册。
3. `ThreadLocal` 在线程池里长期持有大对象。
4. Go 里永远阻塞的 goroutine（等待一个没人写入的 channel）：它的栈和栈上引用的所有对象都存活。

```java
static final Map<Integer, byte[]> CACHE = new HashMap<>();   // never evicted
for (int i = 0; ; i++) CACHE.put(i, new byte[1_000_000]);
```

`java -Xmx64m` 下实测：

```console
java.lang.OutOfMemoryError: Java heap space after 61 entries
```

多次 GC 之后堆仍然装不下，说明这些对象全是可达的，GC 无能为力。

排查思路：看 GC 日志里「回收后占用」是否逐轮上升；Java 用堆转储（heap dump）加 Eclipse MAT 之类的工具找「支配树」里最大的持有者；Go 用 `pprof` 的 heap 与 goroutine profile。修复通常是给缓存加容量上限（LRU）、用 `WeakReference`、或显式取消注册。
