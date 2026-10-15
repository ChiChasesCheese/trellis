/** 交易所 / 网关回给我们的执行回报。sealed：switch 里漏一种，编译器报错。 */
public sealed interface ExecEvent extends DeskEvent permits ExecEvent.Ack, ExecEvent.Fill, ExecEvent.Cancel, ExecEvent.Reject {
    long orderId();

    /** 交易所收下了这张单。 */
    record Ack(long orderId) implements ExecEvent {}

    /** 一笔成交。execId 全局唯一：回报可能重复投递（at-least-once），靠它去重。 */
    record Fill(long orderId, long execId, long qty, long px) implements ExecEvent {
        public Fill {
            if (qty <= 0) throw new IllegalArgumentException("fill qty must be > 0: " + qty);
            if (px <= 0) throw new IllegalArgumentException("fill px must be > 0: " + px);
        }
    }

    /** 撤单已确认（不是「撤单请求」）。 */
    record Cancel(long orderId) implements ExecEvent {}

    /** 交易所拒绝（或本地风控拒绝）。 */
    record Reject(long orderId, String reason) implements ExecEvent {
        public Reject {
            java.util.Objects.requireNonNull(reason, "reason");
        }
    }
}
