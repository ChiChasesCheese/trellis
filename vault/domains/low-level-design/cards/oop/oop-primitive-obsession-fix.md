---
id: oop-primitive-obsession-fix
node: oop.values
type: qa
---
## Q
```java
Ticket issue(String plate, String spotId, double amount, long enteredAt)
```
Name the smell, the failure it enables, and the fix — plus when the fix isn't worth it.

## A
**Primitive obsession.** Two same-typed parameters mean `issue(spotId, plate, ...)` compiles and fails silently at runtime; `double` for money invites rounding drift; validation ("plates are 7 chars") is re-done at every call site or nowhere.

Fix: small value types — `record Plate(String value)`, `Money`, `Instant` — validating in the constructor. Now the compiler rejects swapped arguments, the rule lives in one place, and the type name documents the unit (`Money`, not "amount in cents… probably").

Not worth it for a scalar used in one local computation, or a loop index. Trigger: the primitive **crosses a boundary** or carries a rule.

## Q zh
```java
Ticket issue(String plate, String spotId, double amount, long enteredAt)
```
说出坏味道、它会引发什么故障、修法是什么——以及什么时候这个修法不值得做。

## A zh
**Primitive obsession（基本类型偏执）。** 两个同类型的参数意味着 `issue(spotId, plate, ...)` 能编译通过，然后在运行时静默出错；用 `double` 表示金钱会招来舍入漂移；校验（"车牌是 7 个字符"）要么在每个调用点重复一遍，要么根本没有。

修法：小的值类型 —— `record Plate(String value)`、`Money`、`Instant`，在构造函数里做校验。这样编译器会拒绝调换的参数，规则只存在于一处，类型名本身就说明了单位（是 `Money`，而不是"金额，单位大概是分吧"）。

对只在一处局部计算里用到的标量、或者循环下标，不值得。触发条件：这个基本类型**跨越了边界**，或者它身上带着一条规则。
