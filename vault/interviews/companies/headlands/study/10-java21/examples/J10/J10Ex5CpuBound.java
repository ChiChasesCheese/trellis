import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/** J10 例 5：CPU 密集任务用虚拟线程没有任何好处。24 个纯计算任务：固定池(=核数) vs 虚拟线程。 */
public class J10Ex5CpuBound {
    static long burn(int rounds) {
        long x = 88172645463325252L;   // xorshift：每一步依赖上一步，JIT 无法把循环折叠成公式
        long acc = 0;
        for (int i = 0; i < rounds; i++) {
            x ^= x << 13; x ^= x >>> 7; x ^= x << 17;
            if ((x & 1) == 0) acc += x; else acc ^= x;
        }
        return acc;
    }

    static long run(ExecutorService ex) throws Exception {
        List<Future<Long>> fs = new ArrayList<>();
        long t0 = System.nanoTime();
        for (int i = 0; i < 24; i++) fs.add(ex.submit(() -> burn(200_000_000)));
        for (var f : fs) f.get();
        return (System.nanoTime() - t0) / 1_000_000;
    }

    public static void main(String[] args) throws Exception {
        int cores = Runtime.getRuntime().availableProcessors();
        System.out.println("cores = " + cores);
        try (var ex = Executors.newFixedThreadPool(cores)) { run(ex); }          // 预热
        try (var ex = Executors.newFixedThreadPool(cores)) { System.out.println("固定池(核数): " + run(ex) + " ms"); }
        try (var ex = Executors.newVirtualThreadPerTaskExecutor()) { System.out.println("虚拟线程    : " + run(ex) + " ms"); }
    }
}
