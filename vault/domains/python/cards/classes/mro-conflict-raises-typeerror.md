---
id: mro-conflict-raises-typeerror
node: classes.inheritance-mro
type: qa
source: python-docs
---
## Q
如果 C3 算法在合并（merge）过程中找不到任何一个「不在别的列表尾部里」的合法表头，Python 会怎么处理？给出一个会触发这种情况的最小继承关系例子。

## A
Python 会拒绝创建这个类，抛出 `TypeError`（MRO conflict），而不是像早期版本那样默默选一个不一致的顺序。典型触发例子：`class X(object)`、`class Y(object)`、`class A(X, Y)`、`class B(Y, X)`——`A` 里 X 排在 Y 前面，`B` 里 Y 排在 X 前面，两者互相矛盾，尝试 `class Z(A, B)` 时无法算出一个同时尊重两边局部顺序的线性化，于是创建 `Z` 直接报错。
