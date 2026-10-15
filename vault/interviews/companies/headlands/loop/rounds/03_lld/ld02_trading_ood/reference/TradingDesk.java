import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;

/**
 * Part 4：把订单状态机、仓位、风控装成一个「事件溯源」的单写者对象。
 *
 * 所有状态变化都来自 DeskEvent。每个公开的变更方法做三件事，顺序固定：
 *   1. 把输入追加到 journal（先写日志）；
 *   2. 调 handle(event) 修改内存状态；
 *   3. 把结果返回给调用方。
 * replay(journal) 对一个新 desk 重复第 2 步，得到逐位相同的状态——这就是崩溃恢复。
 * 因此 handle 必须是确定性的：不读时钟、不用随机数、不依赖 HashMap 遍历顺序。
 */
public final class TradingDesk {
    private final RiskLimits limits;
    private final OrderManager orders = new OrderManager();
    private final PositionBook positions = new PositionBook();
    private final RiskEngine risk;
    private final List<DeskEvent> journal = new ArrayList<>();

    public TradingDesk(RiskLimits limits) {
        this.limits = Objects.requireNonNull(limits, "limits");
        this.risk = new RiskEngine(limits);
    }

    public RiskResult submit(Order order) {
        DeskEvent e = new DeskEvent.Submit(order);
        journal.add(e);
        return handleSubmit((DeskEvent.Submit) e);
    }

    /** @return false = 重复的 Fill。非法事件抛 IllegalTransitionException / NoSuchElementException，状态不变（但输入仍在 journal 里）。 */
    public boolean onExec(ExecEvent event) {
        journal.add(Objects.requireNonNull(event, "event"));
        return handleExec(event);
    }

    public void setReferencePrice(String symbol, long px) {
        DeskEvent e = new DeskEvent.SetReferencePrice(symbol, px);
        journal.add(e);
        handle(e);
    }

    public void halt() { var e = new DeskEvent.Halt(); journal.add(e); handle(e); }

    public void resume() { var e = new DeskEvent.Resume(); journal.add(e); handle(e); }

    public OrderView order(long id) { return orders.get(id); }

    public List<OrderView> allOrders() { return orders.all(); }

    public Position position(String symbol) { return positions.get(symbol); }

    public List<String> symbols() { return positions.symbols(); }

    /** journal 的不可变拷贝。 */
    public List<DeskEvent> journal() { return List.copyOf(journal); }

    /** 用空 desk 重放 journal。重放时，原来抛过异常的事件会再抛一次——同样地被吞掉，状态同样不变。 */
    public static TradingDesk replay(RiskLimits limits, List<DeskEvent> journal) {
        TradingDesk d = new TradingDesk(limits);
        for (DeskEvent e : journal) {
            d.journal.add(e);
            try {
                d.handle(e);
            } catch (IllegalArgumentException | IllegalStateException | NoSuchElementException | ArithmeticException sameAsBefore) {
                // 第一次执行时调用方已经看到过这个异常，且状态没有改变
            }
        }
        return d;
    }

    // ---------- 确定性的状态转移 ----------

    private Object handle(DeskEvent e) {
        return switch (e) {
            case DeskEvent.Submit s -> handleSubmit(s);
            case DeskEvent.SetReferencePrice(var symbol, var px) -> { risk.setReferencePrice(symbol, px); yield null; }
            case DeskEvent.Halt h -> { risk.halt(); yield null; }
            case DeskEvent.Resume r -> { risk.resume(); yield null; }
            case ExecEvent x -> handleExec(x);
        };
    }

    private RiskResult handleSubmit(DeskEvent.Submit s) {
        Order o = s.order();
        if (orders.contains(o.id())) throw new IllegalArgumentException("duplicate order id " + o.id());
        RiskResult r = risk.check(o, positions, orders);      // 必须在 submit 之前：否则这张单把自己算进未完成数量
        orders.submit(o);
        if (r instanceof RiskResult.Rejected(var reason)) orders.apply(new ExecEvent.Reject(o.id(), reason.name()));
        return r;
    }

    /** OrderManager.apply 先于仓位更新；PositionBook 的算术溢出是「不可能事件」（数量 * 价格 > 9.2e18），这里不做补偿。 */
    private boolean handleExec(ExecEvent x) {
        boolean applied = orders.apply(x);
        if (applied && x instanceof ExecEvent.Fill(var orderId, var ignoredExecId, var qty, var px)) {
            Order o = orders.get(orderId).order();
            positions.onFill(o.symbol(), o.side(), qty, px);
        }
        return applied;
    }
}
