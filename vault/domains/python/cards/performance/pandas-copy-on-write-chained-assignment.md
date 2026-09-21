---
id: pandas-copy-on-write-chained-assignment
node: performance.pandas-at-scale
type: qa
tags: [grown]
---
## Q
pandas 2.x 引入的写时复制（Copy-on-Write，CoW）机制，是怎么解决 `df[df.x > 0]['y'] = 1` 这类链式赋值（chained assignment）到底改没改到原表的不确定性的？

## A
CoW 之前，`df[df.x > 0]` 返回视图还是拷贝取决于内部实现细节，链式赋值可能悄悄改了原表，也可能改到一个临时对象上没生效，这正是 `SettingWithCopyWarning` 的由来；CoW 让所有可能产生歧义的取子集操作统一表现为「逻辑拷贝」，真正写入时才实际复制底层数据，结果链式赋值永远不会改到原表——要修改必须一步到位写成 `df.loc[df.x > 0, 'y'] = 1`。
