# J18 · `Comparator` 组合子、接口的 `default`/`static`/`private` 方法、`Objects` 卫语句

> 版本：`Comparator.comparing`/`thenComparing`/`reversed`/`nullsFirst` 与接口 `default`/`static` 方法 8 · 接口 `private` 方法、`Objects.requireNonNullElse`/`checkIndex` 9 · `Objects.requireNonNull(T, Supplier)` 8。**全部正式特性。**
> 可运行代码：`examples/J18/`。前置：`class`/`interface`/lambda；`Comparable` 和 `compareTo` 的大概意思（1.1 讲）。

---

## 1. 先看痛点

### 1.1 从零讲：排序需要一个「比较规则」

给一堆东西排序，计算机要知道「哪个排前面」。Java 用一个方法表达这条规则：

```java
int compare(Order a, Order b)    // 返回负数：a 排在 b 前；0：相等；正数：a 排在 b 后
```

装这个方法的接口是 `Comparator<T>`（"外部比较器"）；类自己也可以实现 `Comparable<T>` 的 `compareTo`（"自然顺序"）。排序算法（`List.sort`、`TreeMap` 内部）反复调用它，所以必须满足**契约**（contract）：

1. **反对称**：`compare(a, b)` 与 `compare(b, a)` 符号相反；
2. **传递**：`a<b` 且 `b<c` 则 `a<c`；
3. **一致**：同样的输入永远得到同样的结果。

违反契约，轻则排序结果乱，重则 `TimSort` 抛 `IllegalArgumentException: Comparison method violates its general contract!`。

### 1.2 Java 7 的写法与痛点（`examples/J18/J18Old.java`）

```java
Collections.sort(orders, new Comparator<Order>() {
    @Override public int compare(Order a, Order b) {
        int c = Long.compare(b.px, a.px);       // 降序：把 a、b 对调
        if (c != 0) return c;
        c = Long.compare(a.ts, b.ts);
        if (c != 0) return c;
        return Long.compare(a.id, b.id);
    }
});
```

输出：

```
[Order#3(101@1), Order#2(101@3), Order#1(100@5), Order#4(99@2)]
a - b = -2147483648  (溢出成负数，说明 a<b？)  Integer.compare(a, b) = 1
```

痛点：

1. **啰嗦**：6 行匿名类只为说"价格降序、时间升序、id 升序"。
2. **容易写错**：降序靠"把 a、b 对调"心算；每层 tie-break 都要 `if (c != 0) return c;`，漏一层就悄悄变成"不稳定"排序。
3. **经典 bug：用减法比较** `return a - b;`——`Integer.MAX_VALUE - (-1)` 溢出成负数，于是 "MAX < -1"（上面第二行），违反传递性。永远用 `Integer.compare` / `Long.compare`。

### 1.3 接口的另一个痛点：「加方法会破坏所有实现者」

Java 7 接口里所有方法都是抽象的。给 `Iterable` 加个 `forEach`？世界上所有实现 `Iterable` 的类都会**编译失败**。所以 `Collection` 接口几乎不能演进，JDK 只能把工具方法放进另一个**工具类**（`Collections.sort(list)` 而不是 `list.sort()`），静态方法与对象分离、不能被覆盖、也不多态。

Java 8 的解决：**接口可以有带实现的方法**——`default` 方法（给已有实现一个默认实现）和 `static` 方法；`Iterable.forEach`、`List.sort`、`Comparator.reversed()` 都是这样加进去的。Java 9 再加 `private` 方法（接口内部复用代码）。

---

## 2. 语法逐条讲

### 2.1 `Comparator` 的静态和默认方法（Java 8）

| 方法 | 作用 |
|---|---|
| `Comparator.comparing(keyExtractor)` | 按"从元素里抽出的键"比较，键需要 `Comparable` |
| `Comparator.comparing(keyExtractor, keyComparator)` | 同上，但键用你给的比较器（比如 `String.CASE_INSENSITIVE_ORDER`、`nullsFirst(...)`） |
| `comparingInt` / `comparingLong` / `comparingDouble` | 键是基本类型，**避免装箱** |
| `naturalOrder()` / `reverseOrder()` | 自然顺序 / 反过来 |
| `c.reversed()` | 把比较器 `c` 反过来 |
| `c.thenComparing(...)` / `thenComparingInt/Long/Double` | `c` 比不出来（返回 0）时，再用第二个键 |
| `Comparator.nullsFirst(c)` / `nullsLast(c)` | 包一层：`null` 排前/排后，非 null 用 `c` |

**从左到右**读，每个调用返回新的 `Comparator`，所以能链式：

```java
Comparator.comparingLong(Order::px).reversed().thenComparingLong(Order::ts).thenComparingLong(Order::id)
//          1. 按价格比        2. 反过来(降序)    3. 价格相同按 ts    4. 还相同按 id
```

