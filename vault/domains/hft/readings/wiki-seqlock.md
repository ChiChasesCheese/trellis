---
nodes: [cpp.spsc-seqlock]
url: https://en.wikipedia.org/wiki/Seqlock
---
# 顺序锁（seqlock）

写者递增序号、读者比对前后序号的读写同步机制，读者永不阻塞写者。

**读的时候提取：**
- 读者如何发现读到了半新半旧的数据。
- 为什么写者必须唯一。

%% trellis:begin %%
## Source
[Open the original ↗](https://en.wikipedia.org/wiki/Seqlock)

## Archived copy
![[wiki-seqlock-clip]]
%% trellis:end %%
