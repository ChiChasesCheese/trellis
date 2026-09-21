---
id: not-all-types-support-weakref
node: memory.weakref
type: qa
source: python-docs
---
## Q
`tuple` 和 `int` 即使被子类化，实例也支持弱引用吗？`list` 和 `dict` 呢？

## A
`tuple`、`int` 这类内置类型即使被继承子类化，子类实例仍然不支持弱引用（CPython 实现细节，没有为它们开这个口子）；而 `list`、`dict` 本身不直接支持弱引用，但只要写一个继承它们的子类（哪怕子类体是空的），子类的实例就变得可以被弱引用了——区别在于前者是类型层面写死不支持，后者只是「基类没开」，子类化就能开。
