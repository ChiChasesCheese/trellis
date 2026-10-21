# hc05 · Market Order Book（订单簿 + 撮合 + 低分配版本）—— 讲义

> 读者：只会基本 Java（类、方法、循环、`ArrayList` / `HashMap`）。覆盖订单簿与批量限价撮合。

---

## 1. 问题是什么

### 1.1 订单簿是什么

菜市场里有人举牌「**买**，最多出 100 块，要 5 个」，另一人「**卖**，最少 101 块，要 3 个」。所有「还没成交、挂着等人」的牌子按价格排好，就是**订单簿**（order book）。

* **买单**（BUY，bid）：给出**最高愿意出的价**。
* **卖单**（SELL，ask / offer）：给出**最低愿意收的价**。
* **价位**（price level）：同一价格上所有牌子。
* **最优价**：买盘**最高**价 best bid，卖盘**最低**价 best ask。best bid < best ask 时没人能成交；有人出价 ≥ 对面最低价就**成交**（trade）。

### 1.2 手算例子

簿上现有（价格单位 tick，当作元）：

```
        卖盘 (asks)，价格从低到高，越靠上越"好"
        价位 101:  [#1 数量5] → [#2 数量3]     ← 同价位按"先来后到"排队，#1 先到
        价位 102:  [#3 数量4]
  ------------------------------------------   ← 中间的缝隙叫 spread
        买盘 (bids)：空
```

新单 **#4，买，限价 101，数量 6**：对面最便宜的 101 档 ≤ 限价，可成交；同价位先到先成交 → 先和 #1 成交 5 个（成交价取 **#1 的价 101**），再和 #2 成交 1 个；#4 全部成交不挂簿。簿变成：

```
        价位 101:  [#2 数量2]         ← #2 被吃掉 1 个，还剩 2 个，仍然排在队头
        价位 102:  [#3 数量4]
```

「**价格优先、同价按时间先后**」叫**价格-时间优先**（price-time priority），几乎所有交易所都用。

### 1.3 题目要做的四件事（Part 1–4）

1. **维护**簿：挂单、撤单、改量、问最优价、问前 N 档深度（先不撮合）。
2. **撮合**：新单按价格-时间优先吃对面的单，吃不完的挂簿；用一组"事件"（成交、挂簿、撤销……）描述发生了什么。
3. 一批 `[side, price, qty]` 订单按到达顺序处理并汇总。
4. **性能追问**：「每秒几百万条命令，GC 很忙，怎么办？」

---

## 2. 前置知识

### 2.1 订单簿术语

| 词 | 意思 |
|---|---|
| tick | 最小报价单位。用**整数 tick** 表示价格（"10050" = 100.50 元），不用小数 |
| maker / taker | maker = 已挂在簿上的单（被动方）；taker = 新来主动去吃的单 |
| 限价单（limit） | 带价格上限（买）/ 下限（卖）。吃不完的挂簿 |
| 市价单（market） | 不限价，有多少对手盘吃多少。约定：吃不完的部分**作废**（IOC，立即成交否则取消） |
| 成交价 | 取 **maker 的价**：maker 报的是"愿意的最差价"，taker 限价只是上限，取 maker 价让 taker 有"价格改善" |
| 深度（depth） | 买盘 / 卖盘各档价位上的总量，从最优价往外数 N 档 |

**不用 `double` 表示价格**：`0.1 + 0.2 != 0.3`，二进制浮点存不准十进制小数，两个本该相等的价格会比出"不等"，订单挂在两个"看起来一样"的价位上。整数 tick 没这个问题。

### 2.2 复杂度：O(1)、O(log n)、O(n)

O(1) 常数（数组按下标取、哈希查 key 平均）；O(n) 线性；O(log n) 每步规模减半，n = 100 万只约 20 步。这里所有"改进"都是把 O(n) 变 O(log n) 或 O(1)。例：100 万订单每秒 100 万次撤单，O(n) 要 10^12 次操作（CPU 一秒约 10^9 次，要 1000 秒），O(log n) 约 2×10^7，O(1) 毫秒级。

