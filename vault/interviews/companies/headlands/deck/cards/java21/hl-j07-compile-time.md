---
id: hl-j07-compile-time
node: java21.j07-text-blocks
type: qa
step: 11
---
## Q
文本块的处理发生在编译期还是运行时？编译器依次做哪几步，字节码里是什么，运行时慢吗？

## A
**全在编译期完成，JVM 不知道文本块的存在。** 步骤：
1. 词法分析器读到 `"""` + 换行，读到结束 `"""`；
2. 换行规范化为 `\n`；
3. 执行"去除偶然空白"（等价 `String.stripIndent()`）；
4. 解释转义（等价 `translateEscapes()`）；
5. 得到普通字符串常量放进常量池。

字节码就是一条 `ldc`，没有运行时拼接，没有 `StringBuilder`，**零运行时开销**。
