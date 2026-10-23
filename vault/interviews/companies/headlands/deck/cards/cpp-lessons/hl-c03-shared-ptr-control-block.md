---
id: hl-c03-shared-ptr-control-block
node: cpp-lessons.c03-smart-pointers
type: qa
step: 6
---
## Q
面试问：`shared_ptr` 怎么实现？拷贝要多少成本？线程安全吗？
Interview question: How is `shared_ptr` implemented, and is it thread-safe?

## A
- 由**两个指针**构成：指向对象，和指向**控制块**（control block，堆上一小块）。控制块存**强引用计数**、**弱引用计数**、删除器（和分配器）；`make_shared` 时对象本身也在里面。
- 拷贝 = 对强计数做**原子**加 1，析构 = 原子减 1，减到 0 才销毁对象。
- **计数本身线程安全**，但**指向的对象**不会因此线程安全。
- 同一个 `shared_ptr` **变量**被多线程读写需要同步（或用 `atomic<shared_ptr>`）；各线程持有各自的副本才安全。
- `sizeof(shared_ptr<T>)` 是 16 字节。
