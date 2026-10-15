import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.OptionalLong;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class OrderBookTest {
    private static final OrderBook.Side BUY = OrderBook.Side.BUY;
    private static final OrderBook.Side SELL = OrderBook.Side.SELL;

    private static List<String> lines(String block) { return block.lines().toList(); }

    // ================= Part 1：维护 =================

    @Test @Tag("part1") @Tag("edge")
    void emptyBook() {
        var b = new OrderBook();
        assertEquals(OptionalLong.empty(), b.bestBid());
        assertEquals(OptionalLong.empty(), b.bestAsk());
        assertEquals(List.of(), b.depth(BUY, 5));
        assertEquals(List.of(), b.queue(SELL, 100));
        assertEquals(0, b.size());
        assertFalse(b.cancel(1));
        assertFalse(b.modify(1, 5));
    }

    @Test @Tag("part1")
    void bestBidIsHighestBestAskIsLowest() {
        var b = new OrderBook();
        b.add(1, BUY, 100, 5);
        b.add(2, BUY, 101, 5);
        b.add(3, BUY, 99, 5);
        b.add(4, SELL, 103, 5);
        b.add(5, SELL, 102, 5);
        assertEquals(OptionalLong.of(101), b.bestBid());
        assertEquals(OptionalLong.of(102), b.bestAsk());
        assertEquals(5, b.size());
    }

    @Test @Tag("part1")
    void depthAggregatesAndOrdersBestFirst() {
        var b = new OrderBook();
        b.add(1, BUY, 100, 5);
        b.add(2, BUY, 99, 3);
        b.add(3, BUY, 100, 7);
        b.add(4, SELL, 102, 1);
        b.add(5, SELL, 101, 2);
        b.add(6, SELL, 101, 4);
        assertEquals(List.of(new OrderBook.Level(100, 12, 2), new OrderBook.Level(99, 3, 1)), b.depth(BUY, 10));
        assertEquals(List.of(new OrderBook.Level(100, 12, 2)), b.depth(BUY, 1));
        assertEquals(List.of(new OrderBook.Level(101, 6, 2), new OrderBook.Level(102, 1, 1)), b.depth(SELL, 2));
        assertEquals(List.of(), b.depth(SELL, 0));
        assertThrows(IllegalArgumentException.class, () -> b.depth(BUY, -1));
    }

    @Test @Tag("part1")
    void samePriceIsFifo() {
        var b = new OrderBook();
        b.add(7, SELL, 50, 1);
        b.add(3, SELL, 50, 1);
        b.add(9, SELL, 50, 1);
        assertEquals(List.of(7L, 3L, 9L), b.queue(SELL, 50));
        assertEquals(7L, b.queue(SELL, 50).getFirst());
        assertEquals(9L, b.queue(SELL, 50).getLast());
    }

    @Test @Tag("part1")
    void cancelRemovesAndBestMoves() {
        var b = new OrderBook();
        b.add(1, BUY, 100, 5);
        b.add(2, BUY, 100, 6);
        b.add(3, BUY, 100, 7);
        b.add(4, BUY, 99, 1);
        assertTrue(b.cancel(2));
        assertEquals(List.of(1L, 3L), b.queue(BUY, 100));
        assertEquals(new OrderBook.Level(100, 12, 2), b.depth(BUY, 1).getFirst());
        assertFalse(b.cancel(2));
        assertTrue(b.cancel(1));
        assertTrue(b.cancel(3));
        assertEquals(OptionalLong.of(99), b.bestBid());
        assertEquals(List.of(), b.queue(BUY, 100));
        assertEquals(1, b.size());
    }

    @Test @Tag("part1")
    void modifyDownKeepsPriorityModifyUpGoesToBack() {
        var b = new OrderBook();
        b.add(1, BUY, 100, 10);
        b.add(2, BUY, 100, 10);
        b.add(3, BUY, 100, 10);
        assertTrue(b.modify(1, 4)); // 减量：保持队头
        assertEquals(List.of(1L, 2L, 3L), b.queue(BUY, 100));
        assertEquals(4, b.find(1).orElseThrow().qty());
        assertEquals(24, b.depth(BUY, 1).getFirst().totalQty());
        assertTrue(b.modify(1, 4)); // 等量：什么也不变
        assertEquals(List.of(1L, 2L, 3L), b.queue(BUY, 100));
        assertTrue(b.modify(1, 5)); // 增量：丢失优先级
        assertEquals(List.of(2L, 3L, 1L), b.queue(BUY, 100));
        assertEquals(25, b.depth(BUY, 1).getFirst().totalQty());
        assertFalse(b.modify(99, 1));
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(longs = {0, -1, Long.MIN_VALUE})
    void modifyRejectsNonPositiveQuantity(long q) {
        var b = new OrderBook();
        b.add(1, BUY, 100, 10);
        assertThrows(IllegalArgumentException.class, () -> b.modify(1, q));
        assertThrows(IllegalArgumentException.class, () -> b.modify(404, q)); // 未知 id 也先报参数错
        assertEquals(10, b.find(1).orElseThrow().qty());
    }

    @Test @Tag("part1") @Tag("edge")
    void addValidatesAndRejectsDuplicates() {
        var b = new OrderBook();
        assertThrows(IllegalArgumentException.class, () -> b.add(0, BUY, 100, 1));
        assertThrows(IllegalArgumentException.class, () -> b.add(-5, BUY, 100, 1));
        assertThrows(IllegalArgumentException.class, () -> b.add(1, BUY, 0, 1));
        assertThrows(IllegalArgumentException.class, () -> b.add(1, BUY, -3, 1));
        assertThrows(IllegalArgumentException.class, () -> b.add(1, BUY, 100, 0));
        assertThrows(NullPointerException.class, () -> b.add(1, null, 100, 1));
        b.add(1, BUY, 100, 1);
        assertThrows(IllegalArgumentException.class, () -> b.add(1, SELL, 200, 1)); // id 全簿唯一，与方向无关
        assertEquals(1, b.size());
        b.cancel(1);
        b.add(1, SELL, 200, 1); // 撤掉之后 id 可复用
        assertEquals(OptionalLong.of(200), b.bestAsk());
    }

    @Test @Tag("part1") @Tag("edge")
    void hugePricesAndLevelOverflow() {
        var b = new OrderBook();
        b.add(1, BUY, Long.MAX_VALUE, Long.MAX_VALUE - 5);
        assertEquals(OptionalLong.of(Long.MAX_VALUE), b.bestBid());
        assertThrows(ArithmeticException.class, () -> b.add(2, BUY, Long.MAX_VALUE, 6));
        assertEquals(1, b.size()); // 抛错之后簿不变
        assertEquals(Long.MAX_VALUE - 5, b.depth(BUY, 1).getFirst().totalQty());
        b.add(2, BUY, Long.MAX_VALUE, 5); // 正好到顶：合法
        assertEquals(Long.MAX_VALUE, b.depth(BUY, 1).getFirst().totalQty());
        assertThrows(ArithmeticException.class, () -> b.modify(2, 6)); // 增量也会溢出
        assertEquals(5, b.find(2).orElseThrow().qty());
        assertEquals(List.of(1L, 2L), b.queue(BUY, Long.MAX_VALUE));
    }

    @Test @Tag("part1") @Tag("perf")
    void twoHundredThousandAddsAndCancels() {
        var rnd = new Random(0);
        int n = 200_000;
        var b = new OrderBook();
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            for (int i = 1; i <= n; i++) {
                b.add(i, rnd.nextBoolean() ? BUY : SELL, 1 + rnd.nextInt(5000), 1 + rnd.nextInt(100));
            }
            for (int i = 1; i <= n; i += 2) b.cancel(i);
        });
        assertEquals(n / 2, b.size());
    }

    // ================= Part 2：撮合 + 事件 =================

    private static OrderBook.Limit limit(long id, OrderBook.Side s, long px, long q) { return new OrderBook.Limit(id, s, px, q); }

    @Test @Tag("part2") @Tag("fmt")
    void sampleReplayMatchesProblemStatement() {
        var out = OrderBook.replay(lines("""
                # 样例
                LIMIT 1 SELL 101 5
                LIMIT 2 SELL 101 3
                LIMIT 3 SELL 102 4

                LIMIT 4 BUY 101 6
                limit 5 buy 103 10
                MARKET 6 SELL 5
                CANCEL 3
                MODIFY 9 1
                """));
        assertEquals(lines("""
                REST id=1 side=SELL px=101 qty=5
                REST id=2 side=SELL px=101 qty=3
                REST id=3 side=SELL px=102 qty=4
                TRADE taker=4 maker=1 side=BUY px=101 qty=5
                TRADE taker=4 maker=2 side=BUY px=101 qty=1
                TRADE taker=5 maker=2 side=BUY px=101 qty=2
                TRADE taker=5 maker=3 side=BUY px=102 qty=4
                REST id=5 side=BUY px=103 qty=4
                TRADE taker=6 maker=5 side=SELL px=103 qty=4
                CANCEL id=6 remaining=1
                REJECT id=3 reason=unknown id
                REJECT id=9 reason=unknown id
                """), out);
    }

    @Test @Tag("part2")
    void betterPriceBeatsEarlierArrival() {
        var b = new OrderBook();
        b.execute(limit(1, SELL, 102, 5));
        b.execute(limit(2, SELL, 101, 5)); // 后到，但价格更好
        var ev = b.execute(limit(3, BUY, 110, 5));
        assertEquals(List.of(new OrderBook.Trade(3, 2, BUY, 101, 5)), ev);
        assertEquals(OptionalLong.of(102), b.bestAsk());
    }

    @Test @Tag("part2")
    void samePriceFifoAndTradeAtMakerPrice() {
        var b = new OrderBook();
        b.execute(limit(1, BUY, 100, 3));
        b.execute(limit(2, BUY, 100, 3));
        var ev = b.execute(limit(3, SELL, 90, 4)); // 卖价 90 远低于买价：成交价取 maker 的 100
        assertEquals(List.of(new OrderBook.Trade(3, 1, SELL, 100, 3), new OrderBook.Trade(3, 2, SELL, 100, 1)), ev);
        assertEquals(List.of(2L), b.queue(BUY, 100));
        assertEquals(2, b.find(2).orElseThrow().qty()); // 部分成交的 maker 留在队头，量减少
    }

    @Test @Tag("part2")
    void partialFillRestsRemainderAndNoCrossNoTrade() {
        var b = new OrderBook();
        assertEquals(List.of(new OrderBook.Rested(1, SELL, 100, 4)), b.execute(limit(1, SELL, 100, 4)));
        assertEquals(List.of(new OrderBook.Rested(2, BUY, 99, 4)), b.execute(limit(2, BUY, 99, 4))); // 99 < 100：不交叉
        var ev = b.execute(limit(3, BUY, 100, 10));
        assertEquals(List.of(new OrderBook.Trade(3, 1, BUY, 100, 4), new OrderBook.Rested(3, BUY, 100, 6)), ev);
        assertEquals(OptionalLong.of(100), b.bestBid());
        assertEquals(OptionalLong.empty(), b.bestAsk());
    }

    @Test @Tag("part2")
    void marketOrdersSweepAndExpire() {
        var b = new OrderBook();
        assertEquals(List.of(new OrderBook.Cancelled(1, 5)), b.execute(new OrderBook.Market(1, BUY, 5))); // 空簿
        b.execute(limit(2, SELL, 100, 2));
        b.execute(limit(3, SELL, 105, 2));
        b.execute(limit(4, SELL, 200, 2));
        var ev = b.execute(new OrderBook.Market(5, BUY, 5));
        assertEquals(List.of(new OrderBook.Trade(5, 2, BUY, 100, 2), new OrderBook.Trade(5, 3, BUY, 105, 2),
                new OrderBook.Trade(5, 4, BUY, 200, 1)), ev);
        assertEquals(1, b.find(4).orElseThrow().qty());
        assertEquals(List.of(new OrderBook.Cancelled(6, 4)), b.execute(new OrderBook.Market(6, SELL, 4))); // 买盘为空
    }

    @Test @Tag("part2")
    void modifyAndCancelThroughExecute() {
        var b = new OrderBook();
        b.execute(limit(1, SELL, 100, 5));
        b.execute(limit(2, SELL, 100, 5));
        assertEquals(List.of(new OrderBook.Modified(1, 5, 8)), b.execute(new OrderBook.Modify(1, 8))); // 增量：排到 2 后面
        var ev = b.execute(limit(3, BUY, 100, 6));
        assertEquals(List.of(new OrderBook.Trade(3, 2, BUY, 100, 5), new OrderBook.Trade(3, 1, BUY, 100, 1)), ev);
        assertEquals(List.of(new OrderBook.Modified(1, 7, 2)), b.execute(new OrderBook.Modify(1, 2)));
        assertEquals(List.of(new OrderBook.Cancelled(1, 2)), b.execute(new OrderBook.Cancel(1)));
        assertEquals(0, b.size());
    }

    @Test @Tag("part2") @Tag("edge")
    void rejectionsCarryTheReason() {
        var b = new OrderBook();
        b.execute(limit(1, SELL, 100, 5));
        assertEquals(List.of(new OrderBook.Rejected(0, "invalid id")), b.execute(limit(0, BUY, 100, 1)));
        assertEquals(List.of(new OrderBook.Rejected(2, "invalid price")), b.execute(limit(2, BUY, 0, 1)));
        assertEquals(List.of(new OrderBook.Rejected(2, "invalid quantity")), b.execute(limit(2, BUY, 100, 0)));
        assertEquals(List.of(new OrderBook.Rejected(1, "duplicate id")), b.execute(limit(1, BUY, 50, 1)));
        assertEquals(List.of(new OrderBook.Rejected(1, "duplicate id")), b.execute(new OrderBook.Market(1, BUY, 1)));
        assertEquals(List.of(new OrderBook.Rejected(2, "invalid quantity")), b.execute(new OrderBook.Market(2, BUY, -1)));
        assertEquals(List.of(new OrderBook.Rejected(9, "unknown id")), b.execute(new OrderBook.Cancel(9)));
        assertEquals(List.of(new OrderBook.Rejected(9, "unknown id")), b.execute(new OrderBook.Modify(9, 3)));
        assertEquals(List.of(new OrderBook.Rejected(1, "invalid quantity")), b.execute(new OrderBook.Modify(1, 0)));
        assertEquals(1, b.size()); // 被拒的命令不改变簿
        assertEquals(5, b.find(1).orElseThrow().qty());
    }

    @Test @Tag("part2") @Tag("edge")
    void overflowIsRejectedAtomically() {
        var b = new OrderBook();
        b.execute(limit(1, BUY, 100, Long.MAX_VALUE - 1));
        b.execute(limit(2, SELL, 200, 3));
        // 买 100 × 2 会让 100 档总量溢出：整单拒绝，且不先去吃 200 的卖单
        assertEquals(List.of(new OrderBook.Rejected(3, "overflow")), b.execute(limit(3, BUY, 100, 2)));
        assertEquals(3, b.find(2).orElseThrow().qty());
        // 改量同理：先挂一张 1 把 100 档顶满，再把它改成 2 会溢出
        assertEquals(List.of(new OrderBook.Rested(4, BUY, 100, 1)), b.execute(limit(4, BUY, 100, 1)));
        assertEquals(List.of(new OrderBook.Rejected(4, "overflow")), b.execute(new OrderBook.Modify(4, 2)));
        assertEquals(1, b.find(4).orElseThrow().qty());
    }

    @Test @Tag("part2") @Tag("edge")
    void filledIdsCanBeReused() {
        var b = new OrderBook();
        b.execute(limit(1, SELL, 100, 1));
        b.execute(limit(2, BUY, 100, 1)); // 1 和 2 都成交完了
        assertEquals(List.of(new OrderBook.Rested(1, BUY, 90, 1)), b.execute(limit(1, BUY, 90, 1)));
    }

    @ParameterizedTest @Tag("part2") @Tag("fmt")
    @ValueSource(strings = {"", "   ", "BOGUS 1", "LIMIT 1 BUY 100", "LIMIT 1 BUY 100 5 7", "LIMIT 1 HOLD 100 5", "LIMIT x BUY 100 5",
            "LIMIT 1 BUY 1.5 5", "MARKET 1 BUY", "CANCEL", "CANCEL 1 2", "MODIFY 1", "LIMIT 99999999999999999999 BUY 1 1"})
    void parseRejectsMalformedLines(String bad) {
        assertThrows(IllegalArgumentException.class, () -> OrderBook.parse(bad));
    }

    @Test @Tag("part2") @Tag("fmt")
    void parseAndRenderEveryKind() {
        assertEquals(limit(1, BUY, 100, 5), OrderBook.parse("  LIMIT   1 buy 100 5 "));
        assertEquals(new OrderBook.Market(2, SELL, 7), OrderBook.parse("Market 2 SELL 7"));
        assertEquals(new OrderBook.Cancel(3), OrderBook.parse("CANCEL 3"));
        assertEquals(new OrderBook.Modify(4, 9), OrderBook.parse("MODIFY 4 9"));
        assertEquals("TRADE taker=3 maker=1 side=SELL px=100 qty=3", OrderBook.render(new OrderBook.Trade(3, 1, SELL, 100, 3)));
        assertEquals("REST id=1 side=BUY px=7 qty=2", OrderBook.render(new OrderBook.Rested(1, BUY, 7, 2)));
        assertEquals("CANCEL id=1 remaining=2", OrderBook.render(new OrderBook.Cancelled(1, 2)));
        assertEquals("MODIFY id=1 old=5 new=3", OrderBook.render(new OrderBook.Modified(1, 5, 3)));
        assertEquals("REJECT id=1 reason=duplicate id", OrderBook.render(new OrderBook.Rejected(1, "duplicate id")));
    }

    @Test @Tag("part2") @Tag("fmt")
    void replayReportsTheOffendingLine() {
        var ex = assertThrows(IllegalArgumentException.class,
                () -> OrderBook.replay(List.of("LIMIT 1 BUY 100 5", "", "LIMIT 2 BUY oops 5")));
        assertTrue(ex.getMessage().startsWith("line 3"), ex.getMessage());
    }

    /** 随机命令流：簿永远不交叉；数量守恒 提交量 = 2×成交量 + 剩余挂单量 + 被撤/作废量。 */
    @Test @Tag("part2") @Tag("edge")
    void randomFlowKeepsInvariants() {
        var rnd = new Random(0);
        var b = new OrderBook();
        long submitted = 0, traded = 0, cancelled = 0;
        long nextId = 1;
        for (int step = 0; step < 20_000; step++) {
            int dice = rnd.nextInt(10);
            List<OrderBook.Event> ev;
            if (dice < 6) {
                long q = 1 + rnd.nextInt(20);
                submitted += q;
                ev = b.execute(limit(nextId++, rnd.nextBoolean() ? BUY : SELL, 95 + rnd.nextInt(11), q));
            } else if (dice < 7) {
                long q = 1 + rnd.nextInt(30);
                submitted += q;
                ev = b.execute(new OrderBook.Market(nextId++, rnd.nextBoolean() ? BUY : SELL, q));
            } else {
                ev = b.execute(new OrderBook.Cancel(1 + rnd.nextInt((int) nextId)));
            }
            for (var e : ev) {
                if (e instanceof OrderBook.Trade t) traded += t.qty();
                if (e instanceof OrderBook.Cancelled c) cancelled += c.remaining();
            }
            if (b.bestBid().isPresent() && b.bestAsk().isPresent()) {
                assertTrue(b.bestBid().getAsLong() < b.bestAsk().getAsLong(), "crossed at step " + step);
            }
        }
        long resting = b.depth(BUY, Integer.MAX_VALUE).stream().mapToLong(OrderBook.Level::totalQty).sum()
                + b.depth(SELL, Integer.MAX_VALUE).stream().mapToLong(OrderBook.Level::totalQty).sum();
        assertEquals(submitted, 2 * traded + resting + cancelled);
        assertTrue(traded > 0);
    }

    @Test @Tag("part2") @Tag("perf")
    void threeHundredThousandCommandsInUnderTwoSeconds() {
        var rnd = new Random(0);
        int n = 300_000;
        var cmds = new ArrayList<OrderBook.Command>(n);
        for (int i = 1; i <= n; i++) {
            int dice = rnd.nextInt(10);
            if (dice < 7) cmds.add(limit(i, rnd.nextBoolean() ? BUY : SELL, 9_900 + rnd.nextInt(201), 1 + rnd.nextInt(50)));
            else if (dice < 9) cmds.add(new OrderBook.Cancel(1 + rnd.nextInt(i)));
            else cmds.add(new OrderBook.Modify(1 + rnd.nextInt(i), 1 + rnd.nextInt(50)));
        }
        var b = new OrderBook();
        var events = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> b.executeAll(cmds));
        assertTrue(events.size() >= n / 2);
    }

    // ================= Part 3：批量限价撮合（hc14） =================

    @Test @Tag("part3")
    void batchSample() {
        var s = BatchMatcher.run(new long[][] {{0, 100, 5}, {1, 99, 3}, {1, 100, 4}, {0, 101, 10}});
        assertEquals(List.of(new OrderBook.Trade(2, 1, SELL, 100, 3), new OrderBook.Trade(3, 1, SELL, 100, 2),
                new OrderBook.Trade(4, 3, BUY, 100, 2)), s.trades());
        assertEquals(7, s.filledQty());
        assertEquals(700, s.notional());
        assertEquals(List.of(new OrderBook.Level(101, 8, 1)), s.bids());
        assertEquals(List.of(), s.asks());
    }

    @Test @Tag("part3") @Tag("edge")
    void batchEmptyAndNoCross() {
        var s = BatchMatcher.run(new long[0][]);
        assertEquals(new BatchMatcher.Summary(List.of(), 0, 0, List.of(), List.of()), s);
        var t = BatchMatcher.run(new long[][] {{0, 10, 1}, {1, 11, 1}});
        assertEquals(List.of(), t.trades());
        assertEquals(List.of(new OrderBook.Level(10, 1, 1)), t.bids());
        assertEquals(List.of(new OrderBook.Level(11, 1, 1)), t.asks());
    }

    @Test @Tag("part3") @Tag("edge")
    void batchSweepsSeveralLevelsInPriceOrder() {
        var s = BatchMatcher.run(new long[][] {{1, 103, 2}, {1, 101, 2}, {1, 102, 2}, {0, 105, 5}});
        assertEquals(List.of(new OrderBook.Trade(4, 2, BUY, 101, 2), new OrderBook.Trade(4, 3, BUY, 102, 2),
                new OrderBook.Trade(4, 1, BUY, 103, 1)), s.trades());
        assertEquals(5, s.filledQty());
        assertEquals(2 * 101 + 2 * 102 + 103, s.notional());
        assertEquals(List.of(new OrderBook.Level(103, 1, 1)), s.asks());
    }

    @ParameterizedTest @Tag("part3") @Tag("edge")
    @ValueSource(strings = {"2,100,1", "-1,100,1", "0,0,1", "0,-5,1", "0,100,0", "0,100,-3"})
    void batchRejectsBadRows(String row) {
        var p = java.util.Arrays.stream(row.split(",")).mapToLong(Long::parseLong).toArray();
        var ex = assertThrows(IllegalArgumentException.class, () -> BatchMatcher.run(new long[][] {{0, 1, 1}, p}));
        assertTrue(ex.getMessage().startsWith("row 1"), ex.getMessage());
    }

    @Test @Tag("part3") @Tag("edge")
    void batchRejectsWrongArity() {
        assertThrows(IllegalArgumentException.class, () -> BatchMatcher.run(new long[][] {{0, 1}}));
        assertThrows(IllegalArgumentException.class, () -> BatchMatcher.run(new long[][] {{0, 1, 1, 1}}));
        assertThrows(IllegalArgumentException.class, () -> BatchMatcher.run(new long[][] {null}));
        assertThrows(NullPointerException.class, () -> BatchMatcher.run(null));
    }

    @Test @Tag("part3") @Tag("edge")
    void batchNotionalOverflowIsDetected() {
        var ok = BatchMatcher.run(new long[][] {{0, 3_000_000_000L, 3_000_000_000L}, {1, 3_000_000_000L, 3_000_000_000L}});
        assertEquals(9_000_000_000_000_000_000L, ok.notional()); // 9e18 < Long.MAX_VALUE ≈ 9.22e18
        assertThrows(ArithmeticException.class,
                () -> BatchMatcher.run(new long[][] {{0, 4_000_000_000L, 3_000_000_000L}, {1, 4_000_000_000L, 3_000_000_000L}}));
        // 两笔各 9e18 加起来溢出
        assertThrows(ArithmeticException.class, () -> BatchMatcher.run(new long[][] {
                {0, 3_000_000_000L, 3_000_000_000L}, {1, 3_000_000_000L, 3_000_000_000L},
                {0, 3_000_000_000L, 3_000_000_000L}, {1, 3_000_000_000L, 3_000_000_000L}}));
    }

    @Test @Tag("part3") @Tag("perf")
    void batchOfTwoHundredThousandRows() {
        var rnd = new Random(0);
        var rows = new long[200_000][];
        for (int i = 0; i < rows.length; i++) rows[i] = new long[] {rnd.nextInt(2), 9_900 + rnd.nextInt(201), 1 + rnd.nextInt(100)};
        var s = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> BatchMatcher.run(rows));
        long buy = 0, sell = 0;
        for (var r : rows) { if (r[0] == 0) buy += r[2]; else sell += r[2]; }
        assertTrue(s.filledQty() > 0 && s.filledQty() <= Math.min(buy, sell));
        long restBid = s.bids().stream().mapToLong(OrderBook.Level::totalQty).sum();
        long restAsk = s.asks().stream().mapToLong(OrderBook.Level::totalQty).sum();
        assertEquals(buy, s.filledQty() + restBid);
        assertEquals(sell, s.filledQty() + restAsk);
        assertTrue(s.bids().isEmpty() || s.asks().isEmpty() || s.bids().getFirst().price() < s.asks().getFirst().price());
    }
}
