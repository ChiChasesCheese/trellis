import java.util.List;

/**
 * Part 1：订单状态机。单线程使用。
 * 规则见 problem.md。要点：先验证后修改（异常路径不改状态）；风控要的聚合量增量维护，O(1) 读取。
 */
public final class OrderManager {
    /** 登记新单，初始状态 PENDING。重复 id 抛 IllegalArgumentException。 */
    public void submit(Order order) {
        throw new UnsupportedOperationException("TODO");
    }

    /**
     * 应用一条执行回报。
     * @return true = 已应用；false = 重复的 Fill（execId 见过），无效果。
     * @throws java.util.NoSuchElementException 未知订单
     * @throws IllegalTransitionException       非法转移 / 超量成交 / 成交价越过限价（状态不变）
     */
    public boolean apply(ExecEvent event) {
        throw new UnsupportedOperationException("TODO");
    }

    public boolean contains(long orderId) {
        throw new UnsupportedOperationException("TODO");
    }

    /** @throws java.util.NoSuchElementException 未知订单 */
    public OrderView get(long orderId) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 全部未终结订单（PENDING / WORKING / PARTIALLY_FILLED），按 id 升序。 */
    public List<OrderView> open() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 全部订单（含已终结），按 id 升序。 */
    public List<OrderView> all() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 未终结订单个数。O(1)。 */
    public int openCount() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 某标的某方向所有未终结订单的剩余数量之和（含 PENDING）。O(1)。 */
    public long openLeaves(String symbol, Side side) {
        throw new UnsupportedOperationException("TODO");
    }
}
