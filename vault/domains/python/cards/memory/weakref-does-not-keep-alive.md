---
id: weakref-does-not-keep-alive
node: memory.weakref
type: qa
source: python-docs
---
## Q
弱引用（weak reference）持有一个对象，会不会阻止这个对象被垃圾回收（garbage collection）？

## A
不会。弱引用不计入被引用对象（referent）的引用计数（reference count），当指向某个对象的所有强引用（普通引用）都消失、只剩弱引用时，垃圾回收器可以立即销毁这个对象并回收其内存；此后再通过这个弱引用取对象会得到 `None`（或触发相应异常），弱引用本身并不能让对象「多活一会儿」。
