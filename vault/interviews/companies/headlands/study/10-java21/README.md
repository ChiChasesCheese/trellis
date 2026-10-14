# study/10-java21 · Java 21 特性课本

> 写法说明见 `../TEXTBOOK.md`（「Java 21 特性课本」一节）；特性清单与版本见 `../../CONVENTIONS.md` 的特性矩阵。
> 读者设定：会写基本 Java，但要从零讲。每一课的结构相同：**老写法的痛点（Java 8 代码）→ 语法逐条讲 → 编译器 / JVM 做了什么 → 三个由浅入深的例子 → 坑与限制 → 在本 kit 哪里用到 → 5 道自测题（答案折叠）→ 延伸阅读**。

## 怎么读

1. 先按下面的**建议顺序**读 J01–J09（它们互相依赖，顺序是按依赖排的）。
2. 每课的代码都能直接运行。**示例都在 `examples/Jxx/` 下**，一次编译全部：

   ```bash
   cd vault/interviews/companies/headlands/study/10-java21
   JAVAC=/opt/homebrew/opt/openjdk@21/bin/javac
   mkdir -p /tmp/j21out
   $JAVAC --release 21 --enable-preview -d /tmp/j21out examples/J0*/*.java     # J01–J09
   /opt/homebrew/opt/openjdk@21/bin/java --enable-preview -cp /tmp/j21out J03Ex3   # 运行某一个
   ```

   每个 `.java` 文件是一个独立的 `public class`，有自己的 `main`；类名带课号前缀（`J03Ex2`），所以全部放进同一个输出目录也不会重名。
   `Old` 结尾的文件（`J01Old`…）是**老写法**的对照，也能运行。
3. 想看真实用法：每课第 6 节「在本 kit 哪里用到」给出 `loop/rounds/*/*/reference/*.java` 里的文件和代码片段。

## J01–J09（已写）

| 顺序 | 课 | 一句话 | 版本 | 前置 |
|---|---|---|---|---|
| 1 | [J08 · var](J08_var.md) | 局部变量类型推断：它不是动态类型，字节码里没有任何痕迹；什么时候该用、什么时候不该 | 10 | 无 |
| 2 | [J05 · switch 表达式与 yield](J05_switch_expressions.md) | `switch` 变成能产出值的表达式：没有 fall-through、多标签、穷尽检查 | 14 | 无 |
| 3 | [J07 · 文本块](J07_text_blocks.md) | `"""` 多行字符串：缩进去除规则、`\s`、续行，测试样例的标准写法 | 15 | 无 |
| 4 | [J06 · instanceof 模式](J06_instanceof_pattern.md) | 判断类型 + 转型 + 命名一步完成；绑定变量的作用域规则 | 16 | 无 |
| 5 | [J01 · record](J01_record.md) | 一行声明不可变值对象：紧凑构造器校验、`invokedynamic` 生成的 equals/hashCode | 16 | 无 |
| 6 | [J02 · sealed](J02_sealed.md) | 把「恰好这几种」写进类型：`permits`、三种子类修饰符、`PermittedSubclasses` | 17 | J01 |
| 7 | [J03 · switch 模式匹配](J03_pattern_switch.md) | 按类型分派、`when` 守卫、穷尽性检查、`typeSwitch` 如何工作 | 21 | J02、J05、J06 |
| 8 | [J04 · record 模式](J04_record_patterns.md) | 在 `case` / `instanceof` 里直接拆开（嵌套的）record | 21 | J01、J03 |
| 9 | [J09 · Sequenced Collections](J09_sequenced_collections.md) | `getFirst/getLast/reversed`、`SequencedMap.firstEntry/pollFirstEntry/putLast`；订单簿最优价 | 21 | 无（订单簿例子需会 `TreeMap`） |

读法提示：

* **J08、J05、J07、J06 彼此独立**，每课半小时左右；它们是 Java 10–16 的"小特性"，但本 kit 的所有代码和后面各课都在用，先读它们不吃亏。
* **J01 → J02 → J03 → J04 是主线**：record 提供数据，sealed 圈定种类，pattern switch 按种类分派，record 模式再把数据拆开。这四课合起来叫「数据导向编程」（data-oriented programming），本 kit 的每道参考解几乎都是这个结构（`sealed interface X permits A, B` + `record A(...)` + `switch (x) { case A(var ...) -> ... }`）。
* **J09 独立**，随时读；做订单簿题（hc05）之前读最合适。
* 想先快速看到整体：读 J02 第 4 节例 3 + J03 第 4 节例 3 + J04 第 4 节例 3，三个例子是同一个 `Command / Event` 结构的三个侧面。

## 预览特性提醒

kit 的参考解用到了 Java 21 的**预览**特性：未命名模式 `_`（`case Malformed _ ->`，J13）、结构化并发（J11）。
所以编译和运行都要加 `--enable-preview`（`CONVENTIONS.md` 已规定）。J01–J09 的示例本身**不依赖预览特性**，但用同一组参数编译也没有问题。

## J10–J19（并发与运行时）

下面这些课由另一位作者后续补写，写完后会把标题变成链接。顺序是建议的阅读顺序。

| 课 | 标题（来自特性矩阵） | 版本 |
|---|---|---|
| [J18](J18_comparators_interfaces.md) | `Comparator` 组合子、接口 `default`/`private` 方法、`Objects.requireNonNull*` | 8–9 |
| [J14](J14_stream_api.md) | 新 Stream/Collector API：`Stream.toList()`、`mapMulti`、`Collectors.teeing`、`Stream.iterate(seed, hasNext, next)` | 9–16 |
| [J15](J15_math_string_utils.md) | 数学与字符串小工具：`Math.addExact/multiplyExact`、`Math.clamp`（21）、`StringBuilder.repeat`（21）、`String.formatted`、`HexFormat`、`Integer.compress/expand`（19） | 8–21 |
| [J13](J13_unnamed_variables.md) | 未命名模式和变量 `_`（预览 JEP 443） | 21 预览 |
| [J10](J10_virtual_threads.md) | 虚拟线程（JEP 444）：`Thread.ofVirtual()`、`Executors.newVirtualThreadPerTaskExecutor()` | 21 |
| [J16](J16_concurrency_primitives.md) | 并发原语：`VarHandle`、`LongAdder`、`ConcurrentSkipListMap`、`ReentrantLock`（虚拟线程下不 pin，`synchronized` 在 21 会 pin） | 9–21 |
| [J11](J11_structured_concurrency.md) | 结构化并发 `StructuredTaskScope`（预览 JEP 453） | 21 预览 |
| [J12](J12_scoped_values.md) | `ScopedValue`（预览 JEP 446） | 21 预览 |
| [J17](J17_ffm_api.md) | Foreign Function & Memory API：`Arena`、`MemorySegment`（21 预览，22 正式） | 21 预览 |
| [J19](J19_runtime_zgc_jit.md) | 运行时：Generational ZGC（JEP 439）、JFR、`-XX:+PrintCompilation`/JIT 基础 | 21 |

## 一个需要订正的地方

`CONVENTIONS.md` 特性矩阵 J04 一行写的 `case Order(var id, Side.BUY, var px, var q)` **在 Java 21 里不能编译**（record 模式的子模式只能是模式，不能是常量；实测报 `<identifier> expected`）。
正确写法：`case Order(var id, Side side, var px, var q) when side == Side.BUY`。详见 J04 第 2.7 节。
