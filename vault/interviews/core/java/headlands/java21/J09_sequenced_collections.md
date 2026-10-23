# J09 · Sequenced Collections：给「有顺序」的集合一套统一的两端操作

> 版本：Java 21 正式。**对日常代码影响最大的库特性**之一，纯库改动，没有新语法。可运行代码：`examples/J09/`。
> 前置：`List` / `Deque` / `LinkedHashSet` / `LinkedHashMap` / `TreeMap` 的基本用法；哈希表无序、红黑树按 key 有序。

---

## 1. 先看痛点：「取第一个 / 最后一个」每种集合写法都不同

「**有顺序**」（有 encounter order，遇见顺序）的集合有很多种：`List`、`Deque`、`LinkedHashSet`、`LinkedHashMap`、`TreeSet`、`TreeMap`……都有明确的「第一个」「最后一个」，但 Java 8 里**取法完全不统一**（`examples/J09/J09Old.java`）：

| 想做的事 | `List` | `Deque` | `LinkedHashSet` | `LinkedHashMap` | `TreeMap` |
|---|---|---|---|---|---|
| 第一个 | `list.get(0)` | `dq.peekFirst()` / `getFirst()` | `set.iterator().next()` | `map.entrySet().iterator().next()` | `tm.firstEntry()` |
| 最后一个 | `list.get(list.size() - 1)` | `dq.peekLast()` / `getLast()` | **没有办法，只能遍历到底，O(n)** | **同左** | `tm.lastEntry()` |
| 倒着遍历 | 复制 + `Collections.reverse` | `descendingIterator()` | **没有办法** | **没有办法** | `descendingMap()` |

痛点：

1. **名字不统一**：同一概念在 `List` 叫 `get(0)`，`Deque` 叫 `peekFirst()`/`getFirst()`，`TreeMap` 叫 `firstEntry()`，写泛型代码没法用同一方法。
2. **有些结构没有 O(1) 写法**：`LinkedHashSet`/`LinkedHashMap` 内部明明维护双向链表，最后一个就在链表尾，API 却不给，只能遍历全表。
3. **`list.get(list.size() - 1)` 易写错**，空列表时抛含糊的 `IndexOutOfBoundsException: Index -1`。
4. **没有统一类型**：要写「接受任何有顺序集合并返回最后一个」的方法，`Collection` 太宽（`HashSet` 也是），`List` 太窄（排除 `Deque` 和 `LinkedHashSet`）。

Java 21 加了 `SequencedCollection`、`SequencedSet`、`SequencedMap` 三个接口把它们统一起来。

---

## 2. 语法逐条讲：没有新语法，只有新接口和新方法

### 2.1 新的类型层级

* `Collection`
  * `SequencedCollection`（新）：`addFirst` `addLast` `getFirst` `getLast` `removeFirst` `removeLast` `reversed`
    * `List`：现在是 `SequencedCollection`
    * `Deque`：现在是 `SequencedCollection`
    * `SequencedSet`（新）= `Set` + `SequencedCollection`
      * `LinkedHashSet`
      * `SortedSet` → `NavigableSet` → `TreeSet`
* `Map`
  * `SequencedMap`（新）：`firstEntry` `lastEntry` `pollFirstEntry` `pollLastEntry` `putFirst` `putLast` `reversed` `sequencedKeySet` `sequencedValues` `sequencedEntrySet`
    * `LinkedHashMap`
    * `SortedMap` → `NavigableMap` → `TreeMap`

这个层级是把**已有的接口和类接上去**，不需要改已有代码：`ArrayList` 自动就是 `SequencedCollection`，`TreeMap` 自动就是 `SequencedMap`。

**哪些不是**：`HashSet`、`HashMap`、`PriorityQueue`（遍历顺序不是排序的）、`Set.of(...)`、`Map.of(...)`（顺序故意不固定）。`SequencedMap<String,Integer> m = new HashMap<>();` 编译错误。

### 2.2 `SequencedCollection` 的七个方法

```java
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();   // 倒序视图（不拷贝）
    void addFirst(E e);   void addLast(E e);
    E getFirst();         E getLast();
    E removeFirst();      E removeLast();
}
```

* `getFirst()` / `getLast()`：空集合抛 `NoSuchElementException`（`ArrayList`、`ArrayDeque`、`LinkedHashSet`、`TreeSet` 都是），不返回 `null`，也不是 `IndexOutOfBoundsException`。
* `removeFirst()` / `removeLast()`：同理，空则抛 `NoSuchElementException`。
* `addFirst` / `addLast`：在头/尾加。
  * `List`：`addFirst` 会把所有元素往后挪。
  * `LinkedHashSet`：如果元素已存在，**把它移到头/尾**（不是忽略）。
  * `TreeSet`/`TreeMap` 等由比较器决定位置的：**抛 `UnsupportedOperationException`**。
  * 不可变的 `List.of(...)`：读两端 OK，改动抛 `UnsupportedOperationException`。

