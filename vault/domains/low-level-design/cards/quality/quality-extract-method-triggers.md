---
id: quality-extract-method-triggers
node: quality.refactoring
type: qa
---
## Q
提炼函数：两个经典触发条件是什么，提炼之后一个组合良好的方法长什么样？

## A
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
