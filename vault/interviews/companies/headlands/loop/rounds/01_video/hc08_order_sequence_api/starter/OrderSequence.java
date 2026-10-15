import java.util.List;
import java.util.NoSuchElementException;

/**
 * 插入有序的活跃订单序列。题面见 ../problem.md。把每个 TODO 换成实现。
 * Part 1：先用最朴素的写法把语义做对（ArrayList 线性扫描就行）；
 * Part 2：换成 Fenwick 树（树状数组），让 countUpTo / qtyUpTo / idAt 变成 O(log n)；
 * Part 3：部分删除 + 下标空间写满时压缩（compaction）。
 *
 * 提示：Fenwick 版里每张订单占一个只增不减的「插入下标」，删除只留洞；两棵树 cnt（订单数）与 sum（数量）按下标累加。
 */
public final class OrderSequence {

    /** 一张活跃订单（id，剩余数量）。 */
    public record Entry(long id, long qty) {}

    // ---------- 错误信息（测试按这些字符串比较） ----------
    public static final String INVALID_QTY = "invalid quantity";
    public static final String DUPLICATE_ID = "duplicate id";
    public static final String UNKNOWN_ID = "unknown id";
    public static final String QTY_EXCEEDS = "quantity exceeds remaining";
    public static final String INDEX_RANGE = "index out of range";
    public static final String OVERFLOW = "overflow";

    // ---------- 文本命令（已给出） ----------
    public sealed interface Op permits Put, Delete, CountUpTo, QtyUpTo, IdAt {}
    public record Put(long id, long qty) implements Op {}
    public record Delete(long id, long qty) implements Op {}
    public record CountUpTo(long id) implements Op {}
    public record QtyUpTo(long id) implements Op {}
    public record IdAt(int k) implements Op {}

    public sealed interface Result permits Ok, Num, Err {}
    public record Ok() implements Result {}
    public record Num(long value) implements Result {}
    public record Err(String message) implements Result {}

    public OrderSequence() { this(16); }

    /** 初始下标空间（向上取整到 2 的幂）；compaction 之后容量不会低于它。≤ 0 抛 IAE。 */
    public OrderSequence(int initialCapacity) { throw new UnsupportedOperationException("TODO"); }

    // ---------- Part 1（语义）· Part 2（O(log n)）· Part 3（部分删除 + 压缩） ----------

    /** 放到序列末尾。qty ≤ 0 / id 已活跃 → IAE；活跃总量溢出 long → ArithmeticException（状态不变）。 */
    public void put(long id, long qty) { throw new UnsupportedOperationException("TODO"); }

    /**
     * 删除订单的 qty 个单位；返回剩余数量（0 = 订单已移除）。位置不变。
     * qty ≤ 0 → IAE；未知 id → NoSuchElementException；qty > 剩余 → IAE（状态不变）。
     * Part 1–2 只会整单删除（qty == 剩余）；qty < 剩余的部分删除在 Part 3 才被测试。
     */
    public long delete(long id, long qty) { throw new UnsupportedOperationException("TODO"); }

    /** 从序列头到该订单（含）的活跃订单数。未知 id → NoSuchElementException。 */
    public long countUpTo(long id) { throw new UnsupportedOperationException("TODO"); }

    /** 从序列头到该订单（含）的剩余数量之和。 */
    public long qtyUpTo(long id) { throw new UnsupportedOperationException("TODO"); }

    /** 第 k 张活跃订单（1 起）的 id。越界 → IndexOutOfBoundsException。Part 2：在 Fenwick 树上二分下降，O(log n)。 */
    public long idAt(int k) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }
    public long totalQty() { throw new UnsupportedOperationException("TODO"); }

    /** Part 3：当前下标空间大小（2 的幂）。朴素版本可以返回任意值，Part 3 的测试才检查它。 */
    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    /** Part 3：已发生的 compaction 次数。 */
    public int compactions() { throw new UnsupportedOperationException("TODO"); }

    /** 全部活跃订单，按插入顺序。 */
    public List<Entry> entries() { throw new UnsupportedOperationException("TODO"); }

    // ---------- 文本接口 ----------

    /** PUT id qty · DELETE id qty · COUNT id · QTY id · AT k（大小写不敏感，空白任意）。格式错抛 IAE。 */
    public static Op parse(String line) { throw new UnsupportedOperationException("TODO"); }

    /**
     * 执行一条命令；业务错误（IAE / NoSuchElementException / IndexOutOfBoundsException / ArithmeticException）变成 Err(message)，不抛。
     * 提示：对 sealed Op 写 switch 模式匹配 + record 解构，不要 default。
     */
    public Result apply(Op op) { throw new UnsupportedOperationException("TODO"); }

    /** Ok → "OK"，Num(v) → "v"，Err(m) → "ERR m"。 */
    public static String render(Result r) { throw new UnsupportedOperationException("TODO"); }

    /** 逐行执行脚本（空行与 # 开头的行跳过），格式错抛 IAE，信息以 "line N" 开头（N 从 1 起）。 */
    public static List<String> replay(List<String> lines) { throw new UnsupportedOperationException("TODO"); }
}
