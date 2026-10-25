import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.OptionalLong;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** Part 1：解析、坏行计数、按 symbol 汇总。 */
class TradeLogTest {
    static final String SAMPLE = """
            1000,AAPL,187.25,100
            1500,MSFT,410.5,50
            2000,AAPL,187.3,300
            oops
            2500,AAPL,187,100

            3000,msft,410.0,10
            3500,MSFT,410.5000,150
            4000,AAPL,187.25,0
            4500,AAPL,187.2501,400
            """;

    static List<String> lines(String text) {
        return Arrays.asList(text.split("\n", -1));
    }

    // ---------------------------------------------------------------- 价格语法
    @Test @Tag("part1")
    void parsePriceFixedPoint() {
        assertEquals(OptionalLong.of(1_870_000), TradeLog.parsePrice("187"));
        assertEquals(OptionalLong.of(1_872_500), TradeLog.parsePrice("187.25"));
        assertEquals(OptionalLong.of(1_873_000), TradeLog.parsePrice("187.3"));
        assertEquals(OptionalLong.of(1_872_501), TradeLog.parsePrice("187.2501"));
        assertEquals(OptionalLong.of(1), TradeLog.parsePrice("0.0001"));
        assertEquals(OptionalLong.of(5_000), TradeLog.parsePrice("0.5"));
        assertEquals(OptionalLong.of(75_000), TradeLog.parsePrice("007.5"));
        assertEquals(OptionalLong.of(9_999_999_999_999L), TradeLog.parsePrice("999999999.9999"));
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(strings = {"", ".", ".5", "5.", "0", "0.0", "0.0000", "00", "-1", "+1", "-0.5", "1.23456", "1e3", "1E3", " 1", "1 ",
            "1..2", "1.2.3", "1,5", "1234567890", "1234567890.5", "abc", "0x10", "NaN", "٣٤", "1.٣"})
    void parsePriceRejects(String s) {
        assertTrue(TradeLog.parsePrice(s).isEmpty(), "should be malformed: [" + s + "]");
    }

    // ---------------------------------------------------------------- 一行
    @Test @Tag("part1")
    void parseLineValid() {
        assertEquals(new TradeLog.Trade(1000, "AAPL", 1_872_500, 100), TradeLog.parseLine("1000,AAPL,187.25,100").orElseThrow());
        assertEquals(new TradeLog.Trade(0, "BRK.B", 4_000_000, 1), TradeLog.parseLine("0,BRK.B,400,1").orElseThrow());
        assertEquals(new TradeLog.Trade(7, "A1", 1, 999_999_999_999L), TradeLog.parseLine("007,A1,0.0001,999999999999").orElseThrow());
        assertEquals(1_872_500L * 100, TradeLog.parseLine("1000,AAPL,187.25,100").orElseThrow().notional());
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(strings = {
            "oops", ",,,", "1,AAPL,1", "1,AAPL,1,1,", "1,AAPL,1,1,1", "1,AAPL,1,", ",AAPL,1,1", "1,,1,1", "1,AAPL,,1",  // 字段个数 / 空字段
            "1,aapl,1,1", "1,AA PL,1,1", "1,AAPL ,1,1", "1, AAPL,1,1", "1,AAPL-B,1,1", "1,AAPL_B,1,1", "1,AAPLMSFT123,1,1",   // symbol
            "-1,AAPL,1,1", "+1,AAPL,1,1", "1.5,AAPL,1,1", "x,AAPL,1,1", "1234567890123456789,AAPL,1,1", " 1,AAPL,1,1",           // 时间戳
            "1,AAPL,0,1", "1,AAPL,0.0000,1", "1,AAPL,-1,1", "1,AAPL,1.00001,1", "1,AAPL,.5,1", "1,AAPL,1.,1", "1,AAPL,1e2,1",   // 价格
            "1,AAPL,1,0", "1,AAPL,1,-1", "1,AAPL,1,1.5", "1,AAPL,1,1 ", "1,AAPL,1,1\r", "1,AAPL,1,1000000000000", "1,AAPL,1,abc",  // 数量
            "1,AAPL,100000000.0000,10000000",   // price × qty = 1e19 > Long.MAX
            "1,AAPL,303700.0500,3037000500"})   // 3037000500² 刚好溢出
    void parseLineMalformed(String line) {
        assertTrue(TradeLog.parseLine(line).isEmpty(), "should be malformed: [" + line + "]");
    }

    @Test @Tag("part1") @Tag("edge")
    void fieldLengthBoundaries() {
        assertTrue(TradeLog.parseLine("999999999999999999,A,1,1").isPresent());   // 18 位时间戳
        assertTrue(TradeLog.parseLine("1000000000000000000,A,1,1").isEmpty());    // 19 位
        assertTrue(TradeLog.parseLine("1,ABCDEFGHIJ,1,1").isPresent());           // 10 个字符
        assertTrue(TradeLog.parseLine("1,ABCDEFGHIJK,1,1").isEmpty());            // 11 个
        assertTrue(TradeLog.parseLine("1,A,999999999.9999,1").isPresent());
        assertTrue(TradeLog.parseLine("1,A,1000000000,1").isEmpty());             // 整数部分 10 位
        assertTrue(TradeLog.parseLine("1,A,1,999999999999").isPresent());         // 12 位数量
        assertTrue(TradeLog.parseLine("1,A,1,1000000000000").isEmpty());          // 13 位
        // 3037000499² < Long.MAX_VALUE < 3037000500²
        assertTrue(TradeLog.parseLine("1,A,303700.0499,3037000499").isPresent());
        assertEquals(3037000499L * 3037000499L, TradeLog.parseLine("1,A,303700.0499,3037000499").orElseThrow().notional());
    }

    @Test @Tag("part1") @Tag("edge")
    void onlyAsciiDigitsCount() {
        assertTrue(TradeLog.parseLine("١٢٣,AAPL,1,1").isEmpty());     // 阿拉伯-印度数字：Character.isDigit 为 true，但不是 0..9
        assertTrue(TradeLog.parseLine("1,AAPL,1,٣").isEmpty());
        assertTrue(TradeLog.parseLine("1,ＡＡＰＬ,1,1").isEmpty());     // 全角字母
    }

    @Test @Tag("part1") @Tag("edge")
    void tradeConstructorValidates() {
        assertThrows(IllegalArgumentException.class, () -> new TradeLog.Trade(-1, "A", 1, 1));
        assertThrows(IllegalArgumentException.class, () -> new TradeLog.Trade(0, "a", 1, 1));
        assertThrows(IllegalArgumentException.class, () -> new TradeLog.Trade(0, "A", 0, 1));
        assertThrows(IllegalArgumentException.class, () -> new TradeLog.Trade(0, "A", 1, 0));
        assertThrows(ArithmeticException.class, () -> new TradeLog.Trade(0, "A", Long.MAX_VALUE, 2));
        assertThrows(NullPointerException.class, () -> new TradeLog.Trade(0, null, 1, 1));
    }

    // ---------------------------------------------------------------- VWAP 舍入
    @Test @Tag("part1")
    void vwapRoundsHalfUp() {
        assertEquals(3, TradeLog.vwap(5, 2));   // 2.5 → 3
        assertEquals(2, TradeLog.vwap(4, 2));
        assertEquals(0, TradeLog.vwap(1, 3));   // 0.33 → 0
        assertEquals(1, TradeLog.vwap(2, 3));   // 0.67 → 1
        assertEquals(1, TradeLog.vwap(1, 2));   // 0.5 → 1（半数向上）
        assertEquals(1_872_389, TradeLog.vwap(1_685_150_400L, 900)); // 1872389.33
        assertEquals(1_872_390, TradeLog.vwap(1_685_150_400L + 400, 900)); // 1872389.78
    }

    @Test @Tag("part1") @Tag("edge")
    void vwapNeverOverflows() {
        assertEquals(Long.MAX_VALUE, TradeLog.vwap(Long.MAX_VALUE, 1));
        assertEquals(4_611_686_018_427_387_904L, TradeLog.vwap(Long.MAX_VALUE, 2)); // 2^62 - 0.5 → 2^62；2 * r 的写法会在这里溢出
        assertEquals(1, TradeLog.vwap(Long.MAX_VALUE, Long.MAX_VALUE));
        assertEquals(1, TradeLog.vwap(Long.MAX_VALUE / 2 + 1, Long.MAX_VALUE));  // 刚好 0.5
        assertEquals(0, TradeLog.vwap(Long.MAX_VALUE / 2, Long.MAX_VALUE));      // 刚好小于 0.5
        assertThrows(IllegalArgumentException.class, () -> TradeLog.vwap(5, 0));
        assertThrows(IllegalArgumentException.class, () -> TradeLog.vwap(5, -1));
        assertThrows(IllegalArgumentException.class, () -> TradeLog.vwap(-5, 1));
    }

    // ---------------------------------------------------------------- 汇总
    @Test @Tag("part1")
    void analyzeSample() {
        var r = TradeLog.analyze(lines(SAMPLE));
        assertEquals(6, r.accepted());
        assertEquals(3, r.malformed());   // oops、小写 msft、数量 0；空行不算
        assertEquals(List.of(
                new TradeLog.SymbolStats("AAPL", 4, 900, 1_685_150_400L, 1_872_389, 1_870_000, 1_873_000),
                new TradeLog.SymbolStats("MSFT", 2, 200, 821_000_000L, 4_105_000, 4_105_000, 4_105_000)), r.symbols());
    }

    @Test @Tag("part1") @Tag("fmt")
    void renderSample() {
        assertEquals(List.of(
                "AAPL count=4 volume=900 notional=168515.0400 vwap=187.2389 min=187.0000 max=187.3000",
                "MSFT count=2 volume=200 notional=82100.0000 vwap=410.5000 min=410.5000 max=410.5000",
                "accepted=6 malformed=3"), TradeLog.render(TradeLog.analyze(lines(SAMPLE))));
    }

    @Test @Tag("part1") @Tag("fmt")
    void formatPrice() {
        assertEquals("0.0000", TradeLog.formatPrice(0));
        assertEquals("0.0001", TradeLog.formatPrice(1));
        assertEquals("0.5000", TradeLog.formatPrice(5_000));
        assertEquals("187.2500", TradeLog.formatPrice(1_872_500));
        assertEquals("999999999.9999", TradeLog.formatPrice(9_999_999_999_999L));
        assertEquals("922337203685477.5807", TradeLog.formatPrice(Long.MAX_VALUE));
        assertThrows(IllegalArgumentException.class, () -> TradeLog.formatPrice(-1));
        for (long u : new long[] {1, 10, 99_999, 1_872_500, 9_999_999_999_999L}) {
            assertEquals(OptionalLong.of(u), TradeLog.parsePrice(TradeLog.formatPrice(u)));
        }
    }

    @Test @Tag("part1") @Tag("edge")
    void emptyAndBlank() {
        var empty = TradeLog.analyze(List.of());
        assertEquals(new TradeLog.Report(List.of(), 0, 0), empty);
        assertEquals(List.of("accepted=0 malformed=0"), TradeLog.render(empty));
        assertEquals(new TradeLog.Report(List.of(), 0, 0), TradeLog.analyze(List.of("", "", "")));
        // 只含空白的行不是空行：它是坏行
        assertEquals(new TradeLog.Report(List.of(), 0, 3), TradeLog.analyze(List.of(" ", "\t", "\r")));
    }

    @Test @Tag("part1") @Tag("edge")
    void singleTrade() {
        var r = TradeLog.analyze(List.of("5,X,2.5,4"));
        assertEquals(List.of(new TradeLog.SymbolStats("X", 1, 4, 100_000, 25_000, 25_000, 25_000)), r.symbols());
    }

    @Test @Tag("part1") @Tag("edge")
    void symbolsSortedBytewiseAndTimeOrderIrrelevant() {
        var r = TradeLog.analyze(List.of("9,AA,1,1", "3,A1,1,1", "7,A.B,1,1", "1,B,1,1", "8,AA,3,1"));
        assertEquals(List.of("A.B", "A1", "AA", "B"), r.symbols().stream().map(TradeLog.SymbolStats::symbol).toList());
        var aa = r.symbols().get(2);
        assertEquals(2, aa.count());
        assertEquals(10_000, aa.minPrice());
        assertEquals(30_000, aa.maxPrice());
        assertEquals(20_000, aa.vwap());
    }

    @Test @Tag("part1") @Tag("edge")
    void vwapStaysInsideMinMax() {
        // 1 @ 0.0001 和 2 @ 0.0002：notional = 1 + 4 = 5，volume = 3 → 1.67 → 2，仍在 [min, max] 内
        var r = TradeLog.analyze(List.of("1,Q,0.0001,1", "2,Q,0.0002,2"));
        assertEquals(2, r.symbols().get(0).vwap());
        // 两笔 0.0001 各 1：notional 2，volume 2 → 1
        assertEquals(1, TradeLog.analyze(List.of("1,Q,0.0001,1", "2,Q,0.0001,1")).symbols().get(0).vwap());
    }

    @Test @Tag("part1") @Tag("edge")
    void sumOverflowThrows() {
        // 每笔 1e12 × 9e6 = 9e18 装得进 long（< 9.223e18），两笔相加就溢出
        String big = "1,BIG,100000000.0000,9000000";
        assertTrue(TradeLog.parseLine(big).isPresent());
        assertEquals(9_000_000_000_000_000_000L, TradeLog.parseLine(big).orElseThrow().notional());
        assertEquals(1, TradeLog.analyze(List.of(big)).symbols().size());
        assertThrows(ArithmeticException.class, () -> TradeLog.analyze(List.of(big, big)));
        // 不同 symbol 互不影响
        var ok = TradeLog.analyze(List.of(big, "2,BIG2,100000000.0000,9000000"));
        assertEquals(2, ok.symbols().size());
        // 单行乘积溢出是坏行（不抛异常）
        var bad = TradeLog.analyze(List.of("1,BIG,100000000.0000,10000000", "2,OK,1,1"));
        assertEquals(1, bad.malformed());
        assertEquals(1, bad.accepted());
    }

    @Test @Tag("part1") @Tag("edge")
    void nullHandling() {
        assertThrows(NullPointerException.class, () -> TradeLog.analyze(null));
        var withNull = new ArrayList<String>();
        withNull.add("1,A,1,1");
        withNull.add(null);
        assertThrows(NullPointerException.class, () -> TradeLog.analyze(withNull));
    }
}
