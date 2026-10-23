---
id: hl-j06-basic-form
node: java21.j06-instanceof-pattern
type: qa
step: 2
---
## Q
`o instanceof String s` 一次做哪三件事？`o` 为 `null` 时结果是什么？和旧写法相比类型名写了几次？

## A
```java
if (o instanceof String s) {
    System.out.println(s.length());       // s 的类型是 String，不用再强转
}
```
一次做三件事：
1. 检查 `o` 是不是 `String`（**`null` 永不匹配**，同旧 `instanceof`）；
2. 是则转成 `String`；
3. 声明局部变量 `s` 并绑定。

`String s` 叫**类型模式**（type pattern），`s` 叫**绑定变量**（binding variable）。旧写法类型名出现 3 次、变量范围手动定；新写法 1 次，范围由编译器按"何时一定匹配"推出。Java 16 正式（14、15 为预览）。
