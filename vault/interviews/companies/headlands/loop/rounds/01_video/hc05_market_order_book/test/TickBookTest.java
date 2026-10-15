import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.management.ManagementFactory;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 4：不装箱、定长内存的热路径版本。 */
class TickBookTest {
    private static final OrderBook.Side BUY = OrderBook.Side.BUY;
    private static final OrderBook.Side SELL = OrderBook.Side.SELL;

    /** 记录成交，供对拍。 */
    private static final class Tape implements TickBook.TradeSink {
        final List<long[]> trades = new ArrayList<>();
        @Override public void onTrade(long takerId, long makerId, long price, long qty) {
            trades.add(new long[] {takerId, makerId, price, qty});
        }
        List<List<Long>> asLists() { return trades.stream().map(t -> List.of(t[0], t[1], t[2], t[3])).toList(); }
    }

    /** 什么都不分配的 sink。 */
    private static final class Counter implements TickBook.TradeSink {
        long count, qty;
        @Override public void onTrade(long takerId, long makerId, long price, long q) { count++; qty += q; }
    }

    @Test @Tag("part4")
    void restsAndReportsBestAndLevelQuantity() {
        var b = new TickBook(1_000, 16);
        var t = new Tape();
        assertEquals(TickBook.NONE, b.bestBid());
        assertEquals(TickBook.NONE, b.bestAsk());
        assertEquals(5, b.limit(1, BUY, 100, 5, t));
        assertEquals(3, b.limit(2, BUY, 100, 3, t));
        assertEquals(2, b.limit(3, BUY, 98, 2, t));
        assertEquals(4, b.limit(4, SELL, 105, 4, t));
        assertEquals(100, b.bestBid());
        assertEquals(105, b.bestAsk());
        assertEquals(8, b.qtyAt(BUY, 100));
        assertEquals(0, b.qtyAt(BUY, 101));
        assertEquals(0, b.qtyAt(SELL, 5_000)); // 价格带外：0，不抛
        assertEquals(4, b.liveOrders());
        assertTrue(t.trades.isEmpty());
    }

    @Test @Tag("part4")
    void matchesWithPriceTimePriorityLikeTheEventBook() {
        var b = new TickBook(1_000, 16);
        var t = new Tape();
        b.limit(1, SELL, 101, 5, t);
        b.limit(2, SELL, 101, 3, t);
        b.limit(3, SELL, 102, 4, t);
        assertEquals(0, b.limit(4, BUY, 101, 6, t));
        assertEquals(4, b.limit(5, BUY, 103, 10, t)); // 吃掉 2 + 4，剩 4 挂簿
        assertEquals(List.of(List.of(4L, 1L, 101L, 5L), List.of(4L, 2L, 101L, 1L), List.of(5L, 2L, 101L, 2L),
                List.of(5L, 3L, 102L, 4L)), t.asLists());
        assertEquals(103, b.bestBid());
        assertEquals(TickBook.NONE, b.bestAsk());
        assertEquals(1, b.liveOrders());
    }

    @Test @Tag("part4")
    void cancelFindsNextBestAcrossEmptyWords() {
        var b = new TickBook(100_000, 16);
        var t = new Tape();
        b.limit(1, BUY, 10, 1, t);
        b.limit(2, BUY, 90_000, 1, t);
        b.limit(3, SELL, 99_999, 1, t);
        b.limit(4, SELL, 95_000, 1, t);
        assertEquals(90_000, b.bestBid());
        assertEquals(95_000, b.bestAsk());
        assertTrue(b.cancel(2));
        assertEquals(10, b.bestBid()); // 跨过一万多个空价位
        assertTrue(b.cancel(4));
        assertEquals(99_999, b.bestAsk());
        assertTrue(b.cancel(1));
        assertTrue(b.cancel(3));
        assertEquals(TickBook.NONE, b.bestBid());
        assertEquals(TickBook.NONE, b.bestAsk());
        assertFalse(b.cancel(1));
        assertEquals(0, b.liveOrders());
    }

