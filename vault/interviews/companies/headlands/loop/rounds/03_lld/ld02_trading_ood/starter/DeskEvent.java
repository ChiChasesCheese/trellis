/**
 * TradingDesk 的全部输入。journal 里存的就是这些，replay 把它们按顺序再喂一遍。
 * 注意：风控的拒绝结果、仓位、PnL 都不是输入，是 apply 的输出，replay 时重新算出来。
 */
public sealed interface DeskEvent permits DeskEvent.Submit, DeskEvent.SetReferencePrice, DeskEvent.Halt, DeskEvent.Resume, ExecEvent {
    record Submit(Order order) implements DeskEvent {
        public Submit { java.util.Objects.requireNonNull(order, "order"); }
    }

    record SetReferencePrice(String symbol, long px) implements DeskEvent {
        public SetReferencePrice {
            java.util.Objects.requireNonNull(symbol, "symbol");
            if (px <= 0) throw new IllegalArgumentException("px must be > 0: " + px);
        }
    }

    /** 熔断开关（kill switch）：之后的 Submit 全部被风控拒绝，直到 Resume。 */
    record Halt() implements DeskEvent {}

    record Resume() implements DeskEvent {}
}
