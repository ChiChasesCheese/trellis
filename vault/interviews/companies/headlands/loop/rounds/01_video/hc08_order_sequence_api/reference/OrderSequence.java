import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.stream.IntStream;

/**
 * 插入有序的活跃订单序列。Part 1：语义；Part 2：Fenwick 树（BIT）让前缀 count / quantity 查询 O(log n)；
 * Part 3：部分删除 + 索引空间写满时压缩（compaction）。题面见 ../problem.md。
 *
 * 为什么用 Fenwick 树而不是别的（详见 study/30-articles/hc08_order_sequence_api.md）：
 *  * 查询「序列头到某订单的订单数 / 数量和」就是「前缀和」。朴素做法每次扫一遍 O(n)。
 *  * 前缀和 + 单点修改，线段树和 Fenwick 都是 O(log n)；Fenwick 只要一个数组、循环里只有加法与位运算（i & -i），常数小、代码短。
 *  * 订单一律追加在末尾，所以「插入下标」天然递增，不需要像一般的「按键排序」问题那样先离散化。
 *
 * 结构：每张订单占一个递增的「插入下标」（1..capacity）；删除只把该下标上的数清零（留洞）。
 * 两棵 Fenwick 树按下标累加：cnt（活跃订单数）与 sum（剩余数量）。
 */
public final class OrderSequence {

    /** 一张活跃订单（id，剩余数量）。 */
    public record Entry(long id, long qty) {}

    // ---------- 错误信息 ----------
    public static final String INVALID_QTY = "invalid quantity";
    public static final String DUPLICATE_ID = "duplicate id";
    public static final String UNKNOWN_ID = "unknown id";
    public static final String QTY_EXCEEDS = "quantity exceeds remaining";
    public static final String INDEX_RANGE = "index out of range";
    public static final String OVERFLOW = "overflow";

    // ---------- 文本命令 ----------
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

    // ---------- 状态 ----------
    private final int minCapacity;
    private int capacity;              // 2 的幂
    private int[] cnt;                 // Fenwick：活跃订单数
    private long[] sum;                // Fenwick：剩余数量
    private long[] idByIdx;              // 下标 → id
    private long[] qtyByIdx;             // 下标 → 剩余数量（0 = 洞）
    private int nextIndex = 1;         // 下一个可用下标；下标永不回收，直到 compaction
    private final HashMap<Long, Integer> indexOf = new HashMap<>();
    private long totalQty;
    private int compactions;

    public OrderSequence() { this(16); }

    /** 初始下标空间（向上取整到 2 的幂）；compaction 之后容量不会低于它。 */
    public OrderSequence(int initialCapacity) {
        if (initialCapacity < 1 || initialCapacity > (1 << 29)) throw new IllegalArgumentException("capacity out of range");
        this.minCapacity = pow2AtLeast(initialCapacity);
        allocate(minCapacity);
    }

    private static int pow2AtLeast(int x) { return x <= 1 ? 1 : Integer.highestOneBit(x - 1) << 1; }

    private void allocate(int cap) {
        capacity = cap;
        cnt = new int[cap + 1];
        sum = new long[cap + 1];
        idByIdx = new long[cap + 1];
        qtyByIdx = new long[cap + 1];
    }

    // ---------- API ----------

    /** 放到序列末尾。qty ≤ 0 / id 已活跃 → IAE；总量溢出 → ArithmeticException（状态不变）。 */
    // 为什么先检查再改：所有可能抛异常的检查（qty、重复、溢出）都排在任何修改之前，失败时对象完全不变。
    public void put(long id, long qty) {
        if (qty <= 0) throw new IllegalArgumentException(INVALID_QTY);
        if (indexOf.containsKey(id)) throw new IllegalArgumentException(DUPLICATE_ID);
        long newTotal;
        try {
            newTotal = Math.addExact(totalQty, qty);
        } catch (ArithmeticException e) {
            throw new ArithmeticException(OVERFLOW);
        }
        if (nextIndex > capacity) compact();
        int i = nextIndex++;
        idByIdx[i] = id;
        qtyByIdx[i] = qty;
        addCnt(i, 1);
        addSum(i, qty);
        indexOf.put(id, i);
        totalQty = newTotal;
    }

