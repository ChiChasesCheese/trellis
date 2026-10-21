/** J15 例 1（最简单）：Math 的 Exact 家族、ceilDiv / floorMod、clamp。 */
public class J15Ex1 {
    static void tryIt(String label, java.util.function.LongSupplier s) {
        try { System.out.println(label + " = " + s.getAsLong()); }
        catch (ArithmeticException e) { System.out.println(label + " -> ArithmeticException: " + e.getMessage()); }
    }

    public static void main(String[] args) {
        // 1. Exact：溢出时抛 ArithmeticException，而不是静默回绕
        tryIt("addExact(MAX, 1)", () -> Math.addExact(Long.MAX_VALUE, 1L));
        tryIt("multiplyExact(4e9, 3e9)", () -> Math.multiplyExact(4_000_000_000L, 3_000_000_000L));
        tryIt("toIntExact(3e9)", () -> Math.toIntExact(3_000_000_000L));
        tryIt("negateExact(MIN)", () -> Math.negateExact(Long.MIN_VALUE));   // -MIN 本身放不下
        tryIt("absExact(MIN)", () -> Math.absExact(Long.MIN_VALUE));         // Math.abs(MIN) 会返回 MIN（仍是负数！）
        System.out.println("Math.abs(Long.MIN_VALUE) = " + Math.abs(Long.MIN_VALUE) + "   <- 老 API 的陷阱");
        tryIt("incrementExact(MAX)", () -> Math.incrementExact(Long.MAX_VALUE));

        // 2. 整除的方向：/ 向 0 截断；floorDiv 向 -∞；ceilDiv 向 +∞（Java 18）
        System.out.println("-7 / 2 = " + (-7 / 2) + ", floorDiv = " + Math.floorDiv(-7, 2) + ", ceilDiv = " + Math.ceilDiv(-7, 2));
        System.out.println("7 / 2  = " + (7 / 2) + ", floorDiv = " + Math.floorDiv(7, 2) + ", ceilDiv = " + Math.ceilDiv(7, 2));
        // 取余：% 的符号跟被除数；floorMod 的符号跟除数（做环形下标不会出负数）
        System.out.println("-7 % 5 = " + (-7 % 5) + ", floorMod(-7, 5) = " + Math.floorMod(-7, 5));
        // 经典用途：需要几页/几批？
        System.out.println("103 条记录每页 25 条 -> 页数 = " + Math.ceilDiv(103, 25));

        // 3. clamp（Java 21）：限制到 [min, max]
        System.out.println("clamp(150, 0, 100) = " + Math.clamp(150, 0, 100));
        System.out.println("clamp(-5, 0, 100)  = " + Math.clamp(-5, 0, 100));
        int shift = Math.clamp(40L, 0, 32);           // 注意：(long, int, int) 重载返回 int
        System.out.println("clamp(40L, 0, 32)  = " + shift);
        System.out.println("clamp(3.7, 0.0, 1.0) = " + Math.clamp(3.7, 0.0, 1.0));
        try { Math.clamp(5, 10, 0); } catch (IllegalArgumentException e) { System.out.println("min > max -> IllegalArgumentException"); }
    }
}
