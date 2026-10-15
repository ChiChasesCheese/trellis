import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 2：仓位与盈亏（FIFO，整数）。 */
class PositionBookTest {
    PositionBook book = new PositionBook();

    @Test @Tag("part2")
    void unknownSymbolIsFlat() {
        assertEquals(Position.flat("X"), book.get("X"));
        assertEquals(0, book.netQty("X"));
        assertEquals(0, book.totalRealized());
        assertTrue(book.symbols().isEmpty());
    }

    @Test @Tag("part2")
    void buildLongThenCloseAtProfit() {
        book.onFill("A", Side.BUY, 10, 100);
        book.onFill("A", Side.BUY, 10, 110);
        var p = book.get("A");
        assertEquals(20, p.netQty());
        assertEquals(10 * 100 + 10 * 110, p.openCost());
        assertEquals(0, p.realizedPnl());
        book.onFill("A", Side.SELL, 15, 120);          // FIFO：先平 10@100，再平 5@110
        p = book.get("A");
        assertEquals(5, p.netQty());
        assertEquals(5 * 110, p.openCost());
        assertEquals(10 * (120 - 100) + 5 * (120 - 110), p.realizedPnl());
        book.onFill("A", Side.SELL, 5, 100);           // 亏损平仓
        p = book.get("A");
        assertEquals(0, p.netQty());
        assertEquals(0, p.openCost());
        assertEquals(250 + 5 * (100 - 110), p.realizedPnl());
    }

    @Test @Tag("part2")
    void shortPositionPnlSignsAreMirrored() {
        book.onFill("A", Side.SELL, 10, 100);
        assertEquals(-10, book.netQty("A"));
        assertEquals(1000, book.get("A").openCost());
        book.onFill("A", Side.BUY, 4, 90);             // 空头回补，价格更低 → 赚
        assertEquals(4 * 10, book.get("A").realizedPnl());
        book.onFill("A", Side.BUY, 6, 130);            // 回补更贵 → 亏
        var p = book.get("A");
        assertEquals(0, p.netQty());
        assertEquals(40 + 6 * (100 - 130), p.realizedPnl());
    }

    @Test @Tag("part2") @Tag("edge")
    void flipThroughZeroOpensOppositeLotAtFillPrice() {
        book.onFill("A", Side.BUY, 10, 100);
        book.onFill("A", Side.SELL, 25, 110);          // 平 10 手（+100），翻成空 15 @110
        var p = book.get("A");
        assertEquals(-15, p.netQty());
        assertEquals(15 * 110, p.openCost());
        assertEquals(100, p.realizedPnl());
        book.onFill("A", Side.BUY, 15, 105);           // 回补 15 @105：赚 15*5
        p = book.get("A");
        assertEquals(0, p.netQty());
        assertEquals(100 + 75, p.realizedPnl());
        assertEquals(0, p.openCost());
        // 回到 flat 之后可以再朝任意方向开仓
        book.onFill("A", Side.SELL, 1, 50);
        assertEquals(-1, book.netQty("A"));
    }

    @Test @Tag("part2") @Tag("edge")
    void exactCloseGoesFlatNotNegativeZeroLots() {
        book.onFill("A", Side.BUY, 7, 10);
        book.onFill("A", Side.SELL, 7, 10);
        assertEquals(Position.flat("A").netQty(), book.get("A").netQty());
        assertEquals(0, book.get("A").realizedPnl());
        book.onFill("A", Side.BUY, 3, 11);
        assertEquals(3, book.netQty("A"));
        assertEquals(33, book.get("A").openCost());
    }

    @Test @Tag("part2")
    void symbolsAreIndependentAndSorted() {
        book.onFill("MSFT", Side.BUY, 1, 10);
        book.onFill("AAPL", Side.SELL, 2, 20);
        book.onFill("GOOG", Side.BUY, 3, 30);
        book.onFill("AAPL", Side.BUY, 2, 15);
        assertEquals(List.of("AAPL", "GOOG", "MSFT"), book.symbols());
        assertEquals(10, book.get("AAPL").realizedPnl());
        assertEquals(10, book.totalRealized());
        assertEquals(1, book.netQty("MSFT"));
    }

