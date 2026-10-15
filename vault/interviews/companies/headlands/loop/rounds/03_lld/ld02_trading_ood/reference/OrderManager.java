import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.Set;

/**
 * Part 1：订单状态机。单线程使用（TradingDesk 保证单写者）。
 *
 * 两条设计原则：
 * 1. 先验证、后修改：任何抛异常的路径都不改变状态（replay 能复现「同样的异常、同样的状态」的前提）。
 * 2. 风控要的聚合量（某标的某方向的未完成数量、未完成订单数）在每次状态变化时增量维护，check 时 O(1)，而不是每次扫描所有订单。
 */
public final class OrderManager {
    /** 可变的内部状态；对外只给 OrderView 快照。 */
    private static final class State {
        final Order order;
        OrderStatus status = OrderStatus.PENDING;
        long cumQty;
        long cumNotional;
        String rejectReason;

        State(Order order) { this.order = order; }

        long leaves() { return order.qty() - cumQty; }

        OrderView view() { return new OrderView(order, status, cumQty, cumNotional, rejectReason); }
    }

    private final Map<Long, State> orders = new HashMap<>();
    private final Set<Long> seenExecIds = new HashSet<>();
    /** symbol -> {buyLeaves, sellLeaves}：仅统计未终结订单。 */
    private final Map<String, long[]> openLeaves = new HashMap<>();
    private int openCount;

    public void submit(Order order) {
        Objects.requireNonNull(order, "order");
        if (orders.containsKey(order.id())) throw new IllegalArgumentException("duplicate order id " + order.id());
        orders.put(order.id(), new State(order));
        openLeaves.computeIfAbsent(order.symbol(), k -> new long[2])[slot(order.side())] += order.qty();
        openCount++;
    }

    /** @return true = 已应用；false = 重复的 Fill（execId 已见过），无任何效果。 */
    public boolean apply(ExecEvent event) {
        Objects.requireNonNull(event, "event");
        State s = orders.get(event.orderId());
        if (s == null) throw new NoSuchElementException("unknown order " + event.orderId());
        return switch (event) {
            case ExecEvent.Ack a -> {
                require(s.status == OrderStatus.PENDING, s, "Ack");
                s.status = OrderStatus.WORKING;
                yield true;
            }
            case ExecEvent.Fill f -> {
                if (seenExecIds.contains(f.execId())) yield false;     // 重复投递：先于状态检查（FILLED 之后重放的旧回报也只是重复）
                require(s.status == OrderStatus.WORKING || s.status == OrderStatus.PARTIALLY_FILLED, s, "Fill");
                if (f.qty() > s.leaves()) throw new IllegalTransitionException("overfill on order " + s.order.id());
                boolean outside = s.order.side() == Side.BUY ? f.px() > s.order.px() : f.px() < s.order.px();
                if (outside) throw new IllegalTransitionException("fill px " + f.px() + " outside limit " + s.order.px());
                long notional = Math.multiplyExact(f.qty(), f.px());
                long newCumNotional = Math.addExact(s.cumNotional, notional);   // 可能抛 ArithmeticException：在修改任何东西之前
                seenExecIds.add(f.execId());
                s.cumQty += f.qty();
                s.cumNotional = newCumNotional;
                reduceOpen(s, f.qty());
                if (s.cumQty == s.order.qty()) {
                    s.status = OrderStatus.FILLED;
                    openCount--;
                } else {
                    s.status = OrderStatus.PARTIALLY_FILLED;
                }
                yield true;
            }
            case ExecEvent.Cancel c -> {
                require(s.status == OrderStatus.WORKING || s.status == OrderStatus.PARTIALLY_FILLED, s, "Cancel");
                reduceOpen(s, s.leaves());
                s.status = OrderStatus.CANCELED;
                openCount--;
                yield true;
            }
            case ExecEvent.Reject r -> {
                require(s.status == OrderStatus.PENDING, s, "Reject");
                reduceOpen(s, s.leaves());
                s.status = OrderStatus.REJECTED;
                s.rejectReason = r.reason();
                openCount--;
                yield true;
            }
        };
    }

    public boolean contains(long orderId) { return orders.containsKey(orderId); }

    public OrderView get(long orderId) {
        State s = orders.get(orderId);
        if (s == null) throw new NoSuchElementException("unknown order " + orderId);
        return s.view();
    }

    /** 全部未终结订单，按 id 升序。 */
    public List<OrderView> open() {
        return orders.values().stream().filter(s -> s.status.isOpen()).map(State::view)
                .sorted(Comparator.comparingLong(v -> v.order().id())).toList();
    }

    /** 全部订单（含已终结），按 id 升序。 */
    public List<OrderView> all() {
        List<OrderView> out = new ArrayList<>(orders.size());
        for (State s : orders.values()) out.add(s.view());
        out.sort(Comparator.comparingLong(v -> v.order().id()));
        return out;
    }

    public int openCount() { return openCount; }

    /** 某标的某方向所有未终结订单的剩余数量之和（含 PENDING）。 */
    public long openLeaves(String symbol, Side side) {
        long[] a = openLeaves.get(symbol);
        return a == null ? 0 : a[slot(side)];
    }

    private void reduceOpen(State s, long qty) {
        openLeaves.get(s.order.symbol())[slot(s.order.side())] -= qty;
    }

    private static int slot(Side side) { return side == Side.BUY ? 0 : 1; }

    private static void require(boolean ok, State s, String what) {
        if (!ok) throw new IllegalTransitionException(what + " not allowed in " + s.status + " (order " + s.order.id() + ")");
    }
}
