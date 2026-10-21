/** String identity, interning, hash caching, immutability. */
public class K05Strings {
    public static void main(String[] a) {
        String s1 = "hello", s2 = "hel" + "lo";                 // compile-time constant folding
        String part = "hel"; String s3 = part + "lo";            // runtime concat -> new object
        String s4 = new String("hello");
        System.out.println("literal == folded literal : " + (s1 == s2));
        System.out.println("literal == runtime concat : " + (s1 == s3));
        System.out.println("literal == new String     : " + (s1 == s4));
        System.out.println("literal == s3.intern()    : " + (s1 == s3.intern()));
        System.out.println("equals                    : " + s1.equals(s3));
        // hash is cached in the object: second call is a field read
        String big = "x".repeat(50_000_000);
        long t0 = System.nanoTime(); int h1 = big.hashCode(); long t1 = System.nanoTime(); int h2 = big.hashCode(); long t2 = System.nanoTime();
        System.out.printf("hashCode of 50M chars: first %d us, second %d us (cached)%n", (t1 - t0) / 1000, (t2 - t1) / 1000);
        // substring copies (since 7u6), so a small substring does not pin the big one
        String sub = big.substring(0, 3);
        System.out.println("substring length " + sub.length() + " independent of source: yes (copy)");
        // concat in a loop is O(n^2)
        for (int n : new int[]{20_000, 40_000, 80_000}) {
            long q0 = System.nanoTime(); String r = ""; for (int i = 0; i < n; i++) r += "x";
            long q1 = System.nanoTime(); StringBuilder sb = new StringBuilder(); for (int i = 0; i < n; i++) sb.append('x');
            long q2 = System.nanoTime();
            System.out.printf("n=%6d  += %6d ms | StringBuilder %3d ms%n", n, (q1 - q0) / 1_000_000, (q2 - q1) / 1_000_000);
        }
    }
}