### 2.3 二叉搜索树、红黑树与 `TreeMap`

`TreeMap<K, V>` 是**按 key 排好序**的 Map，可随时问"最小的 key"、"≥ 某 key 的第一个"，也可按顺序遍历。

订单簿要"最优价"，成交吃光一档后要立刻知道"下一个最优价"。`HashMap<价格, 价位>` 不能答"最小价格"（要扫全部 key，O(L)，L 价位数）；排好序的 `ArrayList` 取最小 O(1) 但**插入新价位**要挪元素 O(L)；`TreeMap` 取最小、插入、删除都是 O(log L)。

**怎么工作**——先看**二叉搜索树**（BST）：每个节点左子树所有 key 比它小，右子树所有 key 比它大。

```
              100
             /    \
           98      103
          /  \       \
        97    99      105
```

最小一直往左（97），最大一直往右（105）。查 99：从 100 起往左到 98，再往右到 99，每步淘汰一半，步数 = 树高。问题：key 按 1, 2, 3, 4, 5 顺序插入会退化成一根"棍子"，高度 = n，查找 O(n)。

**红黑树**（red-black tree）是自平衡 BST：节点涂红或黑，规则（根是黑；红节点的孩子是黑；任一节点到其下所有叶子的路径上黑节点数相同）靠"旋转"和"改色"维持，保证**最长路径不超过最短路径的两倍**，高度 ≤ 2·log2(n+1)。不需会写，要知道：**`TreeMap` 就是红黑树，操作 O(log n)，key 有序**。

```java
TreeMap<Long, String> asks = new TreeMap<>();      // 默认按 key 从小到大
asks.put(102L, "b"); asks.put(101L, "a");
asks.firstEntry();        // → 101=a   最小的 key（O(log n)）
asks.pollFirstEntry();    // 取出并删除最小的那一项

TreeMap<Long, String> bids = new TreeMap<>(Comparator.reverseOrder());  // 从大到小
bids.put(99L, "x"); bids.put(100L, "y");
bids.firstEntry();        // → 100=y   "最小"在这个比较器下 = 数值最大 = 最高买价
```

**小技巧**：买盘最优价是**最高**价。买盘用 `Comparator.reverseOrder()`，两边都用 `firstEntry()` 取最优价，代码对称。key 类型是 `Long`（对象）——集合只能装对象，自动"装箱"（2.7）。

### 2.4 `HashMap` 与"按 id 找订单"

`HashMap<K, V>` 由 key 的"哈希值"算数组下标直接取，平均 O(1)，**无顺序**。撤单和改量只带 `id`，没有 `id → 订单` 表就得遍历所有价位的所有队列，O(n)；有了 `HashMap<Long, Node> byId`，一步找到订单并读出它的价格和方向。

```java
HashMap<Long, Node> byId = new HashMap<>();
byId.put(7L, node);
Node n = byId.get(7L);        // 找不到返回 null
byId.remove(7L);
```

### 2.5 队列（FIFO）与 `LinkedHashMap`——同价位怎么排队

同价位先来先成交（FIFO），每个价位内部有个"队伍"。`ArrayDeque<Node>` 入队尾、出队头 O(1)，但撤单者可能在队伍中间，`remove(obj)` 要从头找 O(队伍长度)（排 10 万张单时扫 10 万次）。**更好**：`LinkedHashMap<Long, Node>`，"哈希表 + 双向链表"的合体：

```
哈希表（按 key 找，O(1)）:        双向链表（记录插入顺序）:
  id=7  ──────────────────┐        head ⇄ [#7] ⇄ [#3] ⇄ [#9] ⇄ tail
  id=3  ───────────┐      │              ▲      ▲      ▲
  id=9  ────┐      │      │              └──────┴──────┘  哈希表里每一项同时挂在链表上
```

按 id 找节点 O(1)（哈希表），摘节点只改前后邻居指针 O(1)（双向链表），遍历按插入顺序、队头 = 最先插入的。所以它**既是 Map 又是队列**：`remove(id)`、`firstEntry()`、`pollFirstEntry()`、`putLast(k, v)` 都是 O(1)。

