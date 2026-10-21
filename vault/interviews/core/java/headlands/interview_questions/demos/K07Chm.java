import java.util.*;
import java.util.concurrent.*;

/** HashMap under threads loses updates; ConcurrentHashMap.merge doesn't; CHM rejects null. */
public class K07Chm {
    static void hammer(Map<Integer, Integer> m, String name) throws Exception {
        for (int k = 0; k < 16; k++) m.put(k, 0);                      // no resize during the test
        int threads = 8, per = 200_000;
        ExecutorService ex = Executors.newFixedThreadPool(threads);
        CountDownLatch go = new CountDownLatch(1);
        List<Future<?>> fs = new ArrayList<>();
        for (int t = 0; t < threads; t++) fs.add(ex.submit(() -> {
            go.await(); for (int i = 0; i < per; i++) m.merge(i & 15, 1, Integer::sum); return null; }));
        go.countDown(); for (var f : fs) f.get(); ex.shutdown();
        long total = m.values().stream().mapToLong(Integer::longValue).sum();
        System.out.printf("%-20s expected %,d  got %,d  lost %,d%n", name, (long) threads * per, total, (long) threads * per - total);
    }
    public static void main(String[] a) throws Exception {
        hammer(new HashMap<>(), "HashMap");
        hammer(new ConcurrentHashMap<>(), "ConcurrentHashMap");
        try { new ConcurrentHashMap<String, String>().put("k", null); } catch (NullPointerException e) { System.out.println("CHM.put(k, null) -> NPE"); }
        var c = new ConcurrentHashMap<String, Integer>();
        c.put("a", 1);
        System.out.println("check-then-act race: if(!containsKey) put  vs  putIfAbsent -> " + c.putIfAbsent("a", 2) + " (returned existing)");
    }
}
