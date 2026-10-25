/**
 * hc15 Part 1（starter）：数据流的中位数。价格是 long tick，可以是任意 long（包括负数、Long.MIN_VALUE）。
 *
 * <p>约定：偶数个数时 median() 取「下中位数」（lower median，第 ceil(n/2) 小的那个）。
 * 提示：两个堆——lo = 较小的一半（最大堆），hi = 较大的一半（最小堆）；不变式 lo 里每个数 ≤ hi 里每个数，且 |lo| = |hi| 或 |hi| + 1。
 */
public final class StreamingMedian {
    // 在这里加你的字段（两个堆）

    /** O(log n)。 */
    public void add(long price) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 下中位数，O(1)。还没有数据 → NoSuchElementException。 */
    public long median() {
        throw new UnsupportedOperationException("TODO");
    }

    /**
     * 中位数的两倍：奇数个时 2 × 中间值，偶数个时 下中位数 + 上中位数。O(1)。
     * 和溢出 long → ArithmeticException；没有数据 → NoSuchElementException。
     */
    public long doubledMedian() {
        throw new UnsupportedOperationException("TODO");
    }

    public int size() {
        throw new UnsupportedOperationException("TODO");
    }
}
