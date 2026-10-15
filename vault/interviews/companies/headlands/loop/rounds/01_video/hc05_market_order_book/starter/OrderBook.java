import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalLong;

/**
 * 单品种订单簿。题面见 ../problem.md。把每个 TODO 换成实现。
 * Part 1：add / cancel / modify / best / depth / queue（不撮合）· Part 2：execute（价格-时间优先撮合）+ parse / render / replay。
 *
 * 提示（Part 1）：买盘、卖盘各一个「价格 → 价位」的有序 Map（买盘用 Comparator.reverseOrder()，最优价永远在头部：
 * firstEntry / pollFirstEntry）；价位内部要 FIFO 且能 O(1) 按 id 删除（LinkedHashMap 即 SequencedMap：putLast / firstEntry）；
 * 再加一个 id → 订单 的 HashMap。
 */
public final class OrderBook {

    public enum Side {
        BUY, SELL;
        public Side opposite() { return this == BUY ? SELL : BUY; }
    }

    /** 一档价位的聚合：价格（tick）、总量、订单数。 */
    public record Level(long price, long totalQty, int orderCount) {}

    /** 一张挂单的快照。TODO：紧凑构造器里校验 id > 0、price > 0、qty > 0（抛 IllegalArgumentException，信息用下面的常量），side 非 null。 */
    public record Order(long id, Side side, long price, long qty) {}

    // ---------- Part 2 的类型（已给出） ----------

    public sealed interface Command permits Limit, Market, Cancel, Modify {
        long id();
    }
    public record Limit(long id, Side side, long price, long qty) implements Command {
        public Limit { Objects.requireNonNull(side, "side"); }
    }
    public record Market(long id, Side side, long qty) implements Command {
        public Market { Objects.requireNonNull(side, "side"); }
    }
    public record Cancel(long id) implements Command {}
    public record Modify(long id, long newQty) implements Command {}

    public sealed interface Event permits Trade, Rested, Cancelled, Modified, Rejected {}
    /** 成交价 = 被动方（maker，簿上的挂单）的价格。 */
    public record Trade(long takerId, long makerId, Side takerSide, long price, long qty) implements Event {}
    public record Rested(long id, Side side, long price, long qty) implements Event {}
    public record Cancelled(long id, long remaining) implements Event {}
    public record Modified(long id, long oldQty, long newQty) implements Event {}
    public record Rejected(long id, String reason) implements Event {}

    public static final String INVALID_ID = "invalid id";
    public static final String INVALID_PRICE = "invalid price";
    public static final String INVALID_QTY = "invalid quantity";
    public static final String DUPLICATE_ID = "duplicate id";
    public static final String UNKNOWN_ID = "unknown id";
    public static final String OVERFLOW = "overflow";

    // ---------- Part 1 ----------

    /** 挂单，不撮合。非法参数 / 重复 id 抛 IAE；同价位总量溢出抛 ArithmeticException（簿保持不变）。 */
    public void add(long id, Side side, long price, long qty) { throw new UnsupportedOperationException("TODO"); }

    public boolean cancel(long id) { throw new UnsupportedOperationException("TODO"); }

    /** 减量保持队列位置；增量丢失时间优先（移到队尾）。newQty ≤ 0 抛 IAE（即使 id 未知）；未知 id 返回 false。 */
    public boolean modify(long id, long newQty) { throw new UnsupportedOperationException("TODO"); }

    public OptionalLong bestBid() { throw new UnsupportedOperationException("TODO"); }
    public OptionalLong bestAsk() { throw new UnsupportedOperationException("TODO"); }

    /** 最优的 n 档（买盘价格降序，卖盘升序）；n < 0 抛 IAE。 */
    public List<Level> depth(Side side, int n) { throw new UnsupportedOperationException("TODO"); }

    public Optional<Order> find(long id) { throw new UnsupportedOperationException("TODO"); }

    /** 某价位的 FIFO 队列（队头在前）；没有该价位返回空表。 */
    public List<Long> queue(Side side, long price) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }

    // ---------- Part 2 ----------

    /**
     * 执行一条命令，返回事件。校验顺序 id → price → quantity → 簿状态，失败返回单个 Rejected（不改变簿）。
     * 提示：对 sealed Command 写 switch 模式匹配 + record 解构（case Limit(var id, var side, var px, var q) -> …），不要 default。
     */
    public List<Event> execute(Command cmd) { throw new UnsupportedOperationException("TODO"); }

    public List<Event> executeAll(List<? extends Command> cmds) { throw new UnsupportedOperationException("TODO"); }

    /** LIMIT id BUY|SELL price qty · MARKET id BUY|SELL qty · CANCEL id · MODIFY id newQty（大小写不敏感，空白任意）。格式错抛 IAE。 */
    public static Command parse(String line) { throw new UnsupportedOperationException("TODO"); }

    /** 事件 → 一行文本，格式见 problem.md。对 sealed Event 写穷尽 switch。 */
    public static String render(Event e) { throw new UnsupportedOperationException("TODO"); }

    /** 逐行执行脚本（空行与 # 开头的行跳过），返回渲染后的事件行。格式错抛 IAE，信息以 "line N" 开头（N 从 1 起）。 */
    public static List<String> replay(List<String> lines) { throw new UnsupportedOperationException("TODO"); }
}
