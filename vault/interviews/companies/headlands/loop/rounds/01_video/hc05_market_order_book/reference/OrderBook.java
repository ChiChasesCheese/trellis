import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalLong;
import java.util.SequencedMap;

/**
 * 单品种订单簿。Part 1：维护（add / cancel / modify / best / depth，不撮合）；
 * Part 2：价格-时间优先撮合，产出 sealed 事件流。题面见 ../problem.md。
 */
public final class OrderBook {

    public enum Side {
        BUY, SELL;
        public Side opposite() { return this == BUY ? SELL : BUY; }
    }

    /** 一档价位的聚合：价格（tick）、总量、订单数。 */
    public record Level(long price, long totalQty, int orderCount) {}

    /** 一张挂单的快照。紧凑构造器把「合法订单」写进类型。 */
    public record Order(long id, Side side, long price, long qty) {
        public Order {
            Objects.requireNonNull(side, "side");
            if (id <= 0) throw new IllegalArgumentException(INVALID_ID);
            if (price <= 0) throw new IllegalArgumentException(INVALID_PRICE);
            if (qty <= 0) throw new IllegalArgumentException(INVALID_QTY);
        }
    }

    // ---------- Part 2 的类型 ----------

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

    // ---------- 内部结构 ----------

    private static final class Node {
        final long id;
        final Side side;
        final long price;
        long qty;
        Node(long id, Side side, long price, long qty) { this.id = id; this.side = side; this.price = price; this.qty = qty; }
    }

    /** 一档价位：FIFO 队列（total 是缓存：depth() 不用每次把队列加一遍）（LinkedHashMap：O(1) 按 id 删除，又保序）+ 总量缓存。 */
    private static final class PriceLevel {
        final SequencedMap<Long, Node> fifo = new LinkedHashMap<>();
        long total;
    }

    // 为什么这样组织（详见 study/30-articles/hc05_market_order_book.md）：
    //  * 「最优价」= 买盘最高价 / 卖盘最低价，且成交会把最优价那一档吃光，所以需要「按价格有序、能反复取最小」的结构 → 红黑树 TreeMap，
    //    取最优价 O(log L)（L = 价位数），HashMap 做不到（无序）。
    //  * 同一价位按到达顺序排队（时间优先）→ 队列；但撤单要从队伍中间拿掉，ArrayDeque 做不到 O(1) →
    //    LinkedHashMap<id, Node>：哈希表（O(1) 按 id 找）+ 双向链表（保序，O(1) 删除）。
    //  * byId：撤单 / 改量只给 id，不给价格；没有这张表就得扫遍所有价位（O(n)）。
    // TreeMap 在 Java 21 里是 SequencedMap：firstEntry / pollFirstEntry 就是「最优价」。买盘用 reverseOrder，最优价永远在头部。
    private final SequencedMap<Long, PriceLevel> bids = new java.util.TreeMap<>(Comparator.reverseOrder());
    private final SequencedMap<Long, PriceLevel> asks = new java.util.TreeMap<>();
    private final HashMap<Long, Node> byId = new HashMap<>();

    private SequencedMap<Long, PriceLevel> book(Side s) { return s == Side.BUY ? bids : asks; }

    // ---------- Part 1 ----------

    /** 挂单，不撮合（簿可以被挂成交叉状态）。非法参数 / 重复 id 抛 IAE；同价位总量溢出抛 ArithmeticException（簿不变）。 */
    public void add(long id, Side side, long price, long qty) {
        new Order(id, side, price, qty); // 复用 record 的校验
        if (byId.containsKey(id)) throw new IllegalArgumentException(DUPLICATE_ID);
        rest(id, side, price, qty);
    }

    private void rest(long id, Side side, long price, long qty) {
        var book = book(side);
        var level = book.get(price);
        // 先算后改：addExact 抛异常时下面还没有任何修改，簿保持原样（异常安全 / 强保证）。
        long newTotal = Math.addExact(level == null ? 0L : level.total, qty);
        if (level == null) {
            level = new PriceLevel();
            book.put(price, level);
        }
        var node = new Node(id, side, price, qty);
        level.fifo.putLast(id, node);
        level.total = newTotal;
        byId.put(id, node);
    }

    private void remove(Node n) {
        var book = book(n.side);
        var level = book.get(n.price);
        level.fifo.remove(n.id);
        level.total -= n.qty;
        if (level.fifo.isEmpty()) book.remove(n.price);
        byId.remove(n.id);
    }

    public boolean cancel(long id) {
        var n = byId.get(id);
        if (n == null) return false;
        remove(n);
        return true;
    }

