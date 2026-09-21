---
id: interning-is-implementation-detail
node: model.names-objects
type: qa
source: cpython-internals
---
## Q
为什么不能依赖字符串驻留（interning）或小整数缓存来判断两个值是否相等，而要始终用 `==`？

## A
驻留和缓存只是 CPython 用来加速字典查找、减少内存分配的实现细节（implementation detail），哪些对象会被驻留（短标识符、编译期常量、小整数）依赖具体实现和版本；未命中这些优化路径的相同内容对象身份并不相同。用 `is` 判断值相等在少数场景恰好「能跑」，但不是语言规范保证的行为，换一种构造方式就会失效。
