# hc05 · Market Order Book（订单簿 + 撮合 + 低分配版本）—— 讲义

> 读者：只会基本 Java（类、方法、循环、`ArrayList` / `HashMap`）。本篇覆盖订单簿与批量限价撮合。

---

## 1. 这道题在问什么

### 1.1 订单簿是什么

想象一个只卖一种东西的菜市场。有人举牌说「我要**买**，最多出 100 块，要 5 个」；另一个人说「我要**卖**，最少要 101 块，要 3 个」。
所有这些「还没成交、挂在那里等人」的牌子，按价格排好，就是**订单簿**（order book）。

* **买单**（BUY，也叫 bid）：想买，给出的是**最高愿意出的价**。
* **卖单**（SELL，也叫 ask / offer）：想卖，给出的是**最低愿意收的价**。
* **价位**（price level）：同一个价格上所有牌子合起来叫一个价位。
* **最优价**（best price）：买盘里**最高**的价叫 best bid（买家里出价最高的那个）；卖盘里**最低**的价叫 best ask。
* 只要 best bid < best ask，没人能和别人成交，大家都在等。一旦有人出价 ≥ 对面最低价，就**成交**（trade）。

### 1.2 一个手算例子

簿上现在有（价格单位叫 tick，就当作元）：

```
        卖盘 (asks)，价格从低到高，越靠上越"好"
        价位 101:  [#1 数量5] → [#2 数量3]     ← 同价位按"先来后到"排队，#1 先到
        价位 102:  [#3 数量4]
  ------------------------------------------   ← 中间的缝隙叫 spread
        买盘 (bids)：空
```

新来一张订单：**#4，买，限价 101，数量 6**（限价 = 最多出 101）。

* 对面最便宜的是 101 这一档，101 ≤ 我的限价 101，可以成交。
* 同一价位谁先到谁先成交 → 先和 #1 成交 5 个（成交价取 **#1 的价 101**），再和 #2 成交 1 个。
* #4 的 6 个全部成交，不挂簿。簿变成：

```
        价位 101:  [#2 数量2]         ← #2 被吃掉 1 个，还剩 2 个，仍然排在队头
        价位 102:  [#3 数量4]
```

「**价格优先、同价按时间先后**」叫 **价格-时间优先**（price-time priority），是几乎所有交易所的撮合规则。

### 1.3 题目要你做的四件事（Part 1–4）

1. **维护**一个这样的簿：挂单、撤单、改量、问最优价、问前 N 档的深度。（此时先不撮合。）
2. **撮合**：新单进来，按价格-时间优先去吃对面的单，吃不完的挂簿；用一组"事件"（成交了、挂簿了、被撤了……）描述发生了什么。
3. 一批 `[side, price, qty]` 的订单按到达顺序处理，汇总结果。
4. **性能追问**：「每秒几百万条命令，GC 很忙，怎么办？」

面试里这几步是**一路追问**出来的：先让你把基础版写对，再不断加要求。所以下面也这样走：先做最笨的，再一步步改。

---

## 2. 前置知识

> 本节每个概念按四问写：是什么 → 为什么需要它 → 怎么工作 → Java 里怎么写。

### 2.1 订单簿的术语（一页纸）

| 词 | 意思 |
|---|---|
| tick | 最小报价单位。我们用**整数 tick** 表示价格（"10050" 表示 100.50 元），不用小数 |
| maker / taker | maker = 已经挂在簿上等的单（被动方）；taker = 新来并主动去吃的单 |
| 限价单（limit order） | 带价格上限（买）/ 下限（卖）。吃不完的挂簿 |
| 市价单（market order） | 不限价，有多少对手盘吃多少。我们的约定：吃不完的部分**作废**（IOC，立即成交否则取消） |
| 成交价 | 取 **maker 的价**。道理：maker 当初报的是"我愿意的最差价"，taker 的限价只是上限，取 maker 价让 taker 有"价格改善" |
| 深度（depth） | 买盘 / 卖盘各档价位上的总量，从最优价往外数 N 档 |

**为什么不用 `double` 表示价格**：`0.1 + 0.2 != 0.3`。二进制浮点数存不准十进制小数，两个本该相等的价格会比出"不等"，订单就挂在两个"看起来一样"的价位上。整数 tick 没这个问题。

### 2.2 复杂度记号：O(1)、O(log n)、O(n)

**是什么**：描述"输入变大 10 倍，操作要多做几倍的活"。
* O(1)：常数。数组按下标取一个数；哈希表查一个 key（平均）。
* O(n)：线性。扫一遍 n 个元素。n 翻 10 倍，时间翻 10 倍。
* O(log n)：对数。每做一步，问题规模减半。n = 100 万时，只要约 20 步。

**为什么需要它**：本题所有"改进"都是在把 O(n) 变成 O(log n) 或 O(1)。没有这个尺子，没法说"改进"。

**数一下**：1,000,000 个订单，每次撤单 O(n) = 100 万步；O(log n) ≈ 20 步；O(1) = 1 步。每秒 100 万次撤单，前者要 10^12 次操作（CPU 一秒大约做 10^9 次简单操作，要 1000 秒）；后者 10^6 次，毫秒级。

### 2.3 二叉搜索树、红黑树与 `TreeMap`

**是什么**：`TreeMap<K, V>` 是一个 **按 key 排好序**的 Map。你可以随时问"最小的 key 是谁"、"≥ 某个 key 的第一个是谁"，也可以按顺序遍历。

