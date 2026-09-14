---
id: quality-validate-boundary
node: quality.errors
type: qa
---
## Q
"Validate at the boundary" — what does it mean structurally, and how do value objects make re-validation unnecessary?

## A
Structurally: all input crosses **one checkpoint** (API handler, command constructor) where it's checked and **converted into types that can't hold invalid data**. Inside that boundary, code trusts its inputs — no defensive re-checking scattered through every layer.

The mechanism is **"parse, don't validate"**: instead of passing a `String` plus the knowledge that someone once checked it, construct `Email.of(raw)` which **throws on bad input and cannot exist invalid**. The type system then carries the proof everywhere the value goes.

```java
record Email(String value) {
    Email { if (!value.matches(".+@.+")) throw new InvalidEmailException(value); }
}
```

Interview payoff: "invalid states are unrepresentable" — invariants live in constructors, not in every method that touches the data.

## Q zh
"在边界处校验" —— 它在结构上意味着什么，值对象又是怎样让重复校验变得不必要的？

## A zh
结构上：所有输入都穿过**同一个检查站**（API handler、命令的构造函数），在那里被检查并**转换成无法承载非法数据的类型**。在这个边界之内，代码信任自己的输入 —— 不需要在每一层里散落防御性的重复检查。

机制是 **"parse, don't validate"**：不要传一个 `String` 外加"某人曾经检查过它"这份心照不宣，而是构造 `Email.of(raw)` —— 它**在输入非法时抛异常，因而不可能以非法状态存在**。此后类型系统就把这份证明带到这个值所到的每一个地方。

```java
record Email(String value) {
    Email { if (!value.matches(".+@.+")) throw new InvalidEmailException(value); }
}
```

面试收益：一句"非法状态不可表示" —— 不变量住在构造函数里，而不是住在每一个碰这份数据的方法里。
