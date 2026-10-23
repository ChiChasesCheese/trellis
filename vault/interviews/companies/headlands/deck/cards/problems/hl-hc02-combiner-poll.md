---
id: hl-hc02-combiner-poll
node: problems.hc02-merge-k-streams
type: qa
step: 14
---
## Q
`ConcurrentMerge` 的合并核心 `Combiner.poll(block)` 怎么写？为什么遇到 `null` 要继续循环、选最小时用严格小于？

## A
```java
Poll<T> poll(boolean block) throws InterruptedException {
    boolean pending = false;
    for (int i = 0; i < queues.size(); i++) {
        if (finished[i] || heads.get(i) != null) continue;
        Msg<T> m = block ? queues.get(i).take() : queues.get(i).poll();
        if (m == null) { pending = true; continue; }
        switch (m) {
            case Item<T> item -> heads.set(i, item);
            case End<T> _ -> finished[i] = true;
            case Failed<T>(var cause) -> throw new MergeException(i, cause);
        }
    }
    if (pending) return new Pending<>();
    // 选最小：h.value().compareTo(best.value()) < 0 才替换
}
```
- 对每条「活着但没队首」的流取一条消息；阻塞版 `take()`，非阻塞版 `poll()`（空则 `null`）。
- `m == null` 记为 pending 但**继续循环**，别的流的 `Failed` 才不会被漏掉。
- `switch` 对 sealed 的 `Msg` 穷尽，终止标记不会被漏处理。
- **严格小于**才替换，相等保留编号小的，保证稳定。
- 选最小是 k 个候选线性扫描 O(k)；换堆也省不了，因为每次 `poll` 都要检查是否所有流都有队首（面试提一下这个取舍）。