**为什么需要它**：订单簿需要"最优价"——买盘的最高价、卖盘的最低价。而且成交会把最优价那一档吃光，吃光后要立刻知道"下一个最优价"是谁。
* 用 `HashMap<价格, 价位>`：能 O(1) 找到"价格 100 这一档"，但**不能**回答"最小的价格是多少"，除非把所有 key 扫一遍（O(L)，L 是价位数）。
* 用排好序的 `ArrayList`：取最小 O(1)，但**插入新价位**要把后面的元素往后挪，O(L)。
* `TreeMap`：取最小、插入、删除都是 O(log L)。

**它怎么工作**——先看**二叉搜索树**（BST）。每个节点：左子树所有 key 都比它小，右子树所有 key 都比它大。

```
              100
             /    \
           98      103
          /  \       \
        97    99      105
```

* 找最小：一直往左走（97）。找最大：一直往右走（105）。
* 查 99：从 100 开始，99 < 100 往左到 98，99 > 98 往右到 99，找到。每一步淘汰掉一半，所以步数 = 树的高度。
* 问题：如果 key 按 1, 2, 3, 4, 5 的顺序插入，树会退化成一根"棍子"（每个节点只有右孩子），高度 = n，查找变成 O(n)。

**红黑树**（red-black tree）是 BST 的一种"自平衡"版本：给每个节点涂红或黑，维持几条规则（根是黑；红节点的孩子是黑；任一节点到其下所有叶子的路径上黑节点数相同），
插入 / 删除后用"旋转"和"改色"恢复规则。这些规则保证**最长路径不超过最短路径的两倍**，所以高度 ≤ 2·log2(n+1)，所有操作 O(log n)。
你不需要会写红黑树（面试不会让你写），要知道的是：**`TreeMap` 就是红黑树，所有操作 O(log n)，key 是有序的**。

**Java 里怎么写**：

```java
TreeMap<Long, String> asks = new TreeMap<>();      // 默认按 key 从小到大
asks.put(102L, "b"); asks.put(101L, "a");
asks.firstEntry();        // → 101=a   最小的 key（O(log n)）
asks.pollFirstEntry();    // 取出并删除最小的那一项

TreeMap<Long, String> bids = new TreeMap<>(Comparator.reverseOrder());  // 从大到小
bids.put(99L, "x"); bids.put(100L, "y");
bids.firstEntry();        // → 100=y   "最小"在这个比较器下 = 数值最大 = 最高买价
```

**小技巧**：买盘的最优价是**最高**价，卖盘的是**最低**价。给买盘用 `Comparator.reverseOrder()`，两边就都可以用 `firstEntry()` 取最优价，代码对称。
注意 key 的类型是 `Long`（对象）而不是 `long`（基本类型）——集合只能装对象，Java 会自动"装箱"，见 2.7。

### 2.4 `HashMap` 与"按 id 找订单"

**是什么**：`HashMap<K, V>`：通过 key 的"哈希值"算出一个数组下标，直接去那个位置拿——平均 O(1)，但**没有顺序**。

**为什么需要它**：撤单和改量的命令只带一个 `id`（订单号），不带价格也不带方向。如果没有 `id → 订单` 这张表，你得遍历所有价位的所有队列去找，O(n)。
有了 `HashMap<Long, Node> byId`，一步找到订单，从订单里读出它的价格和方向，再去对应价位操作。

```java
HashMap<Long, Node> byId = new HashMap<>();
byId.put(7L, node);
Node n = byId.get(7L);        // 找不到返回 null
byId.remove(7L);
```

### 2.5 队列（FIFO）与 `LinkedHashMap`——同价位怎么排队

**是什么**：FIFO = First In First Out，先进先出，排队买票。

**为什么需要它**：同一价位上，先来的先成交（时间优先）。所以每个价位内部要有个"队伍"。

**最直接的做法**：`ArrayDeque<Node>`（或 `LinkedList`）。入队尾、出队头都是 O(1)。
**问题**：有人要**撤单**——他可能站在队伍中间。`ArrayDeque.remove(obj)` 要从头找到他，O(队伍长度)。一个价位上排了 10 万张单时，撤一张要扫 10 万次。

**更好的做法**：`LinkedHashMap<Long, Node>`。它是"哈希表 + 双向链表"的合体：

```
哈希表（按 key 找，O(1)）:        双向链表（记录插入顺序）:
  id=7  ──────────────────┐        head ⇄ [#7] ⇄ [#3] ⇄ [#9] ⇄ tail
  id=3  ───────────┐      │              ▲      ▲      ▲
  id=9  ────┐      │      │              └──────┴──────┘  哈希表里每一项同时挂在链表上
```

* 按 id 找到节点：O(1)（走哈希表）。
* 从链表里摘掉一个节点：只要改它前后两个邻居的指针，O(1)（双向链表）。
* 遍历：按插入顺序。队头 = 最先插入的。

所以它**既是 Map 又是队列**：`remove(id)` O(1)，`firstEntry()` 取队头 O(1)，`pollFirstEntry()` 取并删队头 O(1)，`putLast(k, v)` 放到队尾 O(1)。

### 2.6 Sequenced Collections（Java 21）

