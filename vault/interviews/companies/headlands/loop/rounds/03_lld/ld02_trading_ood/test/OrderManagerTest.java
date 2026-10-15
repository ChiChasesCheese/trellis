import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 1：订单状态机。 */
class OrderManagerTest {
    static Order buy(long id, String sym, long qty, long px) { return new Order(id, sym, Side.BUY, qty, px); }
    static Order sell(long id, String sym, long qty, long px) { return new Order(id, sym, Side.SELL, qty, px); }

    OrderManager mgr = new OrderManager();

    @Test @Tag("part1")
    void happyPathPartialThenFull() {
        mgr.submit(buy(1, "AAPL", 100, 150));
        assertEquals(OrderStatus.PENDING, mgr.get(1).status());
        assertTrue(mgr.apply(new ExecEvent.Ack(1)));
        assertEquals(OrderStatus.WORKING, mgr.get(1).status());
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 900, 30, 149)));
        var v = mgr.get(1);
        assertEquals(OrderStatus.PARTIALLY_FILLED, v.status());
        assertEquals(30, v.cumQty());
        assertEquals(30 * 149, v.cumNotional());
        assertEquals(70, v.leavesQty());
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 901, 70, 150)));
        v = mgr.get(1);
        assertEquals(OrderStatus.FILLED, v.status());
        assertEquals(0, v.leavesQty());
        assertEquals(30 * 149 + 70 * 150, v.cumNotional());
        assertTrue(mgr.open().isEmpty());
        assertEquals(0, mgr.openCount());
    }

    @Test @Tag("part1")
    void singleFillCompletesOrder() {
        mgr.submit(sell(5, "MSFT", 10, 300));
        mgr.apply(new ExecEvent.Ack(5));
        mgr.apply(new ExecEvent.Fill(5, 1, 10, 301));
        assertEquals(OrderStatus.FILLED, mgr.get(5).status());
    }

    @Test @Tag("part1")
    void duplicateOrderIdRejected() {
        mgr.submit(buy(1, "A", 1, 1));
        assertThrows(IllegalArgumentException.class, () -> mgr.submit(buy(1, "B", 2, 2)));
        assertEquals("A", mgr.get(1).order().symbol());     // 原单没被覆盖
        assertEquals(1, mgr.openCount());
    }

    @Test @Tag("part1") @Tag("edge")
    void unknownOrder() {
        assertThrows(NoSuchElementException.class, () -> mgr.get(42));
        assertThrows(NoSuchElementException.class, () -> mgr.apply(new ExecEvent.Ack(42)));
        assertFalse(mgr.contains(42));
    }

    @Test @Tag("part1")
    void cancelFromWorkingAndPartial() {
        mgr.submit(buy(1, "A", 10, 5));
        mgr.apply(new ExecEvent.Ack(1));
        assertTrue(mgr.apply(new ExecEvent.Cancel(1)));
        assertEquals(OrderStatus.CANCELED, mgr.get(1).status());
        assertEquals(0, mgr.get(1).leavesQty());

        mgr.submit(buy(2, "A", 10, 5));
        mgr.apply(new ExecEvent.Ack(2));
        mgr.apply(new ExecEvent.Fill(2, 7, 4, 5));
        mgr.apply(new ExecEvent.Cancel(2));
        var v = mgr.get(2);
        assertEquals(OrderStatus.CANCELED, v.status());
        assertEquals(4, v.cumQty());                         // 已成交部分保留
        assertEquals(0, v.leavesQty());                      // 剩余部分不再是风险
        assertEquals(0, mgr.openLeaves("A", Side.BUY));
    }

    @Test @Tag("part1")
    void rejectOnlyFromPending() {
        mgr.submit(buy(1, "A", 10, 5));
        assertTrue(mgr.apply(new ExecEvent.Reject(1, "bad symbol")));
        var v = mgr.get(1);
        assertEquals(OrderStatus.REJECTED, v.status());
        assertEquals("bad symbol", v.rejectReason());
        assertEquals(0, v.leavesQty());

        mgr.submit(buy(2, "A", 10, 5));
        mgr.apply(new ExecEvent.Ack(2));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Reject(2, "late")));
        assertEquals(OrderStatus.WORKING, mgr.get(2).status());
    }

    @Test @Tag("part1") @Tag("edge")
    void illegalTransitionsLeaveStateUntouched() {
        mgr.submit(buy(1, "A", 10, 5));
        // PENDING 不能 Fill / Cancel
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Fill(1, 1, 1, 5)));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Cancel(1)));
        assertEquals(0, mgr.get(1).cumQty());
        mgr.apply(new ExecEvent.Ack(1));
        // 重复 Ack 非法
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Ack(1)));
        mgr.apply(new ExecEvent.Cancel(1));
        // 终态之后什么都不能做
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Cancel(1)));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Ack(1)));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Fill(1, 2, 1, 5)));
        assertEquals(OrderStatus.CANCELED, mgr.get(1).status());
    }

    @Test @Tag("part1") @Tag("edge")
    void overfillRejectedAndNotRecorded() {
        mgr.submit(buy(1, "A", 10, 5));
        mgr.apply(new ExecEvent.Ack(1));
        mgr.apply(new ExecEvent.Fill(1, 1, 6, 5));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Fill(1, 2, 5, 5)));   // 6+5 > 10
        assertEquals(6, mgr.get(1).cumQty());
        // execId 2 没有被记入「已见过」：同一个 execId 用合法数量重发应当成功
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 2, 4, 5)));
        assertEquals(OrderStatus.FILLED, mgr.get(1).status());
    }

    @Test @Tag("part1") @Tag("edge")
    void fillPriceMustRespectLimit() {
        mgr.submit(buy(1, "A", 10, 100));
        mgr.apply(new ExecEvent.Ack(1));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Fill(1, 1, 1, 101)));   // 买单不能高于限价
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 2, 1, 100)));                                              // 等于限价合法
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 3, 1, 90)));                                               // 价格改善合法

        mgr.submit(sell(2, "A", 10, 100));
        mgr.apply(new ExecEvent.Ack(2));
        assertThrows(IllegalTransitionException.class, () -> mgr.apply(new ExecEvent.Fill(2, 4, 1, 99)));
        assertTrue(mgr.apply(new ExecEvent.Fill(2, 5, 1, 100)));
        assertTrue(mgr.apply(new ExecEvent.Fill(2, 6, 1, 120)));
    }

    @Test @Tag("part1") @Tag("edge")
    void duplicateFillIsIdempotent() {
        mgr.submit(buy(1, "A", 10, 5));
        mgr.apply(new ExecEvent.Ack(1));
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 77, 4, 5)));
        assertFalse(mgr.apply(new ExecEvent.Fill(1, 77, 4, 5)));      // 重复投递
        assertEquals(4, mgr.get(1).cumQty());
        assertTrue(mgr.apply(new ExecEvent.Fill(1, 78, 6, 5)));
        assertEquals(OrderStatus.FILLED, mgr.get(1).status());
        // 订单已 FILLED 后，旧回报再来一次：仍然只是重复，不是非法转移
        assertFalse(mgr.apply(new ExecEvent.Fill(1, 77, 4, 5)));
        assertFalse(mgr.apply(new ExecEvent.Fill(1, 78, 6, 5)));
        assertEquals(10, mgr.get(1).cumQty());
    }

    @Test @Tag("part1")
    void openOrdersListedByIdAndExcludeTerminal() {
        for (long id : new long[]{9, 3, 7, 1}) mgr.submit(buy(id, "A", 5, 5));
        mgr.apply(new ExecEvent.Reject(3, "x"));
        List<Long> ids = mgr.open().stream().map(v -> v.order().id()).toList();
        assertEquals(List.of(1L, 7L, 9L), ids);
        assertEquals(List.of(1L, 3L, 7L, 9L), mgr.all().stream().map(v -> v.order().id()).toList());
        assertEquals(3, mgr.openCount());
    }

    @Test @Tag("part1")
    void openLeavesBySymbolAndSide() {
        mgr.submit(buy(1, "A", 10, 5));
        mgr.submit(buy(2, "A", 7, 5));
        mgr.submit(sell(3, "A", 4, 5));
        mgr.submit(buy(4, "B", 100, 5));
        assertEquals(17, mgr.openLeaves("A", Side.BUY));
        assertEquals(4, mgr.openLeaves("A", Side.SELL));
        assertEquals(100, mgr.openLeaves("B", Side.BUY));
        assertEquals(0, mgr.openLeaves("C", Side.BUY));
        mgr.apply(new ExecEvent.Ack(1));
        mgr.apply(new ExecEvent.Fill(1, 1, 3, 5));
        assertEquals(14, mgr.openLeaves("A", Side.BUY));
        mgr.apply(new ExecEvent.Cancel(1));
        assertEquals(7, mgr.openLeaves("A", Side.BUY));
        mgr.apply(new ExecEvent.Reject(2, "r"));
        assertEquals(0, mgr.openLeaves("A", Side.BUY));
    }

    @Test @Tag("part1") @Tag("edge")
    void recordsRejectInvalidValues() {
        assertThrows(IllegalArgumentException.class, () -> new Order(0, "A", Side.BUY, 1, 1));
        assertThrows(IllegalArgumentException.class, () -> new Order(1, "A", Side.BUY, 0, 1));
        assertThrows(IllegalArgumentException.class, () -> new Order(1, "A", Side.BUY, 1, -1));
        assertThrows(IllegalArgumentException.class, () -> new Order(1, " ", Side.BUY, 1, 1));
        assertThrows(IllegalArgumentException.class, () -> new ExecEvent.Fill(1, 1, 0, 1));
        assertThrows(NullPointerException.class, () -> mgr.submit(null));
    }

    @Test @Tag("part1") @Tag("edge")
    void notionalOverflowDoesNotCorruptOrder() {
        mgr.submit(buy(1, "A", Long.MAX_VALUE / 2, Long.MAX_VALUE / 2));
        mgr.apply(new ExecEvent.Ack(1));
        assertThrows(ArithmeticException.class,
                () -> mgr.apply(new ExecEvent.Fill(1, 1, Long.MAX_VALUE / 2, Long.MAX_VALUE / 2)));
        assertEquals(0, mgr.get(1).cumQty());
        assertEquals(OrderStatus.WORKING, mgr.get(1).status());
    }

    /** 随机事件流对照一个朴素模型：每步之后 openLeaves / openCount 与逐单重算一致，非法事件不改状态。 */
    @Test @Tag("part1") @Tag("edge")
    void randomEventsKeepAggregatesConsistent() {
        Random rnd = new Random(7);
        long execId = 0;
        String[] syms = {"A", "B", "C"};
        for (long id = 1; id <= 300; id++) mgr.submit(new Order(id, syms[rnd.nextInt(3)], rnd.nextBoolean() ? Side.BUY : Side.SELL, 1 + rnd.nextInt(20), 100));
        for (int step = 0; step < 4000; step++) {
            long id = 1 + rnd.nextInt(300);
            ExecEvent e = switch (rnd.nextInt(4)) {
                case 0 -> new ExecEvent.Ack(id);
                case 1 -> new ExecEvent.Fill(id, ++execId, 1 + rnd.nextInt(5), 100);
                case 2 -> new ExecEvent.Cancel(id);
                default -> new ExecEvent.Reject(id, "r");
            };
            var before = mgr.get(id);
            try {
                mgr.apply(e);
            } catch (IllegalTransitionException ex) {
                assertEquals(before, mgr.get(id));
            }
            if (step % 97 == 0) checkAggregates(syms);
        }
        checkAggregates(syms);
    }

    private void checkAggregates(String[] syms) {
        int open = 0;
        for (String s : syms) for (Side side : Side.values()) {
            long sum = 0;
            for (var v : mgr.open()) if (v.order().symbol().equals(s) && v.order().side() == side) sum += v.leavesQty();
            assertEquals(sum, mgr.openLeaves(s, side));
        }
        open = mgr.open().size();
        assertEquals(open, mgr.openCount());
    }
}
