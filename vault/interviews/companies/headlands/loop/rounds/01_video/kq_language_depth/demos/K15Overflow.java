/** Defined integer semantics: Java wraps (C++ signed overflow is UB; Python has bigints). */
public class K15Overflow {
    public static void main(String[] a) {
        int m = Integer.MAX_VALUE;
        System.out.println("MAX+1 = " + (m + 1) + "  (wraps, defined by JLS)");
        try { Math.addExact(m, 1); } catch (ArithmeticException e) { System.out.println("Math.addExact -> " + e.getMessage()); }
        System.out.println("-7 / 2 = " + (-7 / 2) + ", -7 % 2 = " + (-7 % 2) + ", Math.floorMod(-7,2) = " + Math.floorMod(-7, 2) + "   (Python: -4, 1)");
        System.out.println("0.1+0.2 == 0.3 ? " + (0.1 + 0.2 == 0.3));
        System.out.println("(int) 3_000_000_000L = " + (int) 3_000_000_000L + ", (byte) 200 = " + (byte) 200);
        System.out.println("1 << 33 = " + (1 << 33) + " (shift count masked to 5 bits), 1L << 33 = " + (1L << 33));
    }
}
