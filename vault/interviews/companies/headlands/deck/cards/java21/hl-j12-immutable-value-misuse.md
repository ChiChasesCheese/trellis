---
id: hl-j12-immutable-value-misuse
node: java21.j12-scoped-values
type: qa
step: 19
---
## Q
用 `ScopedValue` 时值对象本身要注意什么？怎样避免把它变成「隐藏的全局变量」？

## A
- `ScopedValue` 保证**绑定**不可变，不保证**值对象**不可变。绑一个 `ArrayList` 进去，到处都能改它，等于把「可变、随处可改」的毛病请回来。要绑 `record` 或不可变对象。
- 隐式参数让依赖看不见。只放真正**横切**的（身份、追踪、截止时间），业务数据仍用参数。
- 未绑定的 `get()` 抛异常，用 `isBound()` / `orElse()` 保护，或确保所有入口都绑定过。