### 2.3 `reversed()`：倒序**视图**

```java
List<String> rev = list.reversed();     // 没有拷贝！
rev.addFirst("LAST");                    // 修改视图 == 修改原集合（在原列表的末尾加）
list.add("tail");                        // 修改原集合，视图立刻看得到
```

* 返回原集合**倒着看**的视图（view）：O(1) 创建，不复制数据，读写都穿透到原集合。
* `list.reversed().reversed()` 就是原来的 `list`（`==` 为 `true`）。
* 返回类型协变：`List.reversed()` 返回 `List`，`Deque` 返回 `Deque`，`LinkedHashSet` 返回 `SequencedSet`，`SortedSet` 返回 `SortedSet`。
* 遍历视图时修改原集合触发 `ConcurrentModificationException`，同普通 `Iterator`。

### 2.4 `SequencedMap`

```java
interface SequencedMap<K, V> extends Map<K, V> {
    SequencedMap<K, V> reversed();
    Map.Entry<K, V> firstEntry();       Map.Entry<K, V> lastEntry();         // 空 -> null
    Map.Entry<K, V> pollFirstEntry();   Map.Entry<K, V> pollLastEntry();     // 空 -> null；非空则删除并返回
    V putFirst(K k, V v);               V putLast(K k, V v);
    SequencedSet<K> sequencedKeySet();
    SequencedCollection<V> sequencedValues();
    SequencedSet<Map.Entry<K, V>> sequencedEntrySet();
}
```

**与 `SequencedCollection` 的两点不同**：

1. `firstEntry()` / `pollFirstEntry()` 空时**返回 `null`**（沿用 `NavigableMap`），不抛异常。
2. 返回的 `Entry` 是**只读快照**：`m.firstEntry().setValue(99)` 抛 `UnsupportedOperationException`（`LinkedHashMap`、`TreeMap` 都是）；改值用 `m.put(key, newValue)`。

`putFirst` / `putLast` 的语义（`LinkedHashMap`）：

| 操作 | key 不存在 | key 已存在 |
|---|---|---|
| `put(k, v)`（老方法） | 加到末尾 | **只改值，位置不变** |
| `putLast(k, v)` | 加到末尾 | 改值，**并把它挪到末尾** |
| `putFirst(k, v)` | 加到最前 | 改值，**并把它挪到最前** |

`TreeMap`：`putFirst`/`putLast` 抛 `UnsupportedOperationException`（顺序由比较器定）；`firstEntry()`、`pollFirstEntry()` 一直都有，现在也能通过 `SequencedMap` 接口调用。

### 2.5 包装器

* `Collections.unmodifiableSequencedCollection(c)` / `unmodifiableSequencedSet(s)` / `unmodifiableSequencedMap(m)`：只读视图，**保留「有序」类型**（旧的 `unmodifiableCollection` 会丢掉）。
* `Collections.newSequencedSetFromMap(SequencedMap<E, Boolean>)`。

---

## 3. 编译器和 JVM 到底做了什么

**编译器和 JVM 什么都没改**，纯 JDK 库变化：新增接口，给老接口加 `default` 方法，给部分类写高效实现。

### 3.1 `default` 方法

新接口和 `List` 里的新方法大多是 `default`（带方法体的接口方法）。`javap java.util.SequencedCollection`：

```
public interface java.util.SequencedCollection<E> extends java.util.Collection<E> {
  public abstract java.util.SequencedCollection<E> reversed();       // 只有这一个是 abstract
  public default void addFirst(E);
  public default void addLast(E);
  public default E getFirst();
  public default E getLast();
  public default E removeFirst();
  public default E removeLast();
}
```

`default` 的意义：**已有的第三方实现类不用改也能编译运行**。自己写的 `class MyList implements List<X>` 升级到 21 后自动有了 `getFirst()`（默认实现：空则抛 `NoSuchElementException`，否则 `get(0)`）。`reversed()` 虽是 abstract，但 `List`、`Deque`、`SortedSet` 等已各给了 `default` 实现（通用反向视图包装类），自定义类仍不用改。

### 3.2 高效实现与「桥方法」

JDK 对常用类写了专门实现，不全靠 `default`：

