import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Objects;
import java.util.OptionalLong;
import java.util.PriorityQueue;

/**
 * hc14 Part 2 + 3：滑动时间窗口上的 VWAP 与 top-k。
 *
 * <p>成交按时间戳不降的顺序到达。成交在时刻 now 是「活的」当且仅当 now - tsMs &lt; windowMs（窗口是左开右闭 (now-W, now]）。
 * 一个全局 FIFO 队列记着所有活的成交；每个 symbol 一份累计值（笔数 / 数量 / 名义金额）。每笔成交最多进队一次、出队一次，
 * 所以 onTrade 和 vwap 摊还 O(1)。
 */
public final class RollingVwap {
    /** Part 3 的结果行。 */
    public record SymbolNotional(String symbol, long notional) {}

    private static final class Acc {
        long count, volume, notional;
    }

    private final long window;
    private final ArrayDeque<TradeLog.Trade> live = new ArrayDeque<>();
    private final HashMap<String, Acc> bySymbol = new HashMap<>();
    private long now;

    /** windowMs ≥ 1，否则 IAE。 */
    public RollingVwap(long windowMs) {
        if (windowMs < 1) throw new IllegalArgumentException("window must be >= 1: " + windowMs);
        this.window = windowMs;
    }

    /** 时钟推进到 t（t 小于当前时钟 → IAE），并让所有 now - ts >= window 的成交过期。 */
    private void advance(long t) {
        if (t < now) throw new IllegalArgumentException("time went backwards: " + t + " < " + now);
        now = t;
        while (!live.isEmpty() && now - live.getFirst().tsMs() >= window) {
            var old = live.removeFirst();
            var a = bySymbol.get(old.symbol());
            a.count--;
            a.volume -= old.qty();
            a.notional -= old.notional();
            if (a.count == 0) bySymbol.remove(old.symbol());
        }
    }

    /**
     * 一笔成交到达：先把时钟推到 t.tsMs()（早于当前时钟 → IAE），再计入。null → NPE。
     * 该 symbol 的数量或名义金额累计溢出 long → ArithmeticException，这笔不计入（时钟已推进、过期的已清掉）。
     */
    public void onTrade(TradeLog.Trade t) {
        Objects.requireNonNull(t, "trade");
        advance(t.tsMs());
        var a = bySymbol.get(t.symbol());
        long volume = Math.addExact(a == null ? 0 : a.volume, t.qty());
        long notional = Math.addExact(a == null ? 0 : a.notional, t.notional());
        if (a == null) bySymbol.put(t.symbol(), a = new Acc());
        a.count++;
        a.volume = volume;
        a.notional = notional;
        live.addLast(t);
    }

    /** 时刻 nowMs 窗口内该 symbol 的 VWAP（定点，半数向上）；窗口里没有它 → empty。会推进时钟；nowMs 小于当前时钟 → IAE。 */
    public OptionalLong vwap(String symbol, long nowMs) {
        Objects.requireNonNull(symbol, "symbol");
        advance(nowMs);
        var a = bySymbol.get(symbol);
        return a == null ? OptionalLong.empty() : OptionalLong.of(TradeLog.vwap(a.notional, a.volume));
    }

    /** 当前（最近一次推进后的）窗口里该 symbol 的数量；没有 → 0。不推进时钟。 */
    public long volume(String symbol) {
        var a = bySymbol.get(symbol);
        return a == null ? 0 : a.volume;
    }

    /** 同上，名义金额。 */
    public long notional(String symbol) {
        var a = bySymbol.get(symbol);
        return a == null ? 0 : a.notional;
    }

    public int liveTrades() {
        return live.size();
    }

    public int liveSymbols() {
        return bySymbol.size();
    }

    /** 当前时钟；还没有任何事件时为 0。 */
    public long now() {
        return now;
    }

    private static final Comparator<SymbolNotional> BEST_FIRST =
            Comparator.comparingLong(SymbolNotional::notional).reversed().thenComparing(SymbolNotional::symbol);

    /**
     * Part 3：时刻 nowMs 窗口内名义金额最大的 k 个 symbol，金额降序、同额 symbol 升序。会推进时钟。
     * k &lt; 0 → IAE（先于时钟检查）；k = 0 → 空；k 大于 symbol 数 → 全部。
     */
    public List<SymbolNotional> topK(int k, long nowMs) {
        if (k < 0) throw new IllegalArgumentException("k must be >= 0: " + k);
        advance(nowMs);
        if (k == 0) return List.of();
        var heap = new PriorityQueue<SymbolNotional>(k + 1, BEST_FIRST.reversed()); // 堆顶 = 保留集合里最差的
        for (var e : bySymbol.entrySet()) {
            var cand = new SymbolNotional(e.getKey(), e.getValue().notional);
            if (heap.size() < k) heap.add(cand);
            else if (BEST_FIRST.compare(cand, heap.peek()) < 0) {
                heap.poll();
                heap.add(cand);
            }
        }
        var out = new ArrayList<>(heap);
        out.sort(BEST_FIRST);
        return Collections.unmodifiableList(out);
    }
}
