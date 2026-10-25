import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 4：byte[] 上的热路径解析，结果必须和 Part 1 的 String 版逐字段一致。 */
class FastLogTest {
    static byte[] bytes(String s) {
        return s.getBytes(StandardCharsets.ISO_8859_1);
    }

    /** 慢版本：按 '\n' 切行（不用 String.lines()，它还会在 '\r' 处断行）。 */
    static TradeLog.Report slow(String text) {
        return TradeLog.analyze(Arrays.asList(text.split("\n", -1)));
    }

    static void same(String text) {
        assertEquals(slow(text), FastLog.analyze(bytes(text)), "text: " + text.replace("\n", "⏎"));
    }

    @Test @Tag("part4")
    void sampleMatchesStringVersion() {
        var r = FastLog.analyze(bytes(TradeLogTest.SAMPLE));
        assertEquals(6, r.accepted());
        assertEquals(3, r.malformed());
        assertEquals(TradeLog.analyze(TradeLogTest.lines(TradeLogTest.SAMPLE)), r);
        assertEquals(1_872_389, r.symbols().get(0).vwap());
    }

    @Test @Tag("part4") @Tag("edge")
    void emptyAndBlank() {
        assertEquals(new TradeLog.Report(List.of(), 0, 0), FastLog.analyze(new byte[0]));
        assertEquals(new TradeLog.Report(List.of(), 0, 0), FastLog.analyze(bytes("\n\n\n")));
        same("");
        same("\n");
        same(" \n\t\n\r\n");           // 只含空白的行是坏行
    }

    @Test @Tag("part4") @Tag("edge")
    void lastLineWithoutNewline() {
        same("1,A,1,1\n2,A,3,1");
        same("1,A,1,1\n2,A,3,1\n");
        same("1,A,1,1\n\n\n2,A,3,1\n\n");
        assertEquals(2, FastLog.analyze(bytes("1,A,1,1\n2,A,3,1")).accepted());
    }

    @Test @Tag("part4") @Tag("edge")
    void everyMalformedClassAgreesWithStringVersion() {
        String[] bad = {"oops", ",,,", "1,AAPL,1", "1,AAPL,1,1,", "1,AAPL,1,1,1", "1,AAPL,1,", ",AAPL,1,1", "1,,1,1", "1,AAPL,,1",
                "1,aapl,1,1", "1,AA PL,1,1", "1,AAPL ,1,1", "1,AAPL-B,1,1", "1,AAPLMSFT123,1,1", "-1,AAPL,1,1", "+1,AAPL,1,1",
                "1.5,AAPL,1,1", "1234567890123456789,AAPL,1,1", "1,AAPL,0,1", "1,AAPL,0.0000,1", "1,AAPL,-1,1", "1,AAPL,1.00001,1",
                "1,AAPL,.5,1", "1,AAPL,1.,1", "1,AAPL,1e2,1", "1,AAPL,1,0", "1,AAPL,1,-1", "1,AAPL,1,1.5", "1,AAPL,1,1\r",
                "1,AAPL,1,1000000000000", "1,AAPL,1234567890,1", "1,AAPL,100000000.0000,10000000", "1,AAPL,303700.0500,3037000500"};
        for (String line : bad) {
            var r = FastLog.analyze(bytes(line));
            assertEquals(new TradeLog.Report(List.of(), 0, 1), r, "should be malformed: [" + line + "]");
        }
        String[] good = {"0,A,1,1", "999999999999999999,A,1,1", "1,ABCDEFGHIJ,1,1", "1,A.B.C,1,1", "1,A,999999999.9999,1",
                "1,A,0.0001,999999999999", "007,A,007.5,0001", "1,BIG,303700.0499,3037000499", "1,A,5.5000,1"};
        for (String line : good) assertEquals(1, FastLog.analyze(bytes(line)).accepted(), "should be valid: [" + line + "]");
        same(String.join("\n", bad) + "\n" + String.join("\n", good));
    }

    @Test @Tag("part4") @Tag("edge")
    void highBytesAndNulAreMalformedNotCrashes() {
        // byte 是有符号的：0xE9 当数组下标会变成负数
        var data = new byte[] {'1', ',', 'A', (byte) 0xE9, ',', '1', ',', '1', '\n', '1', ',', 'B', ',', '1', ',', '1', '\n',
                0, '\n', (byte) 0xFF, (byte) 0x80, '\n', '1', ',', 'C', ',', '1', ',', '1', 0};
        var r = FastLog.analyze(data);
        assertEquals(1, r.accepted());
        assertEquals(4, r.malformed());
        assertEquals("B", r.symbols().get(0).symbol());
    }

    @Test @Tag("part4") @Tag("edge")
    void overflowBehavesLikeTheStringVersion() {
        String big = "1,BIG,100000000.0000,9000000";
        assertThrows(ArithmeticException.class, () -> FastLog.analyze(bytes(big + "\n" + big)));
        assertThrows(ArithmeticException.class, () -> TradeLog.analyze(TradeLogTest.lines(big + "\n" + big)));
        same(big + "\n2,BIG2,100000000.0000,9000000");
        same("1,BIG,100000000.0000,10000000\n2,OK,1,1"); // 单行乘积溢出 = 坏行
        assertThrows(NullPointerException.class, () -> FastLog.analyze(null));
    }

    static String symbolOf(int n) {
        // 把 n 写成 37 进制：A–Z、0–9、'.'，最多 10 位
        String alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.";
        var sb = new StringBuilder();
        do {
            sb.append(alphabet.charAt(n % 37));
            n /= 37;
        } while (n > 0);
        return sb.toString();
    }

