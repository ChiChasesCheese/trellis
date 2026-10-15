/**
 * Warm-up, inlining via class-hierarchy analysis, and deoptimisation.
 * Phase 1: one implementation seen  -> monomorphic, call inlined.
 * Phase 2: second class loaded       -> bimorphic.
 * Phase 3: third class               -> megamorphic -> vtable/itable call, not inlined.
 * Run plain, then with:  -XX:+PrintCompilation   (grep for "made not entrant")
 */
public class K10Jit {
    interface Shape { int area(int x); }
    static final class Sq implements Shape { public int area(int x) { return x * x; } }
    static final class Tri implements Shape { public int area(int x) { return x * x / 2; } }
    static final class Cir implements Shape { public int area(int x) { return x * 3; } }

    static int run(Shape[] ss, int iters) {
        int s = 0;
        for (int i = 0; i < iters; i++) s += ss[i & (ss.length - 1)].area(i);
        return s;
    }
    static volatile int sink;
    static void phase(String name, Shape[] ss) {
        for (int r = 0; r < 3; r++) {
            long t0 = System.nanoTime(); sink = run(ss, 50_000_000); long ns = System.nanoTime() - t0;
            System.out.printf("%-22s run %d: %5.2f ns/call%n", name, r, ns / 50_000_000.0);
        }
    }
    public static void main(String[] a) {
        // warm-up curve: first batches are slow (interpreter -> C1 -> C2)
        Shape[] one = {new Sq(), new Sq(), new Sq(), new Sq()};
        for (int b = 0; b < 12; b++) {
            long t0 = System.nanoTime(); sink = run(one, 20_000); long ns = System.nanoTime() - t0;
            System.out.printf("cold batch %2d (20k calls): %6d us = %7.1f ns/call%n", b, ns / 1000, ns / 20_000.0);
        }
        phase("1 type  (Sq)", one);
        phase("2 types (Sq,Tri)", new Shape[]{new Sq(), new Tri(), new Sq(), new Tri()});
        phase("3 types (Sq,Tri,Cir)", new Shape[]{new Sq(), new Tri(), new Cir(), new Sq()});
    }
}
