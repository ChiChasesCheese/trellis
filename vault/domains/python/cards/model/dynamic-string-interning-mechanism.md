---
id: dynamic-string-interning-mechanism
node: model.names-objects
type: qa
source: cpython-internals
---
## Q
除了那些静态单例，CPython 如何驻留运行时动态分配的字符串（例如程序里出现的标识符）？这与单例驻留在生命周期上有何不同？

## A
动态字符串被驻留时会加入解释器级别的字典 `PyInterpreterState.cached_objects.interned_strings`，字典的键和值指向同一对象；当该字符串引用计数归零触发析构时，析构函数会先把它从驻留字典里移除。单例则在运行时初始化时一次性建立，永不移除，直到解释器关闭才清空。
