---
id: problems-in-memory-file-system-no-shared-base-class
node: problems.components.in-memory-file-system
type: qa
step: 1
tags: [grown]
---
## Q
设计一个内存文件系统时，组合模式（Composite）的教材写法通常给 `File` 和 `Directory` 一个共同基类 `Node`，两者都要实现同一套接口（比如 `list_children()`），文件对这个方法要么返回空列表要么抛异常。为什么这是一个值得拒绝的设计，应该怎么处理？

## A
这是里氏替换原则（Liskov Substitution Principle）的反例：`list_children()` 对文件完全没有意义，强迫它实现这个方法要么返回一个永远没有信息量的空列表，要么在被调用时直接报错——把 `FileNode` 当成 `Node` 传给任何期待“能列出子节点”的代码，程序会在运行时炸掉而不是在类型层面被挡住。更诚实的做法是不共享基类：`File` 和 `Directory` 是两个互不相干的类，唯一共享的性质（“可以被放进某个目录里”）用一个联合类型 `File | Directory` 表达就够了，区分“这是文件还是目录”交给 `isinstance`——调用方本来就必须知道接下来该怎么处理这个节点，`isinstance` 检查不是在绕开多态，是在诚实地承认文件和目录的操作集合压根不相交。