    @Test @Tag("part4") @Tag("edge")
    void rejectsInvalidAndDuplicate() {
        var b = new TickBook(1_000, 4);
        var t = new Tape();
        assertEquals(TickBook.REJECTED, b.limit(0, BUY, 100, 1, t));
        assertEquals(TickBook.REJECTED, b.limit(-1, BUY, 100, 1, t));
        assertEquals(TickBook.REJECTED, b.limit(1, BUY, 0, 1, t));
        assertEquals(TickBook.REJECTED, b.limit(1, BUY, 1_000, 1, t)); // 上界是开区间
        assertEquals(TickBook.REJECTED, b.limit(1, BUY, Long.MAX_VALUE, 1, t));
        assertEquals(TickBook.REJECTED, b.limit(1, BUY, 100, 0, t));
        assertEquals(TickBook.REJECTED, b.limit(1, BUY, 100, TickBook.MAX_QTY + 1, t));
        assertEquals(TickBook.MAX_QTY, b.limit(1, BUY, 100, TickBook.MAX_QTY, t));
        assertEquals(TickBook.REJECTED, b.limit(1, SELL, 500, 1, t));
        assertEquals(999, b.limit(2, SELL, 999, 999, t)); // 价格带最高一档合法
        assertEquals(2, b.liveOrders());
    }

    @Test @Tag("part4") @Tag("edge")
    void poolFullBackPressuresAndRecovers() {
        var b = new TickBook(1_000, 3);
        var t = new Tape();
        assertEquals(1, b.limit(1, BUY, 10, 1, t));
        assertEquals(1, b.limit(2, BUY, 11, 1, t));
        assertEquals(1, b.limit(3, BUY, 12, 1, t));
        assertEquals(TickBook.FULL, b.limit(4, SELL, 500, 1, t));
        assertEquals(TickBook.FULL, b.limit(5, SELL, 5, 1, t)); // 满了就不撮合
        assertTrue(t.trades.isEmpty());
        assertTrue(b.cancel(2));
        assertEquals(0, b.limit(6, SELL, 5, 2, t)); // 吃掉 12 和 10，无剩余
        assertEquals(2, t.trades.size());
        assertEquals(0, b.liveOrders());
        for (long id = 10; id < 13; id++) assertEquals(1, b.limit(id, BUY, 7, 1, t)); // 槽位被回收
    }

    @Test @Tag("part4") @Tag("edge")
    void idTableSurvivesHeavyChurn() {
        var rnd = new Random(0);
        var b = new TickBook(10_000, 1_024);
        var t = new Tape();
        var live = new HashSet<Long>();
        long nextId = 1;
        for (int i = 0; i < 300_000; i++) {
            if (live.size() < 1_000 && rnd.nextInt(100) < 55) {
                long id = nextId++ * 4096; // 步长 4096：挑战哈希
                assertEquals(1, b.limit(id, BUY, 1 + rnd.nextInt(100), 1, t)); // 只挂买单，不会成交
                live.add(id);
            } else if (!live.isEmpty()) {
                long id = (rnd.nextBoolean() && nextId > 1) ? (1 + rnd.nextInt((int) nextId - 1)) * 4096L : live.iterator().next();
                assertEquals(live.remove(id), b.cancel(id));
            }
            assertEquals(live.size(), b.liveOrders());
        }
    }

