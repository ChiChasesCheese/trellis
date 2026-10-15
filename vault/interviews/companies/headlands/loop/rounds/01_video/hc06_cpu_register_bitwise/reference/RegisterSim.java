import java.util.ArrayList;
import java.util.Arrays;
import java.util.HexFormat;
import java.util.List;
import java.util.Locale;

/**
 * Headlands 电面：模拟一个无符号 32 位寄存器。题面见 ../problem.md。
 *
 * 全文的核心约定：寄存器用 int 存。Java 没有无符号 int，但 32 个 bit 是一样的——
 * 0xFFFFFFFF 存进 int 就是 -1。「无符号」只体现在两件事上：(1) 右移用 >>>（补 0）而不是 >>（补符号位）；
 * (2) 打印 / 比较 / 转 long 时用 Integer.toUnsignedString / toUnsignedLong。
 */
public final class RegisterSim {
    private RegisterSim() {}

    // ------------------------------------------------------------------ 指令层次（sealed）

    /**
     * 指令：改寄存器的 Update，或只读寄存器并输出一个数的 Query。
     * 为什么分成两个子接口而不是在一个 switch 里 17 个 case 平铺：「会不会改寄存器」是类型层面的事实，
     * apply() 只接受 Update，写成「返回新寄存器值」的纯函数；Query 的返回值是另一个含义（要输出的数），混在一起会让返回类型含糊。
     */
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

    // Part 3 的指令
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

    /**
     * 数字：十进制 / 0x 十六进制 / 0b 二进制（前缀不分大小写）；范围 0..0xFFFFFFFF；"010" 是十进制 10，不是八进制。
     * 为什么不用 Long.decode：它把前导 0 当八进制，也接受负号和 '#'。题面要的是严格的小语言，所以自己写。
     * 为什么返回 long 而不是 int：0xFFFFFFFF 放不进「非负 int」，要靠 long 才能做范围检查（> 0xFFFFFFFFL 就是非法）。
     * 逐字符 Character.digit 检查是为了拒绝 "+1" / "-1" / "1_0"——Long.parseLong 会接受 "+1"。
     */
    public static long parseValue(String token) {
        String t = token.strip();
        int radix = 10;
        String digits = t;
        if (t.length() > 2 && t.charAt(0) == '0') {
            switch (t.charAt(1)) {
                case 'x', 'X' -> { radix = 16; digits = t.substring(2); }
                case 'b', 'B' -> { radix = 2; digits = t.substring(2); }
                default -> { }
            }
        }
        if (digits.isEmpty() || digits.length() > 40) throw new MalformedProgramException("bad number: '" + token + "'");
        for (int i = 0; i < digits.length(); i++)
            if (Character.digit(digits.charAt(i), radix) < 0) throw new MalformedProgramException("bad number: '" + token + "'");
        long v;
        try {
            v = Long.parseLong(digits, radix);
        } catch (NumberFormatException e) {
            throw new MalformedProgramException("number too large: '" + token + "'");
        }
        if (v > 0xFFFF_FFFFL) throw new MalformedProgramException("number exceeds 32 bits: '" + token + "'");
        return v;
    }

    private static int mask(String[] p) { return (int) parseValue(arg(p)); }

