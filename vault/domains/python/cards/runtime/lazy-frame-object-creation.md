---
id: lazy-frame-object-creation
node: runtime.frames-eval
type: qa
source: cpython-internals
---
## Q
3.11 起，「帧对象」`PyFrameObject` 为什么说是惰性创建的？什么时候才会真的创建它？

## A
解释器真正操作的是内部轻量结构 `_PyInterpreterFrame`（存在 per-thread 栈上），只有当帧需要暴露给 Python 代码时——比如生成 traceback 或调用 `sys._getframe()`——才会额外创建一个堆分配的 `PyFrameObject`，把 `_PyInterpreterFrame` 的内容拷进去。绝大多数调用从不触发这一步，省掉一次堆分配，这是 3.11 帧相关性能优化的核心。
