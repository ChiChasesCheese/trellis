---
id: hl-j03-guard-restart
node: java21.j03-pattern-switch
type: qa
step: 15
---
## Q
`case Integer i when i < 0` 的守卫为假时，字节码怎么"继续往下试"后面的标签？

## A
`typeSwitch` 的第二个参数是**重启下标**。守卫是普通字节码：

```
53: aload_3; invokevirtual Integer.intValue; iflt 65   // 守卫 i < 0 为真，跳到分支体
60: iconst_1; istore_2                                 // 守卫为假：把「起始下标」改成 1
62: goto 4                                             // 回到 typeSwitch 调用处，从标签 1 再试
```
守卫为假时，把起始下标设为当前标签下标 + 1，`goto` 回 `typeSwitch` 调用处，从下一标签重新匹配。

分工：**类型匹配交给 `typeSwitch`，守卫是普通字节码，二者靠重启下标衔接。**
