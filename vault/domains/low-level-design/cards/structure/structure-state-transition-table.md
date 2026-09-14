---
id: structure-state-transition-table
node: structure.state-machines
type: qa
---
## Q
Where should "can an order go from PAID to CANCELLED?" live, and how does the entity change state without exposing a setter?

## A
In **one declarative transition table**, not in scattered `if`s:

```java
static final Map<State, Set<State>> ALLOWED = Map.of(
    CREATED,  Set.of(PAID, CANCELLED),
    PAID,     Set.of(SHIPPED, CANCELLED),
    SHIPPED,  Set.of(DELIVERED));

private void transitionTo(State next) {
    if (!ALLOWED.getOrDefault(state, Set.of()).contains(next))
        throw new IllegalStateException(state + " -> " + next);
    state = next;
}
```

Public methods are **named events** (`pay()`, `ship()`, `cancel()`) that call `transitionTo` — never a public `setState`. Changing the lifecycle = editing the table, and the guard makes every illegal path fail loudly.


## Q zh
"一个订单能从 PAID 去到 CANCELLED 吗?"应该在哪里生活，实体怎样改变状态不暴露一个 setter?

## A zh
在**一个声明性的转变表**中，不是在零散的 `if` 中:

```java
static final Map<State, Set<State>> ALLOWED = Map.of(
    CREATED,  Set.of(PAID, CANCELLED),
    PAID,     Set.of(SHIPPED, CANCELLED),
    SHIPPED,  Set.of(DELIVERED));

private void transitionTo(State next) {
    if (!ALLOWED.getOrDefault(state, Set.of()).contains(next))
        throw new IllegalStateException(state + " -> " + next);
    state = next;
}
```

`transitionTo(CANCELLED)` 给你表驱动的检查。所有合法转变是一个可视的列表，没有 `setState()` 调用者能操纵。
