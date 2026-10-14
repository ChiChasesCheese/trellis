/**
 * J19 例 2：内联（inlining）。热点循环里调用的小方法，JIT 会把它的代码直接"贴进"调用处，消除调用开销，并让后续优化看到更大的代码块。
 * 观察：java --enable-preview -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining J19Ex2Inline | grep -E "J19Ex2Inline::(add|square|tooBig)"
 */
public class J19Ex2Inline {
    static long square(long x) { return x * x; }                       // 极小，必内联
    static long add(long a, long b) { return a + square(b); }          // 内联进循环，square 再内联进 add

    static long tooBig(long x) {                                        // 故意写长：字节码超过 FreqInlineSize(325) 就不会内联
        long r = x;
        r = r * 3 + 1; r = r * 5 + 2; r = r * 7 + 3; r = r * 11 + 4; r = r * 13 + 5; r = r * 17 + 6; r = r * 19 + 7;
        r = r * 23 + 8; r = r * 29 + 9; r = r * 31 + 10; r = r * 37 + 11; r = r * 41 + 12; r = r * 43 + 13; r = r * 47 + 14;
        r = r * 53 + 15; r = r * 59 + 16; r = r * 61 + 17; r = r * 67 + 18; r = r * 71 + 19; r = r * 73 + 20; r = r * 79 + 21;
        r = r * 83 + 22; r = r * 89 + 23; r = r * 97 + 24; r = r * 101 + 25; r = r * 103 + 26; r = r * 107 + 27; r = r * 109 + 28;
        r = r * 113 + 29; r = r * 127 + 30; r = r * 131 + 31; r = r * 137 + 32; r = r * 139 + 33; r = r * 149 + 34; r = r * 151 + 35;
        r = r * 157 + 36; r = r * 163 + 37; r = r * 167 + 38; r = r * 173 + 39; r = r * 179 + 40; r = r * 181 + 41; r = r * 191 + 42;
        r = r * 193 + 43; r = r * 197 + 44; r = r * 199 + 45; r = r * 211 + 46; r = r * 223 + 47; r = r * 227 + 48; r = r * 229 + 49;
        return r;
    }

    public static void main(String[] args) {
        long s = 0;
        for (int i = 0; i < 5_000_000; i++) {
            s = add(s, i);
            s ^= tooBig(i);
        }
        System.out.println(s);
    }
}
