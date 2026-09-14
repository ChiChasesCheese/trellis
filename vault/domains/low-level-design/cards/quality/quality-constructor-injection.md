---
id: quality-constructor-injection
node: quality.testability
type: qa
---
## Q
Why is constructor injection preferred over setter/field injection — three concrete properties?

## A
- **No invalid intermediate state**: the object is fully usable the moment it exists; setter injection allows a constructed-but-unwired object, adding "was it initialized?" as a bug class.
- **Dependencies are honest and final**: `final` fields, visible in one signature — and a constructor demanding six collaborators is a *feature*: it makes the SRP violation impossible to ignore (field injection hides it).
- **Framework-free tests**: `new Service(fakeRepo, fixedClock)` — no DI container, no reflection in unit tests.

Setter injection's remaining niche: genuinely **optional** or cyclic dependencies — both rare, and a cycle is usually a design smell to break instead.

## Q zh
为什么构造注入优于 setter/字段注入 —— 说出三条具体性质。

## A zh
- **不存在非法的中间状态**：对象一旦存在就完全可用；setter 注入允许出现"已构造但没接好线"的对象，凭空多出"它初始化了吗"这一类 bug。
- **依赖是诚实且 final 的**：`final` 字段，全部出现在一个签名里 —— 而一个要求六个协作者的构造函数是*好事*：它让 SRP 违规无法被忽视（字段注入则会把它藏起来）。
- **测试不需要框架**：`new Service(fakeRepo, fixedClock)` —— 单元测试里没有 DI 容器，也没有反射。

setter 注入仅剩的适用场景：真正**可选的**依赖，或者循环依赖 —— 两者都罕见，而且循环通常是应该去打破的设计坏味道。
