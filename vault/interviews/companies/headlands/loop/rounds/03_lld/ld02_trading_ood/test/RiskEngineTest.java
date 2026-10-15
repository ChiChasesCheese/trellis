import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 3：交易前风控。 */
class RiskEngineTest {
    // maxQty 1000, maxNotional 1_000_000, maxPos 5000, maxOpen 3, band 500bp (5%)
    static final RiskLimits LIMITS = new RiskLimits(1_000, 1_000_000, 5_000, 3, 500);

    PositionBook positions = new PositionBook();
    OrderManager orders = new OrderManager();
    RiskEngine risk = new RiskEngine(LIMITS);

    RiskEngineTest() { risk.setReferencePrice("A", 100); }

    static Order buy(long id, long qty, long px) { return new Order(id, "A", Side.BUY, qty, px); }
    static Order sell(long id, long qty, long px) { return new Order(id, "A", Side.SELL, qty, px); }

    RiskResult check(Order o) { return risk.check(o, positions, orders); }

    void assertRejected(RiskReason reason, Order o) {
        assertEquals(new RiskResult.Rejected(reason), check(o), () -> o.toString());
    }

    @Test @Tag("part3")
    void acceptsOrdinaryOrder() {
        assertTrue(check(buy(1, 100, 100)).isAccepted());
        assertSame(RiskResult.ACCEPTED, check(buy(1, 100, 100)));
    }

    @Test @Tag("part3")
    void quantityLimitBoundary() {
        assertEquals(RiskResult.ACCEPTED, check(buy(1, 1_000, 100)));
        assertRejected(RiskReason.QTY_LIMIT, buy(2, 1_001, 100));
    }

    @Test @Tag("part3")
    void notionalLimitBoundary() {
        RiskEngine r = new RiskEngine(new RiskLimits(1_000_000, 10_000, 1_000_000, 10, 10_000));
        r.setReferencePrice("A", 100);
        assertEquals(RiskResult.ACCEPTED, r.check(buy(1, 100, 100), positions, orders));         // 10_000 == 上限，通过
        assertEquals(new RiskResult.Rejected(RiskReason.NOTIONAL_LIMIT), r.check(buy(2, 101, 100), positions, orders));
    }

    @Test @Tag("part3") @Tag("edge")
    void notionalOverflowIsRejectedNotWrapped() {
        RiskEngine r = new RiskEngine(new RiskLimits(Long.MAX_VALUE, Long.MAX_VALUE, Long.MAX_VALUE, 10, 10_000));
        r.setReferencePrice("A", Long.MAX_VALUE / 2);
        // px * qty 溢出 long：不能回绕成一个小数字而通过
        var res = r.check(new Order(1, "A", Side.BUY, 1L << 40, 1L << 40), positions, orders);
        assertEquals(new RiskResult.Rejected(RiskReason.NOTIONAL_LIMIT), res);
    }

    @Test @Tag("part3")
    void priceBandBoundaryIsInclusive() {
        assertEquals(RiskResult.ACCEPTED, check(buy(1, 10, 105)));          // +5.00% == 带宽
        assertEquals(RiskResult.ACCEPTED, check(buy(2, 10, 95)));           // -5.00%
        assertRejected(RiskReason.PRICE_BAND, buy(3, 10, 106));
        assertRejected(RiskReason.PRICE_BAND, sell(4, 10, 94));
        assertRejected(RiskReason.PRICE_BAND, sell(5, 10, 1));              // 胖手指：少打一个 0
    }

    @Test @Tag("part3") @Tag("edge")
    void priceBandUsesIntegerArithmeticNoRounding() {
        risk.setReferencePrice("B", 10_007);               // 5% = 500.35：501 超，500 不超
        assertEquals(RiskResult.ACCEPTED, risk.check(new Order(1, "B", Side.BUY, 1, 10_507), positions, orders));
        assertEquals(new RiskResult.Rejected(RiskReason.PRICE_BAND), risk.check(new Order(2, "B", Side.BUY, 1, 10_508), positions, orders));
        risk.setReferencePrice("B", 3);                    // 5% of 3 = 0.15 → 只有 px == 3 通过
        assertEquals(RiskResult.ACCEPTED, risk.check(new Order(3, "B", Side.BUY, 1, 3), positions, orders));
        assertEquals(new RiskResult.Rejected(RiskReason.PRICE_BAND), risk.check(new Order(4, "B", Side.BUY, 1, 4), positions, orders));
    }

    @Test @Tag("part3")
    void missingReferencePriceFailsClosed() {
        assertEquals(new RiskResult.Rejected(RiskReason.NO_REFERENCE_PRICE),
                check(new Order(1, "ZZZ", Side.BUY, 1, 1)));
    }

    @Test @Tag("part3")
    void referencePriceCanBeUpdated() {
        assertRejected(RiskReason.PRICE_BAND, buy(1, 1, 200));
        risk.setReferencePrice("A", 200);
        assertEquals(RiskResult.ACCEPTED, check(buy(2, 1, 200)));
        assertThrows(IllegalArgumentException.class, () -> risk.setReferencePrice("A", 0));
    }

    @Test @Tag("part3")
    void openOrdersLimitCountsAllSymbolsAndPendingOrders() {
        orders.submit(buy(1, 1, 100));                                      // PENDING 也算
        orders.submit(new Order(2, "B", Side.SELL, 1, 100));
        orders.submit(buy(3, 1, 100));
        assertRejected(RiskReason.OPEN_ORDERS_LIMIT, buy(4, 1, 100));
        orders.apply(new ExecEvent.Reject(2, "x"));                         // 终结后释放名额
        assertEquals(RiskResult.ACCEPTED, check(buy(4, 1, 100)));
    }

