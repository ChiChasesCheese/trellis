import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/**
 * Part 3：交易前风控（pre-trade risk check）。check 是纯函数式的：只读，不改任何状态（改状态的是 TradingDesk）。
 * 检查按 RiskReason 的声明顺序，第一条违反的就是结论——确定性。
 */
public final class RiskEngine {
    private final RiskLimits limits;
    private final Map<String, Long> refPx = new HashMap<>();
    private boolean halted;

    public RiskEngine(RiskLimits limits) { this.limits = Objects.requireNonNull(limits, "limits"); }

    public void setReferencePrice(String symbol, long px) {
        Objects.requireNonNull(symbol, "symbol");
        if (px <= 0) throw new IllegalArgumentException("px must be > 0");
        refPx.put(symbol, px);
    }

    public void halt() { halted = true; }

    public void resume() { halted = false; }

    public boolean halted() { return halted; }

    public RiskResult check(Order o, PositionBook positions, OrderManager orders) {
        if (halted) return reject(RiskReason.HALTED);
        Long ref = refPx.get(o.symbol());
        if (ref == null) return reject(RiskReason.NO_REFERENCE_PRICE);      // fail closed
        if (o.qty() > limits.maxOrderQty()) return reject(RiskReason.QTY_LIMIT);
        try {
            if (Math.multiplyExact(o.px(), o.qty()) > limits.maxOrderNotional()) return reject(RiskReason.NOTIONAL_LIMIT);
            // |px - ref| / ref <= bps / 10000   <=>   |px - ref| * 10000 <= ref * bps    （整数交叉相乘，不做除法）
            long dev = Math.multiplyExact(Math.abs(o.px() - ref), 10_000L);
            if (dev > Math.multiplyExact(ref, limits.priceBandBps())) return reject(RiskReason.PRICE_BAND);
        } catch (ArithmeticException overflow) {
            return reject(RiskReason.NOTIONAL_LIMIT);
        }
        if (orders.openCount() >= limits.maxOpenOrders()) return reject(RiskReason.OPEN_ORDERS_LIMIT);
        // 最坏情况净仓：假设所有未完成买单都成交 / 所有未完成卖单都成交（含这一单）
        long buyLeaves = orders.openLeaves(o.symbol(), Side.BUY) + (o.side() == Side.BUY ? o.qty() : 0);
        long sellLeaves = orders.openLeaves(o.symbol(), Side.SELL) + (o.side() == Side.SELL ? o.qty() : 0);
        long net = positions.netQty(o.symbol());
        if (net + buyLeaves > limits.maxPosition() || net - sellLeaves < -limits.maxPosition())
            return reject(RiskReason.POSITION_LIMIT);
        return RiskResult.ACCEPTED;
    }

    private static RiskResult reject(RiskReason r) { return new RiskResult.Rejected(r); }
}
