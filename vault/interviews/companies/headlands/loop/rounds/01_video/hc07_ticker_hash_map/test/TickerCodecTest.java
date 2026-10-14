import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;

class TickerCodecTest {

    @Test @Tag("part2")
    void documentedEncoding() {
        // A=1, A=1, P=16, L=12，每个 5 比特，从第 39 位往下排，其余补 0
        long expected = (1L << 35) | (1L << 30) | (16L << 25) | (12L << 20);
        assertEquals(expected, TickerCodec.pack("AAPL"));
        assertEquals(1L << 35, TickerCodec.pack("A"));
        assertEquals((26L << 35) | (26L << 30) | (26L << 25) | (26L << 20) | (26L << 15) | (26L << 10) | (26L << 5) | 26L,
                TickerCodec.pack("ZZZZZZZZ"));
        assertEquals(new TickerCodec.Ticker(expected), TickerCodec.parse("AAPL"));
    }

    @Test @Tag("part2")
    void roundTrip() {
        for (String t : new String[] {"A", "AB", "IBM", "AAPL", "GOOGL", "BRKBXX", "ABCDEFG", "ABCDEFGH"})
            assertEquals(t, TickerCodec.unpack(TickerCodec.pack(t)));
        var r = new Random(0);
        for (String t : Tickers.random(r, 20_000, 8)) assertEquals(t, TickerCodec.unpack(TickerCodec.pack(t)));
    }

    @Test @Tag("part2")
    void distinctTickersGetDistinctPositiveKeys() {
        var seen = new HashSet<Long>();
        for (String t : Tickers.allThreeLetters()) {
            long k = TickerCodec.pack(t);
            assertTrue(k > 0 && k < (1L << 40));
            assertTrue(seen.add(k), "collision at " + t);
        }
        // 前缀关系不能混淆：A、AA、AAA 是三个不同的代码
        assertEquals(3, new HashSet<>(java.util.List.of(TickerCodec.pack("A"), TickerCodec.pack("AA"), TickerCodec.pack("AAA"))).size());
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @NullSource
    @ValueSource(strings = {"", "ABCDEFGHI", "aapl", "AaPL", "BRK.B", "BRK-B", "A1", "A B", " AAPL", "AAPL ", "É", "ＡＢ"})
    void invalidTickers(String bad) {
        var parsed = TickerCodec.parse(bad);
        assertInstanceOf(TickerCodec.Invalid.class, parsed);
        assertFalse(((TickerCodec.Invalid) parsed).reason().isBlank());
        assertThrows(IllegalArgumentException.class, () -> TickerCodec.pack(bad));
    }

    @Test @Tag("part2") @Tag("edge")
    void acceptsAnyCharSequence() {
        assertEquals(TickerCodec.pack("MSFT"), TickerCodec.pack(new StringBuilder("MSFT")));
    }

    @Test @Tag("part2") @Tag("edge")
    void invalidKeysCannotBeUnpacked() {
        long[] bad = {0, -1, Long.MIN_VALUE, Long.MAX_VALUE, 1L << 40,
                (1L << 35) | (1L << 25),            // A 空 A：0 之后又出现字符
                27L << 35,                          // 字段 27 不是字母
                31L << 35, 1L};                     // 最后一个字段有值但前面全空
        for (long k : bad) {
            assertFalse(TickerCodec.isValidKey(k), "isValidKey(" + k + ")");
            assertThrows(IllegalArgumentException.class, () -> TickerCodec.unpack(k));
        }
        assertTrue(TickerCodec.isValidKey(TickerCodec.pack("QQQ")));
    }

    private static byte[] wire(String s) { return s.getBytes(StandardCharsets.US_ASCII); }

    @Test @Tag("part2")
    void wireFormatMatchesStringPacking() {
        assertEquals(TickerCodec.pack("AAPL"), TickerCodec.packWire(wire("AAPL    "), 0));
        assertEquals(TickerCodec.pack("A"), TickerCodec.packWire(wire("A       "), 0));
        assertEquals(TickerCodec.pack("ABCDEFGH"), TickerCodec.packWire(wire("ABCDEFGH"), 0));
        // 报文里夹在别的字段中间
        byte[] msg = wire("xx12AAPL    yy");
        assertEquals(TickerCodec.pack("AAPL"), TickerCodec.packWire(msg, 4));
        var r = new Random(1);
        for (String t : Tickers.random(r, 5000, 8)) {
            byte[] padded = wire((t + "        ").substring(0, 8));
            assertEquals(TickerCodec.pack(t), TickerCodec.packWire(padded, 0));
        }
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(strings = {"        ", " AAPL   ", "AA PL   ", "aapl    ", "AAPL\0\0\0\0", "AAP1    ", "AAPL.B  "})
    void malformedWireFields(String bad) {
        assertThrows(IllegalArgumentException.class, () -> TickerCodec.packWire(wire(bad), 0));
    }

    @Test @Tag("part2") @Tag("edge")
    void wireFieldMustFitInTheBuffer() {
        assertThrows(IndexOutOfBoundsException.class, () -> TickerCodec.packWire(wire("AAPL"), 0));
        assertThrows(IndexOutOfBoundsException.class, () -> TickerCodec.packWire(wire("AAPL    "), 1));
        assertThrows(IndexOutOfBoundsException.class, () -> TickerCodec.packWire(wire("AAPL    "), -1));
    }
}