### 2.2 `reversed()` 作用于"它前面整条链"

最常见的坑：

```java
Comparator.comparing(Person::city).thenComparing(Person::name).reversed()   // city、name 都反了
Comparator.comparing(Person::city).reversed().thenComparing(Person::name)   // 只有 city 降序，name 仍升序
```

例 1 的结果：

```
city 降序、name 升序（正确）: [alice, Bob, Carol, Eve, dave]
reversed 放最后（两个键都反了）: [alice, Eve, Carol, Bob, dave]
```

### 2.3 `null` 的处理

`Comparator.comparing(Person::age)` 遇到 `age == null` 会 NPE。容忍 null：`Comparator.comparing(Person::age, Comparator.nullsFirst(Comparator.naturalOrder()))`。

### 2.4 接口里的五类成员（Java 9 起）

```java
interface Validator<T> {
    boolean test(T t);                                    // 抽象：实现者必须提供。只有一个 -> 函数式接口，可用 lambda
    default Validator<T> negate() { return t -> !test(t); }       // default：有实现，可被覆盖，通过实例调用
    static <T> Validator<T> not(Validator<T> v) { return v.negate(); }   // static：接口自己的方法，通过 Validator.not(...) 调用，不会被继承
    private static <T> boolean check(List<Validator<T>> vs, T t) {...}   // private static：给接口内部的 default/static 复用（Java 9）
    private boolean helper() {...}                                       // private 实例方法：给 default 方法复用（Java 9）
}
```

### 2.5 default 方法的冲突规则（背熟，面试高频）

类实现多个接口、又继承父类，同名方法怎么选？按顺序：

1. **类优先**：父类（或本类）里的方法永远胜过接口的 `default`（`Derived extends Base implements Maker`，`describe()` 是 `base`）。
2. **更具体的接口优先**：`B extends A` 且都有 `m()` 的 default，则 `B` 的赢。
3. **否则必须自己覆盖**，否则编译错误；可用 `X.super.m()` 指名调用某接口的版本（`Maker.super.describe() + "+" + Taker.super.describe()` 得 `maker+taker`）。

另外：`default` 方法**不能**覆盖 `Object` 的方法（`equals`、`hashCode`、`toString`）；接口没有实例状态，`default` 只能通过抽象方法和别的 default 方法工作。

### 2.6 `Objects` 卫语句

| 方法 | 用途 | 版本 |
|---|---|---|
| `Objects.requireNonNull(x, "message")` | 为 null 就抛 `NullPointerException(message)` | 7 |
| `Objects.requireNonNull(x, Supplier<String>)` | 消息很贵时延迟构造，只有真的为 null 才调用 | 8 |
| `Objects.requireNonNullElse(x, 默认值)` / `requireNonNullElseGet(x, supplier)` | null 就用默认 | 9 |
| `Objects.checkIndex(i, length)` | `i` 不在 `[0, length)` 抛 `IndexOutOfBoundsException`，消息自带数值 | 9 |
| `Objects.checkFromToIndex`、`checkFromIndexSize` | 区间检查 | 9 |
| `Objects.equals(a, b)`、`hash(...)`、`toString(o, 默认)`、`isNull`/`nonNull` | null 安全的小工具 | 7 |

**为什么在构造器/公共方法开头就检查**（fail fast）：错误越早抛离原因越近；`null` 被放进对象，几十步后才在别处 NPE，要倒着追半天。

---

## 3. 编译器和 JVM 到底做了什么

* **lambda 与方法引用**：`Person::name` 编译成 `invokedynamic` 调用点，运行时由 `LambdaMetafactory` 生成实现 `Function` 的小类，不是匿名内部类（不产生 `Foo$1.class`）。`Comparator.comparing(Person::name)` 是**一个函数对象包着另一个函数对象**。
* **组合子是一串嵌套的函数对象**：`thenComparing`、`reversed` 每次返回新 `Comparator`，比较一次走过整条链。调用点单态（只见一种比较器）时 JIT 能把整条链内联成直线代码；多态时（同一个排序函数传入各种比较器）会慢些。
* **`comparingLong` vs `comparing`**：`comparing(Order::px)` 的键是 `Long` 装箱对象，每次比较两次装箱（小值有缓存，大值分配）；`comparingLong` 直接比 `long`，**热路径用基本类型版本**。
* **default 方法的实现**：不是把代码复制到每个实现类。JVM 方法解析时按 2.5 的规则查找：先类层级，再接口；`invokeinterface` 调到实现类后，类里找不到就用接口的 default。
* **排序算法**：对象数组/`List.sort` 用 **TimSort**，**稳定**（相等元素保持原相对顺序，例 1 第 7 行）；`Arrays.sort(int[])` 用 Dual-Pivot Quicksort，不稳定但对基本类型无所谓。TimSort 检测到违反契约会抛异常（不保证每次都检测到）。
* **类型推断盲区**：`Comparator.comparing(p -> p.name()).reversed()`——lambda 参数 `p` 被推断成 `Object`，编译失败：

