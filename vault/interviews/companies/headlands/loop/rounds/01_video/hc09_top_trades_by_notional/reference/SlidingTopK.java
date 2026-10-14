import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;
import java.util.TreeSet;

/**
 * hc09 Part 3：流式 top-k ticker，滑动时间窗口 + 过期。
 *
 * <p>成交事件（{@link Fill}）按时间顺序到达（时间戳不降）。窗口长度 W：时间为 t 的成交在
 * 「当前时间 now」满足 {@code now - t < W} 时是<b>活的</b>，{@code now - t >= W} 时过期。
 * 也就是活跃区间是左开右闭 (now - W, now]。
 *
 * <p>为什么只用堆不行：堆（{@code PriorityQueue}）只能高效地取堆顶；一个 ticker 的总额会因为新成交变大、
 * 因为过期变小，也就是要「修改任意一个元素的键」，而堆找不到任意元素（{@code remove(Object)} 是 O(m)）。
 * 所以这里用 {@code TreeSet}（红黑树）按 (总额 降序, ticker 升序) 排好所有活跃 ticker：
 * 删除旧键、插入新键各 O(log m)，取前 k 名是 O(log m + k) 的顺序遍历。
 */
public final class SlidingTopK {

    // ---------------------------------------------------------------- 事件类型（封闭层级）

    public sealed interface Feed permits Fill, Tick, Ask {}

    /** 一笔成交。{@code time >= 0}；价格、数量非负；notional 乘法不能溢出（构造时检查）。 */
    public record Fill(long time, String ticker, long price, long volume) implements Feed {
        public Fill {
            if (time < 0) throw new IllegalArgumentException("negative time: " + time);
            Objects.requireNonNull(ticker, "ticker");
            if (price < 0) throw new IllegalArgumentException("negative price: " + price);
            if (volume < 0) throw new IllegalArgumentException("negative volume: " + volume);
            Math.multiplyExact(price, volume);
        }

        public long notional() {
            return price * volume;
        }
    }

    /** 只推进时钟（没有成交，但时间过去了，窗口里的旧成交要过期）。 */
    public record Tick(long time) implements Feed {}

    /** 在 time 这个时刻查询 top-k。 */
    public record Ask(long time) implements Feed {}

    /** 一次查询的答案。 */
    public record Answer(long time, List<TopTrades.TickerTotal> top) {}

    /** 一个 ticker 在窗口内的累计（可变，只在本类内部使用）。count 是它还有几笔活的成交。 */
    private static final class Acc {
        long total;
        int count;
    }

    // ---------------------------------------------------------------- 状态

    private final long window;
    private final int k;
    /** 活跃成交，按到达（=时间）顺序：队头最老，过期只会发生在队头（J09: peekFirst / removeFirst）。 */
    private final ArrayDeque<Fill> live = new ArrayDeque<>();
    private final HashMap<String, Acc> totals = new HashMap<>();
    /** 所有活跃 ticker 按 BEST_TICKER_FIRST 排好；与 totals 保持一一对应。 */
    private final TreeSet<TopTrades.TickerTotal> ranking = new TreeSet<>(TopTrades.BEST_TICKER_FIRST);
    private long now = 0;

    public SlidingTopK(long window, int k) {
        if (window < 1) throw new IllegalArgumentException("window must be >= 1: " + window);
        if (k < 0) throw new IllegalArgumentException("k must be >= 0: " + k);
        this.window = window;
        this.k = k;
    }

    // ---------------------------------------------------------------- 操作

    /** 加入一笔成交：先把时钟推到 f.time()（过期旧成交），再计入。时间倒退 → IAE。 */
    public void add(Fill f) {
        Objects.requireNonNull(f, "fill");
        advanceTo(f.time());
        var acc = totals.get(f.ticker());
        long oldTotal = acc == null ? 0 : acc.total;
        // 先算新总额：addExact 溢出就抛，此时还没有动任何结构，ticker 的状态保持原样。
        long newTotal = Math.addExact(oldTotal, f.notional());
        if (acc == null) {
            acc = new Acc();
            totals.put(f.ticker(), acc);
        } else {
            ranking.remove(new TopTrades.TickerTotal(f.ticker(), oldTotal)); // 删旧键
        }
        acc.total = newTotal;
        acc.count++;
        ranking.add(new TopTrades.TickerTotal(f.ticker(), newTotal)); // 插新键
        live.addLast(f);
    }

    /** 把时钟推进到 t（t 必须 >= 当前时间），过期所有 now - time >= window 的成交。 */
    public void advanceTo(long t) {
        if (t < now) throw new IllegalArgumentException("time went backwards: " + t + " < " + now);
        now = t;
        Fill f;
        while ((f = live.peekFirst()) != null && now - f.time() >= window) {
            live.removeFirst();
            var acc = totals.get(f.ticker());
            ranking.remove(new TopTrades.TickerTotal(f.ticker(), acc.total));
            acc.total -= f.notional();
            acc.count--;
            if (acc.count == 0) {
                totals.remove(f.ticker());
            } else {
                ranking.add(new TopTrades.TickerTotal(f.ticker(), acc.total));
            }
        }
    }

    /** 当前窗口内 top-k ticker，最好的在前。 */
    public List<TopTrades.TickerTotal> top() {
        return ranking.stream().limit(k).toList();
    }

    /** 某个 ticker 在窗口内的总 notional（没有活跃成交返回 0）。 */
    public long totalOf(String ticker) {
        var acc = totals.get(ticker);
        return acc == null ? 0 : acc.total;
    }

    public int liveEvents() {
        return live.size();
    }

    public int distinctTickers() {
        return totals.size();
    }

    public long now() {
        return now;
    }

    // ---------------------------------------------------------------- 回放

    /** 依次处理一串 Feed，收集每个 Ask 的答案。用 sealed + 模式匹配 switch 分派；少一个 case 编译就报错。 */
    public static List<Answer> replay(long window, int k, List<? extends Feed> feed) {
        var w = new SlidingTopK(window, k);
        var answers = new ArrayList<Answer>();
        for (Feed f : feed) {
            switch (f) {
                case Fill fill -> w.add(fill);
                case Tick(var t) when t == w.now() -> { } // 时钟没动：什么都不用做（守卫 when 的用法示例）
                case Tick(var t) -> w.advanceTo(t);
                case Ask(var t) -> {
                    w.advanceTo(t);
                    answers.add(new Answer(t, w.top()));
                }
            }
        }
        return List.copyOf(answers);
    }
}
