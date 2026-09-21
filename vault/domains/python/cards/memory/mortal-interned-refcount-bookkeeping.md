---
id: mortal-interned-refcount-bookkeeping
node: memory.interning-immortal
type: qa
source: cpython-internals
---
## Q
一个「非不朽（mortal）」的驻留字符串，被驻留字典（interned strings dict）同时当作 key 和 value 引用着，为什么它的引用计数（reference count）不会因为这两份引用而永远大于等于 2、导致无法被回收？

## A
CPython 故意把「驻留字典里 key 和 value 这两份引用」从该字符串的引用计数里排除（不计入 `ob_refcnt`）；当这个字符串在别处的引用计数真正归零时，析构函数（`unicode_dealloc`）会先把它从驻留字典里移除，再正常释放。解释器关闭（shutdown）、驻留字典被清空时，这两份被排除的引用才会被临时加回来，配合字典清空的流程正常走一遍释放。
