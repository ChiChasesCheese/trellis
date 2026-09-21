---
id: local-precedence-ordering-design-rule
node: classes.inheritance-mro
type: qa
source: python-docs
---
## Q
写 `class G(F, E)` 时，`F` 排在 `E` 前面，直觉上应该是 `F` 的属性优先；但如果 `E` 又是 `F` 的子类，该把谁写在前面才不会出问题？

## A
应该把更「具体」（继承层级更深）的类写在前面，即写成 `class G(E, F)`。C3 算法要求的「局部优先顺序（local precedence ordering）」必须和类自身在继承链上的位置一致：`E` 继承自 `F`，说明 `E` 比 `F` 更特化；如果把 `F` 写在 `E` 前面（`class G(F, E)`），就产生了「声明顺序说 F 优先，但继承关系说 E 更特化该优先」的矛盾。C3 算法在这种矛盾下会拒绝创建类（`TypeError`），比早期算法悄悄给出一个反直觉顺序（比如让 `E` 意外地赢）要安全。
