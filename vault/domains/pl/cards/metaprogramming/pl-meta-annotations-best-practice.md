---
id: pl-meta-annotations-best-practice
node: metaprogramming.annotations-decorators
type: qa
step: 9
---
## Q
资深工程师在 Java、Go、Rust、Python 里怎样使用注解、struct tag 和装饰器？规则是什么，何时破例？

## A
**通用规则**：标记只用来描述「是什么」或「要什么」，业务逻辑不要藏在标记背后；标记的处理方式必须有一个可找到的唯一入口。理由是标记让行为脱离了被标记的代码，滥用会让调用链不可追踪。

- **Java**：自定义注解必须写 `@Retention(RUNTIME)` 才能被反射读到（默认 `CLASS` 读不到）；处理者尽量放在启动阶段而非热路径；`@Transactional` 这类基于代理的注解不要在同一个类内部自调用，那一次调用不经过代理。需要更强的编译期保证时选注解处理器。
- **Go**：tag 里只放序列化、校验这类声明；每个项目开 `go vet`（它的 `structtag` 检查能抓格式错误）；横切逻辑用显式的中间件函数，而不是发明基于 tag 的框架。
- **Rust**：优先 `derive`，只在确实有样板时才自己写属性宏；属性宏的输出要通过 `cargo expand` 检查。
- **Python**：装饰器内部一律加 `@functools.wraps(f)`；带参数的装饰器要多一层闭包；多个装饰器叠加时，顺序从下往上包、从上往下执行。

**何时破例**：团队已经采用 Spring 或 JPA 这类以注解为中心的框架时，就按框架的约定写，不要自己发明另一套隐式规则。
