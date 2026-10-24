---
id: pl-abstraction-composition-embedding-foundation-java-forwarding
node: abstraction.composition-embedding
type: qa
step: 2
---
## Q
Java 里的委托（forwarding / wrapper）怎么写？它怎样避开继承带来的脆弱基类问题？

## A
做法：不 `extends`，而是持有一个被包装的对象作为 `private final` 字段，对外暴露的每个方法都自己写，内部调用字段的**公开方法**。

```java
class CountingSet<E> {
    private final Set<E> inner = new HashSet<>();
    int added = 0;
    boolean add(E e) { added++; return inner.add(e); }
    boolean addAll(Collection<? extends E> c) {
        boolean changed = false;
        for (E e : c) changed |= add(e);
        return changed;
    }
    int size() { return inner.size(); }
}
// addAll(List.of("a","b","c")) -> "3 counted, 3 stored"
```

用继承写同样的功能会得到 `6 counted`（父类的 `addAll` 内部又调用了被覆写的 `add`）。组合版本里，`inner` 的内部怎么实现 `addAll` 与我们无关，我们只依赖它「能 add、能 size」这份契约，所以 JDK 以后改实现也不会影响计数。

代价：每个要暴露的方法都得手写转发，接口方法一多就是几十行样板；而且 `CountingSet` 不再是 `Set`，不能传给要 `Set` 的参数，除非也实现 `Set` 接口并转发全部方法。这个成本正是后来 Go 嵌入和 Kotlin `by` 要解决的问题。
