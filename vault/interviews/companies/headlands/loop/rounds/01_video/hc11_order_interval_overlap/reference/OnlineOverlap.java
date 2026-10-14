import java.util.EnumMap;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

/**
 * hc11 Part 3：在线版。订单（Place）和撤单（Cancel）按<b>时间顺序</b>到达（时间戳不降，可以相同），
 * 随时回答「到现在为止的最大重叠数（及最早时刻）」和「t 时刻有几张单活着」。
 *
 * <p>核心想法是<b>差分数组（difference array）</b>：下单在 start 处 +1、在 end 处 -1，某时刻的活跃数 = 这个时刻及以前所有差分之和。
 * 事件按时间到达，所以「过去」的差分已经被累加成了确定的活跃数；只有「未来」的差分（订单的计划结束时间）需要等着。
 * 每个方向（买 / 卖，外加一个「全部」）各有一个 {@link Lane} 记录：
 * <ul>
 *   <li>{@code expiries}：未来差分，结束时间 → 在那一刻结束的订单数（有序 Map，最早的结束时间在最前面）；</li>
 *   <li>{@code history}：已确定的活跃数，时间 → 该时刻的活跃数（阶梯函数，用 floorEntry 回答「t 时刻有几张」）；</li>
 *   <li>{@code live} 与 {@code committedMax}：当前活跃数；已「封账」的最大值。</li>
 * </ul>
 * 每次事件 O(log n)。
 */
public final class OnlineOverlap {

    /** 一个订单的当前状态。撤单时用 record 的新副本替换：把 end 改成撤单时间，之后再撤就看到「已经结束」。 */
    private record Order(long id, OrderIntervals.Side side, long start, long end) {}

    private static final class Lane {
        final TreeMap<Long, Integer> expiries = new TreeMap<>();
        final TreeMap<Long, Integer> history = new TreeMap<>();
        int live;
        /** 所有「已经过去」的时间戳里，最终活跃数的最大值，以及它最早出现的时刻。 */
        int committedMax;
        long committedTime;

        /** 这条 lane 最近一次处理到的时间戳（= 全局 now）。 */
        long lastTick;

        /** 时钟从 lastTick 走到 to（to > lastTick）：先给 lastTick 这个时间戳封账，再把 <= to 的结束折叠进 live。 */
        void advance(long to) {
            if (live > committedMax) {
                committedMax = live;
                committedTime = lastTick;
            }
            Map.Entry<Long, Integer> e;
            while ((e = expiries.firstEntry()) != null && e.getKey() <= to) {
                expiries.pollFirstEntry();
                live -= e.getValue();
                history.put(e.getKey(), live); // 阶梯在结束时间处下降
            }
            lastTick = to;
        }

        void open(long end) {
            live++;
            expiries.merge(end, 1, Integer::sum);
        }

        void cancel(long end) {
            live--;
            expiries.compute(end, (k, c) -> c == 1 ? null : c - 1);
        }

        void stamp() {
            history.put(lastTick, live); // 当前时间戳的最终（到目前为止）活跃数
        }

        int liveAt(long t) {
            var f = history.floorEntry(t);
            return f == null ? 0 : f.getValue();
        }

        OrderIntervals.Peak peak() {
            // 当前时间戳还没封账：live 也是候选。相等时较早的（已封账的）赢。
            return live > committedMax ? new OrderIntervals.Peak(live, lastTick)
                    : new OrderIntervals.Peak(committedMax, committedTime);
        }
    }

    private final Map<Long, Order> orders = new HashMap<>();
    private final Map<OrderIntervals.Side, Lane> lanes = new EnumMap<>(OrderIntervals.Side.class);
    private final Lane all = new Lane();
    private long now = 0;

    public OnlineOverlap() {
        for (var s : OrderIntervals.Side.values()) lanes.put(s, new Lane());
    }

    // ---------------------------------------------------------------- 写

    /** 下单：订单在 start 时刻到达（start >= 上一个事件的时间），计划到 end（不含）结束。 */
    public void place(long id, OrderIntervals.Side side, long start, long end) {
        var p = new OrderIntervals.Place(id, side, start, end); // 复用 record 的校验（非负、end >= start）
        if (start < now) throw new IllegalArgumentException("event out of order: " + start + " < " + now);
        if (orders.containsKey(id)) throw new IllegalArgumentException("duplicate order id " + id);
        advanceTo(start);
        orders.put(id, new Order(id, p.side(), start, end));
        if (end > start) { // 空区间不影响任何计数
            var lane = lanes.get(side);
            lane.open(end);
            all.open(end);
            lane.stamp();
            all.stamp();
        }
    }

    /**
     * 撤单：time 时刻起不再活着。返回 true 表示真的缩短了一张还活着的单；
     * 已经自然结束或已被撤过 → false；id 不存在 → IAE；time 倒退 → IAE。
     */
    public boolean cancel(long id, long time) {
        var o = orders.get(id);
        if (o == null) throw new IllegalArgumentException("cancel of unknown order " + id);
        if (time < now) throw new IllegalArgumentException("event out of order: " + time + " < " + now);
        advanceTo(time);
        boolean effective = o.end() > time; // start <= now == time，所以 end > time 就是还活着
        if (effective) {
            var lane = lanes.get(o.side());
            lane.cancel(o.end());
            all.cancel(o.end());
            lane.stamp();
            all.stamp();
            orders.put(id, new Order(id, o.side(), o.start(), time));
        }
        return effective;
    }

    /** 分派一个 {@link OrderIntervals.OrderEvent}（sealed + 记录模式）。返回 false 只可能是「无效的撤单」。 */
    public boolean apply(OrderIntervals.OrderEvent e) {
        return switch (e) {
            case OrderIntervals.Place(var id, var side, var start, var end) -> {
                place(id, side, start, end);
                yield true;
            }
            case OrderIntervals.Cancel(var id, var time) -> cancel(id, time);
        };
    }

    /** 只推进时钟（没有事件）：让已经到期的订单从「现在」的计数里扣掉。 */
    public void advanceTo(long t) {
        if (t < now) throw new IllegalArgumentException("time went backwards: " + t + " < " + now);
        if (t > now) {
            for (var l : lanes.values()) l.advance(t);
            all.advance(t);
            now = t;
        }
    }

    // ---------------------------------------------------------------- 读

    public long now() {
        return now;
    }

    public int liveNow() {
        return all.live;
    }

    public int liveNow(OrderIntervals.Side side) {
        return lanes.get(side).live;
    }

    /** t 时刻（0 <= t <= now）所有方向合计活着几张。t > now 是预测，不支持 → IAE。 */
    public int liveAt(long t) {
        checkPast(t);
        return all.liveAt(t);
    }

    public int liveAt(OrderIntervals.Side side, long t) {
        checkPast(t);
        return lanes.get(side).liveAt(t);
    }

    /** 到目前为止（含当前时间戳）的最大重叠数及最早时刻。 */
    public OrderIntervals.Peak peak() {
        return all.peak();
    }

    public OrderIntervals.Peak peak(OrderIntervals.Side side) {
        return lanes.get(side).peak();
    }

    public int maxSoFar() {
        return peak().count();
    }

    public int maxSoFar(OrderIntervals.Side side) {
        return peak(side).count();
    }

    private void checkPast(long t) {
        if (t < 0 || t > now) throw new IllegalArgumentException("t must be in [0, now=" + now + "]: " + t);
    }
}