    /** 改量。减量保持队列位置；增量丢失时间优先（移到队尾）。newQty ≤ 0 抛 IAE；未知 id 返回 false。 */
    public boolean modify(long id, long newQty) {
        if (newQty <= 0) throw new IllegalArgumentException(INVALID_QTY);
        var n = byId.get(id);
        if (n == null) return false;
        var level = book(n.side).get(n.price);
        if (newQty > n.qty) {
            long newTotal = Math.addExact(level.total, newQty - n.qty);
            n.qty = newQty;
            level.total = newTotal;
            // 时间优先的规矩：加量等于「重新排队」。LinkedHashMap 对已存在的 key 做 putLast 会把它移到链表末尾（Java 21 的 SequencedMap 方法）。
            // 减量不动位置：交易所的规矩是「只有让你更吃亏的修改才丢优先级」，这里照做。
            level.fifo.putLast(id, n);
        } else {
            level.total -= n.qty - newQty;
            n.qty = newQty;
        }
        return true;
    }

    public OptionalLong bestBid() { return best(bids); }
    public OptionalLong bestAsk() { return best(asks); }

    private static OptionalLong best(SequencedMap<Long, PriceLevel> book) {
        var e = book.firstEntry();
        return e == null ? OptionalLong.empty() : OptionalLong.of(e.getKey());
    }

    /** 最优的 n 档（买盘价格降序，卖盘升序）。 */
    public List<Level> depth(Side side, int n) {
        if (n < 0) throw new IllegalArgumentException("n < 0");
        return book(side).entrySet().stream().limit(n)
                .map(e -> new Level(e.getKey(), e.getValue().total, e.getValue().fifo.size()))
                .toList();
    }

    public Optional<Order> find(long id) {
        var n = byId.get(id);
        return n == null ? Optional.empty() : Optional.of(new Order(n.id, n.side, n.price, n.qty));
    }

    /** 某价位的 FIFO 队列（队头在前）；没有该价位返回空表。 */
    public List<Long> queue(Side side, long price) {
        var level = book(side).get(price);
        return level == null ? List.of() : List.copyOf(level.fifo.keySet());
    }

    public int size() { return byId.size(); }

    // ---------- Part 2 ----------

    public List<Event> execute(Command cmd) {
        Objects.requireNonNull(cmd, "cmd");
        var bad = validate(cmd);
        if (bad != null) return List.of(new Rejected(cmd.id(), bad));
        return switch (cmd) {
            case Limit(var id, var side, var px, var q) -> {
                if (ownLevelWouldOverflow(side, px, q)) yield List.of(new Rejected(id, OVERFLOW));
                var events = new ArrayList<Event>();
                long left = sweep(id, side, px, q, events);
                if (left > 0) {
                    rest(id, side, px, left);
                    events.add(new Rested(id, side, px, left));
                }
                yield events;
            }
            case Market(var id, var side, var q) -> {
                var events = new ArrayList<Event>();
                long left = sweep(id, side, side == Side.BUY ? Long.MAX_VALUE : 0L, q, events);
                if (left > 0) events.add(new Cancelled(id, left)); // IOC：吃不完的部分作废
                yield events;
            }
            case Cancel(var id) -> {
                var n = byId.get(id);
                long left = n.qty;
                remove(n);
                yield List.of(new Cancelled(id, left));
            }
            case Modify(var id, var newQty) -> {
                long old = byId.get(id).qty;
                try {
                    modify(id, newQty);
                } catch (ArithmeticException e) {
                    yield List.of(new Rejected(id, OVERFLOW));
                }
                yield List.of(new Modified(id, old, newQty));
            }
        };
    }

    public List<Event> executeAll(List<? extends Command> cmds) {
        var out = new ArrayList<Event>();
        for (var c : cmds) out.addAll(execute(c));
        return out;
    }

    /**
     * 校验顺序：id → price → quantity → 簿状态。返回 null 表示通过。
     * 写成 switch + when 守卫：从上到下第一个匹配的分支生效，所以「更具体的错误」写在前面；
     * 最后两行没有守卫，让编译器检查 sealed 层级被穷尽了（以后新增 Command 子类，这里编译不过，不会漏校验）。
     */
    private String validate(Command cmd) {
        return switch (cmd) {
            case Limit l when l.id() <= 0 -> INVALID_ID;
            case Limit l when l.price() <= 0 -> INVALID_PRICE;
            case Limit l when l.qty() <= 0 -> INVALID_QTY;
            case Market m when m.id() <= 0 -> INVALID_ID;
            case Market m when m.qty() <= 0 -> INVALID_QTY;
            case Cancel c when c.id() <= 0 -> INVALID_ID;
            case Modify m when m.id() <= 0 -> INVALID_ID;
            case Modify m when m.newQty() <= 0 -> INVALID_QTY;
            case Limit _, Market _ -> byId.containsKey(cmd.id()) ? DUPLICATE_ID : null;
            case Cancel _, Modify _ -> byId.containsKey(cmd.id()) ? null : UNKNOWN_ID;
        };
    }

