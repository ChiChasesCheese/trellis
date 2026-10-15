import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;

/**
 * hc11 Part 1 + Part 2：区间最大重叠（扫描线 sweep line），以及按买 / 卖方向 + 撤单的版本。
 *
 * <p>订单的生命周期是<b>左闭右开</b>区间 [start, end)：start 时刻已经「活着」，end 时刻已经「不活了」。
 * 所以 [1,3) 和 [3,5) 在时刻 3 交接，任何时刻都只有 1 个活着——这就是「同一时刻先处理结束、再处理开始」。
 * 时间是非负整数（long），可以很大（接近 Long.MAX_VALUE），所以本类<b>从不做减法</b>，只做比较。
 */
public final class OrderIntervals {
    private OrderIntervals() {}

    // ---------------------------------------------------------------- 数据类型

    public enum Side { BUY, SELL }

    /** 最大重叠数 count，以及它<b>最早</b>出现的时刻 time。从没有订单活着时是 (0, 0)。 */
    public record Peak(int count, long time) {}

    /** 一条买卖订单的生命周期事件（封闭层级）。 */
    public sealed interface OrderEvent permits Place, Cancel {}

    /** 下单：计划生命周期 [start, end)。end == start 是合法的空区间（从没活过）。 */
    public record Place(long id, Side side, long start, long end) implements OrderEvent {
        public Place {
            Objects.requireNonNull(side, "side");
            if (start < 0) throw new IllegalArgumentException("negative start: " + start);
            if (end < start) throw new IllegalArgumentException("end < start: " + end + " < " + start);
        }
    }

    /** 撤单：time 时刻起这张单不再活着（把区间截成 [start, min(end, time))）。 */
    public record Cancel(long id, long time) implements OrderEvent {
        public Cancel {
            if (time < 0) throw new IllegalArgumentException("negative time: " + time);
        }
    }

    /** 买方、卖方、全部订单各自的峰值。 */
    public record Report(Peak buy, Peak sell, Peak all) {}

    // ---------------------------------------------------------------- Part 1

    /** 同时活着的订单数的最大值，区间 [start, end)。输入允许乱序、重复；空区间忽略；end < start 或 start < 0 → IAE。 */
    public static int maxOverlap(long[][] intervals) {
        return peak(intervals).count();
    }

    /** 同上，并给出最早达到最大值的时刻。 */
    public static Peak peak(long[][] intervals) {
        return sweep(intervals, false);
    }

    /** 闭区间 [start, end] 的版本：end 时刻订单还活着，所以 [1,3] 和 [3,5] 在 3 重叠。 */
    public static int maxOverlapInclusive(long[][] intervals) {
        return sweep(intervals, true).count();
    }

    private static Peak sweep(long[][] intervals, boolean inclusive) {
        Objects.requireNonNull(intervals, "intervals");
        int n = 0;
        var starts = new long[intervals.length];
        var ends = new long[intervals.length];
        for (long[] iv : intervals) {
            Objects.requireNonNull(iv, "interval");
            if (iv.length != 2) throw new IllegalArgumentException("interval must have 2 elements: " + Arrays.toString(iv));
            long s = iv[0];
            long e = iv[1];
            if (s < 0) throw new IllegalArgumentException("negative start: " + s);
            if (e < s) throw new IllegalArgumentException("end < start: " + e + " < " + s);
            if (!inclusive && e == s) continue; // 半开空区间从没活过
            starts[n] = s;
            ends[n] = e;
            n++;
        }
        return peakOf(starts, ends, n, inclusive);
    }

    /**
     * 扫描线的核心，用两个各自排好序的数组代替「事件列表」：
     * 处理第 i 个开始时，先把所有「已经结束」的订单从计数里扣掉，再数现在活着几个。
     * 半开区间：end <= s 就算结束（同一时刻先结束后开始）；闭区间：end < s 才算结束。
     * live = 已开始个数 (i+1) - 已结束个数 (j)。最大值只可能出现在某个 start 上（只有 start 会让计数变大）。
     */
    static Peak peakOf(long[] starts, long[] ends, int n, boolean inclusive) {
        if (n == 0) return new Peak(0, 0);
        Arrays.sort(starts, 0, n);
        Arrays.sort(ends, 0, n);
        int best = 0;
        long bestTime = 0;
        int j = 0; // ends[0..j) 都已结束
        for (int i = 0; i < n; i++) {
            long s = starts[i];
            while (j < n && (inclusive ? ends[j] < s : ends[j] <= s)) j++;
            int live = (i + 1) - j;
            // 严格 > ：多个时刻都达到最大值时保留最早的。同一个 s 重复出现时，后面的 live 更大，time 仍是 s。
            if (live > best) {
                best = live;
                bestTime = s;
            }
        }
        return new Peak(best, bestTime);
    }

    // ---------------------------------------------------------------- Part 2

    /** 一条「车道」：收集某个方向上所有有效区间的 start / end。 */
    private static final class Lane {
        long[] starts;
        long[] ends;
        int n;

        Lane(int capacity) {
            starts = new long[capacity];
            ends = new long[capacity];
        }

        void add(long s, long e) {
            starts[n] = s;
            ends[n] = e;
            n++;
        }

        Peak peak() {
            return peakOf(starts, ends, n, false);
        }
    }

    /**
     * 批量版：一串 Place / Cancel（顺序无所谓），分别给出买方、卖方、全部的峰值。
     *
     * <ul>
     *   <li>每张单的有效区间是 [start, min(end, 最早的撤单时间))；撤单时间 <= start 或区间为空 → 这张单从没活过；</li>
     *   <li>同一个 id 多次撤单：最早的那次生效，其余无影响；</li>
     *   <li>撤单的 id 找不到对应的 Place → IAE；同一个 id 两次 Place → IAE。</li>
     * </ul>
     */
    public static Report analyze(List<? extends OrderEvent> events) {
        Objects.requireNonNull(events, "events");
        var places = new HashMap<Long, Place>();
        var cancelAt = new HashMap<Long, Long>();
        for (OrderEvent e : events) {
            switch (e) { // sealed：少写一个 case 编译就报错，不需要 default
                case Place p -> {
                    if (places.putIfAbsent(p.id(), p) != null) throw new IllegalArgumentException("duplicate order id " + p.id());
                }
                case Cancel(var id, var time) -> cancelAt.merge(id, time, Math::min);
            }
        }
        for (long id : cancelAt.keySet()) {
            if (!places.containsKey(id)) throw new IllegalArgumentException("cancel of unknown order " + id);
        }
        var buy = new Lane(places.size());
        var sell = new Lane(places.size());
        var all = new Lane(places.size());
        for (Place p : places.values()) {
            long end = Math.min(p.end(), cancelAt.getOrDefault(p.id(), Long.MAX_VALUE));
            if (end <= p.start()) continue; // 空区间，或在开始前（或开始的瞬间）就被撤了
            Lane lane = switch (p.side()) {
                case BUY -> buy;
                case SELL -> sell;
            };
            lane.add(p.start(), end);
            all.add(p.start(), end);
        }
        return new Report(buy.peak(), sell.peak(), all.peak());
    }
}
