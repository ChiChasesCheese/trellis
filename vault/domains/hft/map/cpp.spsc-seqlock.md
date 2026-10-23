%% trellis:begin %%
# SPSC 环形队列与 seqlock
*低延迟 C++*

单生产者单消费者环形缓冲区（ring buffer）只靠两个原子下标就能无锁工作；seqlock 让一个写者、多个读者无锁共享一份数据。

**Requires:** [[domains/hft/map/cpp.atomics|std::atomic 与 memory_order]], [[domains/hft/map/machine.false-sharing|伪共享（false sharing）]]

## Readings
- [[lmax-disruptor-paper|LMAX Disruptor 技术论文]]
- [[rigtorp-ringbuffer|Optimizing a ring buffer for throughput]]
- [[wiki-seqlock|顺序锁（seqlock）]]

## Cards (4)
1. [[hft-cpp-spsc-seqlock-no-cas]]
2. [[hft-cpp-spsc-seqlock-cache-line-padding]]
3. [[hft-cpp-spsc-seqlock-seqlock]]
4. [[hft-cpp-spsc-seqlock-misuse]]
%% trellis:end %%

## Notes
