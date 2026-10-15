/**
 * 订单状态。合法转移（其余一律 IllegalTransitionException）：
 * <pre>
 *   PENDING --Ack--> WORKING --Fill--> PARTIALLY_FILLED --Fill--> FILLED
 *      |                |  \--Fill(吃满)--------------------------> FILLED
 *      |                \--Cancel--> CANCELED      (PARTIALLY_FILLED 也可以 Cancel)
 *      \--Reject--> REJECTED
 * </pre>
 */
public enum OrderStatus {
    PENDING, WORKING, PARTIALLY_FILLED, FILLED, CANCELED, REJECTED;

    public boolean isTerminal() { return this == FILLED || this == CANCELED || this == REJECTED; }

    /** 交易所上有这张单（可能被成交）。PENDING 也算：已经发出去、回报还没回来，风险上必须按「已经在市场里」处理。 */
    public boolean isOpen() { return !isTerminal(); }
}