    /**
     * 删除订单的 qty 个单位；返回剩余数量（0 = 订单已移除）。位置不变。
     * qty ≤ 0 → IAE；未知 id → NoSuchElementException；qty > 剩余 → IAE（状态不变）。
     */
    public long delete(long id, long qty) {
        if (qty <= 0) throw new IllegalArgumentException(INVALID_QTY);
        int i = indexOrThrow(id);
        long have = qtyByIdx[i];
        if (qty > have) throw new IllegalArgumentException(QTY_EXCEEDS);
        long left = have - qty;
        qtyByIdx[i] = left;
        addSum(i, -qty);
        totalQty -= qty;
        if (left == 0) {
            addCnt(i, -1);
            indexOf.remove(id);
        }
        return left;
    }

    /** 从序列头到该订单（含）的活跃订单数。未知 id → NoSuchElementException。 */
    public long countUpTo(long id) { return prefixCnt(indexOrThrow(id)); }

    /** 从序列头到该订单（含）的剩余数量之和。 */
    public long qtyUpTo(long id) { return prefixSum(indexOrThrow(id)); }

    /** 第 k 张活跃订单（1 起）的 id。越界 → IndexOutOfBoundsException。Fenwick 上的二分下降，O(log n)。 */
    // 为什么能二分下降：cnt 树里 tree[pos + 2^j] 恰好是区间 (pos, pos + 2^j] 的订单数。
    // 从大步长往小步长试：如果整块的订单数还 < k，说明第 k 个在这块后面，整块跳过（rem 减去它）；否则留在块里、缩小步长。
    // 因为 capacity 是 2 的幂，pos 的二进制每次只往低位多补一个 1，整个过程等于在二进制上逐位确定答案下标。
    public long idAt(int k) {
        if (k < 1 || k > indexOf.size()) throw new IndexOutOfBoundsException(INDEX_RANGE);
        int pos = 0;
        int rem = k;
        for (int pw = capacity; pw > 0; pw >>= 1) {
            int nxt = pos + pw;
            if (nxt <= capacity && cnt[nxt] < rem) {
                pos = nxt;
                rem -= cnt[nxt];
            }
        }
        return idByIdx[pos + 1];
    }

    public int size() { return indexOf.size(); }
    public long totalQty() { return totalQty; }
    /** 当前下标空间大小（2 的幂）。 */
    public int capacity() { return capacity; }
    /** 已发生的 compaction 次数。 */
    public int compactions() { return compactions; }

    /** 全部活跃订单，按插入顺序。O(capacity)。 */
    public List<Entry> entries() {
        return IntStream.range(1, nextIndex).filter(i -> qtyByIdx[i] > 0)
                .mapToObj(i -> new Entry(idByIdx[i], qtyByIdx[i])).toList();
    }

    // ---------- 内部 ----------

    private int indexOrThrow(long id) {
        Integer i = indexOf.get(id);
        if (i == null) throw new NoSuchElementException(UNKNOWN_ID);
        return i;
    }

    // i & -i 取出 i 二进制里最低的那个 1（lowbit）。Fenwick 里 tree[i] 管的是下标区间 (i - lowbit(i), i]：
    //   更新 i：把变化加到所有「管着 i 的节点」上，i += lowbit(i) 就是跳到下一个管着它的节点；
    //   查询 i：把 [1, i] 拆成若干个不相交的块，i -= lowbit(i) 就是去掉最低位、跳到前一块。
    // 每次循环至少消掉（或进位掉）一个 1，所以最多 log2(capacity) 步。
    private void addCnt(int i, int delta) {
        for (; i <= capacity; i += i & -i) cnt[i] += delta;
    }

    private void addSum(int i, long delta) {
        for (; i <= capacity; i += i & -i) sum[i] += delta;
    }

    private long prefixCnt(int i) {
        long r = 0;
        for (; i > 0; i -= i & -i) r += cnt[i];
        return r;
    }

    private long prefixSum(int i) {
        long r = 0;
        for (; i > 0; i -= i & -i) r += sum[i];
        return r;
    }