    private static int small(String[] p) {
        String s = arg(p);
        for (int i = 0; i < s.length(); i++)
            if (!Character.isDigit(s.charAt(i))) throw new MalformedProgramException("bad count: '" + s + "'");
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            throw new MalformedProgramException("count too large: '" + s + "'");
        }
    }

    private static String arg(String[] p) {
        if (p.length != 2) throw new MalformedProgramException(p[0] + " takes exactly one operand");
        return p[1];
    }

    private static <T> T bare(String[] p, T instr) {
        if (p.length != 1) throw new MalformedProgramException(p[0] + " takes no operand");
        return instr;
    }

    /**
     * 一行 → 一条指令；助记符不分大小写；任何问题抛 MalformedProgramException。
     * 为什么 catch IllegalArgumentException：记录的紧凑构造器（SetBit(32) 之类）用 IAE 守卫自己的不变量；
     * 在解析边界把它翻译成「输入格式错误」，让上层只需处理一种异常。MalformedProgramException 不是 IAE 的子类，所以不会被误接。
     */
    public static Instr parseLine(String line) {
        String[] p = line.strip().split("\\s+");
        if (p[0].isEmpty()) throw new MalformedProgramException("empty line");
        try {
            return switch (p[0].toUpperCase(Locale.ROOT)) {
                case "AND" -> new And(mask(p));
                case "OR" -> new Or(mask(p));
                case "XOR" -> new Xor(mask(p));
                case "NOT" -> bare(p, new Not());
                case "SHL" -> new Shl(small(p));
                case "SHR" -> new Shr(small(p));
                case "ROL" -> new Rol(small(p));
                case "ROR" -> new Ror(small(p));
                case "SET" -> new SetBit(small(p));
                case "CLEAR" -> new ClearBit(small(p));
                case "TOGGLE" -> new ToggleBit(small(p));
                case "POPCOUNT" -> bare(p, new Popcount());
                case "COMPRESS" -> new Compress(mask(p));
                case "EXPAND" -> new Expand(mask(p));
                case "REVERSE" -> bare(p, new Reverse());
                case "BSWAP" -> bare(p, new ByteSwap());
                case "CTZ" -> bare(p, new TrailingZeros());
                case "CLZ" -> bare(p, new LeadingZeros());
                default -> throw new MalformedProgramException("unknown instruction: " + p[0]);
            };
        } catch (IllegalArgumentException e) {   // 记录的紧凑构造器报的越界（MalformedProgramException 不是 IAE，原样穿过）
            throw new MalformedProgramException(e.getMessage());
        }
    }

    /** 跳过空行与 # 开头的注释行。 */
    public static List<Instr> parseProgram(List<String> lines) {
        var out = new ArrayList<Instr>();
        for (String line : lines) {
            if (line.isBlank() || line.strip().startsWith("#")) continue;
            out.add(parseLine(line));
        }
        return out;
    }

    /**
     * 执行一条改寄存器的指令。移位 ≥ 32 得 0（Java 的 << 会把位数 mod 32，是陷阱）；SHR 是逻辑右移；旋转位数 mod 32。
     * 为什么 switch 没有 default：Update 是 sealed，编译器知道 15 个实现类一个不少；以后新增指令，这里不补分支就编译不过。
     * 为什么 Rol/Ror 直接用 Integer.rotateLeft：它本来就按 mod 32 取位数，而且 JIT 把它当 intrinsic，
     * 在 x86 / ARM 上就是一条旋转指令。
     */
    public static int apply(int reg, Update u) {
        return switch (u) {
            case And(var m) -> reg & m;
            case Or(var m) -> reg | m;
            case Xor(var m) -> reg ^ m;
            case Not _ -> ~reg;
            case Shl(var n) -> n >= 32 ? 0 : reg << n;
            case Shr(var n) -> n >= 32 ? 0 : reg >>> n;
            case Rol(var n) -> Integer.rotateLeft(reg, n);
            case Ror(var n) -> Integer.rotateRight(reg, n);
            case SetBit(var b) -> reg | (1 << b);
            case ClearBit(var b) -> reg & ~(1 << b);
            case ToggleBit(var b) -> reg ^ (1 << b);
            case Compress(var m) -> Integer.compress(reg, m);
            case Expand(var m) -> Integer.expand(reg, m);
            case Reverse _ -> Integer.reverse(reg);
            case ByteSwap _ -> Integer.reverseBytes(reg);
        };
    }

    /** 执行一条 Query，返回要输出的数。bitCount / numberOfTrailingZeros 对 0 的约定：32（不是 -1，也不是异常）。 */
    public static int query(int reg, Query q) {
        return switch (q) {
            case Popcount _ -> Integer.bitCount(reg);
            case TrailingZeros _ -> Integer.numberOfTrailingZeros(reg);
            case LeadingZeros _ -> Integer.numberOfLeadingZeros(reg);
        };
    }

    /** 初值必须在 0..0xFFFFFFFF，否则 IllegalArgumentException。 */
    public static Run run(long initial, List<Instr> program) {
        int reg = checkedInitial(initial);
        var out = new ArrayList<Integer>();
        for (Instr i : program) {
            switch (i) {
                case Update u -> reg = apply(reg, u);
                case Query q -> out.add(query(reg, q));
            }
        }
        return new Run(reg, List.copyOf(out));
    }

    // 为什么初值用 long 传进来：合法范围是 0..2^32-1，int 表示不了「4294967295」这个数本身，
    // 只能先用 long 接住并检查范围，再 (int) 截断——截断后 32 个 bit 完全保留，正是我们要的寄存器内容。
    private static int checkedInitial(long initial) {
        if (initial < 0 || initial > 0xFFFF_FFFFL) throw new IllegalArgumentException("initial out of 0..2^32-1: " + initial);
        return (int) initial;
    }

    // ------------------------------------------------------------------ Part 2：无符号语义 + 输出格式

    public static long unsigned(int reg) { return Integer.toUnsignedLong(reg); }

    /** 十进制，无符号：-1 → "4294967295"。 */
    public static String dec(int reg) { return Integer.toUnsignedString(reg); }

    /** "0x" + 8 位大写十六进制，补零。 */
    public static String hex(int reg) { return "0x" + HexFormat.of().withUpperCase().toHexDigits(reg); }

    /** 32 位二进制，补零。 */
    public static String bin(int reg) {
        // Integer.toBinaryString 不补前导零（5 → "101"），也不带符号（-1 → 32 个 1），所以只需要左边补零到 32 位。
        String raw = Integer.toBinaryString(reg);
        return new StringBuilder(32).repeat('0', 32 - raw.length()).append(raw).toString();
    }

    /** "hex dec bin"，空格分隔。 */
    public static String describe(int reg) { return hex(reg) + " " + dec(reg) + " " + bin(reg); }

    /** 整题：第一个非空非注释行是初值，其余是程序；输出每个 Query 的值各一行，最后一行 describe(终值)。非法 → ["Malformed Input"]。 */
    public static List<String> solve(List<String> lines) {
        try {
            var body = lines.stream().filter(l -> !l.isBlank() && !l.strip().startsWith("#")).toList();
            if (body.isEmpty()) throw new MalformedProgramException("missing initial value");
            long initial = parseValue(body.getFirst());
            Run r = run(initial, parseProgram(body.subList(1, body.size())));
            var out = new ArrayList<String>();
            for (int v : r.outputs()) out.add(Integer.toString(v));
            out.add(describe(r.register()));
            return List.copyOf(out);
        } catch (MalformedProgramException e) {
            return List.of("Malformed Input");
        }
    }

    // ------------------------------------------------------------------ Part 4：解码一次，int[] 操作码

    private static final int AND = 0, OR = 1, XOR = 2, SHL = 3, SHR = 4, ROL = 5, ROR = 6, COMPRESS = 7, EXPAND = 8,
            REVERSE = 9, BSWAP = 10, POPCOUNT = 11, CTZ = 12, CLZ = 13;

    /**
     * 编译后的程序：两个平行的 int[]（操作码 / 操作数）。NOT 与 SET/CLEAR/TOGGLE 在解码时折叠成 XOR/OR/AND。
     * 为什么用两个平行数组而不是 Instr[]：数组元素是连续存放的 int，CPU 缓存按行预取，顺序读很快；
     * 对象数组存的是引用，每条指令还要再跳到堆上的另一块内存，并做一次类型检查。
     * 为什么折叠：执行时少一种分支；NOT x == x ^ 0xFFFFFFFF，SET b == OR (1<<b)，CLEAR b == AND ~(1<<b)，TOGGLE b == XOR (1<<b)。
     */
    public record Compiled(int[] ops, int[] args, int queryCount) {}

    public static Compiled compile(List<Instr> program) {
        int n = program.size();
        int[] ops = new int[n], args = new int[n];
        int queries = 0, k = 0;
        for (Instr i : program) {
            switch (i) {
                case And(var m) -> { ops[k] = AND; args[k] = m; }
                case Or(var m) -> { ops[k] = OR; args[k] = m; }
                case Xor(var m) -> { ops[k] = XOR; args[k] = m; }
                case Not _ -> { ops[k] = XOR; args[k] = -1; }
                case Shl(var c) -> { ops[k] = SHL; args[k] = Math.clamp(c, 0, 32); }
                case Shr(var c) -> { ops[k] = SHR; args[k] = Math.clamp(c, 0, 32); }
                case Rol(var c) -> { ops[k] = ROL; args[k] = c & 31; }
                case Ror(var c) -> { ops[k] = ROR; args[k] = c & 31; }
                case SetBit(var b) -> { ops[k] = OR; args[k] = 1 << b; }
                case ClearBit(var b) -> { ops[k] = AND; args[k] = ~(1 << b); }
                case ToggleBit(var b) -> { ops[k] = XOR; args[k] = 1 << b; }
                case Compress(var m) -> { ops[k] = COMPRESS; args[k] = m; }
                case Expand(var m) -> { ops[k] = EXPAND; args[k] = m; }
                case Reverse _ -> ops[k] = REVERSE;
                case ByteSwap _ -> ops[k] = BSWAP;
                case Popcount _ -> { ops[k] = POPCOUNT; queries++; }
                case TrailingZeros _ -> { ops[k] = CTZ; queries++; }
                case LeadingZeros _ -> { ops[k] = CLZ; queries++; }
            }
            k++;
        }
        return new Compiled(ops, args, queries);
    }

    /**
     * 热循环：只有 int 数组读写和 tableswitch，没有对象、没有类型检查、没有分配。
     * 移位用 long 做：count 已 clamp 到 [0,32]，(int)(u << 32) 与 (u >>> 32) 天然为 0，不需要 `if (n >= 32)`。
     * 为什么这样就没有分支：u 是 reg 零扩展到 64 位的值；long 的 << 位数最多 63，所以 32 位的移位不会被 mod；
     * 左移 32 把原来的 32 个 bit 全部推到高半部分，(int) 强转只留低 32 位——全是 0。
     * 注意：switch (ops[pc]) 本身是一条间接跳转（tableswitch）；操作码序列随机时 CPU 的分支预测器会频繁猜错，
     * 这才是随机程序上主要的开销（见 REPORT 的实测）。
     */
    public static Run execute(Compiled c, long initial) {
        int reg = checkedInitial(initial);
        int[] ops = c.ops(), args = c.args();
        int[] out = new int[c.queryCount()];
        int q = 0;
        for (int pc = 0; pc < ops.length; pc++) {
            int a = args[pc];
            switch (ops[pc]) {
                case AND -> reg &= a;
                case OR -> reg |= a;
                case XOR -> reg ^= a;
                case SHL -> reg = (int) (Integer.toUnsignedLong(reg) << a);
                case SHR -> reg = (int) (Integer.toUnsignedLong(reg) >>> a);
                case ROL -> reg = Integer.rotateLeft(reg, a);
                case ROR -> reg = Integer.rotateRight(reg, a);
                case COMPRESS -> reg = Integer.compress(reg, a);
                case EXPAND -> reg = Integer.expand(reg, a);
                case REVERSE -> reg = Integer.reverse(reg);
                case BSWAP -> reg = Integer.reverseBytes(reg);
                case POPCOUNT -> out[q++] = Integer.bitCount(reg);
                case CTZ -> out[q++] = Integer.numberOfTrailingZeros(reg);
                case CLZ -> out[q++] = Integer.numberOfLeadingZeros(reg);
                default -> throw new IllegalStateException("bad opcode " + ops[pc]);
            }
        }
        return new Run(reg, Arrays.stream(out).boxed().toList());
    }
}