    @Test @Tag("part2")
    void unrealizedPnl() {
        book.onFill("A", Side.BUY, 10, 100);
        book.onFill("A", Side.BUY, 10, 120);
        assertEquals(20 * 130 - 2200, book.get("A").unrealizedPnl(130));
        assertEquals(20 * 90 - 2200, book.get("A").unrealizedPnl(90));       // 负的
        book.onFill("B", Side.SELL, 5, 200);
        assertEquals(1000 - 5 * 190, book.get("B").unrealizedPnl(190));        // 空头：价格跌 → 赚
        assertEquals(1000 - 5 * 210, book.get("B").unrealizedPnl(210));
        assertEquals(0, book.get("Z").unrealizedPnl(1234));
    }

    @Test @Tag("part2") @Tag("edge")
    void invalidInputsRejected() {
        assertThrows(IllegalArgumentException.class, () -> book.onFill("A", Side.BUY, 0, 10));
        assertThrows(IllegalArgumentException.class, () -> book.onFill("A", Side.BUY, 1, 0));
        assertThrows(NullPointerException.class, () -> book.onFill(null, Side.BUY, 1, 1));
        assertThrows(NullPointerException.class, () -> book.onFill("A", null, 1, 1));
    }

    @Test @Tag("part2") @Tag("edge")
    void overflowThrowsAndLeavesPositionUnchanged() {
        book.onFill("A", Side.BUY, 4_000_000_000L, 1);
        book.onFill("A", Side.SELL, 1, 4_000_000_000L * 3);     // 先建立一个正常状态：平掉 1 手，赚 12e9 - 1
        var before = book.get("A");
        // 乘积 (px - lotPx) * qty 超过 Long.MAX_VALUE
        assertThrows(ArithmeticException.class, () -> book.onFill("A", Side.SELL, 3_000_000_000L, Long.MAX_VALUE / 2));
        assertEquals(before, book.get("A"));
    }

    /** 对照一个朴素 O(n) 实现：把所有成交摊成逐手 FIFO，逐手配对。 */
    @Test @Tag("part2") @Tag("edge")
    void randomFillsMatchUnitByUnitModel() {
        Random rnd = new Random(11);
        java.util.ArrayDeque<Long> units = new java.util.ArrayDeque<>();   // 每个元素 = 一手的开仓价
        int dir = 0;
        long realized = 0;
        for (int i = 0; i < 2000; i++) {
            Side side = rnd.nextBoolean() ? Side.BUY : Side.SELL;
            long qty = 1 + rnd.nextInt(8), px = 90 + rnd.nextInt(21);
            book.onFill("A", side, qty, px);
            for (long u = 0; u < qty; u++) {
                if (dir == 0 || dir == side.sign()) { units.addLast(px); dir = side.sign(); }
                else {
                    long open = units.pollFirst();
                    realized += dir * (px - open);
                    if (units.isEmpty()) dir = 0;
                }
            }
            var p = book.get("A");
            assertEquals(dir * units.size(), p.netQty());
            assertEquals(realized, p.realizedPnl());
            assertEquals(units.stream().mapToLong(Long::longValue).sum(), p.openCost());
        }
    }

    @Test @Tag("part2") @Tag("perf")
    void manyFillsFast() {
        Random rnd = new Random(0);
        org.junit.jupiter.api.Assertions.assertTimeoutPreemptively(java.time.Duration.ofSeconds(2), () -> {
            for (int i = 0; i < 300_000; i++) book.onFill("S" + (i % 50), rnd.nextBoolean() ? Side.BUY : Side.SELL, 1 + rnd.nextInt(5), 100 + rnd.nextInt(10));
        });
    }
}
