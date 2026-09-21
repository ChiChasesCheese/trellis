---
id: finder-returns-spec-loader-executes
node: runtime.import-system
type: qa
source: python-docs
---
## Q
在 `sys.modules` 缓存没命中之后，「查找」（finder）和「加载」（loader）这两步各自负责什么？

## A
查找器（finder）只负责判断自己知不知道怎么找到这个模块，找到了就返回一个「模块规格」（module spec，封装模块的导入相关信息）——finder 本身不执行任何加载动作。真正把模块代码跑起来、填充模块命名空间的是加载器（loader），通过 spec 里指定的 `exec_module()` 方法完成。3.4 之前查找器直接返回 loader，3.4 起改为返回包含 loader 的 spec 对象，职责划分更清楚。
