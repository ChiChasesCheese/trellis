---
id: principles-di-seam
node: principles.coupling
type: qa
---
## Q
What exactly does constructor injection buy over `new`-ing the collaborator inside the class — and does it require a framework?

## A
It creates a **seam**: the class sees only the interface, so tests substitute fakes and "swap MySQL for in-memory" becomes a wiring change instead of an edit. It also makes the dependency graph explicit — hidden `new`s are invisible coupling.

No framework needed: plain constructor parameters wired by hand in `main()` is complete DI. Spring/Guice only automate the wiring — worth saying explicitly in an interview.

## Q zh
依赖注入如何充当一个接缝？它与工厂或服务定位器有什么区别？

## A zh
DI 是一个接缝，因为它让你在不改变代码的情况下在真实和测试依赖之间切换。调用者在构造函数中接收依赖，而不是创建它们，所以测试可以传入模拟对象。

区别：
- 工厂：调用者仍然要求工厂创建依赖。仍然是隐式的依赖。
- 服务定位器：调用者要求定位器查找依赖。同样隐式。
- DI：调用者接收它需要的东西。依赖是显式的，在构造函数签名中可见。
