/** 订单的只读快照（OrderManager.get 返回）。record 自带 equals，测试可以直接比较两个 desk 的状态。 */
public record OrderView(Order order, OrderStatus status, long cumQty, long cumNotional, String rejectReason) {
    /** 还能被成交的数量；已撤销 / 已拒绝的单为 0。 */
    public long leavesQty() {
        return status.isTerminal() && status != OrderStatus.FILLED ? 0 : order.qty() - cumQty;
    }
}