**是什么**：Java 21 给"有顺序的集合"统一加了一套接口 `SequencedCollection / SequencedSet / SequencedMap`，
让你对任何有"头"和"尾"的集合都能用同样的方法：`getFirst()` / `getLast()` / `reversed()`；Map 有 `firstEntry()` / `lastEntry()` / `pollFirstEntry()` / `putFirst()` / `putLast()`。

**为什么需要它**：Java 21 之前没有统一方式取"最后一个"：`List` 用 `list.get(list.size() - 1)`，`LinkedHashSet` 根本没法直接取最后一个（要遍历到底），`Deque` 又是 `getLast()`。

**本题用在哪**：`TreeMap` 和 `LinkedHashMap` 都是 `SequencedMap`，所以价位表和价位内队列我们都声明成同一个类型 `SequencedMap<Long, ...>`，用 `firstEntry` / `pollFirstEntry` 取"最优价档"和"队头订单"。

```java
SequencedMap<Long, Node> fifo = new LinkedHashMap<>();
fifo.putLast(7L, n7);              // 排到队尾；如果 7 已经在队伍里，会被移到队尾（"重新排队"）
Node head = fifo.firstEntry().getValue();   // 队头
fifo.pollFirstEntry();             // 队头出队
```

### 2.7 装箱（boxing）、垃圾回收（GC）与为什么性能题盯着"分配"

**是什么**：Java 的 `long` 是 8 字节的裸数字；`Long` 是堆上的一个对象（带对象头，约 16 字节），里面装着那个数字。集合（`TreeMap<Long,…>`、`HashMap<Long,…>`）只能存对象，
所以 `map.put(5L, x)` 会悄悄 `Long.valueOf(5L)` 创建一个对象——这叫**装箱**。除了 -128..127 这些被缓存的小数，每次都是新对象。

**为什么需要关心**：堆上的对象用完后要由**垃圾回收器（GC）**清理。分配得越快，垃圾越多，GC 越忙；GC 在某些阶段会让程序暂停，
对交易系统来说，一次几毫秒的暂停就是"延迟毛刺"。另外对象散落在内存各处，CPU 读它要"追指针"，缓存命中率低。
所以低延迟系统追求**热路径上零分配**：处理一条命令不 `new` 任何东西。

**实际的数字**（同一串随机命令）：Part 2 的 `OrderBook` 每条命令平均分配约 **420 字节**（20 万条命令共约 84 MB）；
Part 4 的 `TickBook` 处理 60 万条命令分配 **0 字节**。

### 2.8 Part 4 要用的"数组式"技巧

这些在第 4 节第 9 步才用到，先有个印象：

* **结构数组（struct-of-arrays）**：不创建 `Order` 对象，而是 `long[] id`、`long[] qty`、`int[] price`……每个"字段"一个数组，第 i 号订单就是各数组的第 i 个位置。数组一次分配好，之后只读写。
* **侵入式链表**：链表的 `prev` / `next` 不放在节点对象里，而是放在 `int[] prev`、`int[] next` 里，存的是"数组下标"。
* **free list（空闲链表）**：没用的槽位串成一条链，要新订单时从链头拿一个，释放时挂回链头——O(1) 分配 / 释放，不需要 `new`。
* **开放寻址哈希表**：不用 `HashMap`（它会装箱、每个 entry 是对象），自己用两个数组 `long[] keys`、`int[] vals`；冲突了就往后一格找（线性探测）。
* **位图（bitmap）**：用一个 `long[]`，第 p 位是 1 表示"价位 p 非空"。找"下一个非空价位"时，一次检查 64 个价位。

---

## 3. 从最笨的解法开始

最笨的想法：**所有订单放进一个 `ArrayList<Order>`**，按需处理。

```java
List<Order> all = new ArrayList<>();            // 所有挂着的单，按到达顺序

void add(Order o)            { all.add(o); }
boolean cancel(long id)      { return all.removeIf(o -> o.id() == id); }          // 扫一遍
long bestBid()               { /* 扫一遍：所有 BUY 里 price 的最大值 */ }
void match(Order taker) {
    while (taker.qty() > 0) {
        Order best = null;                    // 扫一遍：找对面价格最优、同价里最早的
        for (Order o : all) if (isBetter(o, best, taker)) best = o;
        if (best == null || !crosses(taker, best)) break;
        ... 成交 ...
    }
}
```

**正确**，而且短。**慢在哪**：每个操作都是 O(n)，n 是簿上订单数。
* 簿上 10 万张单，来 10 万条命令：10 万 × 10 万 = 10^10 次比较，几十秒。
* 一张大单扫穿 100 个价位，要扫 100 遍整张表——O(n × 吃掉的订单数)。
* `removeIf` 还会把后面的元素往前挪。

**错在哪**：没有错，但会被追问"能更快吗？"——这就是面试的第一个追问点。

---

## 4. 一步一步改进

### 第 1 步：买卖分开

**发现问题**：每次找最优价都要先过滤方向。
**想法**：`bids`、`asks` 分成两个结构。
**新复杂度**：没变（还是 O(n)），但后面的改进都建立在这上面。

### 第 2 步：按价位分组，价位放进有序 Map

**发现问题**：找最优价要扫全部订单 O(n)。
**想法**：订单按价格分组，一个价位 = 一个"组"；组放进 `TreeMap<价格, 价位>`。最优价 = `firstEntry()`。
**为什么能解决**：`TreeMap` 保证 key 有序，最小的 key 永远在最左边，找到它只需走 O(log L) 步（L = 价位数，通常远小于订单数 n）。买盘用 `Comparator.reverseOrder()`，使"最小"= 最高价。
**新复杂度**：`bestBid` / `bestAsk` 从 O(n) → O(log L)。

