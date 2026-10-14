import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** hc11 Part 3：在线版（订单与撤单按时间顺序到达）。 */
class OnlineOverlapTest {
    static final OrderIntervals.Side BUY = OrderIntervals.Side.BUY;
    static final OrderIntervals.Side SELL = OrderIntervals.Side.SELL;

    static OrderIntervals.Peak pk(int c, long t) {
        return new OrderIntervals.Peak(c, t);
    }

    @Test @Tag("part3")
    void problemSampleStepByStep() {
        // 与 Part 2 的样例是同一批订单，只是按到达时间排好，一边来一边问
        var o = new OnlineOverlap();
        o.place(1, BUY, 0, 10);
        assertEquals(pk(1, 0), o.peak());
        o.place(2, BUY, 2, 8);
        assertEquals(pk(2, 2), o.peak());
        o.place(3, SELL, 3, 6);
        assertEquals(pk(3, 3), o.peak());
        o.place(4, SELL, 4, 12);
        assertEquals(pk(4, 4), o.peak());
        o.place(5, BUY, 5, 9);
        assertEquals(pk(5, 5), o.peak());   // 此刻（t=5）5 张都活着
        assertTrue(o.cancel(4, 5));         // 同一时刻撤掉 4：t=5 的最终活跃数是 4
        assertEquals(pk(4, 4), o.peak());   // 追溯修正：最大值 4 最早出现在 t=4，而不是被 t=5 的瞬时 5 污染
        assertTrue(o.cancel(2, 6));
        assertEquals(pk(4, 4), o.peak());
        assertEquals(pk(3, 5), o.peak(BUY));
        assertEquals(pk(2, 4), o.peak(SELL));
        assertEquals(6, o.now());
        // 回看历史：liveAt 是一个阶梯函数
        int[] expect = {1, 1, 2, 3, 4, 4, 2};   // t = 0..6
        for (int t = 0; t <= 6; t++) assertEquals(expect[t], o.liveAt(t), "t=" + t);
        assertEquals(2, o.liveNow());
        assertEquals(1, o.liveAt(BUY, 1));
        assertEquals(2, o.liveAt(SELL, 4));
    }

    @Test @Tag("part3") @Tag("edge")
    void sameTimestampPlaceThenCancelDoesNotInflateTheMax() {
        var o = new OnlineOverlap();
        o.place(1, BUY, 5, 9);
        o.place(2, BUY, 5, 9);
        assertEquals(2, o.maxSoFar());
        assertTrue(o.cancel(1, 5));   // 订单 1 实际是 [5,5) 空区间
        assertEquals(1, o.maxSoFar());
        assertEquals(pk(1, 5), o.peak());
    }

    @Test @Tag("part3") @Tag("edge")
    void expiryIsExclusiveAndFoldsLazily() {
        var o = new OnlineOverlap();
        o.place(1, SELL, 0, 5);
        o.place(2, SELL, 1, 5);
        o.place(3, SELL, 2, 6);
        assertEquals(3, o.liveNow());
        o.advanceTo(4);
        assertEquals(3, o.liveNow());
        o.advanceTo(5);                     // 1、2 在 5 结束（不含）
        assertEquals(1, o.liveNow());
        assertEquals(3, o.liveAt(4));
        assertEquals(1, o.liveAt(5));
        o.advanceTo(100);
        assertEquals(0, o.liveNow());
        assertEquals(1, o.liveAt(5));       // 历史不变
        assertEquals(0, o.liveAt(6));
        assertEquals(pk(3, 2), o.peak());
    }

    @Test @Tag("part3") @Tag("edge")
    void cancelReturnValues() {
        var o = new OnlineOverlap();
        o.place(1, BUY, 0, 5);
        o.place(2, BUY, 1, 100);
        assertTrue(o.cancel(2, 3));
        assertFalse(o.cancel(2, 4));        // 已经被撤过
        assertFalse(o.cancel(1, 5));        // 恰好在计划结束时刻：已经结束，撤单无效
        assertFalse(o.cancel(1, 9));        // 结束之后
        assertThrows(IllegalArgumentException.class, () -> o.cancel(99, 10));   // 不存在
        assertEquals(0, o.liveNow());
    }

