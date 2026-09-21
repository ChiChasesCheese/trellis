---
id: free-threading-split-refcount
node: memory.refcounting
type: qa
source: cpython-internals
---
## Q
Python 3.13 自由线程（free-threading，PEP 703）构建下，对象头部为什么把单一的 `ob_refcnt` 拆成 `ob_ref_local`（本线程本地计数）和 `ob_ref_shared`（跨线程共享计数）两个字段？

## A
默认（带 GIL）构建里同一时刻只有一个线程在执行字节码，改写 `ob_refcnt` 不需要额外同步；自由线程构建没有 GIL，多个线程可能并发修改同一对象的引用计数，拆成本地计数与共享计数后，本线程发起的增减大多只需改本地字段，只有涉及跨线程引用时才需要对共享字段做原子操作，减少了同步开销。