### 第 3 步：价位内部用队列保证时间优先

**发现问题**：同价位谁先成交？
**想法**：每个价位内放一个 FIFO 队列；成交从队头取。

```java
class PriceLevel { ArrayDeque<Node> fifo = new ArrayDeque<>(); long total; }
```

**新复杂度**：撮合时每吃一张单 O(1)（取队头），加上价位吃光时从 `TreeMap` 删除 O(log L)。

### 第 4 步：撤单太慢 → `LinkedHashMap` + `byId`

**发现问题**：`cancel(id)`：先要知道订单在哪个价位。`ArrayDeque` 还不能 O(1) 删中间元素。撤单变成 O(n)。
**想法 A**：加一个 `HashMap<Long, Node> byId`——给定 id 一步找到订单，订单里记着自己的价格和方向，于是知道去哪个价位。
**想法 B**：价位内的队列换成 `LinkedHashMap<Long, Node>`（2.5 节）——按 id 摘除 O(1)，又保序。
**新复杂度**：`cancel` = `byId.get` O(1) + `book.get(price)` O(log L) + `fifo.remove` O(1) + 价位空了删 `TreeMap` O(log L) → **O(log L)**。

### 第 5 步：缓存价位总量

**发现问题**：`depth()` 要报每个价位的总量，每次把队列加一遍太慢。
**想法**：`PriceLevel` 里存一个 `total`，每次入队 / 出队 / 改量时顺手加减。
**代价**：必须保证**每一处**修改都同步更新 `total`——否则它与真实队列不一致（不变量要时刻维护）。

### 第 6 步：改量的优先级规则

`modify(id, newQty)`：
* **减量**：不动位置。——"让你更吃亏的修改才丢优先级"，减量对别人没有额外伤害。
* **增量**：移到队尾。——否则可以先挂 1 个占着队头，再改成 1000 个，白占便宜。
实现：增量时 `fifo.putLast(id, node)`（对已存在的 key，`LinkedHashMap` 会把它移到链表末尾）。

### 第 7 步：撮合循环

```
left = 新单数量
while left > 0:
    top = 对面 TreeMap.firstEntry()          // 对面最优价那一档
    if top 不存在 或 不交叉: break            // 买：top.price <= 我的限价；卖：top.price >= 我的限价
    maker = top 的队头订单
    fill = min(left, maker.qty)
    产生 Trade(taker, maker, price = maker 的价, fill)
    left -= fill;  maker.qty -= fill;  level.total -= fill
    if maker.qty == 0: 队头出队（pollFirstEntry）；若队空 → 对面 TreeMap 也 pollFirstEntry
剩 left > 0 时：限价单挂簿，市价单作废
```

**为什么这样一定对**：循环每一轮要么把 maker 吃光（它被移除）要么把新单吃光（循环结束），所以必然终止；每一轮都取当前最优的一张单，所以满足价格-时间优先。
**复杂度**：每个成交 O(1)，每吃光一档 O(log L)。总体 O(成交笔数 + 吃光的档数 · log L)。

### 第 8 步：用"事件"描述结果（sealed 类型）

**发现问题**：撮合的结果有很多种：成交了 / 挂簿了 / 被撤了 / 被拒了。返回一个 `String` 或一堆布尔值很难处理。
**想法**：每种结果一个 `record`，它们共同实现一个 **sealed** 接口 `Event`：

```java
sealed interface Event permits Trade, Rested, Cancelled, Modified, Rejected {}
record Trade(long takerId, long makerId, Side takerSide, long price, long qty) implements Event {}
...
```

**为什么能解决**：`sealed` 告诉编译器"Event 只有这五种"。以后用 `switch` 处理 Event 时，漏了任何一种编译器直接报错，不需要 `default`。这比"忘了处理新类型、运行时才发现"可靠得多（见第 6 节）。
同样的做法用在命令 `Command`（`Limit` / `Market` / `Cancel` / `Modify`）上。

### 第 9 步：热路径零分配（Part 4：`TickBook`）

**发现问题**：第 8 步之后的 `OrderBook`：每张订单一个 `Node`、每个价位一个 `PriceLevel` + `LinkedHashMap`（里面每项又是一个 entry 对象）、key 装箱成 `Long`、每条命令返回一个 `ArrayList<Event>`。实际约 420 字节 / 命令。
**想法**：把"对象图"换成"几个预分配好的数组"，整个簿在构造时一次性分配，之后处理命令只读写数组。逐个替换：

| 原来 | 换成 | 为什么可以 |
|---|---|---|
| `TreeMap<Long, PriceLevel>`（价格→价位） | 数组下标：`head[side][tick]` | 价格是**有界整数**（`1..maxTicks-1`），可以直接用价格当下标，O(1)，不用比较 |
| "取 `firstEntry()`" | `bestBid` / `bestAsk` 两个 `int` 变量 + 位图 | 最优价只在"价位变空 / 新价位出现"时变化；变空时用位图找下一档 |
| `Node` 对象 | `long[] oid`、`long[] oqty`、`int[] oprice`、`byte[] oside` | 同一个槽位号在各数组里是同一张订单 |
| `LinkedHashMap` 队列 | `int[] prev`、`int[] next`（侵入式双向链表）+ `head` / `tail` 数组 | 知道槽位号就能 O(1) 摘除 |
| 分配 `new Node` | free list | 释放的槽位串起来重用 |
| `HashMap<Long, Node>` | 开放寻址 `long[] keys` + `int[] vals` | 不装箱 |
| `List<Event>` | 回调 `TradeSink.onTrade(taker, maker, price, qty)` | 调用方决定怎么处理，不创建事件对象 |

