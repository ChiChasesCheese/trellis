---
id: hi-c-lld-design-principles-x01-smell-to-principle
node: lld.in-a-hurry.design-principles.exam
type: qa
step: 1
---
## Q
**设计原则 · 症状对应原则**｜考点 · 必会

五个症状：(1) 加一种折扣要改五处 `if`；(2) 子类的方法里只有 `raise NotImplementedError`；(3) 业务类里直接 `new` 数据库连接；(4) 业务方法里拼 HTML；(5) 三层 getter 链。各违反哪条原则？

## A
| 症状 | 原则 |
|---|---|
| 加折扣改五处 | OCP |
| 子类只抛未实现 | LSP（或 ISP：接口太大） |
| 直接 `new` 连接 | DIP |
| 业务里拼 HTML | 关注点分离 |
| getter 链 | 迪米特 |

- 同一个症状常能指向两条，说出判断依据比选对一条重要