    @Test @Tag("part3") @Tag("edge")
    void zeroLengthOrderIsRegisteredButNeverLive() {
        var o = new OnlineOverlap();
        o.place(1, BUY, 3, 3);
        assertEquals(0, o.liveNow());
        assertEquals(pk(0, 0), o.peak());
        assertFalse(o.cancel(1, 3));
        assertThrows(IllegalArgumentException.class, () -> o.place(1, SELL, 4, 9));   // id 已用过
    }

    @Test @Tag("part3") @Tag("edge")
    void outOfOrderAndInvalidArguments() {
        var o = new OnlineOverlap();
        o.place(1, BUY, 10, 20);
        assertThrows(IllegalArgumentException.class, () -> o.place(2, BUY, 9, 12));
        assertThrows(IllegalArgumentException.class, () -> o.cancel(1, 9));
        assertThrows(IllegalArgumentException.class, () -> o.advanceTo(9));
        assertThrows(IllegalArgumentException.class, () -> o.place(3, BUY, 12, 11));
        assertThrows(IllegalArgumentException.class, () -> o.place(3, BUY, -1, 11));
        assertThrows(NullPointerException.class, () -> o.place(3, null, 12, 15));
        assertThrows(IllegalArgumentException.class, () -> o.liveAt(11));    // 未来：不支持
        assertThrows(IllegalArgumentException.class, () -> o.liveAt(-1));
        // 失败的调用不改变状态
        assertEquals(10, o.now());
        assertEquals(1, o.liveNow());
        o.place(2, SELL, 10, 15);   // 同一时刻 OK
        assertEquals(pk(2, 10), o.peak());
    }

    @Test @Tag("part3") @Tag("edge")
    void manyOrdersEndingAtTheSameInstant() {
        var o = new OnlineOverlap();
        for (int i = 0; i < 1000; i++) o.place(i, i % 2 == 0 ? BUY : SELL, i / 100, 50);
        assertEquals(1000, o.liveNow());
        assertEquals(500, o.liveNow(BUY));
        // 撤掉其中几个：计划结束时间 50 处的计数要同步减少
        assertTrue(o.cancel(0, 20));
        assertTrue(o.cancel(1, 20));
        o.advanceTo(50);
        assertEquals(0, o.liveNow());
        assertEquals(998, o.liveAt(49));
        assertEquals(pk(1000, 9), o.peak());
    }

    @Test @Tag("part3") @Tag("edge")
    void applyDispatchesSealedEvents() {
        var o = new OnlineOverlap();
        assertTrue(o.apply(new OrderIntervals.Place(1, BUY, 1, 9)));
        assertTrue(o.apply(new OrderIntervals.Cancel(1, 4)));
        assertFalse(o.apply(new OrderIntervals.Cancel(1, 5)));
        assertEquals(0, o.liveNow());
    }

    @Test @Tag("part3")
    void textBlockScriptDrivesTheSameSample() {
        // P id side start end | C id time —— 与 Part 2 的样例同一批订单，按到达时间排好
        var script = """
                P 1 BUY  0 10
                P 2 BUY  2  8
                P 3 SELL 3  6
                P 4 SELL 4 12
                P 5 BUY  5  9
                C 4 5
                C 2 6
                """;
        var o = new OnlineOverlap();
        var results = new ArrayList<Boolean>();
        for (var line : script.lines().toList()) {
            var f = line.strip().split("\\s+");
            results.add(o.apply(switch (f[0]) {
                case "P" -> new OrderIntervals.Place(Long.parseLong(f[1]), OrderIntervals.Side.valueOf(f[2]),
                        Long.parseLong(f[3]), Long.parseLong(f[4]));
                case "C" -> new OrderIntervals.Cancel(Long.parseLong(f[1]), Long.parseLong(f[2]));
                default -> throw new IllegalArgumentException(line);
            }));
        }
        assertEquals(List.of(true, true, true, true, true, true, true), results);
        assertEquals(pk(4, 4), o.peak());
        assertEquals(pk(3, 5), o.peak(BUY));
        assertEquals(pk(2, 4), o.peak(SELL));
    }

