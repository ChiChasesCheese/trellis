---
id: patterns-prototype-when
node: patterns.creational
type: qa
step: 5
---
## Q
Prototype 模式"调用 clone() 而不是 new"，在 Python 里对应哪个标准库工具？它什么时候比工厂更合适？

## A
对应 `copy.deepcopy`（需要更细控制时自定义 `__deepcopy__`）。它比工厂更合适的场景：已经有一个配置好的"样板对象"，要批量造出很多相似的副本（连接池里的样例连接、游戏里的敌人模板）；或者初始化开销大（要建连接、读大配置文件），复制现成对象比重新走一遍初始化流程快。

常见陷阱是深浅拷贝搞混：`copy.copy` 只拷贝一层，内部嵌套的列表、字典仍然和原对象共享，改一个另一个也跟着变。
