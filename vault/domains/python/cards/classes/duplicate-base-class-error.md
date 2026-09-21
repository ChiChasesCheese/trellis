---
id: duplicate-base-class-error
node: classes.inheritance-mro
type: qa
source: python-docs
---
## Q
写 `class C(A, A)`（同一个基类在父类列表里出现两次）会发生什么？

## A
C3 算法会在计算 MRO 之前就识别出这是重复的基类，直接抛出 `TypeError`（duplicate base class），拒绝创建这个类。这是 C3 算法比早期方案更严格的一个体现：它会主动拦截明显写错的继承声明，而不是安静地接受一个冗余或有歧义的层级。
