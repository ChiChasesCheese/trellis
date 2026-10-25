import java.util.Collections;
import java.util.NoSuchElementException;
import java.util.PriorityQueue;

/**
 * hc15 Part 3a：固定百分位 p 的两堆法。lo = 最小的 rank(n, p) 个数（最大堆），hi = 其余（最小堆）；value() = lo 的堆顶。
 * add 之后 rank 最多加 1，所以最多挪一两个元素：O(log n)；value() O(1)。代价：p 在构造时固定，换一个 p 要重建。
 * p = 50 就是 Part 1 的下中位数。
 */
public final class TwoHeapPercentile {
    private final int p;
    private final PriorityQueue<Long> lo = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Long> hi = new PriorityQueue<>();
    private long n;

    /** 1 ≤ p ≤ 100，否则 IAE。 */
    public TwoHeapPercentile(int p) {
        OrderStatistics.rank(1, p); // 复用 p 的检查
        this.p = p;
    }

    public void add(long price) {
        n++;
        if (lo.isEmpty() || price <= lo.peek()) lo.add(price);
        else hi.add(price);
        long target = OrderStatistics.rank(n, p);
        while (lo.size() > target) hi.add(lo.poll());
        while (lo.size() < target) lo.add(hi.poll());
    }

    /** 第 rank(n, p) 小的价格。还没有数据 → NoSuchElementException。 */
    public long value() {
        if (lo.isEmpty()) throw new NoSuchElementException("no prices yet");
        return lo.peek();
    }

    public long size() {
        return n;
    }
}
