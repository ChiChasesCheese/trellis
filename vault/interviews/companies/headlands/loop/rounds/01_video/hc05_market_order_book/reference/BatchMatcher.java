import java.util.List;
import java.util.Objects;

/** Part 3（hc14 Limit Order Matching）：按到达顺序处理一批 [side, price, quantity]。 */
public final class BatchMatcher {
    private BatchMatcher() {}

    public record Summary(List<OrderBook.Trade> trades, long filledQty, long notional,
                          List<OrderBook.Level> bids, List<OrderBook.Level> asks) {}

    /**
     * rows[i] = {side, price, qty}，side 0 = BUY / 1 = SELL (reconstructed)；订单 id = i + 1。
     * 全部行先校验再处理（非法 → IAE，信息带行号）。notional = Σ price × qty，溢出抛 ArithmeticException。
     */
    // 为什么先整体校验再处理：半途发现第 9999 行非法时，前面的行已经改了簿；调用方要么拿到完整结果，要么拿到异常，不要半个状态。
    public static Summary run(long[][] rows) {
        Objects.requireNonNull(rows, "rows");
        for (int i = 0; i < rows.length; i++) {
            var r = rows[i];
            if (r == null || r.length != 3) throw new IllegalArgumentException("row " + i + ": expected [side, price, quantity]");
            if (r[0] != 0 && r[0] != 1) throw new IllegalArgumentException("row " + i + ": bad side");
            if (r[1] <= 0) throw new IllegalArgumentException("row " + i + ": " + OrderBook.INVALID_PRICE);
            if (r[2] <= 0) throw new IllegalArgumentException("row " + i + ": " + OrderBook.INVALID_QTY);
        }
        var book = new OrderBook();
        var cmds = new java.util.ArrayList<OrderBook.Command>(rows.length);
        for (int i = 0; i < rows.length; i++) {
            var side = rows[i][0] == 0 ? OrderBook.Side.BUY : OrderBook.Side.SELL;
            cmds.add(new OrderBook.Limit(i + 1, side, rows[i][1], rows[i][2]));
        }
        var events = book.executeAll(cmds);
        for (var e : events) {
            if (e instanceof OrderBook.Rejected(var id, var why)) {
                throw new ArithmeticException("row " + (id - 1) + ": " + why);
            }
        }
        List<OrderBook.Trade> trades = events.stream().<OrderBook.Trade>mapMulti((e, sink) -> {
            if (e instanceof OrderBook.Trade t) sink.accept(t);
        }).toList();
        // 名义金额 = Σ 价格 × 数量。两个 long 相乘很容易超 9.2e18（价格 4e9 × 数量 3e9 就超），
        // 静默回绕会得到负数 / 错数，所以用 multiplyExact / addExact 让它直接抛异常。
        long filled = 0, notional = 0;
        for (var t : trades) {
            filled = Math.addExact(filled, t.qty());
            notional = Math.addExact(notional, Math.multiplyExact(t.price(), t.qty()));
        }
        return new Summary(trades, filled, notional,
                book.depth(OrderBook.Side.BUY, Integer.MAX_VALUE), book.depth(OrderBook.Side.SELL, Integer.MAX_VALUE));
    }
}