### 2.6 Sequenced Collections（Java 21）

Java 21 给"有顺序的集合"统一加了 `SequencedCollection / SequencedSet / SequencedMap`：`getFirst()` / `getLast()` / `reversed()`；Map 有 `firstEntry()` / `lastEntry()` / `pollFirstEntry()` / `putFirst()` / `putLast()`。此前取"最后一个"无统一方式（`List` 用 `get(size() - 1)`，`LinkedHashSet` 要遍历到底，`Deque` 用 `getLast()`）。这里 `TreeMap` 和 `LinkedHashMap` 都是 `SequencedMap`，价位表和价位内队列都声明成 `SequencedMap<Long, ...>`。

```java
SequencedMap<Long, Node> fifo = new LinkedHashMap<>();
fifo.putLast(7L, n7);              // 排到队尾；如果 7 已经在队伍里，会被移到队尾（"重新排队"）
Node head = fifo.firstEntry().getValue();   // 队头
fifo.pollFirstEntry();             // 队头出队
```

### 2.7 装箱（boxing）、GC 与为什么性能题盯着"分配"

`long` 是 8 字节裸数字；`Long` 是堆上对象（对象头约 16 字节）。集合只能存对象，`map.put(5L, x)` 会悄悄创建 `Long`——**装箱**（-128..127 有缓存，其余每次新对象）。

堆对象由**垃圾回收器（GC）**清理；分配越快 GC 越忙，GC 暂停对交易系统是"延迟毛刺"，对象散落内存还要"追指针"，缓存命中率低。所以低延迟系统追求**热路径零分配**：处理一条命令不 `new`。

**数字**（同一串随机命令）：Part 2 的 `OrderBook` 每条命令平均分配约 **420 字节**（20 万条共约 84 MB）；Part 4 的 `TickBook` 处理 60 万条命令分配 **0 字节**。

### 2.8 Part 4 的"数组式"技巧（第 4 节第 9 步用）

* **结构数组（struct-of-arrays）**：不建 `Order` 对象，而是 `long[] id`、`long[] qty`、`int[] price`……第 i 号订单是各数组第 i 位，一次分配只读写。
* **侵入式链表**：`prev` / `next` 放进 `int[]`，存"数组下标"。
* **free list**：没用的槽位串成链，要新订单从链头拿，释放挂回链头，O(1)、不 `new`。
* **开放寻址哈希表**：自己用 `long[] keys`、`int[] vals`，冲突就往后一格找（线性探测），不装箱。
* **位图（bitmap）**：`long[]` 的第 p 位为 1 表示"价位 p 非空"，找下一个非空价位时一次查 64 个。

---

## 3. 从最笨的解法开始

**所有订单放进一个 `ArrayList<Order>`**：

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

**正确**而且短，但每个操作 O(n)（n 是簿上订单数）：10 万张单、10 万条命令要 10^10 次比较，几十秒；一张大单扫穿 100 个价位要扫 100 遍整表；`removeIf` 还会前挪元素。会被追问"能更快吗？"。

---

## 4. 一步一步改进

### 第 1 步：买卖分开

每次找最优价都要先过滤方向，所以 `bids`、`asks` 分成两个结构（复杂度没变，后面的改进建立在此上）。

### 第 2 步：按价位分组，价位放进有序 Map

找最优价要扫全部订单 O(n)。订单按价格分组，组放进 `TreeMap<价格, 价位>`，最优价 = `firstEntry()`，走 O(log L) 步（L = 价位数，远小于订单数 n）。买盘用 `reverseOrder()` 使"最小"= 最高价。`bestBid` / `bestAsk` 从 O(n) → O(log L)。

### 第 3 步：价位内部用队列保证时间优先

同价位谁先成交？每个价位内放 FIFO 队列，成交从队头取。

```java
class PriceLevel { ArrayDeque<Node> fifo = new ArrayDeque<>(); long total; }
```

撮合时每吃一张单 O(1)，价位吃光时从 `TreeMap` 删除 O(log L)。

