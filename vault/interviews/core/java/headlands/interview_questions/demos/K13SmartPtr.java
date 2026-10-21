import java.lang.ref.*;
import java.util.*;

/** What Java has instead of unique_ptr / shared_ptr / weak_ptr / RAII. */
public class K13SmartPtr {
    static class Res implements AutoCloseable {
        final String n; Res(String n) { this.n = n; System.out.println("open  " + n); }
        public void close() { System.out.println("close " + n); }
    }
    static class Big { final byte[] data = new byte[8 << 20]; }

    public static void main(String[] a) throws Exception {
        // RAII analogue: try-with-resources, closed in reverse order, even on exception
        try (Res r1 = new Res("A"); Res r2 = new Res("B")) { System.out.println("body"); throw new RuntimeException("boom"); }
        catch (RuntimeException e) { System.out.println("caught " + e.getMessage()); }

        // weak_ptr analogue
        Big b = new Big();
        WeakReference<Big> w = new WeakReference<>(b);
        System.out.println("strong ref alive -> weak.get() != null : " + (w.get() != null));
        b = null; System.gc(); Thread.sleep(100);
        System.out.println("after dropping strong ref + System.gc() -> weak.get() == null : " + (w.get() == null));

        // cycles are fine (no refcount): A <-> B collected
        class Node { Node other; byte[] pad = new byte[1 << 20]; }
        Node n1 = new Node(), n2 = new Node(); n1.other = n2; n2.other = n1;
        WeakReference<Node> wn = new WeakReference<>(n1); n1 = n2 = null; System.gc(); Thread.sleep(100);
        System.out.println("reference cycle collected (shared_ptr would leak): " + (wn.get() == null));

        // Cleaner: safety net, not a destructor -- no ordering/timing guarantee
        Cleaner cl = Cleaner.create();
        Object o = new Object(); cl.register(o, () -> System.out.println("Cleaner action ran (some time after unreachable)"));
        o = null; System.gc(); Thread.sleep(200);
    }
}
