---
id: pl-memana-found-go-heap
node: engineering.memory-analysis
type: qa
step: 2
---
## Q
Go 的堆剖析（heap profile）记录什么？`inuse_space` 和 `alloc_space` 有什么区别，各用来查什么问题？

## A
Go 运行时对堆分配做**采样**：默认平均每分配 512 KiB 记录一次调用栈（由 `runtime.MemProfileRate` 控制），并按分配点聚合。一份 heap profile 含两对指标：
- `inuse_space` / `inuse_objects`：当前仍然存活的字节与对象数（反映最近一次完成的 GC 时的状态）；
- `alloc_space` / `alloc_objects`：程序启动以来**累计**分配的字节与对象数，包含已被回收的。

用途不同：
- 查**泄漏**看 `inuse_*`：哪个分配点持续增长；
- 查**GC 压力**与过度分配看 `alloc_*`：即使对象马上被回收，大量分配也在消耗 CPU 并触发更频繁的 GC。

**例**：一个全局 `map` 缓存存了 3000 个 10 KB 切片、从不淘汰，另有一次 1 MiB 的临时分配。`go tool pprof -top`：

```text
-sample_index=inuse_space
  32.33MB 96.99%  main.handle (inline)
-sample_index=alloc_space
  32.33MB 93.74%  main.handle (inline)
   1.16MB  3.35%  main.main
```

那次 1 MiB 的临时切片已被回收，只出现在 `alloc_space`。

**线上用法**：`net/http/pprof` 暴露 `/debug/pprof/heap`，隔一段时间抓两份，用 `go tool pprof -base old.prof new.prof` 相减，只看增长部分。局限：Go 的 heap profile 只有分配点，没有对象引用图；要找持有者得读代码，或看 goroutine 剖析里是不是有卡住的 goroutine 在持有数据。