### 第 4 步：撤单太慢 → `LinkedHashMap` + `byId`

`cancel(id)` 要先知道订单在哪个价位，`ArrayDeque` 又不能 O(1) 删中间元素，撤单 O(n)。**A**：`byId` 表——给 id 一步找到订单（记着价格和方向）。**B**：价位内队列换成 `LinkedHashMap<Long, Node>`（2.5）——按 id 摘除 O(1)，又保序。

`cancel` = `byId.get` O(1) + `book.get(price)` O(log L) + `fifo.remove` O(1) + 价位空了删 `TreeMap` O(log L) → **O(log L)**。

### 第 5 步：缓存价位总量

`depth()` 要报每价位总量，每次把队列加一遍太慢。`PriceLevel` 存 `total`，入队 / 出队 / 改量时顺手加减。**代价**：**每一处**修改都必须同步更新，否则与真实队列不一致（不变量）。

### 第 6 步：改量的优先级规则

`modify(id, newQty)`：
* **减量**：不动位置——让别人没额外损失的修改不丢优先级。
* **增量**：移到队尾——否则可先挂 1 个占队头，再改成 1000 个，白占便宜。

增量时 `fifo.putLast(id, node)`（对已存在的 key，`LinkedHashMap` 会把它移到链表末尾）。

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

每轮要么吃光 maker（被移除）要么吃光新单（循环结束），必然终止；每轮取当前最优的一张单，满足价格-时间优先。每个成交 O(1)，每吃光一档 O(log L)。

### 第 8 步：用"事件"描述结果（sealed 类型）

撮合结果有成交 / 挂簿 / 撤销 / 拒绝等多种，返回 `String` 或布尔值难处理。每种一个 `record`，共同实现 **sealed** 接口 `Event`：

```java
sealed interface Event permits Trade, Rested, Cancelled, Modified, Rejected {}
record Trade(long takerId, long makerId, Side takerSide, long price, long qty) implements Event {}
...
```

`sealed` 告诉编译器"Event 只有这五种"，`switch` 漏一种直接编译报错，不需 `default`，比运行时才发现可靠得多（第 6 节）。命令 `Command`（`Limit` / `Market` / `Cancel` / `Modify`）同理。

### 第 9 步：热路径零分配（Part 4：`TickBook`）

第 8 步的 `OrderBook`：每订单一个 `Node`、每价位一个 `PriceLevel` + `LinkedHashMap`、key 装箱、每条命令返回 `ArrayList<Event>`，约 420 字节 / 命令。**想法**：把"对象图"换成预分配好的数组，构造时一次性分配，之后只读写：

| 原来 | 换成 | 为什么可以 |
|---|---|---|
| `TreeMap<Long, PriceLevel>`（价格→价位） | 数组下标 `head[side][tick]` | 价格是**有界整数**（`1..maxTicks-1`），直接当下标 O(1)，不用比较 |
| "取 `firstEntry()`" | `bestBid` / `bestAsk` 两个 `int` + 位图 | 最优价只在"价位变空 / 新价位出现"时变；变空时用位图找下一档 |
| `Node` 对象 | `long[] oid`、`long[] oqty`、`int[] oprice`、`byte[] oside` | 同一槽位号在各数组里是同一张订单 |
| `LinkedHashMap` 队列 | `int[] prev`、`int[] next`（侵入式双向链表）+ `head` / `tail` 数组 | 知道槽位号就能 O(1) 摘除 |
| `new Node` | free list | 释放的槽位串起来重用 |
| `HashMap<Long, Node>` | 开放寻址 `long[] keys` + `int[] vals` | 不装箱 |
| `List<Event>` | 回调 `TradeSink.onTrade(taker, maker, price, qty)` | 调用方决定怎么处理，不建事件对象 |

**代价**（面试必讲）：
* 价格带固定（`maxTicks`），超出的拒绝；订单数上限固定（`capacity`），满了返回 `FULL`——"有界内存"的取舍。
* 代码更长、更易出 bug（手写哈希删除、链表摘除），所以要**用 Part 2 的 `OrderBook` 当真值对拍**。

