import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 4：TradingDesk —— 三个部件装在一起 + 事件溯源 / 重放。 */
class TradingDeskTest {
    static final RiskLimits LIMITS = new RiskLimits(1_000, 10_000_000, 3_000, 50, 1_000);

    TradingDesk desk = new TradingDesk(LIMITS);

    TradingDeskTest() { desk.setReferencePrice("A", 100); desk.setReferencePrice("B", 50); }

    static Order buy(long id, String sym, long qty, long px) { return new Order(id, sym, Side.BUY, qty, px); }
    static Order sell(long id, String sym, long qty, long px) { return new Order(id, sym, Side.SELL, qty, px); }

    @Test @Tag("part4")
    void fullLifecycleUpdatesOrderAndPosition() {
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(1, "A", 100, 100)));
        assertEquals(OrderStatus.PENDING, desk.order(1).status());
        desk.onExec(new ExecEvent.Ack(1));
        assertTrue(desk.onExec(new ExecEvent.Fill(1, 10, 60, 99)));
        assertEquals(60, desk.position("A").netQty());
        assertEquals(60 * 99, desk.position("A").openCost());
        desk.onExec(new ExecEvent.Fill(1, 11, 40, 100));
        assertEquals(OrderStatus.FILLED, desk.order(1).status());
        assertEquals(100, desk.position("A").netQty());
        // 卖出平仓
        desk.submit(sell(2, "A", 100, 101));
        desk.onExec(new ExecEvent.Ack(2));
        desk.onExec(new ExecEvent.Fill(2, 12, 100, 105));
        assertEquals(0, desk.position("A").netQty());
        assertEquals(60 * (105 - 99) + 40 * (105 - 100), desk.position("A").realizedPnl());
    }

    @Test @Tag("part4")
    void riskRejectedOrderIsRecordedAsRejectedWithReason() {
        var r = desk.submit(buy(1, "A", 2_000, 100));
        assertEquals(new RiskResult.Rejected(RiskReason.QTY_LIMIT), r);
        var v = desk.order(1);
        assertEquals(OrderStatus.REJECTED, v.status());
        assertEquals("QTY_LIMIT", v.rejectReason());
        assertEquals(0, v.cumQty());
        // 被拒的单不再占用未完成名额 / 仓位额度：能立刻再下一张顶格的
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(2, "A", 1_000, 100)));
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(3, "A", 1_000, 100)));
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(4, "A", 1_000, 100)));       // 3000 总暴露 == 上限
        assertEquals(new RiskResult.Rejected(RiskReason.POSITION_LIMIT), desk.submit(buy(5, "A", 1, 100)));
    }

    @Test @Tag("part4")
    void orderDoesNotCountItselfAgainstPositionLimit() {
        // 单笔恰好顶格的单子，如果先登记再检查，会把自己算两遍而被误拒
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(1, "A", 1_000, 100)));
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(2, "A", 1_000, 100)));
    }

    @Test @Tag("part4")
    void haltAndResumeAreEventsToo() {
        desk.halt();
        assertEquals(new RiskResult.Rejected(RiskReason.HALTED), desk.submit(buy(1, "A", 1, 100)));
        desk.resume();
        assertEquals(RiskResult.ACCEPTED, desk.submit(buy(2, "A", 1, 100)));
        assertEquals(OrderStatus.REJECTED, desk.order(1).status());
    }

    @Test @Tag("part4") @Tag("edge")
    void duplicateOrderIdThrowsAndDoesNotChangeExistingOrder() {
        desk.submit(buy(1, "A", 10, 100));
        assertThrows(IllegalArgumentException.class, () -> desk.submit(sell(1, "B", 5, 50)));
        assertEquals("A", desk.order(1).order().symbol());
    }

    @Test @Tag("part4") @Tag("edge")
    void duplicateFillDoesNotDoublePosition() {
        desk.submit(buy(1, "A", 100, 100));
        desk.onExec(new ExecEvent.Ack(1));
        assertTrue(desk.onExec(new ExecEvent.Fill(1, 5, 30, 100)));
        assertFalse(desk.onExec(new ExecEvent.Fill(1, 5, 30, 100)));
        assertEquals(30, desk.position("A").netQty());
    }

    @Test @Tag("part4") @Tag("edge")
    void illegalEventThrowsLeavesStateButStaysInJournal() {
        desk.submit(buy(1, "A", 10, 100));
        assertThrows(IllegalTransitionException.class, () -> desk.onExec(new ExecEvent.Fill(1, 1, 1, 100)));   // 未 Ack
        assertThrows(NoSuchElementException.class, () -> desk.onExec(new ExecEvent.Ack(99)));
        assertEquals(0, desk.position("A").netQty());
        assertEquals(OrderStatus.PENDING, desk.order(1).status());
        long exceptional = desk.journal().stream().filter(e -> e instanceof ExecEvent).count();
        assertEquals(2, exceptional);                      // 输入先于处理被记录
    }

    @Test @Tag("part4")
    void journalIsAnImmutableCopyInInputOrder() {
        desk.submit(buy(1, "A", 10, 100));
        desk.onExec(new ExecEvent.Ack(1));
        List<DeskEvent> j = desk.journal();
        assertEquals(List.of(
                new DeskEvent.SetReferencePrice("A", 100),
                new DeskEvent.SetReferencePrice("B", 50),
                new DeskEvent.Submit(buy(1, "A", 10, 100)),
                new ExecEvent.Ack(1)), j);
        assertThrows(UnsupportedOperationException.class, () -> j.add(new DeskEvent.Halt()));
        desk.halt();
        assertEquals(4, j.size());                         // 之前取出的是快照
        assertEquals(5, desk.journal().size());
    }

    @Test @Tag("part4")
    void replayReproducesStateExactly() {
        desk.submit(buy(1, "A", 500, 100));
        desk.submit(sell(2, "B", 200, 50));
        desk.submit(buy(3, "A", 5_000, 100));                    // 被拒
        desk.onExec(new ExecEvent.Ack(1));
        desk.onExec(new ExecEvent.Ack(2));
        desk.onExec(new ExecEvent.Fill(1, 1, 300, 99));
        desk.onExec(new ExecEvent.Fill(2, 2, 200, 51));
        desk.onExec(new ExecEvent.Cancel(1));
        desk.halt();
        desk.submit(buy(4, "A", 1, 100));                        // HALTED

        TradingDesk copy = TradingDesk.replay(LIMITS, desk.journal());
        assertSameState(desk, copy);
        assertEquals(desk.journal(), copy.journal());
        assertEquals("HALTED", copy.order(4).rejectReason());
        // 重放出来的 desk 可以继续工作
        copy.resume();
        assertEquals(RiskResult.ACCEPTED, copy.submit(buy(5, "A", 1, 100)));
    }

    @Test @Tag("part4") @Tag("edge")
    void replaySwallowsInputsThatFailedTheFirstTime() {
        desk.submit(buy(1, "A", 10, 100));
        try { desk.onExec(new ExecEvent.Fill(1, 1, 1, 100)); } catch (IllegalTransitionException expected) { }
        try { desk.submit(buy(1, "A", 10, 100)); } catch (IllegalArgumentException expected) { }
        try { desk.onExec(new ExecEvent.Cancel(77)); } catch (NoSuchElementException expected) { }
        desk.onExec(new ExecEvent.Ack(1));
        TradingDesk copy = TradingDesk.replay(LIMITS, desk.journal());
        assertSameState(desk, copy);
        assertEquals(OrderStatus.WORKING, copy.order(1).status());
    }

    @Test @Tag("part4") @Tag("edge")
    void replayEqualsOriginalOnRandomEventStreams() {
        for (int seed = 0; seed < 25; seed++) {
            Random rnd = new Random(seed);
            TradingDesk d = new TradingDesk(LIMITS);
            d.setReferencePrice("A", 100);
            d.setReferencePrice("B", 50);
            long nextId = 1, execId = 1;
            for (int step = 0; step < 600; step++) {
                try {
                    switch (rnd.nextInt(10)) {
                        case 0, 1, 2 -> {
                            String sym = rnd.nextBoolean() ? "A" : "B";
                            long ref = sym.equals("A") ? 100 : 50;
                            d.submit(new Order(nextId++, sym, rnd.nextBoolean() ? Side.BUY : Side.SELL, 1 + rnd.nextInt(1_200), ref - 5 + rnd.nextInt(12) * (rnd.nextInt(8) == 0 ? 20 : 1)));
                        }
                        case 3, 4 -> d.onExec(new ExecEvent.Ack(1 + rnd.nextInt((int) nextId)));
                        case 5, 6, 7 -> d.onExec(new ExecEvent.Fill(1 + rnd.nextInt((int) nextId), rnd.nextInt(8) == 0 ? execId : execId++, 1 + rnd.nextInt(200), 40 + rnd.nextInt(70)));
                        case 8 -> d.onExec(new ExecEvent.Cancel(1 + rnd.nextInt((int) nextId)));
                        default -> { if (rnd.nextInt(6) == 0) d.halt(); else d.resume(); }
                    }
                } catch (IllegalStateException | IllegalArgumentException | NoSuchElementException expected) { }
            }
            assertSameState(d, TradingDesk.replay(LIMITS, d.journal()));
        }
    }

    @Test @Tag("part4")
    void multipleSymbolsAndSortedSymbolList() {
        desk.submit(buy(1, "B", 10, 50));
        desk.submit(buy(2, "A", 10, 100));
        desk.onExec(new ExecEvent.Ack(1)); desk.onExec(new ExecEvent.Ack(2));
        desk.onExec(new ExecEvent.Fill(1, 1, 10, 50)); desk.onExec(new ExecEvent.Fill(2, 2, 10, 100));
        assertEquals(List.of("A", "B"), desk.symbols());
        assertEquals(List.of(1L, 2L), desk.allOrders().stream().map(v -> v.order().id()).toList());
    }

    @Test @Tag("part4") @Tag("perf")
    void twoHundredThousandEventsReplayFast() {
        TradingDesk d = new TradingDesk(new RiskLimits(1_000, Long.MAX_VALUE, 1_000_000_000L, 1_000_000, 10_000));
        d.setReferencePrice("A", 100);
        assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            long exec = 1;
            for (long id = 1; id <= 50_000; id++) {
                d.submit(new Order(id, "A", id % 2 == 0 ? Side.BUY : Side.SELL, 10, 100));
                d.onExec(new ExecEvent.Ack(id));
                d.onExec(new ExecEvent.Fill(id, exec++, 4, 100));
                d.onExec(new ExecEvent.Fill(id, exec++, 6, 100));
            }
            TradingDesk copy = TradingDesk.replay(new RiskLimits(1_000, Long.MAX_VALUE, 1_000_000_000L, 1_000_000, 10_000), d.journal());
            assertEquals(d.position("A"), copy.position("A"));
        });
    }

    private static void assertSameState(TradingDesk a, TradingDesk b) {
        assertEquals(a.allOrders(), b.allOrders());
        assertEquals(a.symbols(), b.symbols());
        for (String s : a.symbols()) assertEquals(a.position(s), b.position(s), s);
    }
}
