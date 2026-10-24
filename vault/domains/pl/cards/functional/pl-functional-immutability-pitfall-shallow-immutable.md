---
id: pl-functional-immutability-pitfall-shallow-immutable
node: functional.immutability
type: qa
step: 10
---
## Q
Java 的 `record` 或不可变视图在什么情况下仍然被悄悄修改？「浅不可变」的真实事故长什么样？

## A
两个典型：

```java
List<String> src = new ArrayList<>(List.of("ann"));
record Team(String name, List<String> members) {}
var t = new Team("x", src);
t.members().add("eve");      // record 不拦它
System.out.println(t + " " + src);
// Team[name=x, members=[ann, eve]] [ann, eve]
```

`record` 保证字段 `members` 不会指向别的列表，但列表本身仍然可变。更糟的是 `t` 持有的是调用者传入的**同一个列表**，调用者之后修改 `src`，`t` 就跟着变，两个本该独立的对象被偷偷耦合。

第二个：

```java
List<String> view = Collections.unmodifiableList(src);
src.add("bob");
// view -> [ann, bob]：「不可修改」的列表在变
```

事故形态：配置对象在启动后被某个组件改了；缓存里的值被调用者改了，其他调用者拿到脏数据；放进 `HashSet` 的 `record` 因为内部列表变化而哈希值变化，再也找不到（与可变键的陷阱同源）。

修法：在构造器里做**防御性复制**。

```java
record Team(String name, List<String> members) {
    Team { members = List.copyOf(members); }
}
```

`List.copyOf` 返回独立、不可变的副本；若传入的已是不可变列表，则直接复用不复制。对 Python 的 `frozen` dataclass、tuple 中放 list，原理一样；Rust 里这类问题被所有权避开：把 `Vec` 移进结构体后，调用者不再持有它。
