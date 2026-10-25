import java.util.List;
import java.util.OptionalLong;

/**
 * hc14 Part 2 + 3（starter）：滑动时间窗口上的 VWAP 与 top-k。
 *
 * <p>成交按时间戳不降的顺序到达。成交在时刻 now 是「活的」当且仅当 now - tsMs &lt; windowMs（窗口 (now-W, now]）。
 * 提示：一个全局 FIFO 队列（活的成交，队头最老）+ 每个 symbol 一份累计值；每笔成交最多进队一次出队一次，所以摊还 O(1)。
 */
public final class RollingVwap {
    /** Part 3 的结果行。 */
    public record SymbolNotional(String symbol, long notional) {}

    // 在这里加你的字段（活的成交队列、symbol → 累计值、当前时钟）

    /** windowMs ≥ 1，否则 IAE。 */
    public RollingVwap(long windowMs) {
        throw new UnsupportedOperationException("TODO");
    }

    /**
     * 一笔成交到达：先把时钟推到 t.tsMs()（早于当前时钟 → IAE），让过期的成交出队，再计入。null → NPE。
     * 该 symbol 的数量或名义金额累计溢出 long → ArithmeticException，这笔不计入（时钟已推进、过期的已清掉）。
     */
    public void onTrade(TradeLog.Trade t) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 时刻 nowMs 窗口内该 symbol 的 VWAP（定点，半数向上）；窗口里没有它 → empty。会推进时钟；nowMs 小于当前时钟 → IAE。 */
    public OptionalLong vwap(String symbol, long nowMs) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 当前（最近一次推进后的）窗口里该 symbol 的数量 / 名义金额；没有 → 0。不推进时钟。 */
    public long volume(String symbol) {
        throw new UnsupportedOperationException("TODO");
    }

    public long notional(String symbol) {
        throw new UnsupportedOperationException("TODO");
    }

    public int liveTrades() {
        throw new UnsupportedOperationException("TODO");
    }

    public int liveSymbols() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 当前时钟；还没有任何事件时为 0。 */
    public long now() {
        throw new UnsupportedOperationException("TODO");
    }

    /**
     * Part 3：时刻 nowMs 窗口内名义金额最大的 k 个 symbol，金额降序、同额 symbol 升序。会推进时钟。
     * k &lt; 0 → IAE（先于时钟检查）；k = 0 → 空；k 大于 symbol 数 → 全部。
     */
    public List<SymbolNotional> topK(int k, long nowMs) {
        throw new UnsupportedOperationException("TODO");
    }
}