* `ArrayList` 重写了 `getFirst/getLast/removeFirst/removeLast/addFirst/addLast`，`getFirst` 直接读内部数组。
* `LinkedHashMap` 用内部链表实现 `putFirst/putLast/sequencedKeySet` 等，O(1)。
* `reversed()` 各有对应视图类：

  | 集合 | `reversed()` 的实际类 |
  |---|---|
  | `ArrayList` | `java.util.ReverseOrderListView$Rand` |
  | `ArrayDeque` | `java.util.ReverseOrderDequeView` |
  | `LinkedHashMap` | `java.util.LinkedHashMap$ReversedLinkedHashMapView` |
  | `LinkedHashSet` | `java.util.LinkedHashSet$1ReverseLinkedHashSetView` |
  | `LinkedList` | `java.util.LinkedList$ReverseOrderLinkedListView` |

  类名是实现细节，只说明 `reversed()` 返回**包装现有数据的小对象**，不是拷贝。

`javap java.util.List` 里能看到两行 `reversed()`：

```
public default java.util.List<E> reversed();                 // 新签名（协变返回 List）
public default java.util.SequencedCollection reversed();     // 编译器生成的桥方法（bridge），返回类型是父接口的
```

桥方法是协变返回类型的实现机制：子接口收窄了返回类型，为保持二进制兼容父接口签名，编译器额外生成一个转发方法。

### 3.3 复杂度

| 操作 | `ArrayList` | `ArrayDeque` | `LinkedList` | `LinkedHashSet/Map` | `TreeSet/Map` |
|---|---|---|---|---|---|
| `getFirst` / `getLast` / `firstEntry` / `lastEntry` | O(1) | O(1) | O(1) | O(1) | O(log n) |
| `addLast` / `removeLast` | 摊还 O(1) | O(1) | O(1) | O(1) | 不支持添加；`pollLastEntry` O(log n) |
| `addFirst` / `removeFirst` | **O(n)**（要挪动所有元素） | O(1) | O(1) | O(1) | 不支持添加；`pollFirstEntry` O(log n) |
| `reversed()` 创建 | O(1) | O(1) | O(1) | O(1) | O(1) |

n 是元素个数。（`TreeMap.firstEntry` 要沿红黑树最左边走到底，树高 O(log n)。）

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——`List`/`Deque` 的两端操作与 `reversed()` 视图

`examples/J09/J09Ex1.java` 输出：

```
a c                                 list.getFirst() + list.getLast()
[z, a, b, c, d]                     addFirst("z"); addLast("d")
z d                                 removeFirst() + removeLast()
[a, b, c]
empty list -> NoSuchElementException
[c, b, a]                           rev = list.reversed()
[a, b, c, LAST]                     rev.addFirst("LAST") 写穿到原列表的末尾
[tail, LAST, c, b, a]               list.add("tail") 之后，视图立刻跟着变
3 [3, 2, 1]                         List.of(1,2,3).getLast() + reversed()
List.of(...).addFirst -> UnsupportedOperationException
x z [z, y, x]                       ArrayDeque 同样的方法名
```

### 例 2：进阶——`LinkedHash*` 的重排、`Tree*` 的限制、快照、只读包装

`examples/J09/J09Ex2.java` 输出：

```
[c, b, a] first=c last=a            LinkedHashSet: addFirst("c")、addLast("a") 对已存在元素=移动
[a, b, c]                           .reversed()
{x=10, y=2, z=3}                    put("x", 10) 已存在 key：只改值，位置不变
{y=2, z=3, x=11}                    putLast("x", 11)：改值并挪到最后
{w=0, y=2, z=3, x=11} first=w=0 last=x=11    putFirst 新 key
poll: w=0 then x=11 -> {y=2, z=3}   pollFirstEntry / pollLastEntry
z 2                                 sequencedKeySet().getLast() + sequencedValues().getFirst()
firstEntry().setValue -> UnsupportedOperationException       Entry 是快照
1 5 [5, 3, 1]                       TreeSet: getFirst/getLast/reversed 可以
TreeSet.addFirst -> UnsupportedOperationException            但不能指定位置添加
TreeMap.putFirst -> UnsupportedOperationException
1=one 3=three {2=two, 1=one}        TreeMap: firstEntry, pollLastEntry, reversed
y=2                                 unmodifiableSequencedMap(m).firstEntry()
unmodifiableSequencedMap.putLast -> UnsupportedOperationException
```

### 例 3：贴近真实——订单簿的最优价与价格-时间优先

`examples/J09/J09Ex3.java` 是订单簿的简化版，核心思路：

