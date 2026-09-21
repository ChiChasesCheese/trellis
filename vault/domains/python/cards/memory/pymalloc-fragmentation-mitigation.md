---
id: pymalloc-fragmentation-mitigation
node: memory.allocator
type: qa
tags: [grown]
source: python-docs
---
## Q
pymalloc 的这种「按 arena/pool/block 分层、arena 只有全空才释放」的设计，主要代价是什么？工程上通常怎么缓解？

## A
代价是内存碎片化（fragmentation）：只要某个 arena 里散落着极少数存活对象，整个约 1 MiB 的 arena 就无法归还操作系统，导致进程实际占用的内存明显高于「存活对象理论上需要的内存」。工程上常见的缓解手段是避免长期持有大量生命周期参差不齐的小对象（例如用完即弃的缓存要设过期/上限），或者干脆定期重启长驻 worker 进程，让操作系统直接收回整个进程的内存。
