import java.util.List;
import java.util.Objects;

/**
 * hc09 Part 3（starter）：流式 top-k ticker，滑动时间窗口 + 过期。
 *
 * <p>成交（Fill）按时间顺序到达（时间戳不降）。窗口长度 W：now - time < W 时成交是活的，>= W 时过期。
 * 提示：为什么只用堆不行？一个 ticker 的总额会变大也会变小——要「改任意元素的键」。试试 TreeSet + HashMap + ArrayDeque。
 */
public final class SlidingTopK {

    public sealed interface Feed permits Fill, Tick, Ask {}

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

    /** 只推进时钟。 */
    public record Tick(long time) implements Feed {}

    /** 在 time 这个时刻查询 top-k。 */
    public record Ask(long time) implements Feed {}

    public record Answer(long time, List<TopTrades.TickerTotal> top) {}

    // 在这里加你的字段（活跃成交队列、ticker → 累计、排名结构、当前时间）

    /** window >= 1，k >= 0，否则 IAE。 */
    public SlidingTopK(long window, int k) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 加入一笔成交：先把时钟推到 f.time()，再计入；加总额溢出 → ArithmeticException 且状态不变。 */
    public void add(Fill f) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 时钟推进到 t（t < now → IAE），过期所有 now - time >= window 的成交。 */
    public void advanceTo(long t) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 当前窗口内 top-k ticker，最好的在前（总额降序、ticker 升序）。 */
    public List<TopTrades.TickerTotal> top() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 某 ticker 在窗口内的总 notional（没有活跃成交返回 0）。 */
    public long totalOf(String ticker) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 窗口内活跃的成交笔数。 */
    public int liveEvents() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 窗口内出现过的不同 ticker 数。 */
    public int distinctTickers() {
        throw new UnsupportedOperationException("TODO");
    }

    public long now() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 依次处理一串 Feed，收集每个 Ask 的答案。用 sealed + 模式匹配 switch。 */
    public static List<Answer> replay(long window, int k, List<? extends Feed> feed) {
        throw new UnsupportedOperationException("TODO");
    }
}