**代价**（面试一定要讲）：
* 价格带固定（`maxTicks`），超出的拒绝；订单数上限固定（`capacity`），满了返回 `FULL`。——这是"有界内存"的取舍。
* 代码更长、更容易出 bug（手写哈希删除、链表摘除）。所以要**用 Part 2 的 `OrderBook` 当真值做对拍测试**。
**新复杂度**：`limit` O(成交笔数)；`cancel` O(1)；最优价被吃光 / 撤光后找下一档：位图扫描，最坏 O(maxTicks / 64)，实际常数很小。

---

## 5. 逐段讲解法

### 5.1 数据成员

```java
private final SequencedMap<Long, PriceLevel> bids = new TreeMap<>(Comparator.reverseOrder());
private final SequencedMap<Long, PriceLevel> asks = new TreeMap<>();
private final HashMap<Long, Node> byId = new HashMap<>();
```

三个结构各管一件事：`bids` / `asks` 回答"最优价是多少、下一档是谁"；每个 `PriceLevel` 里的 `fifo`（`LinkedHashMap`）回答"谁排第一、怎么 O(1) 摘掉某人"；`byId` 回答"这个 id 的订单在哪"。
变量声明成 `SequencedMap` 而不是 `TreeMap`，是为了让读代码的人一眼看出"我只用到有序、取头尾这几个能力"。

`Node` 是**可变**的（`qty` 会被成交减少），而对外暴露的 `Order` 是不可变 record（`find` 每次返回新快照）。——内部可变是为了性能，外部不可变是为了安全。

### 5.2 `add` 与"先算后改"

```java
long newTotal = Math.addExact(level == null ? 0L : level.total, qty);
if (level == null) { level = new PriceLevel(); book.put(price, level); }
level.fifo.putLast(id, node);
level.total = newTotal;
byId.put(id, node);
```

`Math.addExact` 在溢出时抛 `ArithmeticException`，普通的 `+` 会静默回绕成负数。把它放在**所有修改之前**：抛出时簿还没变——这叫**异常安全**（失败不留下半个状态）。
如果换成先 `put` 再加总量，抛异常时队列里已经多了一个订单而 `total` 没更新，簿就坏了。

### 5.3 `modify`

增量分支先 `addExact` 算新总量，再改 `n.qty`、`level.total`，最后 `putLast` 移到队尾；减量分支只改数字。注意 `newQty <= 0` 的检查放在"找 id"之前，所以对未知 id 也先报参数错。

### 5.4 撮合循环 `sweep`

```java
while (left > 0) {
    var top = opp.firstEntry();                   // 对面最优档
    if (top == null) break;
    long px = top.getKey();
    boolean crosses = side == Side.BUY ? px <= limit : px >= limit;
    if (!crosses) break;
    var level = top.getValue();
    var maker = level.fifo.firstEntry().getValue(); // 队头
    long fill = Math.min(left, maker.qty);
    out.add(new Trade(takerId, maker.id, side, px, fill));
    ...
    if (maker.qty == 0) {
        level.fifo.pollFirstEntry();
        byId.remove(maker.id);
        if (level.fifo.isEmpty()) opp.pollFirstEntry();
    }
}
```

逐行：`firstEntry` 取对面最优档；`crosses` 判断是否交叉（买单：最低卖价 ≤ 我的限价）；取队头 maker；成交量取两者较小；成交价 `px` 是 maker 所在档的价；maker 吃光就出队并从 `byId` 删除，档空了连价位一起删。
**市价单**复用这个循环：把限价设成"无穷"（买 `Long.MAX_VALUE`，卖 `0`），`crosses` 永远为真。如果换成"另写一个市价单循环"，两份几乎一样的代码迟早会改漏一份。

### 5.5 `execute`：sealed + 模式匹配

```java
return switch (cmd) {
    case Limit(var id, var side, var px, var q)  -> { ... yield events; }
    case Market(var id, var side, var q)          -> { ... }
    case Cancel(var id)                           -> { ... }
    case Modify(var id, var newQty)               -> { ... }
};
```

没有 `default`：`Command` 是 sealed，四种全覆盖编译器才放行。`case Limit(var id, var side, var px, var q)` 一行同时完成"判断类型 + 拆出四个字段"。
校验放在 switch 之前的 `validate` 里，同样是 sealed switch，带 `when` 守卫（`case Limit l when l.price() <= 0 -> INVALID_PRICE`）——**从上到下第一个匹配的生效**，所以"更具体的错误"写在前面。

**为什么 `ownLevelWouldOverflow` 在撮合之前**：限价单最后可能挂簿。若撮合完才发现挂不进去（总量溢出），成交事件已经发出，收不回。所以先做保守检查，宁可误拒也不做半件事。

### 5.6 `BatchMatcher`

