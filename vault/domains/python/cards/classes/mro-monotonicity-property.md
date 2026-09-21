---
id: mro-monotonicity-property
node: classes.inheritance-mro
type: qa
source: python-docs
---
## Q
MRO 的「单调性（monotonicity）」具体指什么？为什么早期（非 C3）算法违反单调性会是个隐患？

## A
单调性指：如果类 `C1` 在类 `C` 的线性化（linearization，即 MRO 列表）里排在 `C2` 前面，那么在 `C` 的任意子类的线性化里，`C1` 也必须仍然排在 `C2` 前面。违反单调性意味着：仅仅派生出一个新的子类这个无害操作，就可能悄悄改变父类原有方法的解析顺序——同一个方法调用在子类里神不知鬼不觉地换成了另一个实现，属于极难排查的 bug 来源。C3 算法就是为了保证单调性而被 Python 2.3 采纳，取代了之前不满足这条性质的算法。