    @Test @Tag("part4") @Tag("edge")
    void tableGrowsAndKeepsEverySymbol() {
        var sb = new StringBuilder();
        for (int i = 0; i < 30_000; i++) sb.append(i).append(',').append(symbolOf(i)).append(',').append(1 + i % 50).append('.').append(i % 7).append(',').append(1 + i % 9).append('\n');
        sb.append("5,ZZZZZZZZZZ,1,1\n5,9999999999,1,1\n5,..........,1,1\n"); // 10 个字符，各 6 位：满 60 位
        same(sb.toString());
        assertEquals(30_003, FastLog.analyze(bytes(sb.toString())).symbols().size());
    }

    @Test @Tag("part4")
    void fuzzMatchesStringVersion() {
        var rnd = new Random(42);
        String junk = ",.0123456789ABCz- \r+eEé";
        for (int round = 0; round < 40; round++) {
            var sb = new StringBuilder();
            for (int i = 0; i < 500; i++) {
                var line = new StringBuilder("%d,%s,%d.%d,%d".formatted(rnd.nextInt(100_000), symbolOf(rnd.nextInt(60)),
                        rnd.nextInt(1000), rnd.nextInt(10_000), rnd.nextInt(5_000)));
                int edits = rnd.nextInt(3);   // 大多数行改 0–2 处：删、改、插
                for (int e = 0; e < edits && line.length() > 0; e++) {
                    int at = rnd.nextInt(line.length());
                    switch (rnd.nextInt(3)) {
                        case 0 -> line.deleteCharAt(at);
                        case 1 -> line.setCharAt(at, junk.charAt(rnd.nextInt(junk.length())));
                        default -> line.insert(at, junk.charAt(rnd.nextInt(junk.length())));
                    }
                }
                sb.append(line).append(rnd.nextInt(30) == 0 ? "\n\n" : "\n");
            }
            same(sb.toString());
        }
    }

    // ---------------------------------------------------------------- 性能
    record Gen(byte[] data, long accepted, long malformed, long volume, long notional) {}

    /** n 行，symbolCount 个不同的 symbol，大约 1% 的坏行；同时用最直接的办法记下期望的总量。 */
    static Gen generate(int n, int symbolCount, long seed) {
        var rnd = new Random(seed);
        String[] syms = new String[symbolCount];
        for (int i = 0; i < symbolCount; i++) syms[i] = symbolOf(i * 7919 + 13);
        var sb = new StringBuilder(n * 30);
        long accepted = 0, malformed = 0, volume = 0, notional = 0;
        for (int i = 0; i < n; i++) {
            int whole = 1 + rnd.nextInt(999), digits = rnd.nextInt(5), frac = digits == 0 ? 0 : rnd.nextInt((int) Math.pow(10, digits));
            long qty = 1 + rnd.nextInt(5000);
            String price = digits == 0 ? Integer.toString(whole) : "%d.%0" + digits + "d";
            price = digits == 0 ? price : price.formatted(whole, frac);
            long units = whole * 10_000L + (digits == 0 ? 0 : frac * (long) Math.pow(10, 4 - digits));
            sb.append(1_700_000_000_000L + i).append(',').append(syms[rnd.nextInt(symbolCount)]).append(',');
            if (rnd.nextInt(100) == 0) { // 坏行：价格前多一个 x，或者数量为 0
                sb.append(rnd.nextBoolean() ? "x" + price + "," + qty : price + ",0").append('\n');
                malformed++;
                continue;
            }
            sb.append(price).append(',').append(qty).append('\n');
            accepted++;
            volume += qty;
            notional += units * qty;
        }
        return new Gen(sb.toString().getBytes(StandardCharsets.ISO_8859_1), accepted, malformed, volume, notional);
    }

    @Test @Tag("part4") @Tag("perf")
    void oneMillionLinesFastAndAllocationLight() {
        var g = generate(1_000_000, 2_000, 5);
        assertTrue(g.data().length > 30_000_000, "input should be ~35 MB, got " + g.data().length);
        var mx = (com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean();
        // 先在小数据上热身，让 JIT 编译热点循环；计时的是第二次完整运行
        var warm = generate(200_000, 2_000, 1);
        FastLog.analyze(warm.data());
        FastLog.analyze(warm.data());
        long[] allocated = new long[1];
        var r = assertTimeoutPreemptively(Duration.ofSeconds(1), () -> {
            long tid = Thread.currentThread().threadId();
            long before = mx.getThreadAllocatedBytes(tid);
            var rep = FastLog.analyze(g.data());
            allocated[0] = mx.getThreadAllocatedBytes(tid) - before;
            return rep;
        });
        assertEquals(g.accepted(), r.accepted());
        assertEquals(g.malformed(), r.malformed());
        assertEquals(g.volume(), r.symbols().stream().mapToLong(TradeLog.SymbolStats::volume).sum());
        assertEquals(g.notional(), r.symbols().stream().mapToLong(TradeLog.SymbolStats::notional).sum());
        assertEquals(2_000, r.symbols().size());
        // 每行建一个 String / Trade 的写法要几百 MB；这里只允许哈希表和结果本身
        assertTrue(allocated[0] < 4 * 1024 * 1024, "allocated " + allocated[0] + " bytes");
    }

    @Test @Tag("part4") @Tag("perf")
    void stringVersionAgreesOnALargeInput() {
        var g = generate(200_000, 500, 9);
        var text = new String(g.data(), StandardCharsets.ISO_8859_1);
        assertEquals(slow(text), FastLog.analyze(g.data()));
    }
}
