import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.NoSuchElementException;
import java.util.PriorityQueue;

/**
 * hc15 Part 2：最近 k 笔成交价的滑动窗口中位数（下中位数）。
 *
 * <p>堆不支持「删任意元素」，所以用<b>惰性删除</b>（lazy deletion）：窗口滑出的旧值先记在 delayed 表里，
 * 等它浮到堆顶再真正弹出。lo / hi 各有一张 delayed 表和一个「有效元素个数」：
 * 按个数而不是 heap.size() 做平衡；堆顶始终保持有效（每次操作之后 prune）。
 * 旧值属于 lo 还是 hi 由 old ≤ lo.peek() 判定——lo 里每个数 ≤ hi 里每个数，所以这个判定可以相信，
 * 而且相等的值在 lo 顶一定有一份有效拷贝。每个数最多进堆一次、出堆一次：摊还 O(log k)。
 *
 * <p>惰性删除的代价：埋在堆底的失效元素不会自己浮上来（升序的流里，lo 的堆顶一直在变大，旧的小值永远沉在底下），
 * 堆会长到 O(n)。所以失效元素多于 2k 个时整体重建（排序窗口，O(k log k)，至少隔 2k 次 add 才发生一次），堆里最多留 3k 个。
 */
public final class WindowMedian {
    private final int k;
    private final long[] ring; // 最近 k 个值，环形缓冲
    private int head, count;
    private final PriorityQueue<Long> lo = new PriorityQueue<>(Collections.reverseOrder());
    private final PriorityQueue<Long> hi = new PriorityQueue<>();
    private final HashMap<Long, Integer> delayedLo = new HashMap<>(), delayedHi = new HashMap<>();
    private int loValid, hiValid;

    /** k ≥ 1，否则 IAE。 */
    public WindowMedian(int k) {
        if (k < 1) throw new IllegalArgumentException("k must be >= 1: " + k);
        this.k = k;
        this.ring = new long[k];
    }

    public void add(long price) {
        long old = 0;
        boolean evict = count == k;
        if (evict) {
            old = ring[head];
            ring[head] = price;
            head = (head + 1) % k;
        } else {
            ring[(head + count) % k] = price;
            count++;
        }
        if (loValid == 0 || price <= lo.peek()) {
            lo.add(price);
            loValid++;
        } else {
            hi.add(price);
            hiValid++;
        }
        if (evict) {
            if (old <= lo.peek()) {
                delayedLo.merge(old, 1, Integer::sum);
                loValid--;
            } else {
                delayedHi.merge(old, 1, Integer::sum);
                hiValid--;
            }
        }
        // 平衡：|lo| = |hi| 或 |hi| + 1（按有效个数）
        if (loValid > hiValid + 1) {
            prune(lo, delayedLo);
            hi.add(lo.poll());
            loValid--;
            hiValid++;
        } else if (loValid < hiValid) {
            prune(hi, delayedHi);
            lo.add(hi.poll());
            hiValid--;
            loValid++;
        }
        prune(lo, delayedLo);
        prune(hi, delayedHi);
        if (lo.size() + hi.size() - loValid - hiValid > 2L * k) rebuild();
    }

    private void rebuild() {
        long[] w = new long[count];
        for (int i = 0; i < count; i++) w[i] = ring[(head + i) % k];
        Arrays.sort(w);
        lo.clear();
        hi.clear();
        delayedLo.clear();
        delayedHi.clear();
        loValid = (count + 1) / 2;
        hiValid = count - loValid;
        for (int i = 0; i < count; i++) (i < loValid ? lo : hi).add(w[i]);
    }

    private static void prune(PriorityQueue<Long> heap, HashMap<Long, Integer> delayed) {
        while (!heap.isEmpty()) {
            Integer n = delayed.get(heap.peek());
            if (n == null) return;
            if (n == 1) delayed.remove(heap.peek());
            else delayed.put(heap.peek(), n - 1);
            heap.poll();
        }
    }

    /** 窗口里（最近 min(n, k) 个价格）的下中位数。还没有数据 → NoSuchElementException。 */
    public long median() {
        if (count == 0) throw new NoSuchElementException("no prices yet");
        return lo.peek();
    }

    /** 窗口里现在有几个价格：min(已加入个数, k)。 */
    public int size() {
        return count;
    }

    /** 两个堆里实际占着的元素个数（含还没被惰性清掉的失效元素）。必须保持 ≤ 4k，不随流的长度增长。 */
    public int retained() {
        return lo.size() + hi.size();
    }

    /** 每加入一个价格之后的窗口中位数：result[i] = 加入 prices[0..i] 后的 median()。k ≥ 1 否则 IAE；null → NPE。 */
    public static long[] slide(long[] prices, int k) {
        var w = new WindowMedian(k);
        long[] out = new long[prices.length];
        for (int i = 0; i < prices.length; i++) {
            w.add(prices[i]);
            out[i] = w.median();
        }
        return out;
    }
}
