---
id: except-as-name-deleted-to-break-refcycle
node: runtime.exceptions
type: qa
source: cpython-internals
---
## Q
`except E as e: ...` 结束时，`e` 这个名字为什么会被自动删除？不删除会有什么后果？

## A
因为异常对象上挂着回溯（traceback），回溯又引用了触发异常的栈帧，栈帧又引用了自己的局部变量——如果 `e` 一直存在，就会形成「异常对象→回溯→帧→局部变量里的 e」这样一个引用环。CPython 在 except 子句结束时自动做等价于 `del e` 的清理，把这个环在源头掐断，让这些帧不用等到下一次垃圾回收循环检测才能被释放；这也是为什么把异常对象存到 except 块外的变量里，出了 except 块立刻变成 `NameError`。
