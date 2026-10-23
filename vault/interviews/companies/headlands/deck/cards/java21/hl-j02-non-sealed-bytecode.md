---
id: hl-j02-non-sealed-bytecode
node: java21.j02-sealed
type: qa
step: 12
---
## Q
`non-sealed` 在编译后的 class 文件里有没有痕迹？编译器怎么知道它下面可能有任意后代？

## A
**没有痕迹**：`non-sealed` 只存在于源码。编译后的 `Custom` 既没有 `PermittedSubclasses` 也没有 `ACC_FINAL`，和普通可继承类一样。

编译器靠这条推理得知：父类有名单、`Custom` 在名单里、它自己既无名单也不 `final`，所以它下面可能有任意后代。
