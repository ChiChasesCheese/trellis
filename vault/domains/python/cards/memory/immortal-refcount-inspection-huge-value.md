---
id: immortal-refcount-inspection-huge-value
node: memory.interning-immortal
type: qa
source: cpython-internals
---
## Q
3.12 起，对一个不朽对象（如 `None`）调用 `sys.getrefcount()`，看到的值和一个普通（非不朽）对象比会有什么明显不同？

## A
会看到一个非常大、几乎不会变化的数字，而不是随代码里对它的引用数量正常增减的小整数：因为该对象的引用计数被固定在一个特殊的巨大标记值上，`Py_INCREF`/`Py_DECREF` 对它不再做真实的加减操作，所以看到的值不能再被当作「这个对象实际被引用了多少次」来解读。
