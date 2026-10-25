import java.util.Collections;
import java.util.NoSuchElementException;
import java.util.PriorityQueue;

/**
 * hc15 Part 1：数据流的中位数。价格是 long tick，可以是任意 long（包括负数、Long.MIN_VALUE）。
 *
 * <p>约定：偶数个数时 median() 取「下中位数」（lower median，第 ceil(n/2) 小的那个）。理由：结果一定是真实出现过的价格、
 * 还是整数 tick、而且等于 Part 3 的最近秩百分位 p = 50。需要真正的平均数时用 doubledMedian()（中位数的两倍，整数，不用约定舍入）。
 *
 * <p>两个堆：lo = 较小的一半（最大堆），hi = 较大的一半（最小堆）；不变式 lo 里每个数 ≤ hi 里每个数，且 |lo| = |hi| 或 |hi| + 1。
 */
public final class StreamingMedian {
    private final PriorityQueue<Long> lo = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Long> hi = new PriorityQueue<>();

    /** O(log n)。 */
    public void add(long price) {
        if (lo.isEmpty() || price <= lo.peek()) lo.add(price);
        else hi.add(price);
        if (lo.size() > hi.size() + 1) hi.add(lo.poll());
        else if (hi.size() > lo.size()) lo.add(hi.poll());
    }

    /** 下中位数，O(1)。还没有数据 → NoSuchElementException。 */
    public long median() {
        if (lo.isEmpty()) throw new NoSuchElementException("no prices yet");
        return lo.peek();
    }

    /**
     * 中位数的两倍：奇数个时 2 × 中间值，偶数个时 下中位数 + 上中位数。O(1)。
     * 和溢出 long → ArithmeticException；没有数据 → NoSuchElementException。
     */
    public long doubledMedian() {
        if (lo.isEmpty()) throw new NoSuchElementException("no prices yet");
        long upper = lo.size() == hi.size() ? hi.peek() : lo.peek();
        return Math.addExact(lo.peek(), upper);
    }

    public int size() {
        return lo.size() + hi.size();
    }
}