校验整张表 → 转成 `Limit` 命令 → 复用 `OrderBook.executeAll` → 从事件流里挑出 `Trade`。

```java
List<OrderBook.Trade> trades = events.stream().<OrderBook.Trade>mapMulti((e, sink) -> {
    if (e instanceof OrderBook.Trade t) sink.accept(t);
}).toList();
```

`mapMulti` 对每个元素可以输出 0 个或多个结果，这里相当于"filter + 强转"一步到位。名义金额 `Σ price × qty` 用 `multiplyExact` / `addExact`：价格 4×10^9、数量 3×10^9 的乘积 1.2×10^19 已经超过 `long` 上限 9.22×10^18，普通乘法会得到一个看起来正常的错数。

### 5.7 `TickBook`

**槽位池与 free list**（构造器）：`next[i] = i + 1`，把所有槽位串成一条空闲链，`freeHead = 0`。分配 `slot = freeHead; freeHead = next[slot]`；释放 `next[slot] = freeHead; freeHead = slot`。两步都是 O(1)，不分配内存。

**`rest`（挂簿）**：把槽位接到 `tail[s][p]` 之后；如果这个价位原本是空的（`t < 0`），还要：设队头、位图置位、必要时更新 `bestBid` / `bestAsk`。

**`unlink`（摘除，撮合吃光 / 撤单共用）**：

```java
if (pr >= 0) next[pr] = nx; else head[s][p] = nx;   // 前驱的 next 指向后继；没有前驱说明我是队头
if (nx >= 0) prev[nx] = pr; else tail[s][p] = pr;   // 后继的 prev 指向前驱；没有后继说明我是队尾
```

价位变空后：清位图的位；如果它正是最优价，用位图找下一档：

```java
bestBid = atOrBelow(bits[0], p - 1);   // 买盘：找 ≤ p-1 的最高非空价位
bestAsk = atOrAbove(bits[1], p + 1);   // 卖盘：找 ≥ p+1 的最低非空价位
```

`atOrAbove` 的做法：先取出 `from` 所在的那个 64 位字，用 `-1L << (from & 63)` 屏蔽掉 `from` 之前的位；字非零就用 `Long.numberOfTrailingZeros` 定位最低的 1；否则看下一个字。每个字 64 个价位，一条指令搞定。

**开放寻址哈希表**：`hash(id)` 先乘黄金比例常数再折叠高位，打散连续 id；`find` 从 `hash` 开始线性往后找，遇到空槽（`keys[i] == 0`，所以 `id` 必须 > 0）就是"没有"。
**删除**最微妙：不能直接把槽位置 0，否则会"切断"后面那些因冲突被挤到后面的 key 的探测链，导致 `find` 找不到它们。回移删除（backward shift）把后面能挪的元素挪回空洞，不留"墓碑"。判断元素 j（理想位置 k）能否挪到空洞 i：`((j - k) & mask) >= ((j - i) & mask)`，即 k 不在环形区间 (i, j] 内。

**哨兵值**：`bestBid = 0` 表示没有买盘（合法价格 ≥ 1），`bestAsk = maxTicks` 表示没有卖盘（合法价格 ≤ maxTicks-1）。这样撮合条件 `bestAsk <= p`（买）/ `bestBid >= p`（卖）在对面为空时自然为假，**循环里不用单独判空**。

**为什么 `MAX_QTY = 2^40`、`capacity ≤ 2^22`**：价位总量最坏是 capacity × MAX_QTY = 2^62 < 2^63，所以价位总量永远不会溢出 `long`，热路径里不需要 `addExact`。这是"用输入上限换掉运行时检查"。

---

## 6. Java 21 特性小课

> 这里只讲本题用到的部分。

### `record`（含紧凑构造器）

旧写法：一个 `Trade` 类要手写字段、构造器、getter、`equals`、`hashCode`、`toString`，40 行。
新写法：`record Trade(long takerId, long makerId, Side takerSide, long price, long qty) implements Event {}` 一行，且 `equals` 按字段比较——可以直接用 `equals` 比较事件列表。
紧凑构造器：`record Order(...) { Order { if (qty <= 0) throw ...; } }`，字段赋值由编译器在你的代码之后自动补上，所以"非法的订单根本构造不出来"。
**不该用**：需要可变状态的（`Node` 的 `qty` 会变，所以 `Node` 是普通类）。

### `sealed` + `switch` 模式匹配 + record 解构

旧写法：

```java
String render(Event e) {
    if (e instanceof Trade) { Trade t = (Trade) e; return "TRADE ..." + t.price(); }
    else if (e instanceof Rested) { ... }
    ...
    else throw new IllegalStateException();     // 新增一种 Event 时这里不会报编译错误
}
```

新写法：

```java
case Trade(var taker, var maker, var side, var px, var q) -> "TRADE taker=%d ...".formatted(...);
```

* `sealed ... permits` 声明"只有这几种"；
* `switch` 对 sealed 类型做**穷尽检查**：少一种直接编译错误，不需要 `default`；
* record 模式把字段拆出来绑定成变量，省掉强转和 getter 调用；
* `when` 守卫：`case Limit l when l.price() <= 0 -> ...`。
**坑**：加了 `default` 就丧失穷尽检查——sealed switch 里不要写 `default`。守卫分支的顺序有意义（第一个匹配的生效），不加守卫的"兜底"分支必须写在后面，否则编译器报"被支配"（dominated）。

