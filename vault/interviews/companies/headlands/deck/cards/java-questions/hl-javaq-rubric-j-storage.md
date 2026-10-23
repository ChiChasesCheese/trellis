---
id: hl-javaq-rubric-j-storage
node: java-questions.rubric
type: qa
step: 14
---
## Q
回答存储（fsync、mmap、B 树 vs LSM、复制）的问题时，强、一般、弱的答案各有什么特征？

## A
- **强**：`write` 只到 page cache，`fsync` / `force` 才耐久；每条 fsync vs 组提交的数量级差（约 900 倍 vs 约 4 倍）及原因；WAL、顺序写、预分配；mmap 的收益与坑（缺页尾延迟、unmap、2 GB、错误语义）；B 树 vs LSM 的读写放大权衡；复制 / 共识的延迟代价；能把存储选型与"研究数据一次写多次读"联系起来。
- **一般**：知道 fsync 慢、知道 LSM 写快，但说不出为什么，或不会谈一致性与复制。
- **弱**：认为 `write` 返回即持久；认为 mmap 总是更快；把 CAP 当口号。