    @Test @Tag("part3") @Tag("edge")
    void hugeTimestamps() {
        long max = Long.MAX_VALUE;
        var o = new OnlineOverlap();
        o.place(1, BUY, 0, max);
        o.place(2, SELL, max - 3, max - 1);
        assertEquals(pk(2, max - 3), o.peak());
        assertEquals(2, o.liveAt(max - 3));
        o.advanceTo(max - 1);
        assertEquals(2, o.liveAt(max - 2));   // 历史阶梯：max-3 处记录的 2 一直到 max-1 才下降
        assertEquals(1, o.liveNow());
        assertEquals(1, o.liveAt(max - 1));
    }

    @ParameterizedTest @Tag("part3")
    @ValueSource(longs = {61, 62, 63, 64, 65, 66})
    void everyPrefixAgreesWithTheBatchSolution(long seed) {
        var rnd = new Random(seed);
        var feed = new ArrayList<OrderIntervals.OrderEvent>();
        var placed = new ArrayList<Long>();
        long time = 0;
        long nextId = 0;
        for (int step = 0; step < 220; step++) {
            time += rnd.nextInt(3);
            if (placed.isEmpty() || rnd.nextInt(3) != 0) {
                long id = nextId++;
                placed.add(id);
                feed.add(new OrderIntervals.Place(id, rnd.nextBoolean() ? BUY : SELL, time, time + rnd.nextInt(14)));
            } else {
                feed.add(new OrderIntervals.Cancel(placed.get(rnd.nextInt(placed.size())), time));
            }
        }
        var o = new OnlineOverlap();
        for (int i = 0; i < feed.size(); i++) {
            o.apply(feed.get(i));
            var batch = OrderIntervals.analyze(feed.subList(0, i + 1));
            assertEquals(batch.all(), o.peak(), "all, seed " + seed + " prefix " + (i + 1));
            assertEquals(batch.buy(), o.peak(BUY), "buy, seed " + seed + " prefix " + (i + 1));
            assertEquals(batch.sell(), o.peak(SELL), "sell, seed " + seed + " prefix " + (i + 1));
        }
        // 最终状态：liveAt(t) 与按有效区间暴力计数一致
        var finalEff = new java.util.HashMap<Long, long[]>();
        for (var e : feed) {
            if (e instanceof OrderIntervals.Place(var id, _, var s, var en)) finalEff.put(id, new long[]{s, en});
            else if (e instanceof OrderIntervals.Cancel(var id, var t)) finalEff.get(id)[1] = Math.min(finalEff.get(id)[1], t);
        }
        for (long t = 0; t <= o.now(); t++) {
            int live = 0;
            for (long[] x : finalEff.values()) if (x[0] <= t && t < x[1]) live++;
            assertEquals(live, o.liveAt(t), "liveAt " + t + ", seed " + seed);
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void eightHundredThousandEventsUnderTwoSeconds() {
        int n = 600_000;
        var rnd = new Random(0);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var o = new OnlineOverlap();
            long time = 0;
            for (int i = 0; i < n; i++) {
                time += rnd.nextInt(3);
                o.place(i, (i & 1) == 0 ? BUY : SELL, time, time + 1 + rnd.nextInt(5_000));
                if (i % 3 == 2) o.cancel(rnd.nextInt(i + 1), time);
                if (i % 1000 == 0) o.liveAt(rnd.nextInt((int) Math.min(time, Integer.MAX_VALUE) + 1));
            }
            assertTrue(o.maxSoFar() > 100);
        });
    }
}