复杂度：`limit` O(成交笔数)；`cancel` O(1)；最优价被吃光 / 撤光后找下一档用位图扫描，最坏 O(maxTicks / 64)，常数很小。

---

## 5. 逐段讲解法

### 5.1 数据成员

```java
private final SequencedMap<Long, PriceLevel> bids = new TreeMap<>(Comparator.reverseOrder());
private final SequencedMap<Long, PriceLevel> asks = new TreeMap<>();
private final HashMap<Long, Node> byId = new HashMap<>();
```

`bids` / `asks` 答"最优价、下一档是谁"；每个 `PriceLevel` 的 `fifo` 答"谁排第一、怎么 O(1) 摘掉某人"；`byId` 答"这个 id 的订单在哪"。声明成 `SequencedMap` 而非 `TreeMap`，表明只用到有序、取头尾的能力。`Node` **可变**（`qty` 被成交减少），对外的 `Order` 是不可变 record（`find` 返回新快照）——内部可变为性能，外部不可变为安全。

### 5.2 `add` 与"先算后改"

```java
long newTotal = Math.addExact(level == null ? 0L : level.total, qty);
if (level == null) { level = new PriceLevel(); book.put(price, level); }
level.fifo.putLast(id, node);
level.total = newTotal;
byId.put(id, node);
```

`addExact` 溢出抛 `ArithmeticException`（普通 `+` 静默回绕成负数）。放在**所有修改之前**：抛出时簿还没变——**异常安全**。若先 `put` 再加总量，抛异常时队列已多一个订单而 `total` 没更新，簿就坏了。

### 5.3 `modify`

增量先 `addExact` 算新总量，再改 `n.qty`、`level.total`，最后 `putLast` 移队尾；减量只改数字。`newQty <= 0` 检查在"找 id"之前，未知 id 也先报参数错。

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

`firstEntry` 取对面最优档；`crosses` 判交叉（买单：最低卖价 ≤ 限价）；取队头 maker；成交量取较小者；成交价 `px` 是 maker 所在档的价；maker 吃光就出队并从 `byId` 删除，档空连价位一起删。**市价单**复用此循环：限价设成"无穷"（买 `Long.MAX_VALUE`，卖 `0`），`crosses` 永远为真——两份几乎一样的循环迟早改漏一份。

### 5.5 `execute`：sealed + 模式匹配

```java
return switch (cmd) {
    case Limit(var id, var side, var px, var q)  -> { ... yield events; }
    case Market(var id, var side, var q)          -> { ... }
    case Cancel(var id)                           -> { ... }
    case Modify(var id, var newQty)               -> { ... }
};
```

没有 `default`：`Command` 是 sealed，四种全覆盖才放行。`case Limit(var id, var side, var px, var q)` 一行完成"判断类型 + 拆字段"。校验在 switch 之前的 `validate`（同样是 sealed switch，带 `when` 守卫，如 `case Limit l when l.price() <= 0 -> INVALID_PRICE`）——**从上到下第一个匹配的生效**，"更具体的错误"写前面。

**`ownLevelWouldOverflow` 为何在撮合之前**：限价单最后可能挂簿；若撮合完才发现挂不进去（总量溢出），成交事件已发出收不回。先保守检查，宁可误拒也不做半件事。

### 5.6 `BatchMatcher`

校验整张表 → 转成 `Limit` 命令 → 复用 `OrderBook.executeAll` → 从事件流挑出 `Trade`。

```java
List<OrderBook.Trade> trades = events.stream().<OrderBook.Trade>mapMulti((e, sink) -> {
    if (e instanceof OrderBook.Trade t) sink.accept(t);
}).toList();
```

`mapMulti` 对每元素输出 0 个或多个结果，相当于"filter + 强转"一步。名义金额 `Σ price × qty` 用 `multiplyExact` / `addExact`：价格 4×10^9、数量 3×10^9 的乘积 1.2×10^19 超过 `long` 上限 9.22×10^18，普通乘法会给出看似正常的错数。

