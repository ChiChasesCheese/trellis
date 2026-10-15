/**
 * Part 4：热路径版订单簿。价格是 long tick（有界价格带 1..maxTicks-1），不装箱，稳态下 limit / cancel 不分配对象。
 *
 * 提示：订单池用结构数组（long[] id、long[] qty、int[] prev/next…）+ 侵入式双向链表，空闲槽用 free list；
 * 价位 = 数组下标（head[side][tick]、tail[side][tick]、levelQty[side][tick]）；id → 槽位用开放寻址（long[] keys，0 = 空，注意回移删除）；
 * 最优价被吃光后找下一档：非空价位位图 + Long.numberOfTrailingZeros / numberOfLeadingZeros。
 */
public final class TickBook {
    public static final long NONE = -1;
    public static final long REJECTED = -1;
    public static final long FULL = -2;
    /** 单笔数量上限：保证价位总量（≤ 2^22 张 × 2^40）不会溢出 long。 */
    public static final long MAX_QTY = 1L << 40;

    /** 成交回调：不产生事件对象。 */
    public interface TradeSink {
        void onTrade(long takerId, long makerId, long price, long qty);
    }

    /** maxTicks ≥ 2；1 ≤ capacity ≤ 2^22（最多同时挂这么多单）。 */
    public TickBook(int maxTicks, int capacity) { throw new UnsupportedOperationException("TODO"); }

    /**
     * 限价单：先吃对手盘（价格-时间优先，每笔成交回调 sink，价格取 maker 价），剩余挂簿。
     * 返回挂簿的剩余量（0 = 全部成交）；非法返回 REJECTED（id ≤ 0、id 已在簿上、价格不在 1..maxTicks-1、数量不在 1..MAX_QTY）；
     * 池满返回 FULL（此时不撮合，也不改变簿）。
     */
    public long limit(long id, OrderBook.Side side, long price, long qty, TradeSink sink) { throw new UnsupportedOperationException("TODO"); }

    /** O(1)：按 id 撤单。 */
    public boolean cancel(long id) { throw new UnsupportedOperationException("TODO"); }

    /** 没有时返回 NONE。 */
    public long bestBid() { throw new UnsupportedOperationException("TODO"); }
    public long bestAsk() { throw new UnsupportedOperationException("TODO"); }

    public int liveOrders() { throw new UnsupportedOperationException("TODO"); }

    /** 某价位总量；价格带外返回 0。 */
    public long qtyAt(OrderBook.Side side, long price) { throw new UnsupportedOperationException("TODO"); }
}
