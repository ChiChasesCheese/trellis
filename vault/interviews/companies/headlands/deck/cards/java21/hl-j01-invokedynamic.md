---
id: hl-j01-invokedynamic
node: java21.j01-record
type: qa
step: 15
---
## Q
`invokedynamic` 指令和普通调用指令（如 `invokevirtual`）有什么区别？`record` 的 `equals` 方法体具体是什么？

## A
- 普通调用指令在**编译时**就写死了调用哪个方法。
- `invokedynamic`：**第一次执行时**，JVM 调用指定的**引导方法**（bootstrap method），由它**现场生成**真正要执行的代码（方法句柄 `MethodHandle`），之后这条指令直连那段代码。

`record` 的 `equals` / `hashCode` / `toString` 方法体只有一条 `invokedynamic`，指向 `java.lang.runtime.ObjectMethods.bootstrap`。引导方法拿到 record 类、组件名列表（如 `"symbol;priceTicks;qty"`）和各字段 getter 句柄，据此造出这三个方法。
