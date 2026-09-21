---
id: shallow-vs-deep-copy-definition
node: model.copy
type: qa
source: python-docs
---
## Q
`copy.copy(obj)` 与 `copy.deepcopy(obj)` 的核心区别是什么？为什么这个区别只对「复合对象」（如包含其他对象的 list、自定义实例）才有意义？

## A
浅拷贝（shallow copy）新建一个复合对象，但内部各元素仍是对原对象里同一批对象的引用（reference）；深拷贝（deep copy）新建复合对象后递归地把内部元素也逐个复制一份放进去。不包含其他对象的简单对象（如一个整数）没有「内部元素」可复制，浅拷贝和深拷贝对它没有区别；只有复合对象才谈得上内部对象是共享还是独立复制。
