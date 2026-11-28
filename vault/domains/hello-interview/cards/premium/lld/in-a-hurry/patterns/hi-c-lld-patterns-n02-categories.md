---
id: hi-c-lld-patterns-n02-categories
node: lld.in-a-hurry.patterns.notes
type: qa
step: 2
---
## Q
**设计模式 · 三类模式各管什么**｜摘要 · 必会

创建型、结构型、行为型模式各解决什么问题？各包含面试常见的哪几个？

## A
| 类别 | 解决什么问题 | 面试常见 |
|---|---|---|
| 创建型 | 对象怎么创建：把构造细节藏起来、让实现可替换，避免代码绑死在某个具体类上 | Factory、Builder、Singleton |
| 结构型 | 对象怎么连接：在类之间建立灵活的关系，避免紧耦合和混乱的依赖 | Decorator、Facade |
| 行为型 | 控制流和职责怎么分配：对象之间怎样通信 | Strategy、Observer、State Machine |

- **怎么用这个分类：** 先判断你的麻烦属于"怎么造对象""怎么组织对象""怎么让对象协作"中的哪一类，再去想对应的模式。
