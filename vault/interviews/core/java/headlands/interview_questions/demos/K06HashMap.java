import java.lang.reflect.Field;
import java.util.*;

/**
 * HashMap internals via reflection.  Run with:
 *   java --add-opens java.base/java.util=ALL-UNNAMED K06HashMap
 */
public class K06HashMap {
    static Object[] table(HashMap<?, ?> m) throws Exception {
        Field f = HashMap.class.getDeclaredField("table"); f.setAccessible(true);
        return (Object[]) f.get(m);
    }
    static int spread(Object k) { int h = k.hashCode(); return h ^ (h >>> 16); }

    record BadKey(int id) implements Comparable<BadKey> {            // every key collides
        @Override public int hashCode() { return 42; }
        public int compareTo(BadKey o) { return Integer.compare(id, o.id); }
    }
    static final class BadNoCmp {                                    // collides AND not Comparable
        final int id; BadNoCmp(int id) { this.id = id; }
        @Override public int hashCode() { return 42; }
        @Override public boolean equals(Object o) { return o instanceof BadNoCmp b && b.id == id; }
    }

    public static void main(String[] a) throws Exception {
        HashMap<Integer, Integer> m = new HashMap<>();
        System.out.println("new HashMap(): table = " + table(m) + " (lazy allocation)");
        int lastLen = -1;
        for (int i = 0; i < 100; i++) {
            m.put(i, i);
            int len = table(m).length;
            if (len != lastLen) { System.out.println("after " + (i + 1) + " puts: table.length = " + len); lastLen = len; }
        }
        String k = "Aa", k2 = "BB";
        System.out.println("\"Aa\".hashCode()==\"BB\".hashCode(): " + (k.hashCode() == k2.hashCode()) + " (" + k.hashCode() + ")");
        Object big = 0x12345678;
        System.out.printf("spread(0x12345678)=0x%08x ; index in 16 buckets = %d%n", spread(big), spread(big) & 15);

        HashMap<Object, Integer> c = new HashMap<>();
        for (int i = 1; i <= 12; i++) {
            c.put(new BadKey(i), i);
            Object[] t = table(c); Object bin = null; for (Object o : t) if (o != null) bin = o;
            System.out.println("colliding put #" + i + ": table.length=" + t.length + ", bin type=" + bin.getClass().getSimpleName());
        }
        for (var kind : List.of("Comparable-colliding", "non-Comparable-colliding")) {
            HashMap<Object, Integer> h = new HashMap<>();
            for (int i = 0; i < 2000; i++) h.put(kind.startsWith("Comp") ? new BadKey(i) : new BadNoCmp(i), i);
            Object[] t = table(h); Object bin = null;
            for (Object o : t) if (o != null) bin = o;
            long t0 = System.nanoTime(); int s = 0;
            for (int r = 0; r < 200; r++) for (int i = 0; i < 2000; i += 50)
                s += h.get(kind.startsWith("Comp") ? new BadKey(i) : new BadNoCmp(i));
            System.out.printf("%-26s table.length=%d, the one used bin is a %s; 8000 lookups took %d us%n",
                kind, t.length, bin.getClass().getSimpleName(), (System.nanoTime() - t0) / 1000);
        }
    }
}