    /** 对拍：同一串随机命令喂给 Part 2 的 OrderBook 和 Part 4 的 TickBook，成交序列、最优价、每档数量必须逐步一致。 */
    @Test @Tag("part4") @Tag("edge")
    void differentialAgainstEventBook() {
        var rnd = new Random(0);
        var ref = new OrderBook();
        var fast = new TickBook(200, 100_000);
        long nextId = 1;
        for (int step = 0; step < 50_000; step++) {
            if (rnd.nextInt(10) < 7) {
                var side = rnd.nextBoolean() ? BUY : SELL;
                long px = 90 + rnd.nextInt(21), q = 1 + rnd.nextInt(10), id = nextId++;
                var tape = new Tape();
                long rest = fast.limit(id, side, px, q, tape);
                var expect = new ArrayList<List<Long>>();
                long expectRest = 0;
                for (var e : ref.execute(new OrderBook.Limit(id, side, px, q))) {
                    if (e instanceof OrderBook.Trade tr) expect.add(List.of(tr.takerId(), tr.makerId(), tr.price(), tr.qty()));
                    if (e instanceof OrderBook.Rested r) expectRest = r.qty();
                }
                assertEquals(expect, tape.asLists(), "trades at step " + step);
                assertEquals(expectRest, rest, "rest at step " + step);
            } else {
                long id = 1 + rnd.nextInt((int) nextId);
                var evs = ref.execute(new OrderBook.Cancel(id));
                assertEquals(evs.getFirst() instanceof OrderBook.Cancelled, fast.cancel(id), "cancel at step " + step);
            }
            assertEquals(ref.bestBid().orElse(TickBook.NONE), fast.bestBid(), "bid at step " + step);
            assertEquals(ref.bestAsk().orElse(TickBook.NONE), fast.bestAsk(), "ask at step " + step);
            assertEquals(ref.size(), fast.liveOrders());
        }
        for (var s : OrderBook.Side.values()) {
            for (var lvl : ref.depth(s, Integer.MAX_VALUE)) assertEquals(lvl.totalQty(), fast.qtyAt(s, lvl.price()));
        }
    }

    // ---- perf：吞吐 + 分配 ----

    /** 预生成 op：type 0 = limit，1 = cancel。热路径里只有数组读写。 */
    private static final class Ops {
        final int n;
        final byte[] type;
        final boolean[] buy;
        final int[] px;
        final int[] qty;
        final long[] id;
        Ops(int n, Random rnd) {
            this.n = n;
            type = new byte[n]; buy = new boolean[n]; px = new int[n]; qty = new int[n]; id = new long[n];
            long next = 1;
            for (int i = 0; i < n; i++) {
                if (rnd.nextInt(10) < 6 || next == 1) {
                    type[i] = 0; id[i] = next++; buy[i] = rnd.nextBoolean();
                    px[i] = 49_950 + rnd.nextInt(101); qty[i] = 1 + rnd.nextInt(100);
                } else {
                    type[i] = 1; id[i] = 1 + rnd.nextInt((int) next - 1);
                }
            }
        }
    }

    private static void apply(TickBook b, Ops o, int from, int to, TickBook.TradeSink sink) {
        for (int i = from; i < to; i++) {
            if (o.type[i] == 0) b.limit(o.id[i], o.buy[i] ? BUY : SELL, o.px[i], o.qty[i], sink);
            else b.cancel(o.id[i]);
        }
    }

    @Test @Tag("part4") @Tag("perf")
    void twoMillionOperationsInUnderTwoSeconds() {
        var ops = new Ops(2_000_000, new Random(0));
        var b = new TickBook(100_000, 1 << 21);
        var sink = new Counter();
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> apply(b, ops, 0, ops.n, sink));
        assertTrue(sink.count > 100_000, "should trade a lot: " + sink.count);
    }

    @Test @Tag("part4") @Tag("perf")
    void steadyStateDoesNotAllocate() {
        var ops = new Ops(1_000_000, new Random(1));
        var b = new TickBook(100_000, 1 << 21);
        var sink = new Counter();
        long allocated = assertTimeoutPreemptively(Duration.ofSeconds(5), () -> {
            var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
            long tid = Thread.currentThread().threadId();
            apply(b, ops, 0, 400_000, sink); // 预热 + 把池、表都用起来
            long before = mx.getThreadAllocatedBytes(tid);
            apply(b, ops, 400_000, 1_000_000, sink);
            return mx.getThreadAllocatedBytes(tid) - before;
        });
        // 60 万个操作，允许 JIT/OSR 之类的零星分配；装箱或事件对象的写法会是几十 MB
        assertTrue(allocated < 512 * 1024, "allocated " + allocated + " bytes for 600k ops");
    }
}