    @Test @Tag("part3")
    void positionLimitCountsExistingNetPosition() {
        positions.onFill("A", Side.BUY, 4_500, 100);
        assertEquals(RiskResult.ACCEPTED, check(buy(1, 500, 100)));         // 4500 + 500 == 5000
        assertRejected(RiskReason.POSITION_LIMIT, buy(2, 501, 100));
        // 卖出是减仓，不受多头限额影响；卖到空头一侧才受限
        assertEquals(RiskResult.ACCEPTED, check(sell(3, 1_000, 100)));
    }

    @Test @Tag("part3")
    void positionLimitCountsOpenOrdersWorstCase() {
        orders.submit(buy(1, 1_000, 100));
        orders.submit(buy(2, 1_000, 100));
        orders.apply(new ExecEvent.Ack(1));
        orders.apply(new ExecEvent.Ack(2));
        positions.onFill("A", Side.BUY, 2_500, 100);
        // 净仓 2500 + 未完成买单 2000 = 4500：再买 500 恰好顶格，501 超（只看净仓的话 2500+501 完全没问题）
        assertEquals(RiskResult.ACCEPTED, check(buy(3, 500, 100)));
        assertRejected(RiskReason.POSITION_LIMIT, buy(3, 501, 100));
        // 订单 1 全部成交：1000 从「未完成」移到「净仓」，总暴露不变，结论不变
        orders.apply(new ExecEvent.Fill(1, 1, 1_000, 100));
        positions.onFill("A", Side.BUY, 1_000, 100);
        assertEquals(RiskResult.ACCEPTED, check(buy(3, 500, 100)));
        assertRejected(RiskReason.POSITION_LIMIT, buy(3, 501, 100));
        // 订单 2 撤销：释放 1000
        orders.apply(new ExecEvent.Cancel(2));
        assertEquals(RiskResult.ACCEPTED, check(buy(3, 1_000, 100)));
    }

    @Test @Tag("part3") @Tag("edge")
    void positionLimitWorstCaseShortSide() {
        RiskEngine r = new RiskEngine(new RiskLimits(1_000, 1_000_000, 5_000, 10, 500));
        r.setReferencePrice("A", 100);
        orders.submit(sell(1, 1_000, 100));
        orders.submit(sell(2, 1_000, 100));
        positions.onFill("A", Side.SELL, 2_500, 100);                       // 净 -2500，未完成卖 2000：最坏 -4500
        assertEquals(RiskResult.ACCEPTED, r.check(sell(3, 500, 100), positions, orders));        // -5000 == 下限
        orders.submit(sell(3, 500, 100));
        assertEquals(new RiskResult.Rejected(RiskReason.POSITION_LIMIT), r.check(sell(4, 1, 100), positions, orders));
        assertEquals(RiskResult.ACCEPTED, r.check(buy(5, 1, 100), positions, orders));            // 买单不增加空头暴露
    }

    @Test @Tag("part3")
    void positionLimitIsPerSymbol() {
        risk.setReferencePrice("B", 50);
        positions.onFill("A", Side.BUY, 5_000, 100);
        assertEquals(RiskResult.ACCEPTED, risk.check(new Order(1, "B", Side.BUY, 1_000, 50), positions, orders));
        assertRejected(RiskReason.POSITION_LIMIT, buy(2, 1, 100));
    }

    @Test @Tag("part3")
    void haltRejectsEverythingUntilResume() {
        risk.halt();
        assertTrue(risk.halted());
        assertRejected(RiskReason.HALTED, buy(1, 1, 100));
        assertRejected(RiskReason.HALTED, sell(2, 1, 100));          // 减仓单也拒绝：kill switch 不挑单
        risk.resume();
        assertFalse(risk.halted());
        assertEquals(RiskResult.ACCEPTED, check(buy(3, 1, 100)));
    }

    @Test @Tag("part3") @Tag("edge")
    void firstViolatedCheckIsReportedInDeclaredOrder() {
        // 同时违反：数量、名义金额、价带 → 报 QTY_LIMIT
        assertRejected(RiskReason.QTY_LIMIT, buy(1, 2_000, 1_000));
        // 同时违反：名义金额、价带 → 报 NOTIONAL_LIMIT
        RiskEngine r = new RiskEngine(new RiskLimits(1_000, 1_000, 5_000, 3, 500));
        r.setReferencePrice("A", 100);
        assertEquals(new RiskResult.Rejected(RiskReason.NOTIONAL_LIMIT), r.check(buy(2, 10, 1_000), positions, orders));
        // halted 压过一切
        risk.halt();
        assertRejected(RiskReason.HALTED, new Order(3, "ZZZ", Side.BUY, 5_000_000, 1));
    }

    @Test @Tag("part3")
    void checkDoesNotMutateAnything() {
        orders.submit(buy(1, 10, 100));
        var before = orders.all();
        for (int i = 0; i < 10; i++) check(buy(100 + i, 10, 100));
        assertEquals(before, orders.all());
        assertEquals(1, orders.openCount());
        assertEquals(0, positions.netQty("A"));
    }

    @Test @Tag("part3") @Tag("edge")
    void limitsMustBePositive() {
        assertThrows(IllegalArgumentException.class, () -> new RiskLimits(0, 1, 1, 1, 1));
        assertThrows(IllegalArgumentException.class, () -> new RiskLimits(1, 1, 1, 0, 1));
        assertThrows(IllegalArgumentException.class, () -> new RiskLimits(1, 1, 1, 1, 0));
    }
}
