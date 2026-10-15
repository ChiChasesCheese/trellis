import java.util.Objects;
import java.util.OptionalLong;
import java.util.function.ObjLongConsumer;

/**
 * Part 1：从零手写的哈希表，key = String（股票代码），value = long（比如累计成交量）。
 *
 * 方案：开放寻址 (open addressing) + 线性探测 (linear probing)。
 * 所有条目直接放在两个并行数组里（keys[i] 和 vals[i] 是同一条记录），没有「桶里的链表节点」这种额外对象。
 * 一个 key 先算出「家」(home slot)；家被别人占了就看下一格，再下一格……直到找到它自己或碰到空格。
 *
 * 格子有三种状态：
 *   空 (keys[i] == null)       从来没放过东西 —— 探测遇到它就可以确定「key 不在表里」
 *   墓碑 (keys[i] == TOMB)     放过东西、被删掉了 —— 探测遇到它必须继续往后找，因为后面可能还有同一条探测链上的 key
 *   占用 (其他)                正常条目
 * 为什么删除不能直接把格子置空？见 remove() 的注释，以及讲义 2.5 节。
 */
public final class TickerMap {
    /** 墓碑哨兵。用 new String 保证它和任何用户传入的字符串「不是同一个对象」，比较时用 == 而不是 equals。 */
    private static final String TOMB = new String("<deleted>");
    private static final int MIN_CAPACITY = 8;

    private String[] keys;
    private long[] vals;
    private int size;       // 占用格子数
    private int tombs;      // 墓碑格子数
    private int mask;       // capacity - 1；capacity 是 2 的幂，所以 (i & mask) == (i % capacity)，但没有除法
    private int shift;      // 32 - log2(capacity)

    public TickerMap() { this(0); }

    /** expectedSize：预计放多少条，预留够用的容量，避免途中 resize。 */
    public TickerMap(int expectedSize) {
        if (expectedSize < 0) throw new IllegalArgumentException("expectedSize < 0");
        allocate(capacityFor((long) expectedSize, 2));
    }

    // ------------------------------------------------------------------ 容量与哈希

    /**
     * 容纳 entries 条记录、且装载因子 <= 1/loadInverse 的最小 2 的幂。
     * 构造时按 1/2 预留（刚好不触发 resize）；resize 时按 1/4 重建，于是纯插入场景下每次正好翻倍。
     */
    private static int capacityFor(long entries, int loadInverse) {
        long want = Math.max(MIN_CAPACITY, entries * loadInverse);
        if (want > (1 << 30)) throw new IllegalStateException("map too large");
        return Integer.highestOneBit((int) want - 1) << 1;
    }

    private void allocate(int capacity) {
        keys = new String[capacity];
        vals = new long[capacity];
        mask = capacity - 1;
        shift = 32 - Integer.numberOfTrailingZeros(capacity);
        size = 0;
        tombs = 0;
    }

    /**
     * 斐波那契哈希 (Fibonacci hashing)：把 String.hashCode() 乘以 2^32/黄金比例 再取「高位」。
     * 为什么不直接 hashCode() & mask？String.hashCode 的低位只和最后几个字符有关，
     * 相近的代码（AAPL / AAPM / AAPN）会落在相邻格子里连成一大片 —— 这叫聚集 (clustering)。
     * 乘一个奇数常数再取高位，会让「每一位输入」都影响「高位输出」。
     */
    private int home(String key) {
        return (key.hashCode() * 0x9E3779B9) >>> shift;
    }

    // ------------------------------------------------------------------ 查询

    /** 返回 key 所在的格子，没有返回 -1。装载因子 <= 1/2 保证表里一定有空格，所以循环必然结束。 */
    private int find(String key) {
        int i = home(key);
        while (true) {
            String k = keys[i];
            if (k == null) return -1;                    // 碰到空格：key 不在表里
            if (k != TOMB && k.equals(key)) return i;    // 墓碑要跳过，继续往后
            i = (i + 1) & mask;
        }
    }

    public int size() { return size; }
    public int capacity() { return keys.length; }
    public int tombstones() { return tombs; }

    public boolean containsKey(String key) {
        Objects.requireNonNull(key, "key");
        return find(key) >= 0;
    }

