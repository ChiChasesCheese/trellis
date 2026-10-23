---
id: hl-j03-typeswitch-indy
node: java21.j03-pattern-switch
type: qa
step: 13
---
## Q
模式匹配 `switch` 编译后，字节码里的 `invokedynamic typeSwitch` 做什么？它的参数和返回值各是什么？

## A
与 `record` 的 `equals` 同一机制：第一次执行时调用引导方法 `java.lang.runtime.SwitchBootstraps.typeSwitch`，静态参数是**标签列表**（如 `Ok.class`、`Err.class`）。

- 调用时传 `(选择器, 起始下标)`；
- 返回**第一个匹配标签的下标**；都不匹配返回标签个数；选择器为 `null` 返回 **`-1`**。

返回值上再做普通 `lookupswitch` / `tableswitch` 跳到分支；分支里先 `checkcast`——就是 Java 8 手写的强转，现在由编译器生成并保证与判断同一类型。