```
error: cannot find symbol
  symbol:   method name()
  location: variable p of type Object
```

  因为 `.reversed()` 接在后面，编译器无法用目标类型 `Comparator<P>` 反推 `comparing` 的 `T`。解决：方法引用 `Comparator.comparing(P::name).reversed()`，或显式类型 `Comparator.<P, String>comparing(p -> p.name())`，或 `(P p) -> p.name()`。

---

## 4. 三个例子（由浅入深）

### 例 1：最简单——组合子与 `reversed()` 陷阱（`J18Ex1.java`）

输出：

```
按 name(忽略大小写): [alice, Bob, Carol, dave, Eve]
年龄降序再 name（nullsLast 被 reversed 翻成 null 在最前）: [dave, Bob, Carol, alice, Eve]
city 降序、name 升序（正确）: [alice, Bob, Carol, Eve, dave]
reversed 放最后（两个键都反了）: [alice, Eve, Carol, Bob, dave]
age 升序，null 在最前: [dave, alice, Eve, Bob, Carol]
comparing(Person::age) 遇到 null -> NPE
按 city 排序（稳定，同城保持原顺序）: [dave, Bob, Carol, Eve, alice]
(a - b) = -2147483648, Integer.compare = 1
```

细看第 2 行：`nullsLast(...)` 再整体 `.reversed()`，null 排最后被反成最前（`dave` 年龄 null 排第一）——**`reversed()` 反转完整的比较结果，包括 null 的位置**。想"降序且 null 仍在最后"，把 `nullsLast` 套在 `reverseOrder()` 外面：`nullsLast(Comparator.reverseOrder())`。第 7 行：按 `city` 排，`Bob`、`Carol`、`Eve` 同为 `NY`，保持原相对顺序，这就是稳定性。

### 例 2：进阶——接口 default/static/private 与冲突规则（`J18Ex2.java`）

```java
interface Validator<T> {
    boolean test(T t);
    default Validator<T> and(Validator<? super T> other) { return t -> test(t) && other.test(t); }
    default Validator<T> negate() { return t -> !test(t); }
    static <T> Validator<T> not(Validator<T> v) { return v.negate(); }
    static <T> Validator<T> all(List<Validator<T>> vs) { return t -> check(vs, t); }
    private static <T> boolean check(List<Validator<T>> vs, T t) {...}
}
var ok = positiveQty.and(priceInBand).and(aapl);
```

输出：

```
合法单: true
价格越界: false
not(positiveQty): true
all(...): true
Both.describe = maker+taker
Derived.describe = base  (类 Base 胜过接口 Maker)
```

只有一个抽象方法的接口 + 若干 default 方法 = **可组合的函数式接口**（`java.util.function.Predicate` 就是这样设计的）。

### 例 3：贴近真实——订单簿价格-时间优先 + `Objects` 卫语句（`J18Ex3.java`）

```java
static final Comparator<Order> BUY_PRIORITY = Comparator
        .comparingLong(Order::px).reversed()      // 价高者优先
        .thenComparingLong(Order::ts)             // 同价，先到者优先
        .thenComparingLong(Order::id);            // 再相同按 id，保证全序
```

输出：

```
requireNonNull(side) -> NPE: side
Supplier 版本 -> NPE: true
requireNonNullElse = default
requireNonNullElseGet = computed
Objects.toString(null, "-") = -
Objects.equals(null, null) = true, hash(1,2,3) = 30817
checkIndex -> Index 5 out of bounds for length 2
买盘优先级: [#3(101@t1), #5(101@t1), #2(101@t3), #1(100@t5), #4(99@t2)]
缺 tie-break 的 TreeSet 里剩 3 个订单；完整 tie-break 的剩 5 个
```

最后一行是重点：订单 `#2, #3, #5` 价格都是 101。只按价格排序的 `TreeSet` 认为它们"相等"（`compare == 0`），**重复的被静默丢弃**——5 个订单只剩 3 个。`TreeSet`/`TreeMap` 判断"同一个元素"完全靠比较器，不是 `equals`。所以订单簿比较器必须是**全序**，最后一层用唯一的 `id` 兜底（排序一定写全 tie-break）。`#3` 和 `#5`（价格 101、时间 t1 相同）按 `id` 排：3 在 5 前。

---

## 5. 坑与限制

