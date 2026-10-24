---
id: pl-data-maps-intro-java
node: data.maps-collections
type: qa
step: 3
---
## Q
Java 的 `HashMap`、`LinkedHashMap`、`TreeMap` 分别是什么？`hashCode`/`equals` 契约和「把可变对象当键」会出什么问题？

## A
**`HashMap`**：链表法的哈希表。数组里每个格子是一条链；同一格子里元素达到 8 个且数组容量不小于 64 时，链表转成红黑树（JDK 8 起），把最坏情形从 O(n) 压到 O(log n)，防止哈希洪泛。键用 `hashCode()` 算位置，用 `equals()` 判相等。迭代顺序没有保证：例子里 `banana, apple, cherry, date, elder` 迭代出来是 `[banana, date, apple, cherry, elder]`。

**`LinkedHashMap`**：在哈希表之外再串一条双向链表，记录插入顺序（也可配成访问顺序，做 LRU 缓存）。迭代是插入顺序 `[banana, apple, cherry]`。

**`TreeMap`**：红黑树，按键的自然顺序或 `Comparator` 排序，O(log n)，支持 `floorKey`、`subMap` 这类范围查询。迭代是排序顺序 `[apple, banana, cherry, date, elder]`。

**契约**：相等的对象必须有相同的 `hashCode`。如果你把一个对象放进 `HashMap` 当键，之后又修改了参与哈希的字段，它在表里的位置就是按旧哈希算的，再也找不到：

```java
K k = new K(1);  map.put(k, "x");
k.v = 2;         // field used by hashCode/equals
map.get(k);      // null
map.get(new K(1)); // null   (equals no longer matches)
// map.size() == 1: the entry is still there, unreachable
```

真实输出：两次 `get` 都是 `null`，`size` 仍为 1，条目成了无法访问的垃圾。

**要记住的一点**：键应该是不可变的（`String`、`Integer`、`record`）；`Map` 接口让你换实现不换代码，但不同实现的顺序、性能、线程安全差别很大。并发场景用 `ConcurrentHashMap`，不要给 `HashMap` 加外部假设。
