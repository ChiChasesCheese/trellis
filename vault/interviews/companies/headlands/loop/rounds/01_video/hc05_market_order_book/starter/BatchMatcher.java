import java.util.List;

/** Part 3（hc14 Limit Order Matching）：按到达顺序处理一批 [side, price, quantity]。可以直接复用 Part 2 的 OrderBook。 */
public final class BatchMatcher {
    private BatchMatcher() {}

    public record Summary(List<OrderBook.Trade> trades, long filledQty, long notional,
                          List<OrderBook.Level> bids, List<OrderBook.Level> asks) {}

    /**
     * rows[i] = {side, price, qty}，side 0 = BUY / 1 = SELL (reconstructed)；订单 id = i + 1。
     * 全部行先校验再处理（非法 → IAE，信息以 "row i" 开头，i 从 0 起）。
     * notional = Σ price × qty，溢出抛 ArithmeticException。rows 为 null 抛 NPE。
     */
    public static Summary run(long[][] rows) { throw new UnsupportedOperationException("TODO"); }
}
