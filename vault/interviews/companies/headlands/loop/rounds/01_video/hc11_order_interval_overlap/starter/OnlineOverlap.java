/**
 * hc11 Part 3（starter）：在线版。订单（Place）和撤单（Cancel）按时间顺序到达（时间戳不降，可以相同），
 * 随时回答「到现在为止的最大重叠数（及最早时刻）」和「t 时刻有几张单活着」。
 *
 * <p>提示：差分数组。过去的差分已累加成确定的活跃数；未来的差分（订单的计划结束时间）放在有序 Map 里等着。
 * 每个方向（BUY、SELL，再加一个「全部」）各一份状态。小心：同一时间戳内先 place 后 cancel，
 * 最终该时刻的活跃数会变小，最大值要在时间戳「过去」之后才算数。每次事件应是 O(log n)。
 */
public final class OnlineOverlap {

    public OnlineOverlap() {
        // 在这里初始化你的状态
    }

    /** 下单：订单在 start 时刻到达（start >= 上一个事件的时间），计划到 end（不含）结束。
     *  start 倒退 / id 重复 / end < start → IAE。end == start 合法但从没活过。 */
    public void place(long id, OrderIntervals.Side side, long start, long end) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 撤单：time 时刻起不再活着。返回 true 表示真的缩短了一张还活着的单；已结束 / 已撤过 → false；
     *  id 不存在或 time 倒退 → IAE。 */
    public boolean cancel(long id, long time) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 分派一个事件（sealed + 记录模式）。Place 返回 true；Cancel 返回 cancel(..) 的结果。 */
    public boolean apply(OrderIntervals.OrderEvent e) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 只推进时钟：让到期的订单从「现在」的计数里扣掉。t 倒退 → IAE。 */
    public void advanceTo(long t) {
        throw new UnsupportedOperationException("TODO");
    }

    public long now() {
        throw new UnsupportedOperationException("TODO");
    }

    public int liveNow() {
        throw new UnsupportedOperationException("TODO");
    }

    public int liveNow(OrderIntervals.Side side) {
        throw new UnsupportedOperationException("TODO");
    }

    /** t 时刻（0 <= t <= now）所有方向合计活着几张。t 越界 → IAE。 */
    public int liveAt(long t) {
        throw new UnsupportedOperationException("TODO");
    }

    public int liveAt(OrderIntervals.Side side, long t) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 到目前为止（含当前时间戳）的最大重叠数及最早时刻。 */
    public OrderIntervals.Peak peak() {
        throw new UnsupportedOperationException("TODO");
    }

    public OrderIntervals.Peak peak(OrderIntervals.Side side) {
        throw new UnsupportedOperationException("TODO");
    }

    public int maxSoFar() {
        throw new UnsupportedOperationException("TODO");
    }

    public int maxSoFar(OrderIntervals.Side side) {
        throw new UnsupportedOperationException("TODO");
    }
}
