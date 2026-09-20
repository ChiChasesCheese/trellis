---
nodes: [problems.social.instagram]
url: https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf
---
# Finding a Needle in Haystack: Facebook's Photo Storage

值得读：OSDI 2010 的学术论文，是"为什么海量小文件不能直接用传统文件系统存"这个问题
最权威的原始出处——传统 NAS/NFS 式存储读一张照片平均需要约 3 次磁盘 I/O（文件名转
inode、读 inode、读文件内容），Haystack 通过把每张照片的元数据压缩到可以整体常驻内存、
用大的追加写物理卷代替海量小文件，把这个数字降到接近 1 次磁盘 I/O。本题解「深入探讨」
的小文件存储一节引用了这个真实的问题背景和设计思路，但给出了和论文本身不同的落地结论：
本题解认为现代云对象存储已经在内部实现了类似的优化，多数系统不需要真的从零自建
Haystack，只有在极端规模或特殊成本约束下才值得考虑，并用本设计自己假设的字节数估算了
这两种索引方式的内存占用差距（约 6.4 倍）。
