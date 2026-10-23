---
id: hl-j06-bytecode
node: java21.j06-instanceof-pattern
type: qa
step: 12
---
## Q
`instanceof` 模式编译后和手写的 `instanceof` + 强转在字节码层面有什么区别？绑定变量在运行时是什么？

## A
**没有区别**：JVM 没有新指令，编译器语法糖，编译后是：

```
instanceof java/lang/String    // 旧的 instanceof 指令
ifeq ...                       // 不是 String 就跳走
aload_0; checkcast String      // 转型（编译器自动加）
astore_1                       // 存进局部变量槽 —— 这就是绑定变量 s
```
- 性能与手写相同；`checkcast` 前有 `instanceof` 保护，**永不**抛 `ClassCastException`。
- 绑定变量就是普通**局部变量槽**；"作用域"只是**编译期名字可见性检查**，运行时不存在。