    public OptionalLong get(String key) {
        Objects.requireNonNull(key, "key");
        int i = find(key);
        return i < 0 ? OptionalLong.empty() : OptionalLong.of(vals[i]);
    }

    // ------------------------------------------------------------------ 修改

    /** 放入 key -> value；返回旧值（没有则 empty）。 */
    public OptionalLong put(String key, long value) {
        Objects.requireNonNull(key, "key");
        return upsert(key, value, false);
    }

    /** vals[key] += delta（不存在当作 0）；返回新值。溢出抛 ArithmeticException 且表保持原样。 */
    public long add(String key, long delta) {
        Objects.requireNonNull(key, "key");
        upsert(key, delta, true);
        return vals[find(key)];
    }

    private OptionalLong upsert(String key, long value, boolean accumulate) {
        int i = home(key);
        int firstTomb = -1;
        while (true) {
            String k = keys[i];
            if (k == null) break;
            if (k == TOMB) {
                if (firstTomb < 0) firstTomb = i;   // 记下第一个墓碑：新 key 可以复用它，探测链不会变长
            } else if (k.equals(key)) {
                long old = vals[i];
                vals[i] = accumulate ? Math.addExact(old, value) : value; // addExact 先算完才写，溢出时不会改坏
                return OptionalLong.of(old);
            }
            i = (i + 1) & mask;
        }
        // key 不在表里 —— 插入
        if (firstTomb >= 0) {                        // 复用墓碑：占用数 +1，墓碑数 -1，「已用格子」不变
            keys[firstTomb] = key;
            vals[firstTomb] = value;
            size++;
            tombs--;
            return OptionalLong.empty();
        }
        if ((size + tombs + 1) * 2 > keys.length) {  // 已用格子（含墓碑）超过一半 -> 重建
            rehash();
            i = home(key);
            while (keys[i] != null) i = (i + 1) & mask; // 新表里没有墓碑也没有这个 key，直接找空格
        }
        keys[i] = key;
        vals[i] = value;
        size++;
        return OptionalLong.empty();
    }

    /**
     * 删除。注意不能把格子置 null：假设 A、B 的家都是第 5 格，A 在 5，B 被挤到 6。
     * 删 A 时若置空，之后查 B 从 5 出发先碰到空格 -> 误判「B 不存在」。所以放一个墓碑，查找时跳过它。
     */
    public OptionalLong remove(String key) {
        Objects.requireNonNull(key, "key");
        int i = find(key);
        if (i < 0) return OptionalLong.empty();
        long old = vals[i];
        keys[i] = TOMB;
        vals[i] = 0;
        size--;
        tombs++;
        return OptionalLong.of(old);
    }

    /**
     * 重建：新容量只按「活的条目数」算，墓碑在这一步全部消失。
     * 所以大量插入 + 删除（比如每天换一批代码）时，表不会被墓碑越撑越大，探测链也不会越来越长。
     */
    private void rehash() {
        String[] oldKeys = keys;
        long[] oldVals = vals;
        allocate(capacityFor(size, 4)); // 触发 rehash 时 size == capacity/2（纯插入），所以新容量正好翻倍
        for (int j = 0; j < oldKeys.length; j++) {
            String k = oldKeys[j];
            if (k == null || k == TOMB) continue;
            int i = home(k);
            while (keys[i] != null) i = (i + 1) & mask;
            keys[i] = k;
            vals[i] = oldVals[j];
            size++;
        }
    }

    public void forEach(ObjLongConsumer<String> action) {
        Objects.requireNonNull(action, "action");
        for (int i = 0; i < keys.length; i++) {
            String k = keys[i];
            if (k != null && k != TOMB) action.accept(k, vals[i]);
        }
    }

    /** 诊断：所有活 key 里「离自己的家最远」的距离（0 = 都在家）。聚集越严重这个数越大。 */
    public int maxProbeLength() {
        int worst = 0;
        for (int i = 0; i < keys.length; i++) {
            String k = keys[i];
            if (k == null || k == TOMB) continue;
            worst = Math.max(worst, (i - home(k)) & mask);
        }
        return worst;
    }
}
