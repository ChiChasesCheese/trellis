/**
 * 某个标的的仓位快照。
 *
 * @param netQty      净仓：多头为正、空头为负
 * @param openCost    未平仓位的成本（各未平仓 lot 的 qty * px 之和，恒 ≥ 0）
 * @param realizedPnl 已实现盈亏（FIFO：先开的仓先平）
 */
public record Position(String symbol, long netQty, long openCost, long realizedPnl) {
    public static Position flat(String symbol) { return new Position(symbol, 0, 0, 0); }

    /** 按 markPx 估值的未实现盈亏。多头 = 市值 - 成本；空头 = 成本 - 回补成本。flat 为 0。溢出抛 ArithmeticException。 */
    public long unrealizedPnl(long markPx) {
        throw new UnsupportedOperationException("TODO");
    }
}
