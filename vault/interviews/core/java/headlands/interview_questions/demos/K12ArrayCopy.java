import java.util.Arrays;

/** System.arraycopy = memmove semantics (overlap safe) + type checks; timing vs a hand loop. */
public class K12ArrayCopy {
    static final long[] SMALL = new long[16], SMALL2 = new long[16];
    public static void main(String[] a) {
        int[] x = {1, 2, 3, 4, 5, 6};
        System.arraycopy(x, 0, x, 2, 4);                 // overlapping, forward: memcpy would be UB in C
        System.out.println("overlap copy (src=0,dst=2,len=4): " + Arrays.toString(x));
        Object[] objs = new String[2];
        try { System.arraycopy(new Object[]{1}, 0, objs, 0, 1); } catch (ArrayStoreException e) { System.out.println("ArrayStoreException: " + e.getMessage()); }
        try { System.arraycopy(x, 0, x, 5, 4); } catch (ArrayIndexOutOfBoundsException e) { System.out.println("bounds: " + e.getMessage()); }

        byte[] src = new byte[64 << 20], dst = new byte[64 << 20];
        for (int r = 0; r < 4; r++) {
            long t0 = System.nanoTime(); System.arraycopy(src, 0, dst, 0, src.length); long t1 = System.nanoTime();
            for (int i = 0; i < src.length; i++) dst[i] = src[i]; long t2 = System.nanoTime();
            byte[] c = Arrays.copyOf(src, src.length); long t3 = System.nanoTime();
            System.out.printf("64MB: arraycopy %4d ms | for-loop %4d ms | Arrays.copyOf (alloc+zero+copy) %4d ms%n", (t1 - t0) / 1_000_000, (t2 - t1) / 1_000_000, (t3 - t2) / 1_000_000);
        }
        for (int r = 0; r < 3; r++) {
            long acc = 0; long t0 = System.nanoTime();
            for (int i = 0; i < 50_000_000; i++) { SMALL[0] = i; System.arraycopy(SMALL, 0, SMALL2, 0, 16); acc += SMALL2[0]; }
            long t1 = System.nanoTime();
            System.out.printf("16-long arraycopy + store + load: %.2f ns/iter (acc=%d)%n", (t1 - t0) / 50_000_000.0, acc);
        }
    }
}
