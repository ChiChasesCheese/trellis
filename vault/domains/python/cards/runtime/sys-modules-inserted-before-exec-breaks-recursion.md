---
id: sys-modules-inserted-before-exec-breaks-recursion
node: runtime.import-system
type: qa
source: python-docs
---
## Q
导入机制在真正执行模块代码之前，为什么要先把这个（还没执行完的）模块对象塞进 `sys.modules`？

## A
因为模块代码在执行过程中可能直接或间接地再次 import 自己（循环导入）。如果不先占位，这种自引用会无限递归下去；提前把半成品模块对象放进 `sys.modules`，循环导入到这里时会直接拿到这个已存在但还没执行完的模块对象，从而截断递归——代价是拿到手的可能是一个属性还没全部定义的「半初始化」模块。
