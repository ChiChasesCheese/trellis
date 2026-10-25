/**
 * hc15 Part 3a（starter）：固定百分位 p 的两堆法。
 *
 * <p>提示：lo = 最小的 OrderStatistics.rank(n, p) 个数（最大堆），hi = 其余（最小堆）；value() = lo 的堆顶。
 * 每次 add 之后 rank 最多加 1，所以最多挪一两个元素。p = 50 就是 Part 1。
 */
public final class TwoHeapPercentile {
    // 在这里加你的字段

    /** 1 ≤ p ≤ 100，否则 IAE。 */
    public TwoHeapPercentile(int p) {
        throw new UnsupportedOperationException("TODO");
    }

    /** O(log n)。 */
    public void add(long price) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 第 rank(n, p) 小的价格，O(1)。还没有数据 → NoSuchElementException。 */
    public long value() {
        throw new UnsupportedOperationException("TODO");
    }

    public long size() {
        throw new UnsupportedOperationException("TODO");
    }
}