    /**
     * 保守检查：挂单后同价位总量会溢出就整单拒绝。必须在撮合之前做——否则先成交了一半、
     * 挂剩余部分时才发现溢出，已经发出去的成交收不回来（要的是「整单要么全做要么不做」）。
     */
    private boolean ownLevelWouldOverflow(Side side, long price, long qty) {
        var level = book(side).get(price);
        return level != null && level.total > Long.MAX_VALUE - qty;
    }

    /**
     * 吃对手盘直到吃完或不再交叉；返回剩余量。
     * 为什么成交价取 maker（簿上先到的订单）的价格：maker 当初报的价是它愿意成交的最差价，taker 的限价只是上限；
     * 取 maker 价让 taker 拿到「价格改善」，这是几乎所有交易所的规则。
     * 市价单 = 限价设成无穷（买 Long.MAX_VALUE、卖 0），复用同一个循环。
     */
    private long sweep(long takerId, Side side, long limit, long qty, List<Event> out) {
        var opp = book(side.opposite());
        long left = qty;
        while (left > 0) {
            var top = opp.firstEntry();
            if (top == null) break;
            long px = top.getKey();
            boolean crosses = side == Side.BUY ? px <= limit : px >= limit;
            if (!crosses) break;
            var level = top.getValue();
            var maker = level.fifo.firstEntry().getValue();
            long fill = Math.min(left, maker.qty);
            out.add(new Trade(takerId, maker.id, side, px, fill));
            left -= fill;
            maker.qty -= fill;
            level.total -= fill;
            if (maker.qty == 0) {
                level.fifo.pollFirstEntry();
                byId.remove(maker.id);
                if (level.fifo.isEmpty()) opp.pollFirstEntry();
            }
        }
        return left;
    }

    // ---------- 文本接口 ----------

    /** LIMIT id BUY|SELL price qty · MARKET id BUY|SELL qty · CANCEL id · MODIFY id newQty（大小写不敏感）。 */
    public static Command parse(String line) {
        var t = Objects.requireNonNull(line, "line").strip().split("\\s+");
        if (t.length == 0 || t[0].isEmpty()) throw new IllegalArgumentException("empty command");
        try {
            return switch (t[0].toUpperCase(Locale.ROOT)) {
                case "LIMIT" -> {
                    needArgs(t, 5);
                    yield new Limit(Long.parseLong(t[1]), side(t[2]), Long.parseLong(t[3]), Long.parseLong(t[4]));
                }
                case "MARKET" -> {
                    needArgs(t, 4);
                    yield new Market(Long.parseLong(t[1]), side(t[2]), Long.parseLong(t[3]));
                }
                case "CANCEL" -> {
                    needArgs(t, 2);
                    yield new Cancel(Long.parseLong(t[1]));
                }
                case "MODIFY" -> {
                    needArgs(t, 3);
                    yield new Modify(Long.parseLong(t[1]), Long.parseLong(t[2]));
                }
                default -> throw new IllegalArgumentException("unknown command: " + t[0]);
            };
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("bad number in: " + line.strip());
        }
    }

    private static void needArgs(String[] t, int n) {
        if (t.length != n) throw new IllegalArgumentException(t[0] + " expects " + (n - 1) + " arguments");
    }

    private static Side side(String s) {
        return switch (s.toUpperCase(Locale.ROOT)) {
            case "BUY" -> Side.BUY;
            case "SELL" -> Side.SELL;
            default -> throw new IllegalArgumentException("bad side: " + s);
        };
    }

    /** 事件 → 一行文本。 */
    public static String render(Event e) {
        return switch (e) {
            case Trade(var taker, var maker, var side, var px, var q) ->
                    "TRADE taker=%d maker=%d side=%s px=%d qty=%d".formatted(taker, maker, side, px, q);
            case Rested(var id, var side, var px, var q) -> "REST id=%d side=%s px=%d qty=%d".formatted(id, side, px, q);
            case Cancelled(var id, var left) -> "CANCEL id=%d remaining=%d".formatted(id, left);
            case Modified(var id, var oldQty, var newQty) -> "MODIFY id=%d old=%d new=%d".formatted(id, oldQty, newQty);
            case Rejected(var id, var why) -> "REJECT id=%d reason=%s".formatted(id, why);
        };
    }

    /** 逐行执行脚本（空行与 # 开头的行跳过），返回渲染后的事件行。格式错抛 IAE，信息带行号（从 1 起）。 */
    public static List<String> replay(List<String> lines) {
        var book = new OrderBook();
        var out = new ArrayList<String>();
        for (int i = 0; i < lines.size(); i++) {
            var line = lines.get(i).strip();
            if (line.isEmpty() || line.startsWith("#")) continue;
            Command cmd;
            try {
                cmd = parse(line);
            } catch (IllegalArgumentException e) {
                throw new IllegalArgumentException("line " + (i + 1) + ": " + e.getMessage());
            }
            for (var ev : book.execute(cmd)) out.add(render(ev));
        }
        return out;
    }
}