### `switch` 表达式 + `yield`

旧写法：`switch` 语句里每个 case 要 `break`，忘了就 fallthrough（穿透到下一个 case）。
新写法：`case X -> 值;` 无穿透；需要多行时用块 `{ ...; yield 值; }`。`execute` 里每个 case 是个块，最后 `yield events`。

### `instanceof` 模式

旧：`if (e instanceof Trade) { Trade t = (Trade) e; ... }`。新：`if (e instanceof Trade t) { ... }`——判断和强转一步，`t` 只在条件为真的范围内可见。

### Sequenced Collections

见 2.6。旧写法取队头：`map.entrySet().iterator().next()`（又长又容易忘了判空）；新写法 `map.firstEntry()`。
`LinkedHashMap.putLast` 对已有 key 的"移到队尾"语义，在 Java 21 之前要 `remove` 再 `put` 两步。

### 未命名模式 `_`（Java 21 预览，需要 `--enable-preview`）

`case Limit _, Market _ -> ...`：不需要绑定变量时写 `_`，明确告诉读者"我不关心里面是什么"，还允许在一个 case 里写多个模式。
**限制**：Java 21 里是预览特性（JDK 22 正式）；编译运行需要 `--enable-preview`。

### `Stream.mapMulti` / `toList()`

旧：`.filter(e -> e instanceof Trade).map(e -> (Trade) e).collect(Collectors.toList())`。新：`mapMulti` 一步，`toList()` 返回不可变列表。
**什么时候不该用**：简单的 filter+map 用 filter+map 更好读；`mapMulti` 适合"每个元素产出少量结果、不想创建中间 Stream"的场景。

### `Math.addExact` / `multiplyExact` / `String.formatted`

旧：`a + b` 溢出静默回绕；要检查得手写 `if (a > Long.MAX_VALUE - b)`。新：`addExact` 溢出时抛 `ArithmeticException`。
`"…%d".formatted(x)` 代替 `String.format("…%d", x)`，少一个参数位置的跳转。

### 文本块、`var`、`Comparator.reverseOrder()` / `Objects.requireNonNull`

文本块 `"""` 让多行脚本样例原样出现在代码里（不用 `"…\n" + "…\n"`）；`var` 只在右边类型显然时用（`var events = new ArrayList<Event>()`）；`Comparator.reverseOrder()` 让买盘"最小的 key = 最高价"。

---

## 7. 追问预演

**Q1. 为什么价位内用 `LinkedHashMap` 而不是 `ArrayDeque`？**
思考：先想撤单的流程——撤的订单可能在队伍中间。`ArrayDeque.remove(Object)` 要线性查找 + 挪动元素，O(队伍长度)。需要"按 id O(1) 找到并摘除，同时保序"的结构 → 哈希表 + 链表。
答案要点：LinkedHashMap = HashMap + 双向链表；撤单、改量 O(1)；队头 `firstEntry`。代价是每项多一个 entry 对象，更占内存。
可以说的话：「我需要两件事：先来后到，和按 id O(1) 撤单。ArrayDeque 只有前者，LinkedHashMap 两个都有。」

**Q2. 撤单的复杂度是多少？**
O(log L)，L 是价位数：`byId.get` O(1)，找价位 `TreeMap.get` O(log L)，`fifo.remove` O(1)；如果价位空了再 `TreeMap.remove` O(log L)。想要真正 O(1) 要把价位换成数组下标（Part 4）。

**Q3. 为什么用 `long` 不用 `double` 表示价格？**
浮点数存不准十进制小数，`0.1 + 0.2 != 0.3`；两个"相等"的价格可能分到两个价位，比较也要处理 epsilon。整数 tick 精确、可比较、可以直接当数组下标。数量同理。

**Q4. 同价位怎么保证先来先成交？**
价位内队列按到达顺序入队，撮合只从队头取；部分成交的 maker 留在队头（量减少）。modify 增量会丢优先级（移到队尾），减量不会。

**Q5. 市价单没有价格，怎么放进你的结构？**
把它当成限价无穷大（买）/ 0（卖）走同一个撮合循环，吃完剩余的作废。避免写两套循环。

**Q6. 怎么让它更快？（Part 4 的开场白）**
思考：先 profile 看是 CPU 还是 GC。这里是对象多：装箱 key、Node、entry、Event 列表。要把"对象图"变成"数组"：价格是有界整数 → 数组下标代替 `TreeMap`；订单池 + 侵入式链表代替 Node 和 LinkedHashMap；开放寻址哈希代替 `HashMap<Long,…>`；回调代替事件对象。
答案要点：表格见第 4 节第 9 步；取舍是有界内存（价格带、容量），超出就拒绝 / 返回 FULL。
可以说的话：「热路径零分配，所有内存启动时一次分配；价格是有界整数，所以树换成数组；代价是价格带和容量是固定的，我会在边界上拒绝并返回错误码。」

**Q7. 价格范围很大（不是有界的）怎么办？**
数组放不下。折中：只对"靠近中间价的一段"用数组（比如 ±几千 tick），远处的价位放一棵 `TreeMap`（很少被访问）。或用 sorted array + 二分（价位少、缓存友好）。

