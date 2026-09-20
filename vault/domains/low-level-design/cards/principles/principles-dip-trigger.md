---
id: principles-dip-trigger
node: principles.solid
type: qa
step: 6
---
## Q
什么信号说明一段代码需要做依赖倒置（Dependency Inversion）？

## A
触发信号：
- 高层模块（业务逻辑）直接 `import` 一个低层模块（具体的数据库、第三方 SDK、框架代码）；
- 低层模块的任何一次改动，都强制沿着 import 链改到依赖它的所有东西；
- 给一个类写测试要费很大力气去隔离它：得起一个真实数据库连接、真的去调外部 API，才能让这个类跑起来。

修法：让高层模块依赖一个由自己定义的抽象（`Protocol`/`ABC`），低层的具体实现反过来去实现这个抽象——依赖方向被"倒转"成都指向抽象。
