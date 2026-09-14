---
id: quality-extract-method-triggers
node: quality.refactoring
type: qa
---
## Q
Extract method: what are the two classic triggers, and what does a well-composed method look like afterward?

## A
Triggers:

- **A comment announcing a block** — `// validate input` above six lines means the block wants to be `validateInput()`; the name replaces the comment.
- **A fragment you must study to see what it does** — or one you'd like to reuse or test in isolation.

Target shape (**composed method**): the body reads as a sequence of same-altitude, intention-named steps —

```java
void checkout(Cart c) {
    validate(c);
    var total = priceWithDiscounts(c);
    charge(c.customer(), total);
    emitReceipt(c, total);
}
```

Each step is one level of abstraction; details live one call down. When several extracted methods keep sharing the same parameters, that's the follow-on trigger for **extract class**.

## Q zh
提炼函数：两个经典触发条件是什么，提炼之后一个组合良好的方法长什么样？

## A zh
触发条件：

- **一句给代码块作预告的注释** —— 六行代码上面写着 `// validate input`，说明这个块想成为 `validateInput()`；用名字取代那句注释。
- **一段你必须琢磨才能看懂在干嘛的片段** —— 或者一段你想复用、想单独测试的片段。

目标形态（**composed method**）：方法体读起来是一串处在同一抽象高度、以意图命名的步骤 ——

```java
void checkout(Cart c) {
    validate(c);
    var total = priceWithDiscounts(c);
    charge(c.customer(), total);
}
```
