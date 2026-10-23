---
id: hl-j19-printcompilation
node: java21.j19-runtime-zgc-jit
type: qa
step: 21
---
## Q
怎么读 `-XX:+PrintCompilation` 的一行 `19  138  4  J19Ex1Jit::work (58 bytes)`？`made not entrant` 和 `%` 分别是什么意思？

## A
列含义：第一列 = JVM 启动后毫秒；第二列 = 编译任务编号；第三列 = 编译标志（`%` 表示 OSR）；第四列 = **层级**；然后是方法与字节码大小。

例：`work` 在 17 ms 被 C1（层级 3）编译，2 ms 后被 C2（层级 4）编译；C2 版本就绪后旧的 C1 版本被标为 **`made not entrant`**（不再被新调用进入，因为被更高层版本取代，或因去优化）。

**`%` = OSR**（On-Stack Replacement，栈上替换）：`main` 只调用一次但里面的循环非常热，JVM 在循环运行中途把解释执行「换」成编译版本。