### 5.7 `TickBook`

**槽位池与 free list**：`next[i] = i + 1` 串成空闲链，`freeHead = 0`。分配 `slot = freeHead; freeHead = next[slot]`；释放 `next[slot] = freeHead; freeHead = slot`。都 O(1) 且不分配内存。

**`rest`（挂簿）**：槽位接到 `tail[s][p]` 之后；价位原本为空（`t < 0`）时还要设队头、位图置位、必要时更新 `bestBid` / `bestAsk`。

**`unlink`（摘除，撮合吃光 / 撤单共用）**：

```java
if (pr >= 0) next[pr] = nx; else head[s][p] = nx;   // 前驱的 next 指向后继；没有前驱说明我是队头
if (nx >= 0) prev[nx] = pr; else tail[s][p] = pr;   // 后继的 prev 指向前驱；没有后继说明我是队尾
```

价位变空后清位图；若它正是最优价，用位图找下一档：

```java
bestBid = atOrBelow(bits[0], p - 1);   // 买盘：找 ≤ p-1 的最高非空价位
bestAsk = atOrAbove(bits[1], p + 1);   // 卖盘：找 ≥ p+1 的最低非空价位
```

`atOrAbove`：取 `from` 所在的 64 位字，用 `-1L << (from & 63)` 屏蔽 `from` 之前的位；字非零就用 `Long.numberOfTrailingZeros` 定位最低的 1，否则看下一个字。

**开放寻址哈希表**：`hash(id)` 乘黄金比例常数再折叠高位，打散连续 id；`find` 线性往后找，遇空槽（`keys[i] == 0`，所以 `id` 必须 > 0）即"没有"。**删除**最微妙：直接置 0 会"切断"后面因冲突被挤后的 key 的探测链，`find` 找不到它们。用回移删除（backward shift）把后面能挪的元素挪回空洞，不留"墓碑"。元素 j（理想位置 k）能挪到空洞 i 当且仅当 `((j - k) & mask) >= ((j - i) & mask)`，即 k 不在环形区间 (i, j] 内。

**哨兵值**：`bestBid = 0` 表示没买盘（合法价格 ≥ 1），`bestAsk = maxTicks` 表示没卖盘。撮合条件 `bestAsk <= p`（买）/ `bestBid >= p`（卖）在对面为空时自然为假，**循环里不用判空**。

**`MAX_QTY = 2^40`、`capacity ≤ 2^22`**：价位总量最坏 2^62 < 2^63，永不溢出 `long`，热路径不需 `addExact`——"用输入上限换掉运行时检查"。

---

## 6. Java 21 特性小课

### `record`（含紧凑构造器）

旧写法 `Trade` 类手写字段、构造器、getter、`equals`、`hashCode`、`toString`，40 行。新写法 `record Trade(long takerId, long makerId, Side takerSide, long price, long qty) implements Event {}` 一行，`equals` 按字段比较，可直接比较事件列表。紧凑构造器 `record Order(...) { Order { if (qty <= 0) throw ...; } }` 让"非法订单构造不出来"。**不该用**：需可变状态的（`Node` 的 `qty` 会变，所以是普通类）。

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

`sealed ... permits` 声明"只有这几种"；`switch` 对 sealed 类型**穷尽检查**，不需 `default`；record 模式拆字段，省强转和 getter；`when` 守卫写附加条件。

**坑**：加了 `default` 就丧失穷尽检查，sealed switch 里别写。守卫分支顺序有意义（第一个匹配的生效），不加守卫的"兜底"分支必须写后面，否则编译器报"被支配"（dominated）。

### `switch` 表达式 + `yield`

旧：`switch` 语句每个 case 要 `break`，忘了就 fallthrough。新：`case X -> 值;` 无穿透；多行用块 `{ ...; yield 值; }`。

### `instanceof` 模式、Sequenced Collections

