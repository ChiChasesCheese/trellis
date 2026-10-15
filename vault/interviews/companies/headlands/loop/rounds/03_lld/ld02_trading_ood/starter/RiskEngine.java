/**
 * Part 3：交易前风控。check 只读，不改状态。检查顺序 = RiskReason 声明顺序，第一条违反的即结论。
 */
public final class RiskEngine {
    public RiskEngine(RiskLimits limits) {
        throw new UnsupportedOperationException("TODO");
    }

    public void setReferencePrice(String symbol, long px) {
        throw new UnsupportedOperationException("TODO");
    }

    public void halt() {
        throw new UnsupportedOperationException("TODO");
    }

    public void resume() {
        throw new UnsupportedOperationException("TODO");
    }

    public boolean halted() {
        throw new UnsupportedOperationException("TODO");
    }

    public RiskResult check(Order o, PositionBook positions, OrderManager orders) {
        throw new UnsupportedOperationException("TODO");
    }
}