**Q8. 多线程怎么办？**
订单簿的撮合有严格的顺序依赖，锁的粒度很难细分。常见做法：**单线程撮合引擎**（一个品种一个线程），所有命令通过队列（如 LMAX Disruptor 的 ring buffer）串行送进来——没有锁、可重现、延迟稳定；横向扩展靠"按品种分片"。不要给订单簿的每个方法加 `synchronized`——撮合仍然要整体串行，锁只会增加开销。

**Q9. 怎么测试撮合正确？**
(1) 手算样例；(2) 不变量：簿永远不交叉（best bid < best ask）、数量守恒（提交量 = 2 × 成交量 + 剩余挂单 + 被撤量）；(3) 对拍：快版本和慢但明显正确的版本喂同一串随机命令，逐步比较。三种都值得做。

---

## 8. 常见误区

1. **`add` 就撮合。** Part 1 的 `add` 是"只挂不撮"，两张交叉的单可以同时在簿上；撮合是 `execute(Limit)` 的事。混在一起会让 Part 1 的深度查询（故意挂出交叉的簿）出错。
2. **成交价取 taker 的限价。** 买 110 的单吃卖 101 的单，成交价是 101（maker 价），不是 110。
3. **部分成交的 maker 被放到队尾。** 它应该留在队头，只是数量减少。放到队尾等于让它插队的反面。
4. **增量 modify 保留了位置。** 加量必须重新排队，否则可以先挂小单占队头再偷偷加量。
5. **价位空了不删。** 空的 `PriceLevel` 留在 `TreeMap` 里，`firstEntry()` 会返回一个空价位当作"最优价"。撤单、成交吃光都要检查"队空就删价位"。
6. **先改后查溢出。** `total += qty` 溢出回绕成负数，簿悄悄坏掉；要先 `addExact` 再改。
7. **`double` 价格 / `int` 数量。** `int` 在大单累加时溢出；`double` 比较相等不可靠。
8. **`Long` 用 `==` 比较。** 装箱对象比较的是引用；缓存范围（-128..127）之内碰巧相等、之外不等——典型的"小数据里过、线上错"。用 `equals` 或者保持基本类型。
9. **（Part 4）开放寻址删除直接置 0。** 会断掉探测链，要用回移删除。
10. **（Part 4）最优价被吃光后忘了更新。** 位图和 `bestBid` / `bestAsk` 必须在"价位变空"和"新价位出现"两处都维护。最优价被吃光后，要能跨过一万多个空价位找到下一档。

---

## 9. 自测题

**Q1（概念）** 为什么买盘的 `TreeMap` 要用 `Comparator.reverseOrder()`？

<details><summary>答案</summary>买盘的最优价是最高价。`TreeMap` 的 `firstEntry()` 返回比较器下"最小"的 key；用反序比较器后，最大价格排在最前面，这样两边都可以用 `firstEntry()` 取最优价，代码对称。</details>

**Q2（手算）** 簿上卖盘：100:[#1 x2, #2 x3]，101:[#3 x4]。来 `LIMIT 9 BUY 101 8`，写出事件，并说出最终簿。

<details><summary>答案</summary>先吃 100 档队头：Trade(9,1,BUY,100,2)，再 Trade(9,2,BUY,100,3)；100 档空；再吃 101 档：Trade(9,3,BUY,101,3)（剩 3 要凑 8-5=3，吃 #3 的 3 个）。#9 吃光，不挂簿。最终卖盘：101:[#3 x1]；买盘空。</details>

**Q3（复杂度）** 撤单为什么是 O(log L) 而不是 O(1)？怎样让它变成 O(1)？

<details><summary>答案</summary>瓶颈在用价格找价位：`TreeMap.get(price)` 是 O(log L)。如果价格有界，价位用数组下标存（`head[side][tick]`），找价位 O(1)；再配合侵入式链表 O(1) 摘除，整个撤单 O(1)（价位变空时更新最优价另算）。</details>

**Q4（找 bug）** 下面的 `modify` 有什么问题？

```java
boolean modify(long id, long newQty) {
    Node n = byId.get(id);
    if (n == null) return false;
    PriceLevel lv = book(n.side).get(n.price);
    lv.total += newQty - n.qty;
    n.qty = newQty;
    return true;
}
```

<details><summary>答案</summary>(1) 没检查 `newQty <= 0`；(2) 增量没有移到队尾（丢优先级）；(3) `total += …` 可能溢出且没有先检查，抛异常前簿已被改。</details>

**Q5（小编程）** 写一个方法 `long spread(OrderBook b)`：返回 best ask − best bid，任一侧为空返回 −1。用 `OptionalLong` 的 API。

<details><summary>答案</summary>

```java
static long spread(OrderBook b) {
    var bid = b.bestBid();
    var ask = b.bestAsk();
    return bid.isPresent() && ask.isPresent() ? ask.getAsLong() - bid.getAsLong() : -1;
}
```
注意：Part 1 的 `add` 不撮合，簿可能交叉，此时 spread 为负数——调用方需要知道这一点。</details>

**Q6（设计）** 为什么 `TickBook.limit` 在池满时返回 `FULL` 且不撮合，而不是先撮合再拒绝剩余部分？

<details><summary>答案</summary>先撮合再发现没地方挂，成交已经发生（回调已经通知出去），"拒绝"的语义就不干净了。池满时对一张可能会完全成交的单误拒是保守的，但简单、可预测、状态不会半改。这是有界内存系统常见的"背压（back-pressure）"策略。</details>

---

「延伸」CLRS《算法导论》「红黑树」一章。