旧：`if (e instanceof Trade) { Trade t = (Trade) e; ... }`；新：`if (e instanceof Trade t) { ... }`，`t` 只在条件为真时可见。取队头旧写 `map.entrySet().iterator().next()`（长且易忘判空），新 `map.firstEntry()`；`LinkedHashMap.putLast` 的"移到队尾"，Java 21 之前要 `remove` 再 `put`。

### 未命名模式 `_`（Java 21 预览，需 `--enable-preview`）

`case Limit _, Market _ -> ...`：不需绑定变量时写 `_`，还允许一个 case 写多个模式。JDK 22 正式。

### `Stream.mapMulti` / `toList()`、`Math.addExact`、其他

旧 `.filter(e -> e instanceof Trade).map(e -> (Trade) e).collect(Collectors.toList())`；新 `mapMulti` 一步，`toList()` 返回不可变列表。**不该用**：简单 filter+map 更好读；`mapMulti` 适合"每元素产出少量结果、不想建中间 Stream"。

`a + b` 溢出静默回绕，`addExact` 溢出抛 `ArithmeticException`。`"…%d".formatted(x)` 代替 `String.format`；文本块 `"""` 让多行脚本样例原样出现；`var` 只在右边类型显然时用。

---

## 7. 追问预演

**Q1. 为什么价位内用 `LinkedHashMap` 而不是 `ArrayDeque`？**
撤的订单可能在队伍中间，`ArrayDeque.remove(Object)` 线性查找，O(队伍长度)。需要"按 id O(1) 摘除且保序"→ 哈希表 + 链表（LinkedHashMap），撤单、改量 O(1)，代价是每项多一个 entry 对象。
说：「我需要先来后到，和按 id O(1) 撤单。ArrayDeque 只有前者，LinkedHashMap 两个都有。」

**Q2. 撤单复杂度？**
O(log L)：`byId.get` O(1)，`TreeMap.get` O(log L)，`fifo.remove` O(1)，价位空了再 `TreeMap.remove` O(log L)。真 O(1) 要把价位换成数组下标（Part 4）。

**Q3. 为什么用 `long` 不用 `double` 表示价格？**
浮点存不准十进制小数（`0.1 + 0.2 != 0.3`），"相等"价格可能分到两个价位，比较还要处理 epsilon。整数 tick 精确、可比较、可当数组下标。数量同理。

**Q4. 同价位怎么保证先来先成交？**
价位内队列按到达顺序入队，撮合只从队头取；部分成交的 maker 留队头（量减少）。modify 增量丢优先级（移队尾），减量不丢。

**Q5. 市价单没有价格，怎么放进结构？**
当成限价无穷大（买）/ 0（卖）走同一个撮合循环，吃完剩余作废。避免写两套循环。

**Q6. 怎么让它更快？（Part 4 开场白）**
先 profile 看 CPU 还是 GC。这里是对象多（装箱 key、Node、entry、Event 列表），把"对象图"变"数组"（表见第 4 节第 9 步）。取舍是有界内存（价格带、容量），超出就拒绝 / 返回 FULL。
说：「热路径零分配，内存启动时一次分配；价格是有界整数，所以树换成数组；代价是价格带和容量固定，边界上拒绝并返回错误码。」

**Q7. 价格范围很大（不是有界的）怎么办？**
数组放不下。折中：只对靠近中间价的一段（±几千 tick）用数组，远处价位放 `TreeMap`（很少访问）；或 sorted array + 二分。

**Q8. 多线程怎么办？**
撮合有严格顺序依赖，锁粒度难细分。常见：**单线程撮合引擎**（一品种一线程），命令经队列（如 LMAX Disruptor 的 ring buffer）串行送入——无锁、可重现、延迟稳定；扩展靠按品种分片。别给每个方法加 `synchronized`，撮合仍要整体串行，锁只增加开销。

**Q9. 怎么测试撮合正确？**
(1) 手算样例；(2) 不变量：簿永不交叉（best bid < best ask）、数量守恒（提交量 = 2 × 成交量 + 剩余挂单 + 被撤量）；(3) 对拍：快版本与慢但明显正确的版本喂同一串随机命令逐步比较。

---

## 8. 常见误区

