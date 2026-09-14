%% trellis:begin %%
# 不同键（dual-heap-shared-mutable-object-sync）
*设计与模拟（design / simulation）*

当需要用两把按 不同键 排序的堆维护同一批会被部分消耗或过期的元素时，应考虑让两把堆共享同一个 可变对象 的引用，而不是各自存值。

## Cards (3)
- [[leetcode-c-endlesscheng-7c1ifr-dual-heap-shared-mutable-object-sync-invariant]]
- [[leetcode-c-endlesscheng-7c1ifr-dual-heap-shared-mutable-object-sync-recognition]]
- [[leetcode-c-endlesscheng-7c1ifr-dual-heap-shared-mutable-object-sync-template]]
%% trellis:end %%

## Notes