```java
// 买盘价格从高到低，卖盘从低到高；两者的「最优价」都是 firstEntry()
final SequencedMap<Long, Level> bids = new TreeMap<>(Comparator.reverseOrder());
final SequencedMap<Long, Level> asks = new TreeMap<>();

static final class Level {
    final SequencedMap<Long, Long> fifo = new LinkedHashMap<>();   // 一个价位上的排队：id -> 剩余数量
    long total;
}

long buy(long takerId, long limit, long qty) {
    long left = qty;
    while (left > 0) {
        var top = asks.firstEntry();                         // 最优卖价；空簿返回 null
        if (top == null || top.getKey() > limit) break;
        Level lv = top.getValue();
        var head = lv.fifo.firstEntry();                     // 该价位排最前面的订单（价格-时间优先里的「时间」）
        long fill = Math.min(left, head.getValue());
        ...
        if (fill == head.getValue()) {
            lv.fifo.pollFirstEntry();                        // 队头成交完，出队
            if (lv.fifo.isEmpty()) asks.pollFirstEntry();    // 这个价位空了，整档删掉
        } else {
            lv.fifo.put(head.getKey(), head.getValue() - fill);   // 部分成交：已存在 key，put 只改值，位置不变，仍在队头
        }
    }
    return left;
}

void increase(SequencedMap<Long, Level> book, long px, long id, long extra) {
    ...
    lv.fifo.putLast(id, newQty);       // 加量 == 重新排队（时间优先被重置）：putLast 把已存在的 key 挪到队尾
}
```

注意最后两处：**部分成交用 `put`（保持位置），加量用 `putLast`（挪到队尾）**——正是 `LinkedHashMap` 里 `put` 与 `putLast` 对已存在 key 行为不同的实际用途。

输出：

```
best bid=100 best ask=101
left=0 best ask=101 queue@101={2=2}          吃掉 id=1 的 5 手 + id=2 的 1 手后，id=2 剩 2 手，仍在队头
queue@101={5=9, 2=7}                         id=2 加量两次后排到 id=5 后面
left=0
最近成交（新 -> 旧）：                       ArrayDeque.reversed() 从新到旧遍历，不用复制
  TRADE taker=6 maker=2 px=101 qty=1
  TRADE taker=6 maker=5 px=101 qty=9
  TRADE taker=4 maker=2 px=101 qty=1
  TRADE taker=4 maker=1 px=101 qty=5
[100, 99]                                    买盘价位：高 -> 低
```

---

## 5. 坑与限制

### 5.1 `ArrayList.removeFirst()` / `addFirst()` 是 O(n)

新 API 让 `list.removeFirst()` 和 `deque.removeFirst()` 一样顺手，**代价却完全不同**：`ArrayList` 是数组，删第一个要把后面所有元素前移。20 万个元素逐个 `removeFirst()` 到空：

```
ArrayList.removeFirst x200000: 1147 ms;  ArrayDeque.removeFirst x200000: 1 ms
```

（机器相关，数量级才有意义：O(n²) 对 O(n)。）当**队列**（FIFO）用，请用 `ArrayDeque`，别用 `ArrayList`。

### 5.2 异常 vs `null` 的不对称

* `SequencedCollection.getFirst()`：空 → **抛** `NoSuchElementException`。
* `SequencedMap.firstEntry()`：空 → **返回 `null`**。

两者来自不同传统（`Deque.getFirst` vs `NavigableMap.firstEntry`）。写 `m.firstEntry().getKey()` 前要判 null。

### 5.3 `reversed()` 是视图

* 修改视图 = 修改原集合；遍历视图时修改原集合会 `ConcurrentModificationException`。
* 需要独立副本时：`new ArrayList<>(list.reversed())` 或 `List.copyOf(list.reversed())`。

### 5.4 `TreeSet` / `TreeMap` 不能指定位置添加

`addFirst` / `addLast` / `putFirst` / `putLast` 抛 `UnsupportedOperationException`；读（`getFirst`、`firstEntry`、`reversed`）和删除（`removeFirst`、`pollFirstEntry`）正常。

### 5.5 `LinkedHashSet.addFirst` 对已存在元素是「移动」

不是忽略。与 `Set.add` 对已存在元素「返回 false 什么都不做」的直觉不同。

### 5.6 `PriorityQueue` 不是 SequencedCollection

`PriorityQueue.iterator()` 的顺序不是优先级顺序（是堆数组层序）；要最小的用 `peek()`/`poll()`，它没有 `getFirst`。

### 5.7 线程安全

