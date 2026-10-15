import java.util.List;

/**
 * Part 4：事件溯源的单写者 desk。每个变更方法：先把输入追加到 journal，再改内存状态。
 * replay(limits, journal) 在新 desk 上重放，得到相同的订单、仓位、风控结论。
 */
public final class TradingDesk {
    public TradingDesk(RiskLimits limits) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 重复 id 抛 IllegalArgumentException。风控拒绝的单仍登记，状态 REJECTED，rejectReason = 原因名。 */
    public RiskResult submit(Order order) {
        throw new UnsupportedOperationException("TODO");
    }

    /** @return false = 重复 Fill。Fill 成功时同步更新 PositionBook。 */
    public boolean onExec(ExecEvent event) {
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

    public OrderView order(long id) {
        throw new UnsupportedOperationException("TODO");
    }

    public List<OrderView> allOrders() {
        throw new UnsupportedOperationException("TODO");
    }

    public Position position(String symbol) {
        throw new UnsupportedOperationException("TODO");
    }

    public List<String> symbols() {
        throw new UnsupportedOperationException("TODO");
    }

    /** journal 的不可变拷贝（含抛了异常的输入）。 */
    public List<DeskEvent> journal() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 用空 desk 重放；原来抛过异常的事件重放时同样被吞掉。 */
    public static TradingDesk replay(RiskLimits limits, List<DeskEvent> journal) {
        throw new UnsupportedOperationException("TODO");
    }
}