1. **`reversed()` 的位置**：2.2。
2. **减法比较**：`a - b` 溢出。永远用 `Integer.compare`、`Long.compare`、`Double.compare`；`Double.compare` 还正确处理 `NaN` 与 `-0.0`，`<` / `>` 不处理。
3. **比较器与 `equals` 不一致**：`TreeSet`/`TreeMap`/`PriorityQueue` 用比较器判等，不用 `equals`（例 3 丢订单），会让集合违反 `Set` 的约定。
4. **比较器要处理 null 或保证不传 null**：`comparing(X::key)` 遇 null key 就 NPE。
5. **装箱**：`Comparator.comparing(Order::px)` 对 `long` 字段装箱；热路径用 `comparingLong`。
6. **键是可变字段**：对象放进 `TreeSet` 后修改参与比较的字段，内部顺序就坏了，`contains`/`remove` 不可预测。用不可变键（`record`）。
7. **类型推断**：`comparing(p -> p.x()).reversed()` 编译失败（第 3 节）；用方法引用。
8. **default 方法的菱形冲突**：编译错误，必须覆盖并 `X.super.m()` 指名。
9. **接口 default 不是多继承状态**：接口不能有实例字段，default 只能调抽象方法与其他 default 方法。
10. **接口的 `private` 方法**只能被接口内部方法调用，实现类看不到，也不能覆盖。
11. **不要滥用 `default`**：只用于"向已发布接口添加方法而不破坏实现者"（接口演进）和"可组合的小帮助方法"；能改全部实现者的内部接口，用抽象方法更清楚。
12. **`requireNonNull` 抛 NPE 是约定，不是 bug**：《Effective Java》建议对"传了 null 参数"抛 `NullPointerException`（而非 `IllegalArgumentException`）。
12. **`requireNonNull` 抛 NPE 是约定，不是 bug**：《Effective Java》建议对"传了 null 参数"抛 `NullPointerException`（而不是 `IllegalArgumentException`）。

---

## 6. 真实代码里的比较器与卫语句

* `JobChains`：`out.sort(Comparator.comparingLong(Chain::totalSeconds).reversed().thenComparingInt(Chain::startJob));` —— 总时长降序、同时长按起点升序（`reversed()` 位置正确）；基本类型版避免装箱。
* `MergeK`：`Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream)` —— k 路合并堆比较器，**值相同按流编号 tie-break**，保证稳定确定；显式类型 `<Head<T>, T>` 正是第 3 节"类型推断盲区"的解法。
* `OrderBook`：`new java.util.TreeMap<>(Comparator.reverseOrder())` —— 买盘价位表价格降序，`firstEntry()` 就是最优买价。
* `OrderBook`：`Objects.requireNonNull(side, "side");` 出现在 `Order`、`Limit`、`Market` 的紧凑构造器里；`Objects.requireNonNull(cmd, "cmd")` 在公共入口 —— fail fast，null 不能进入对象。
* `TickerMap`：每个公共方法第一行 `Objects.requireNonNull(key, "key");`。
* `MergeK`：`Objects.requireNonNull(h.source.next(), "null element in stream " + h.stream);` —— 消息带流编号，出错能定位。
* `StockTrading`：`Objects.requireNonNull(prices, "prices");` 等。

参考实现没有自己定义带 `default`/`private` 方法的接口；最接近的是 `sealed interface` 层级，成员都是 record。default 方法作为概念课放在这里，因为面试会问冲突规则。

---

## 7. 自测题

1. 写出 `Comparator<Order>`：先按价格降序，价格相同按时间升序，时间也相同按 id 升序（用 `long` 字段）。
2. `Comparator.comparing(A::x).thenComparing(A::y).reversed()` 与 `Comparator.comparing(A::x).reversed().thenComparing(A::y)` 的区别？
3. 为什么 `return a - b;` 是错的？给一个反例。
4. `TreeSet<Order>` 用只比较价格的比较器，放入价格相同的两个不同订单，结果如何？为什么？
5. 类 `C extends B implements I`，`B` 和 `I` 都有 `m()`（`I` 的是 default），`new C().m()` 调谁？若 `C implements I, J` 且两者都有 default `m()` 呢？

<details><summary>答案</summary>

1. `Comparator.comparingLong(Order::px).reversed().thenComparingLong(Order::ts).thenComparingLong(Order::id)`
2. 前者：x 降序、y 也降序（`reversed()` 反转了整条链）；后者：x 降序、y 升序。
3. 减法可能溢出：`Integer.MAX_VALUE - (-1)` 得 `-2147483648`，使 "MAX < -1"，违反传递性/反对称。应使用 `Integer.compare(a, b)`。
4. 只保留第一个：`TreeSet` 用比较器判等，`compare == 0` 即视为同一元素，后加入的被丢弃（不报错）。应加 tie-break（时间、id）保证全序。
5. 调 `B.m()`（类优先于接口 default）。第二种编译错误，`C` 必须覆盖 `m()`，可写 `I.super.m()` 或 `J.super.m()` 指名调用其一。

</details>

---

「延伸」J19 运行时：ZGC 与 JIT。