新方法没带来任何同步保证，`Collections.synchronizedList(...)` 等包装器保持原样。并发场景用 `ConcurrentSkipListMap`（`NavigableMap`，所以也是 `SequencedMap`）或 `ConcurrentLinkedDeque`。

### 5.8 兼容性

给 `List` 等**已有接口**加方法，理论上可能与使用者的类冲突（如自己有个不同返回类型的 `reversed()`，或同时实现 `List` 和 `Deque`），JDK 自己的类（如 `LinkedList`）已处理。业务类若实现 `List` 并自带 `getFirst`/`getLast`/`reversed`，升级到 21 后编译错误就是这个原因。

### 5.9 `Stream.toList()` 返回的也是 `List`

`stream.toList()` 返回的不可修改 `List` 现在有了 `getFirst`/`getLast`/`reversed`：`stream.toList().getLast()` 比 `list.get(list.size() - 1)` 简洁。

---

## 6. 真实代码里的 Sequenced Collections

* **`OrderBook`** —— 用得最重的地方：
  ```java
  // 一档价位里的排队
  final SequencedMap<Long, Node> fifo = new LinkedHashMap<>();

  // TreeMap 在 Java 21 里是 SequencedMap：firstEntry / pollFirstEntry 就是「最优价」。买盘用 reverseOrder，最优价永远在头部。
  private final SequencedMap<Long, PriceLevel> bids = new java.util.TreeMap<>(Comparator.reverseOrder());
  private final SequencedMap<Long, PriceLevel> asks = new java.util.TreeMap<>();
  private SequencedMap<Long, PriceLevel> book(Side s) { return s == Side.BUY ? bids : asks; }

  private static OptionalLong best(SequencedMap<Long, PriceLevel> book) {
      var e = book.firstEntry();
      return e == null ? OptionalLong.empty() : OptionalLong.of(e.getKey());
  }
  ```
  `sweep`（撮合循环）：
  ```java
  var top = opp.firstEntry();
  ...
  var maker = level.fifo.firstEntry().getValue();
  ...
  level.fifo.pollFirstEntry();
  ...
  if (level.fifo.isEmpty()) opp.pollFirstEntry();
  ```
  `modify`：
  ```java
  // 时间优先的规矩：加量等于「重新排队」。LinkedHashMap 对已存在的 key 做 putLast 会把它移到链表末尾（Java 21 的 SequencedMap 方法）。
  level.fifo.putLast(id, n);
  ```
  方法参数写成 `SequencedMap<Long, PriceLevel>` 而非 `TreeMap`，是为了**只暴露需要的能力**：`bids` 和 `asks` 共用 `book(Side)`，调用方不关心底层是 `TreeMap`。
* **`RegisterSim`**：`long initial = parseValue(body.getFirst());` —— `body` 是 `stream...toList()` 的 `List<String>`，`getFirst()` 代替 `body.get(0)`。
* 别把 `Comparator.reversed()` 与 Sequenced Collections 的 `reversed()` 混淆。

---

## 7. 自测题

1. Java 21 之前，如何拿到 `LinkedHashSet` 的最后一个元素？现在呢？复杂度分别是多少？
2. `new ArrayList<String>().getFirst()` 和 `new TreeMap<String,Integer>().firstEntry()` 在空集合上分别会发生什么？
3. `LinkedHashMap` 里已有 key `"x"`，`put("x", 1)` 和 `putLast("x", 1)` 有什么区别？
4. `list.reversed()` 是拷贝还是视图？举一个能证明的操作。
5. 为什么说「队列场景下用 `ArrayList.removeFirst()` 是个坑」？应该用什么？

<details><summary>答案</summary>

1. 之前：遍历到底 O(n)（或 `new ArrayList<>(set)` 再取，也是 O(n)）。现在：`set.getLast()` 直接读内部链表尾，O(1)。
2. `ArrayList.getFirst()` 抛 `NoSuchElementException`；`TreeMap.firstEntry()` 返回 `null`。
3. `put("x", 1)` 只改值，位置不变；`putLast("x", 1)` 改值并把 `x` 挪到最后。
4. 视图。`rev = list.reversed(); rev.addFirst("A");` 后 `list` 末尾多了 `"A"`；或 `list.add("B")` 后 `rev` 头部是 `"B"`。
5. `ArrayList` 是数组，`removeFirst()` 要前移所有元素 O(n)，循环出队 O(n²)（20 万元素 1147 ms vs `ArrayDeque` 1 ms）。队列用 `ArrayDeque`。

</details>

---

「延伸」J10–J19：虚拟线程、并发与运行时。
