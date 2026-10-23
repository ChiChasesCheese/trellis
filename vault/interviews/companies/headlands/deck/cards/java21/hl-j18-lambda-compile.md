---
id: hl-j18-lambda-compile
node: java21.j18-comparators-interfaces
type: qa
step: 13
---
## Q
`Person::name` 这样的方法引用和 lambda 在 JVM 里怎么编译？组合出来的比较器在运行时长什么样，JIT 能优化吗？

## A
- 编译成 `invokedynamic` 调用点，运行时由 `LambdaMetafactory` 生成实现 `Function` 的小类，**不是匿名内部类**（不产生 `Foo$1.class`）。
- `Comparator.comparing(Person::name)` 是**一个函数对象包着另一个函数对象**；`thenComparing`、`reversed` 每次返回新 `Comparator`，是一串嵌套的函数对象，比较一次走过整条链。
- 调用点**单态**（只见一种比较器）时，JIT 能把整条链内联成直线代码；**多态**（同一个排序函数传入各种比较器）时会慢些。
