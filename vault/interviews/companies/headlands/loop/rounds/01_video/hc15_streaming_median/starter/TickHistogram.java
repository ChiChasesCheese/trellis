/**
 * hc15 Part 4（starter）：价格范围有界（0..maxTick-1）时的直方图。
 *
 * <p>要求：add / percentile 都是 O(log maxTick)，构造之后零分配（不用堆、树结点、装箱）；1e6 次 add + 1e6 次查询 &lt; 1 s。
 * 提示：计数放进一棵树状数组（Fenwick tree / BIT）：add 是单点加；第 r 小用「倍增下降」——
 * 从最高位的 2 的幂开始，tree[pos + step] &lt; r 就整段跳过并把 r 减掉。
 */
public final class TickHistogram {
    public static final int MAX_TICKS = 1 << 22;

    // 在这里加你的字段

    /** 1 ≤ maxTick ≤ MAX_TICKS，否则 IAE。合法价格是 0..maxTick-1。 */
    public TickHistogram(int maxTick) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 价格不在 0..maxTick-1 → IAE。 */
    public void add(long price) {
        throw new UnsupportedOperationException("TODO");
    }

    public long count() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 小于等于 price 的个数；price &lt; 0 → 0，price ≥ maxTick → count()。 */
    public long countAtMost(long price) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 第 rank 小（1 起）的价格。rank 不在 1..count() → IAE。 */
    public long kth(long rank) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 最近秩百分位，语义同 OrderStatistics.percentile（p 先检查，再检查空）。 */
    public long percentile(int p) {
        throw new UnsupportedOperationException("TODO");
    }

    public long median() {
        throw new UnsupportedOperationException("TODO");
    }
}
