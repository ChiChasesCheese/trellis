---
id: storage-btree-branching-depth
node: storage.internals.btree
type: cloze
---
A B-tree stores data in fixed-size pages (commonly 4KB), each internal page holding hundreds of child references — a branching factor of {{c1::~500}} is typical. Depth therefore grows with the *logarithm* of row count, so almost every real table fits in {{c2::3–4}} levels: with 4KB pages and 500-way branching, a 4-level tree already addresses about {{c3::256 TB}}. Practical consequence: a point lookup costs at most depth page reads, and since the root and inner levels are a tiny fraction of the tree they stay cached — usually leaving {{c4::one disk read (the leaf page)}} per lookup.

## zh
B-tree 把数据存在固定大小的页面里（常见 4KB），每个内部页面持有数百个子页面引用 — 典型的分支因子（branching factor）约为 {{c1::~500}}。因此深度随行数的*对数*增长，几乎所有真实的表都能装进 {{c2::3–4}} 层：4KB 页面、500 路分支下，4 层的树已经能寻址约 {{c3::256 TB}}。实际后果：一次点查最多花费"深度"次页面读取，而根和内层页面只占整棵树的极小部分、始终留在缓存中 — 通常每次查找只剩 {{c4::一次磁盘读取（叶子页面）}}。
