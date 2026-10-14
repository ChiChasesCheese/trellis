import java.util.List;

/**
 * Headlands 电面：模拟一个无符号 32 位寄存器。题面见 ../problem.md。
 * Java 没有无符号 int：寄存器用 int 存 32 位，「按无符号解释」是你要处处小心的地方。
 */
public final class RegisterSim {
    private RegisterSim() {}

    // ------------------------------------------------------------------ 指令层次（已给出）

    /** 指令：改寄存器的 Update，或只读寄存器并输出一个数的 Query。 */
    public sealed interface Instr permits Update, Query {}

    public sealed interface Update extends Instr
            permits And, Or, Xor, Not, Shl, Shr, Rol, Ror, SetBit, ClearBit, ToggleBit, Compress, Expand, Reverse, ByteSwap {}

    public sealed interface Query extends Instr permits Popcount, TrailingZeros, LeadingZeros {}

    // Part 1 的指令
    public record And(int mask) implements Update {}
    public record Or(int mask) implements Update {}
    public record Xor(int mask) implements Update {}
    public record Not() implements Update {}
    public record Shl(int count) implements Update {
        public Shl { if (count < 0) throw new IllegalArgumentException("count < 0: " + count); }
    }
    public record Shr(int count) implements Update {
        public Shr { if (count < 0) throw new IllegalArgumentException("count < 0: " + count); }
    }
    public record Rol(int count) implements Update {
        public Rol { if (count < 0) throw new IllegalArgumentException("count < 0: " + count); }
    }
    public record Ror(int count) implements Update {
        public Ror { if (count < 0) throw new IllegalArgumentException("count < 0: " + count); }
    }
    public record SetBit(int bit) implements Update {
        public SetBit { checkBit(bit); }
    }
    public record ClearBit(int bit) implements Update {
        public ClearBit { checkBit(bit); }
    }
    public record ToggleBit(int bit) implements Update {
        public ToggleBit { checkBit(bit); }
    }
    public record Popcount() implements Query {}

    // Part 3 的指令（Part 1 的 switch 里先对它们抛 UnsupportedOperationException 或直接实现都行）
    public record Compress(int mask) implements Update {}
    public record Expand(int mask) implements Update {}
    public record Reverse() implements Update {}
    public record ByteSwap() implements Update {}
    public record TrailingZeros() implements Query {}
    public record LeadingZeros() implements Query {}

    private static void checkBit(int bit) {
        if (bit < 0 || bit > 31) throw new IllegalArgumentException("bit out of 0..31: " + bit);
    }

    public static final class MalformedProgramException extends RuntimeException {
        public MalformedProgramException(String msg) { super(msg); }
    }

    /** 运行结果：寄存器终值（int 存 32 位，按无符号解释）+ 各 Query 的输出。 */
    public record Run(int register, List<Integer> outputs) {
        public long unsigned() { return Integer.toUnsignedLong(register); }
    }

    // ------------------------------------------------------------------ Part 1：解析 + 执行

    /** 数字：十进制 / 0x 十六进制 / 0b 二进制；范围 0..0xFFFFFFFF；"010" 是十进制 10；非法抛 MalformedProgramException。 */
    public static long parseValue(String token) { throw new UnsupportedOperationException("TODO"); }

    /** 一行 → 一条指令；助记符不分大小写；操作数个数 / 取值不对抛 MalformedProgramException（记录构造器的 IAE 也要转换）。 */
    public static Instr parseLine(String line) { throw new UnsupportedOperationException("TODO"); }

    /** 跳过空行与 # 开头的注释行。 */
    public static List<Instr> parseProgram(List<String> lines) { throw new UnsupportedOperationException("TODO"); }

    /** 执行一条 Update。移位 ≥ 32 得 0；SHR 是逻辑右移；旋转位数 mod 32。试试对 sealed 类型写穷尽的模式匹配 switch。 */
    public static int apply(int reg, Update u) { throw new UnsupportedOperationException("TODO"); }

    /** 执行一条 Query，返回要输出的数。 */
    public static int query(int reg, Query q) { throw new UnsupportedOperationException("TODO"); }

    /** 初值必须在 0..0xFFFFFFFF，否则 IllegalArgumentException。 */
    public static Run run(long initial, List<Instr> program) { throw new UnsupportedOperationException("TODO"); }

    // ------------------------------------------------------------------ Part 2：无符号语义 + 输出格式

    public static long unsigned(int reg) { throw new UnsupportedOperationException("TODO"); }

    /** 十进制，无符号：-1 → "4294967295"。 */
    public static String dec(int reg) { throw new UnsupportedOperationException("TODO"); }

    /** "0x" + 8 位大写十六进制，补零。提示：HexFormat。 */
    public static String hex(int reg) { throw new UnsupportedOperationException("TODO"); }

    /** 32 位二进制，补零。 */
    public static String bin(int reg) { throw new UnsupportedOperationException("TODO"); }

    /** "hex dec bin"，空格分隔。 */
    public static String describe(int reg) { throw new UnsupportedOperationException("TODO"); }

    /** 整题：首个有效行是初值，其余是程序；每个 Query 输出一行，最后一行 describe(终值)；非法 → ["Malformed Input"]。 */
    public static List<String> solve(List<String> lines) { throw new UnsupportedOperationException("TODO"); }

    // ------------------------------------------------------------------ Part 4：解码一次，int[] 操作码

    /** 编译后的程序：两个平行的 int[]（操作码 / 操作数）+ Query 的个数。NOT 与 SET/CLEAR/TOGGLE 可以在解码时折叠成 XOR/OR/AND。 */
    public record Compiled(int[] ops, int[] args, int queryCount) {}

    /** 解码一次：List<Instr> → int[]。移位位数在这里 clamp 到 [0,32]，旋转位数 & 31。 */
    public static Compiled compile(List<Instr> program) { throw new UnsupportedOperationException("TODO"); }

    /** 热循环：只做 int 数组读写 + switch，不分配对象（返回值除外）。结果必须与 run() 完全相同。 */
    public static Run execute(Compiled c, long initial) { throw new UnsupportedOperationException("TODO"); }
}
