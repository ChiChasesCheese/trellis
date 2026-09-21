---
id: len-bool-fallback-and-maxsize
node: model.dunder-protocols
type: qa
source: python-docs
---
## Q
一个自定义容器类只实现了 `__len__` 而没有实现 `__bool__`，在 `if container:` 这样的布尔上下文里解释器怎么判断真假？这对 `__len__` 的返回值有什么限制？

## A
没有 `__bool__` 时，解释器退回调用 `__len__()`：返回 0 被当作假（False），非零正整数被当作真（True）。这也是为什么在 CPython 里 `__len__()` 的返回值被要求不超过 `sys.maxsize`——超过这个上限，`len()` 等依赖它的功能可能抛出 `OverflowError`；要绕开这个限制，对象必须显式实现 `__bool__()`，不能只靠长度值判断真假。
