import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.Future;
import java.util.concurrent.RecursiveTask;
import java.util.concurrent.StructuredTaskScope;
import java.util.ArrayList;
import java.util.stream.IntStream;

/**
 * hc09 Part 4：把事件切成块（chunk），每块各自聚合成「ticker → 总 notional」，最后合并。
 *
 * <p>合并之所以正确，靠三条性质：
 * <ol>
 *   <li>整数加法满足<b>结合律和交换律</b>：怎么分块、按什么顺序合并，结果都一样（浮点数不满足，所以才用整数 tick）；</li>
 *   <li>每块的 Map 只被一个任务写，没有共享可变状态——不需要锁；</li>
 *   <li>所有 notional 非负，部分和单调不减：只要任何一块或任何一次合并溢出，真实总和就一定超过 Long.MAX_VALUE，
 *       所以「是否抛 ArithmeticException」也与分块方式无关。</li>
 * </ol>
 */
public final class ParallelNotional {
    private ParallelNotional() {}

    /** 顺序基线。 */
    public static Map<String, Long> totalsSequential(String[] tickers, long[] prices, long[] volumes) {
        int n = TopTrades.checkInputs(tickers, prices, volumes, 0);
        var m = new HashMap<String, Long>();
        accumulate(m, tickers, prices, volumes, 0, n);
        return m;
    }

    // ---------------------------------------------------------------- 方案 A：并行流

    /**
     * 并行流的三参数 collect：supplier 给每个线程一个<b>新</b>容器，accumulator 往容器里加，
     * combiner 把右边容器并进<b>左边</b>容器（BiConsumer 没有返回值，所以必须改第一个参数！）。
     */
    public static Map<String, Long> totalsParallelStream(String[] tickers, long[] prices, long[] volumes) {
        int n = TopTrades.checkInputs(tickers, prices, volumes, 0);
        return IntStream.range(0, n).parallel().collect(
                HashMap<String, Long>::new,
                (m, i) -> m.merge(tickers[i], TopTrades.notionalAt(tickers, prices, volumes, i), Math::addExact),
                (left, right) -> right.forEach((k, v) -> left.merge(k, v, Math::addExact)));
    }

    // ---------------------------------------------------------------- 方案 B：ForkJoin 递归切分

    /** 区间 [from, to) 不大于 threshold 就直接算，否则一分为二：一半 fork 出去，另一半自己算，最后 join 并合并。 */
    public static Map<String, Long> totalsForkJoin(String[] tickers, long[] prices, long[] volumes, int threshold) {
        int n = TopTrades.checkInputs(tickers, prices, volumes, 0);
        if (threshold < 1) throw new IllegalArgumentException("threshold must be >= 1: " + threshold);
        return ForkJoinPool.commonPool().invoke(new Sum(tickers, prices, volumes, 0, n, threshold));
    }

    private static final class Sum extends RecursiveTask<Map<String, Long>> {
        private final String[] tickers;
        private final long[] prices;
        private final long[] volumes;
        private final int from;
        private final int to;
        private final int threshold;

        Sum(String[] tickers, long[] prices, long[] volumes, int from, int to, int threshold) {
            this.tickers = tickers;
            this.prices = prices;
            this.volumes = volumes;
            this.from = from;
            this.to = to;
            this.threshold = threshold;
        }

        @Override
        protected Map<String, Long> compute() {
            if (to - from <= threshold) {
                var m = new HashMap<String, Long>();
                accumulate(m, tickers, prices, volumes, from, to);
                return m;
            }
            int mid = (from + to) >>> 1; // 无符号右移：from + to 即使接近 int 上限也不会变负
            var left = new Sum(tickers, prices, volumes, from, mid, threshold);
            var right = new Sum(tickers, prices, volumes, mid, to, threshold);
            left.fork();                       // 左半边交给工作队列（别的线程可以来偷）
            var r = right.compute();           // 右半边在当前线程直接算，不浪费这个线程
            var l = left.join();               // 等左半边（join 会帮忙干活，不是干等）
            return mergeInto(l, r);
        }
    }

    // ---------------------------------------------------------------- 方案 C：虚拟线程 + StructuredTaskScope

