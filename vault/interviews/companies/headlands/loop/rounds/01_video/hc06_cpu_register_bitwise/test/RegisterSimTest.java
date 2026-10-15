import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class RegisterSimTest {

    private static final RegisterSim.Instr[] NONE = {};

    private static List<String> lines(String block) { return block.lines().toList(); }

    private static int apply(int reg, RegisterSim.Update u) { return RegisterSim.apply(reg, u); }

    // ---------- Part 1：解析 + 执行 ----------

    @Test @Tag("part1")
    void parsesEveryBaseMnemonic() {
        assertEquals(new RegisterSim.And(0xFF), RegisterSim.parseLine("AND 0xFF"));
        assertEquals(new RegisterSim.And(255), RegisterSim.parseLine("and 255"));
        assertEquals(new RegisterSim.Or(0b1010), RegisterSim.parseLine("  OR   0b1010 "));
        assertEquals(new RegisterSim.Xor(0xF0), RegisterSim.parseLine("Xor 0XF0"));
        assertEquals(new RegisterSim.Not(), RegisterSim.parseLine("NOT"));
        assertEquals(new RegisterSim.Shl(3), RegisterSim.parseLine("SHL 3"));
        assertEquals(new RegisterSim.Shr(4), RegisterSim.parseLine("SHR 4"));
        assertEquals(new RegisterSim.Rol(5), RegisterSim.parseLine("ROL 5"));
        assertEquals(new RegisterSim.Ror(6), RegisterSim.parseLine("ROR 6"));
        assertEquals(new RegisterSim.SetBit(7), RegisterSim.parseLine("SET 7"));
        assertEquals(new RegisterSim.ClearBit(8), RegisterSim.parseLine("CLEAR 8"));
        assertEquals(new RegisterSim.ToggleBit(31), RegisterSim.parseLine("TOGGLE 31"));
        assertEquals(new RegisterSim.Popcount(), RegisterSim.parseLine("POPCOUNT"));
    }

    @Test @Tag("part1") @Tag("edge")
    void maskOperandsAreUnsigned32Bit() {
        assertEquals(new RegisterSim.And(-1), RegisterSim.parseLine("AND 0xFFFFFFFF"));
        assertEquals(new RegisterSim.Or(Integer.MIN_VALUE), RegisterSim.parseLine("OR 2147483648"));
        assertEquals(new RegisterSim.And(-1), RegisterSim.parseLine("AND 4294967295"));
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(strings = {"", "   ", "FOO", "AND", "AND 1 2", "NOT 3", "POPCOUNT 1", "SHL -1", "SHL 1.5", "SET 32", "SET -1",
            "CLEAR 99", "TOGGLE 3x", "AND 0x1FFFFFFFF", "AND 4294967296", "AND -1", "AND xyz", "AND 0x", "AND 0b2",
            "SHL 99999999999"})
    void rejectsMalformedLines(String bad) {
        assertThrows(RegisterSim.MalformedProgramException.class, () -> RegisterSim.parseLine(bad));
    }

    @Test @Tag("part1") @Tag("edge")
    void recordsGuardTheirOwnInvariants() {
        assertThrows(IllegalArgumentException.class, () -> new RegisterSim.SetBit(32));
        assertThrows(IllegalArgumentException.class, () -> new RegisterSim.ClearBit(-1));
        assertThrows(IllegalArgumentException.class, () -> new RegisterSim.ToggleBit(40));
        assertThrows(IllegalArgumentException.class, () -> new RegisterSim.Shl(-1));
        assertThrows(IllegalArgumentException.class, () -> new RegisterSim.Rol(-5));
    }

    @Test @Tag("part1")
    void parseProgramSkipsCommentsAndBlankLines() {
        var prog = RegisterSim.parseProgram(lines("""
                # a comment

                AND 0xFF
                   # indented comment
                NOT
                """));
        assertEquals(List.of(new RegisterSim.And(255), new RegisterSim.Not()), prog);
        assertEquals(List.of(), RegisterSim.parseProgram(List.of()));
    }

    @Test @Tag("part1")
    void bitwiseTruthTables() {
        assertEquals(0b1000, apply(0b1100, new RegisterSim.And(0b1010)));
        assertEquals(0b1110, apply(0b1100, new RegisterSim.Or(0b1010)));
        assertEquals(0b0110, apply(0b1100, new RegisterSim.Xor(0b1010)));
        assertEquals(0xFFFFFFFF, apply(0, new RegisterSim.Not()));
        assertEquals(0xFFFF0000, apply(0x0000FFFF, new RegisterSim.Not()));
    }

    @Test @Tag("part1") @Tag("edge")
    void shiftsAreLogicalAndDropBits() {
        assertEquals(0, apply(0x80000000, new RegisterSim.Shl(1)));            // 最高位移出去
        assertEquals(1, apply(0x80000000, new RegisterSim.Shr(31)));           // 逻辑右移：补 0，不是补符号位
        assertEquals(0x0F000000, apply(0xF0000000, new RegisterSim.Shr(4)));   // 常见错误：>> 得到 0xFF000000
        assertEquals(0x00000300, apply(0x30, new RegisterSim.Shl(4)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Shl(0)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Shr(0)));
    }

    @Test @Tag("part1") @Tag("edge")
    void shiftsOf32OrMoreClearTheRegister() {
        // Java 的 `reg << 32` 等于 `reg << 0`（位数只取低 5 位）；硬件语义要的是 0
        for (int n : new int[] {32, 33, 64, 1000, Integer.MAX_VALUE}) {
            assertEquals(0, apply(0xFFFFFFFF, new RegisterSim.Shl(n)), "SHL " + n);
            assertEquals(0, apply(0xFFFFFFFF, new RegisterSim.Shr(n)), "SHR " + n);
        }
        assertEquals(0x80000000, apply(0xFFFFFFFF, new RegisterSim.Shl(31)));
        assertEquals(1, apply(0xFFFFFFFF, new RegisterSim.Shr(31)));
    }

    @Test @Tag("part1") @Tag("edge")
    void rotationsWrapAroundAndTakeModulo32() {
        assertEquals(0x23456781, apply(0x12345678, new RegisterSim.Rol(4)));
        assertEquals(0x81234567, apply(0x12345678, new RegisterSim.Ror(4)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Rol(32)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Ror(64)));
        assertEquals(apply(0x12345678, new RegisterSim.Rol(4)), apply(0x12345678, new RegisterSim.Rol(36)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Rol(0)));
        assertEquals(1, apply(0x80000000, new RegisterSim.Rol(1)));
        assertEquals(0x80000000, apply(1, new RegisterSim.Ror(1)));
    }

    @Test @Tag("part1") @Tag("edge")
    void singleBitOperationsAtTheEnds() {
        assertEquals(1, apply(0, new RegisterSim.SetBit(0)));
        assertEquals(0x80000000, apply(0, new RegisterSim.SetBit(31)));
        assertEquals(0x80000000, apply(0x80000000, new RegisterSim.SetBit(31)));      // 幂等
        assertEquals(0x7FFFFFFF, apply(0xFFFFFFFF, new RegisterSim.ClearBit(31)));
        assertEquals(0xFFFFFFFE, apply(0xFFFFFFFF, new RegisterSim.ClearBit(0)));
        assertEquals(0xFFFFFFFF, apply(0xFFFFFFFE, new RegisterSim.SetBit(0)));
        assertEquals(0x80000000, apply(0, new RegisterSim.ToggleBit(31)));
        assertEquals(0, apply(0x80000000, new RegisterSim.ToggleBit(31)));
    }

    @Test @Tag("part1")
    void runSampleProgram() {
        var prog = RegisterSim.parseProgram(lines("""
                AND 0x3C
                SHL 4
                OR 0x0F
                POPCOUNT
                NOT
                SHR 28
                POPCOUNT
                """));
        var r = RegisterSim.run(0xF0, prog);
        assertEquals(List.of(6, 4), r.outputs());
        assertEquals(0xF, r.register());
        assertEquals(15L, r.unsigned());
    }

    @Test @Tag("part1") @Tag("edge")
    void initialValueRange() {
        assertEquals(-1, RegisterSim.run(0xFFFF_FFFFL, List.of()).register());
        assertEquals(4_294_967_295L, RegisterSim.run(0xFFFF_FFFFL, List.of()).unsigned());
        assertEquals(0, RegisterSim.run(0, List.of()).register());
        assertThrows(IllegalArgumentException.class, () -> RegisterSim.run(-1, List.of()));
        assertThrows(IllegalArgumentException.class, () -> RegisterSim.run(1L << 32, List.of()));
    }

    @Test @Tag("part1") @Tag("edge")
    void matchesALongBasedOracle() {
        var rnd = new Random(0);
        for (int round = 0; round < 2_000; round++) {
            long oracle = rnd.nextLong() & 0xFFFF_FFFFL;
            int reg = (int) oracle;
            for (int step = 0; step < 20; step++) {
                int n = rnd.nextInt(40);
                long m = rnd.nextLong() & 0xFFFF_FFFFL;
                switch (rnd.nextInt(8)) {
                    case 0 -> { reg = apply(reg, new RegisterSim.And((int) m)); oracle &= m; }
                    case 1 -> { reg = apply(reg, new RegisterSim.Or((int) m)); oracle |= m; }
                    case 2 -> { reg = apply(reg, new RegisterSim.Xor((int) m)); oracle ^= m; }
                    case 3 -> { reg = apply(reg, new RegisterSim.Not()); oracle = ~oracle & 0xFFFF_FFFFL; }
                    case 4 -> { reg = apply(reg, new RegisterSim.Shl(n)); oracle = n >= 32 ? 0 : (oracle << n) & 0xFFFF_FFFFL; }
                    case 5 -> { reg = apply(reg, new RegisterSim.Shr(n)); oracle = n >= 32 ? 0 : oracle >>> n; }
                    case 6 -> { reg = apply(reg, new RegisterSim.Rol(n)); int k = n % 32;
                        oracle = ((oracle << k) | (oracle >>> (32 - k))) & 0xFFFF_FFFFL; }
                    default -> { reg = apply(reg, new RegisterSim.Ror(n)); int k = n % 32;
                        oracle = ((oracle >>> k) | (oracle << (32 - k))) & 0xFFFF_FFFFL; }
                }
                assertEquals(oracle, Integer.toUnsignedLong(reg), "round " + round + " step " + step);
            }
        }
    }

    // ---------- Part 2：无符号语义 + 输出格式 ----------

    @Test @Tag("part2")
    void unsignedInterpretation() {
        assertEquals(4_294_967_295L, RegisterSim.unsigned(-1));
        assertEquals(2_147_483_648L, RegisterSim.unsigned(Integer.MIN_VALUE));
        assertEquals(0L, RegisterSim.unsigned(0));
        assertEquals(2_147_483_647L, RegisterSim.unsigned(Integer.MAX_VALUE));
        assertEquals("4294967295", RegisterSim.dec(-1));
        assertEquals("2147483648", RegisterSim.dec(Integer.MIN_VALUE));
        assertEquals("0", RegisterSim.dec(0));
    }

    @Test @Tag("part2") @Tag("fmt")
    void hexIsEightUppercaseDigits() {
        assertEquals("0x00000000", RegisterSim.hex(0));
        assertEquals("0x000000FF", RegisterSim.hex(255));
        assertEquals("0xFFFFFFFF", RegisterSim.hex(-1));
        assertEquals("0xDEADBEEF", RegisterSim.hex(0xDEADBEEF));
        assertEquals("0x80000000", RegisterSim.hex(Integer.MIN_VALUE));
    }

    @Test @Tag("part2") @Tag("fmt")
    void binIsThirtyTwoDigitsZeroPadded() {
        assertEquals("00000000000000000000000000000000", RegisterSim.bin(0));
        assertEquals("00000000000000000000000000000101", RegisterSim.bin(5));
        assertEquals("11111111111111111111111111111111", RegisterSim.bin(-1));
        assertEquals("10000000000000000000000000000000", RegisterSim.bin(Integer.MIN_VALUE));
    }

    @Test @Tag("part2") @Tag("fmt")
    void describeJoinsThreeViews() {
        assertEquals("0x0000000F 15 00000000000000000000000000001111", RegisterSim.describe(15));
        assertEquals("0xFFFFFFFF 4294967295 11111111111111111111111111111111", RegisterSim.describe(-1));
    }

    @Test @Tag("part2")
    void parseValueBases() {
        assertEquals(255, RegisterSim.parseValue("255"));
        assertEquals(255, RegisterSim.parseValue("0xFF"));
        assertEquals(255, RegisterSim.parseValue("0Xff"));
        assertEquals(5, RegisterSim.parseValue("0b101"));
        assertEquals(10, RegisterSim.parseValue("010"));                // 十进制，不是八进制
        assertEquals(0, RegisterSim.parseValue("0"));
        assertEquals(0xFFFF_FFFFL, RegisterSim.parseValue("0xFFFFFFFF"));
        assertEquals(0xFFFF_FFFFL, RegisterSim.parseValue("4294967295"));
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(strings = {"", "-1", "+1", "0x", "0b", "0b2", "0xG", "4294967296", "0x100000000", "99999999999999999999", "1_000", "12 3"})
    void parseValueRejects(String bad) {
        assertThrows(RegisterSim.MalformedProgramException.class, () -> RegisterSim.parseValue(bad));
    }

    @Test @Tag("part2")
    void hexRoundTrip() {
        var rnd = new Random(0);
        for (int i = 0; i < 1_000; i++) {
            int x = rnd.nextInt();
            assertEquals(Integer.toUnsignedLong(x), RegisterSim.parseValue(RegisterSim.hex(x)));
            assertEquals(Integer.toUnsignedLong(x), RegisterSim.parseValue(RegisterSim.dec(x)));
            assertEquals(Integer.toUnsignedLong(x), RegisterSim.parseValue("0b" + RegisterSim.bin(x)));
        }
    }

    @Test @Tag("part2") @Tag("fmt")
    void solveSample() {
        var out = RegisterSim.solve(lines("""
                0xF0
                AND 0x3C
                SHL 4
                OR 0x0F
                POPCOUNT
                NOT
                SHR 28
                POPCOUNT
                """));
        assertEquals(List.of("6", "4", "0x0000000F 15 00000000000000000000000000001111"), out);
    }

    @Test @Tag("part2") @Tag("fmt")
    void solveWithNoInstructionsAndWithHighBit() {
        assertEquals(List.of("0x00000000 0 00000000000000000000000000000000"), RegisterSim.solve(List.of("0")));
        assertEquals(List.of("0x80000000 2147483648 10000000000000000000000000000000"),
                RegisterSim.solve(lines("""
                        # initial
                        0

                        SET 31
                        """)));
        assertEquals(List.of("0xFFFFFFFF 4294967295 11111111111111111111111111111111"), RegisterSim.solve(List.of("4294967295")));
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(strings = {"", "# only a comment", "-5", "4294967296", "abc", "0\nFOO", "0\nAND", "0\nSET 32", "0\nSHL -1"})
    void solveMalformed(String text) {
        assertEquals(List.of("Malformed Input"), RegisterSim.solve(text.lines().toList()));
    }

    // ---------- Part 3：扩展指令 ----------

    @Test @Tag("part3")
    void parsesExtendedMnemonics() {
        assertEquals(new RegisterSim.Compress(0xF0), RegisterSim.parseLine("COMPRESS 0xF0"));
        assertEquals(new RegisterSim.Expand(0xF0), RegisterSim.parseLine("expand 0xF0"));
        assertEquals(new RegisterSim.Reverse(), RegisterSim.parseLine("REVERSE"));
        assertEquals(new RegisterSim.ByteSwap(), RegisterSim.parseLine("BSWAP"));
        assertEquals(new RegisterSim.TrailingZeros(), RegisterSim.parseLine("CTZ"));
        assertEquals(new RegisterSim.LeadingZeros(), RegisterSim.parseLine("CLZ"));
        assertThrows(RegisterSim.MalformedProgramException.class, () -> RegisterSim.parseLine("REVERSE 1"));
        assertThrows(RegisterSim.MalformedProgramException.class, () -> RegisterSim.parseLine("COMPRESS"));
    }

    @Test @Tag("part3")
    void compressAndExpandKnownValues() {
        assertEquals(0xB, apply(0xB6, new RegisterSim.Compress(0xF0)));          // 取出高半字节
        assertEquals(0xB0, apply(0xB, new RegisterSim.Expand(0xF0)));            // 放回掩码位置
        assertEquals(0b111, apply(0b10100100, new RegisterSim.Compress(0b10100100)));   // 掩码位上全是 1 → 压成连续的 3 个 1
        assertEquals(0b101, apply(0b10000100, new RegisterSim.Compress(0b10100100)));   // 掩码位 2,5,7 上的值依次是 1,0,1 → 低位在前拼成 101
        assertEquals(0, apply(0xFFFFFFFF, new RegisterSim.Compress(0)));
        assertEquals(0, apply(0xFFFFFFFF, new RegisterSim.Expand(0)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Compress(-1)));
        assertEquals(0x12345678, apply(0x12345678, new RegisterSim.Expand(-1)));
    }

    @Test @Tag("part3") @Tag("edge")
    void compressExpandMatchALoopOracleAndRoundTrip() {
        var rnd = new Random(0);
        for (int i = 0; i < 5_000; i++) {
            int x = rnd.nextInt(), m = rnd.nextInt();
            int expectedCompress = 0, k = 0;
            for (int b = 0; b < 32; b++) if ((m >>> b & 1) != 0) { expectedCompress |= (x >>> b & 1) << k++; }
            assertEquals(expectedCompress, apply(x, new RegisterSim.Compress(m)));
            assertEquals(x & m, apply(apply(x, new RegisterSim.Compress(m)), new RegisterSim.Expand(m)), "expand(compress(x,m),m) == x & m");
        }
    }

    @Test @Tag("part3")
    void reverseAndByteSwap() {
        assertEquals(0x80000000, apply(1, new RegisterSim.Reverse()));
        assertEquals(0, apply(0, new RegisterSim.Reverse()));
        assertEquals(0xF0000000, apply(0x0F, new RegisterSim.Reverse()));
        assertEquals(0x78563412, apply(0x12345678, new RegisterSim.ByteSwap()));
        var rnd = new Random(0);
        for (int i = 0; i < 100; i++) {
            int x = rnd.nextInt();
            assertEquals(x, apply(apply(x, new RegisterSim.Reverse()), new RegisterSim.Reverse()));
            assertEquals(x, apply(apply(x, new RegisterSim.ByteSwap()), new RegisterSim.ByteSwap()));
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void countingQueries() {
        assertEquals(32, RegisterSim.query(0, new RegisterSim.TrailingZeros()));
        assertEquals(3, RegisterSim.query(8, new RegisterSim.TrailingZeros()));
        assertEquals(31, RegisterSim.query(0x80000000, new RegisterSim.TrailingZeros()));
        assertEquals(0, RegisterSim.query(1, new RegisterSim.TrailingZeros()));
        assertEquals(32, RegisterSim.query(0, new RegisterSim.LeadingZeros()));
        assertEquals(31, RegisterSim.query(1, new RegisterSim.LeadingZeros()));
        assertEquals(0, RegisterSim.query(-1, new RegisterSim.LeadingZeros()));
        assertEquals(32, RegisterSim.query(-1, new RegisterSim.Popcount()));
        assertEquals(0, RegisterSim.query(0, new RegisterSim.Popcount()));
        assertEquals(1, RegisterSim.query(0x80000000, new RegisterSim.Popcount()));
    }

    @Test @Tag("part3") @Tag("fmt")
    void extendedProgramEndToEnd() {
        // 0x12345678 -BSWAP→ 0x78563412 (CTZ=1) -COMPRESS 每字节低半字节→ 0x8642 -REVERSE→ 0x42610000 (CLZ=1)
        var out = RegisterSim.solve(lines("""
                0x12345678
                BSWAP
                CTZ
                COMPRESS 0x0F0F0F0F
                REVERSE
                CLZ
                """));
        assertEquals(List.of("1", "1", "0x42610000 1113653248 01000010011000010000000000000000"), out);
    }

    // ---------- Part 4：解码一次 + int[] ----------

    private static RegisterSim.Instr randomInstr(Random rnd) {
        int n = rnd.nextInt(70), m = rnd.nextInt(), b = rnd.nextInt(32);
        return switch (rnd.nextInt(18)) {
            case 0 -> new RegisterSim.And(m);
            case 1 -> new RegisterSim.Or(m);
            case 2 -> new RegisterSim.Xor(m);
            case 3 -> new RegisterSim.Not();
            case 4 -> new RegisterSim.Shl(n);
            case 5 -> new RegisterSim.Shr(n);
            case 6 -> new RegisterSim.Rol(n);
            case 7 -> new RegisterSim.Ror(n);
            case 8 -> new RegisterSim.SetBit(b);
            case 9 -> new RegisterSim.ClearBit(b);
            case 10 -> new RegisterSim.ToggleBit(b);
            case 11 -> new RegisterSim.Compress(m);
            case 12 -> new RegisterSim.Expand(m);
            case 13 -> new RegisterSim.Reverse();
            case 14 -> new RegisterSim.ByteSwap();
            case 15 -> new RegisterSim.Popcount();
            case 16 -> new RegisterSim.TrailingZeros();
            default -> new RegisterSim.LeadingZeros();
        };
    }

    private static List<RegisterSim.Instr> randomProgram(int n, long seed) {
        var rnd = new Random(seed);
        var prog = new ArrayList<RegisterSim.Instr>(n);
        for (int i = 0; i < n; i++) prog.add(randomInstr(rnd));
        return prog;
    }

    @Test @Tag("part4")
    void compiledAgreesWithInterpreterOnSmallPrograms() {
        for (long seed = 0; seed < 300; seed++) {
            var prog = randomProgram(60, seed);
            long init = new Random(seed).nextLong() & 0xFFFF_FFFFL;
            var expected = RegisterSim.run(init, prog);
            assertEquals(expected, RegisterSim.execute(RegisterSim.compile(prog), init), "seed " + seed);
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void compiledEdgeCases() {
        var empty = RegisterSim.compile(List.of());
        assertEquals(new RegisterSim.Run(-1, List.of()), RegisterSim.execute(empty, 0xFFFF_FFFFL));
        var shifts = List.<RegisterSim.Instr>of(new RegisterSim.Shl(32), new RegisterSim.Popcount());
        assertEquals(new RegisterSim.Run(0, List.of(0)), RegisterSim.execute(RegisterSim.compile(shifts), 0xFFFF_FFFFL));
        for (int n : new int[] {0, 1, 31, 32, 33, 63, 2_000_000_000, Integer.MAX_VALUE}) {
            for (RegisterSim.Instr i : new RegisterSim.Instr[] {new RegisterSim.Shl(n), new RegisterSim.Shr(n),
                    new RegisterSim.Rol(n), new RegisterSim.Ror(n)}) {
                var p = List.of(i);
                assertEquals(RegisterSim.run(0x89ABCDEFL, p), RegisterSim.execute(RegisterSim.compile(p), 0x89ABCDEFL), i.toString());
            }
        }
        assertThrows(IllegalArgumentException.class, () -> RegisterSim.execute(empty, -1));
        assertThrows(IllegalArgumentException.class, () -> RegisterSim.execute(empty, 1L << 32));
    }

    @Test @Tag("part4")
    void compilationFoldsBitOpsAndIsReusable() {
        var prog = List.<RegisterSim.Instr>of(new RegisterSim.SetBit(4), new RegisterSim.ClearBit(0), new RegisterSim.ToggleBit(1),
                new RegisterSim.Not(), new RegisterSim.Popcount());
        var c = RegisterSim.compile(prog);
        assertEquals(5, c.ops().length);
        assertEquals(5, c.args().length);
        assertEquals(1, c.queryCount());
        // 同一个 Compiled 可以对不同初值反复执行
        for (long init : new long[] {0, 1, 0xFFFF_FFFFL, 0x1234_5678L})
            assertEquals(RegisterSim.run(init, prog), RegisterSim.execute(c, init));
    }

    @Test @Tag("part4") @Tag("perf")
    void perfTwoMillionInstructions() {
        var prog = randomProgram(2_000_000, 0);
        long init = 0xDEADBEEFL;
        var expected = RegisterSim.run(init, prog);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var c = RegisterSim.compile(prog);
            for (int pass = 0; pass < 20; pass++) assertEquals(expected, RegisterSim.execute(c, init));
        });
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> assertEquals(expected, RegisterSim.run(init, prog)));
    }
}
