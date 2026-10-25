import java.util.NoSuchElementException;

/**
 * hc15 Part 4：价格范围有界（0..maxTick-1）时的直方图。counts 放在一棵树状数组（Fenwick tree / BIT）里：
 * add 是 O(log T) 的单点加，第 r 小是 O(log T) 的「倍增下降」，没有任何堆、树结点或装箱。构造时一次分配，之后零分配。
 */
public final class TickHistogram {
    public static final int MAX_TICKS = 1 << 22;

    private final int maxTick;
    private final long[] tree; // 1 起的树状数组：tree[i] = 区间 (i - lowbit(i), i] 的计数
    private final int top;     // ≤ maxTick 的最大 2 的幂
    private long total;

    /** 1 ≤ maxTick ≤ MAX_TICKS，否则 IAE。合法价格是 0..maxTick-1。 */
    public TickHistogram(int maxTick) {
        if (maxTick < 1 || maxTick > MAX_TICKS) throw new IllegalArgumentException("maxTick must be in 1.." + MAX_TICKS + ": " + maxTick);
        this.maxTick = maxTick;
        this.tree = new long[maxTick + 1];
        this.top = Integer.highestOneBit(maxTick);
    }

    /** 价格不在 0..maxTick-1 → IAE。 */
    public void add(long price) {
        if (price < 0 || price >= maxTick) throw new IllegalArgumentException("price out of range: " + price);
        for (int i = (int) price + 1; i <= maxTick; i += i & -i) tree[i]++;
        total++;
    }

    public long count() {
        return total;
    }

    /** 小于等于 price 的个数；price &lt; 0 → 0，price ≥ maxTick → count()。 */
    public long countAtMost(long price) {
        if (price < 0) return 0;
        if (price >= maxTick) return total;
        long c = 0;
        for (int i = (int) price + 1; i > 0; i -= i & -i) c += tree[i];
        return c;
    }

    /** 第 rank 小（1 起）的价格。rank 不在 1..count() → IAE。 */
    public long kth(long rank) {
        if (rank < 1 || rank > total) throw new IllegalArgumentException("rank out of range: " + rank + " (count " + total + ")");
        int pos = 0;
        long r = rank;
        for (int step = top; step > 0; step >>= 1) {
            int next = pos + step;
            if (next <= maxTick && tree[next] < r) {
                pos = next;
                r -= tree[next];
            }
        }
        return pos; // 下标 pos + 1 对应价格 pos
    }

    /** 最近秩百分位，语义同 OrderStatistics.percentile。 */
    public long percentile(int p) {
        long r = OrderStatistics.rank(total, p);
        if (total == 0) throw new NoSuchElementException("no prices yet");
        return kth(r);
    }

    public long median() {
        return percentile(50);
    }
}