    /**
     * 切成 chunks 块，每块一个虚拟线程。ShutdownOnFailure：任何一块失败（比如溢出）→ scope 关闭 →
     * 其余块被中断（协作式：{@link #accumulate} 里会定期检查中断标志）→ join 返回 → 抛出<b>原始</b>异常。
     */
    public static Map<String, Long> totalsScoped(String[] tickers, long[] prices, long[] volumes, int chunks)
            throws InterruptedException {
        int n = TopTrades.checkInputs(tickers, prices, volumes, 0);
        if (chunks < 1) throw new IllegalArgumentException("chunks must be >= 1: " + chunks);
        try (var scope = new StructuredTaskScope.ShutdownOnFailure("totals", Thread.ofVirtual().factory())) {
            var subtasks = new ArrayList<StructuredTaskScope.Subtask<Map<String, Long>>>(chunks);
            for (int c = 0; c < chunks; c++) {
                final int from = boundary(n, chunks, c);
                final int to = boundary(n, chunks, c + 1);
                subtasks.add(scope.fork(() -> {
                    var m = new HashMap<String, Long>();
                    accumulate(m, tickers, prices, volumes, from, to);
                    return m;
                }));
            }
            scope.join();
            scope.throwIfFailed(e -> e instanceof RuntimeException re ? re : new IllegalStateException(e));
            // 到这里所有子任务都成功了。按块的顺序合并（顺序其实无所谓，但固定顺序便于调试）。
            Map<String, Long> acc = subtasks.getFirst().get();
            for (int c = 1; c < subtasks.size(); c++) acc = mergeInto(acc, subtasks.get(c).get());
            return acc;
        }
    }

    // ---------------------------------------------------------------- 方案 D：共享 ConcurrentHashMap（对照组）

    /**
     * 所有线程直接往同一个 ConcurrentHashMap 里 merge。正确（merge 对单个 key 是原子的，溢出抛异常时不记录），
     * 但热点 ticker 上所有线程抢同一个桶的锁，扩展性差；对照 A–C「各算各的，最后合并」。
     */
    public static Map<String, Long> totalsSharedMap(String[] tickers, long[] prices, long[] volumes, int chunks)
            throws InterruptedException {
        int n = TopTrades.checkInputs(tickers, prices, volumes, 0);
        if (chunks < 1) throw new IllegalArgumentException("chunks must be >= 1: " + chunks);
        var shared = new ConcurrentHashMap<String, Long>();
        try (var pool = Executors.newVirtualThreadPerTaskExecutor()) {
            var futures = new ArrayList<Future<?>>(chunks);
            for (int c = 0; c < chunks; c++) {
                final int from = boundary(n, chunks, c);
                final int to = boundary(n, chunks, c + 1);
                futures.add(pool.submit(() -> {
                    for (int i = from; i < to; i++) {
                        shared.merge(tickers[i], TopTrades.notionalAt(tickers, prices, volumes, i), Math::addExact);
                    }
                }));
            }
            for (var f : futures) {
                try {
                    f.get();
                } catch (ExecutionException e) {
                    // 还没完成的块不再关心：关闭 pool 时会等它们结束。把原始异常交给调用方。
                    if (e.getCause() instanceof RuntimeException re) throw re;
                    throw new IllegalStateException(e.getCause());
                }
            }
        }
        return new HashMap<>(shared);
    }

    // ---------------------------------------------------------------- 组合：并行汇总 + 堆取 top-k

    public static List<TopTrades.TickerTotal> topTickersParallel(
            String[] tickers, long[] prices, long[] volumes, int k, int chunks) throws InterruptedException {
        if (k < 0) throw new IllegalArgumentException("k must be >= 0: " + k);
        return TopTrades.topOf(totalsScoped(tickers, prices, volumes, chunks), k);
    }

    // ---------------------------------------------------------------- 工具

    /** 把 [from, to) 的事件累加进 m。每 4096 个事件看一眼中断标志：协作式取消。 */
    static void accumulate(Map<String, Long> m, String[] tickers, long[] prices, long[] volumes, int from, int to) {
        for (int i = from; i < to; i++) {
            if ((i & 0xFFF) == 0 && Thread.currentThread().isInterrupted()) throw new CancellationException("chunk cancelled");
            m.merge(tickers[i], TopTrades.notionalAt(tickers, prices, volumes, i), Math::addExact);
        }
    }

    /** 把两张表合并成一张：小的并进大的（少做 merge）。两张表都归调用方所有，调用后不要再使用它们。 */
    static Map<String, Long> mergeInto(Map<String, Long> a, Map<String, Long> b) {
        if (a.size() < b.size()) {
            var t = a;
            a = b;
            b = t;
        }
        for (var e : b.entrySet()) a.merge(e.getKey(), e.getValue(), Math::addExact);
        return a;
    }

    /** 第 c 块的起点：n * c / chunks（用 long 乘，避免 n * c 溢出 int）。 */
    static int boundary(int n, int chunks, int c) {
        return (int) ((long) n * c / chunks);
    }
}
