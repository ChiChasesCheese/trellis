---
id: python-protocol-neither
node: python.protocols-abc
type: qa
step: 6
tags: [grown]
---
## Q
什么时候一个方法根本不需要声明成 `Protocol` 或 `ABC`？

## A
只有**一个调用点**和**一个实现**时——这种“接口”只是在为将来可能存在的第二个实现预付利息。Python 是鸭子类型语言，直接调用对象的方法（EAFP：先做，出错再处理）就够了；等真的出现第二个实现、或者需要给类型检查器一个契约时，再回头提炼出 `Protocol`（这正是 YAGNI 在类型系统层面的体现）。