    /**
     * 下标空间写满：把活跃订单按原顺序重新编号 1..m，O(capacity) 线性建树。
     * 新容量 = 2 的幂 ≥ max(初始容量, 1.5m + 1)：压缩后至少腾出约 m/2 个空位，所以摊还到每次 put 是 O(1)；
     * 活跃订单少时容量还会缩回去（内存跟着活跃量走，而不是跟着历史总量走）。
     */
    // 为什么需要它：删除只"留洞"、下标不回收（回收会破坏插入顺序），所以下标只增不减；不压缩的话，
    // 哪怕任何时刻只有 1000 张活跃订单，处理 200 万张订单也要 200 万的数组。压缩 = 按原顺序把活跃订单重新编号。
    private void compact() {
        int m = indexOf.size();
        int newCap = pow2AtLeast(Math.max(minCapacity, m + (m >> 1) + 1));
        long[] oldId = idByIdx, oldQty = qtyByIdx;
        int oldNext = nextIndex;
        allocate(newCap);
        int j = 0;
        for (int i = 1; i < oldNext; i++) {
            if (oldQty[i] == 0) continue;
            j++;
            idByIdx[j] = oldId[i];
            qtyByIdx[j] = oldQty[i];
            cnt[j] = 1;
            sum[j] = oldQty[i];
            indexOf.put(oldId[i], j);
        }
        for (int i = 1; i <= newCap; i++) { // 线性建 Fenwick：每个节点把自己加到父节点
            int p = i + (i & -i);
            if (p <= newCap) {
                cnt[p] += cnt[i];
                sum[p] += sum[i];
            }
        }
        nextIndex = j + 1;
        compactions++;
    }

    // ---------- 文本接口 ----------

    /** PUT id qty · DELETE id qty · COUNT id · QTY id · AT k（大小写不敏感）。格式错抛 IAE。 */
    public static Op parse(String line) {
        var t = Objects.requireNonNull(line, "line").strip().split("\\s+");
        if (t[0].isEmpty()) throw new IllegalArgumentException("empty command");
        try {
            return switch (t[0].toUpperCase(Locale.ROOT)) {
                case "PUT" -> {
                    args(t, 3);
                    yield new Put(Long.parseLong(t[1]), Long.parseLong(t[2]));
                }
                case "DELETE" -> {
                    args(t, 3);
                    yield new Delete(Long.parseLong(t[1]), Long.parseLong(t[2]));
                }
                case "COUNT" -> {
                    args(t, 2);
                    yield new CountUpTo(Long.parseLong(t[1]));
                }
                case "QTY" -> {
                    args(t, 2);
                    yield new QtyUpTo(Long.parseLong(t[1]));
                }
                case "AT" -> {
                    args(t, 2);
                    yield new IdAt(Integer.parseInt(t[1]));
                }
                default -> throw new IllegalArgumentException("unknown command: " + t[0]);
            };
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("bad number in: " + line.strip());
        }
    }

    private static void args(String[] t, int n) {
        if (t.length != n) throw new IllegalArgumentException(t[0] + " expects " + (n - 1) + " arguments");
    }

    /** 执行一条命令；业务错误变成 Err，不抛。 */
    public Result apply(Op op) {
        try {
            return switch (Objects.requireNonNull(op, "op")) {
                case Put(var id, var q) -> {
                    put(id, q);
                    yield new Ok();
                }
                case Delete(var id, var q) -> new Num(delete(id, q));
                case CountUpTo(var id) -> new Num(countUpTo(id));
                case QtyUpTo(var id) -> new Num(qtyUpTo(id));
                case IdAt(var k) -> new Num(idAt(k));
            };
        } catch (IllegalArgumentException | NoSuchElementException | IndexOutOfBoundsException | ArithmeticException e) {
            return new Err(e.getMessage());
        }
    }

    public static String render(Result r) {
        return switch (r) {
            case Ok _ -> "OK";
            case Num(var v) -> Long.toString(v);
            case Err(var m) -> "ERR " + m;
        };
    }

    /** 逐行执行脚本（空行与 # 行跳过）。格式错抛 IAE，信息以 "line N" 开头。 */
    public static List<String> replay(List<String> lines) {
        var seq = new OrderSequence();
        var out = new ArrayList<String>();
        for (int i = 0; i < lines.size(); i++) {
            var line = lines.get(i).strip();
            if (line.isEmpty() || line.startsWith("#")) continue;
            Op op;
            try {
                op = parse(line);
            } catch (IllegalArgumentException e) {
                throw new IllegalArgumentException("line " + (i + 1) + ": " + e.getMessage());
            }
            out.add(render(seq.apply(op)));
        }
        return out;
    }
}