1. **`add` 就撮合。** Part 1 的 `add` 只挂不撮，两张交叉的单可同时在簿上；撮合是 `execute(Limit)` 的事。
2. **成交价取 taker 的限价。** 买 110 的单吃卖 101 的单，成交价是 101（maker 价）。
3. **部分成交的 maker 被放到队尾。** 应留队头，只是数量减少。
4. **增量 modify 保留了位置。** 加量必须重新排队，否则可先挂小单占队头再偷偷加量。
5. **价位空了不删。** 空 `PriceLevel` 留在 `TreeMap`，`firstEntry()` 会把它当"最优价"。撤单、吃光都要"队空就删价位"。
6. **先改后查溢出。** `total += qty` 溢出回绕成负数，簿悄悄坏掉；先 `addExact` 再改。
7. **`double` 价格 / `int` 数量。** `int` 大单累加溢出；`double` 比较相等不可靠。
8. **`Long` 用 `==` 比较。** 装箱对象比较引用；缓存范围（-128..127）内碰巧相等、之外不等——"小数据里过、线上错"。用 `equals` 或保持基本类型。
9. **（Part 4）开放寻址删除直接置 0。** 断掉探测链，要回移删除。
10. **（Part 4）最优价被吃光后忘了更新。** 位图和 `bestBid` / `bestAsk` 必须在"价位变空"和"新价位出现"两处都维护，并能跨过一万多个空价位找到下一档。

---

## 9. 自测题

**Q1（概念）** 为什么买盘的 `TreeMap` 要用 `Comparator.reverseOrder()`？

<details><summary>答案</summary>买盘最优价是最高价。`firstEntry()` 返回比较器下"最小"的 key；反序比较器让最大价格排最前，两边都用 `firstEntry()` 取最优价，代码对称。</details>

**Q2（手算）** 卖盘：100:[#1 x2, #2 x3]，101:[#3 x4]。来 `LIMIT 9 BUY 101 8`，写出事件和最终簿。

<details><summary>答案</summary>先吃 100 档队头：Trade(9,1,BUY,100,2)，再 Trade(9,2,BUY,100,3)；100 档空；再吃 101 档：Trade(9,3,BUY,101,3)（剩 8-5=3，吃 #3 的 3 个）。#9 吃光不挂簿。最终卖盘：101:[#3 x1]；买盘空。</details>

**Q3（复杂度）** 撤单为什么是 O(log L) 不是 O(1)？怎样变 O(1)？

<details><summary>答案</summary>瓶颈在用价格找价位：`TreeMap.get(price)` 是 O(log L)。价格有界时价位用数组下标存（`head[side][tick]`），找价位 O(1)；配合侵入式链表 O(1) 摘除，撤单整体 O(1)（价位变空时更新最优价另算）。</details>

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

<details><summary>答案</summary>(1) 没检查 `newQty <= 0`；(2) 增量没移到队尾（丢优先级）；(3) `total += …` 可能溢出且没先检查，抛异常前簿已被改。</details>

**Q5（小编程）** 写 `long spread(OrderBook b)`：返回 best ask − best bid，任一侧为空返回 −1。用 `OptionalLong` 的 API。

<details><summary>答案</summary>

```java
static long spread(OrderBook b) {
    var bid = b.bestBid();
    var ask = b.bestAsk();
    return bid.isPresent() && ask.isPresent() ? ask.getAsLong() - bid.getAsLong() : -1;
}
```
注意：Part 1 的 `add` 不撮合，簿可能交叉，此时 spread 为负——调用方需知道。</details>

**Q6（设计）** 为什么 `TickBook.limit` 在池满时返回 `FULL` 且不撮合，而不是先撮合再拒绝剩余部分？

<details><summary>答案</summary>先撮合再发现没地方挂，成交已发生（回调已通知），"拒绝"语义就不干净了。池满时对可能完全成交的单误拒是保守的，但简单、可预测、状态不会半改。这是有界内存系统常见的"背压（back-pressure）"策略。</details>

---

## 延伸阅读

* CLRS《算法导论》「红黑树」一章。
