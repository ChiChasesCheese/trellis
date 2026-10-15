import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.util.Arrays;

/**
 * 讲义 ld01 §4.4 的实验：把「伪共享」单独拎出来量。两个线程各自只改自己的计数器，逻辑上毫无关系；
 * 区别只在两个计数器在内存里相隔多远：相邻（同一条缓存行）还是相隔 128 字节以上（不同缓存行）。
 *
 * 编译 / 运行：
 *   javac --release 21 -d /tmp/ld01b study/30-articles/examples/ld01/FalseSharingBench.java
 *   java -cp /tmp/ld01b FalseSharingBench
 */
public class FalseSharingBench {
    static class Adjacent { long a, b; }
    static class P0 { long a; }
    static class Pad extends P0 { long p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15, p16; }
    static class Apart extends Pad { long b; }

    static final VarHandle ADJ_A, ADJ_B, APART_A, APART_B;
    static {
        try {
            var l = MethodHandles.lookup();
            ADJ_A = l.findVarHandle(Adjacent.class, "a", long.class);
            ADJ_B = l.findVarHandle(Adjacent.class, "b", long.class);
            APART_A = l.findVarHandle(P0.class, "a", long.class);
            APART_B = l.findVarHandle(Apart.class, "b", long.class);
        } catch (ReflectiveOperationException e) { throw new ExceptionInInitializerError(e); }
    }

    static final long ITER = 200_000_000L;

    static long timeMs(Object o, VarHandle x, VarHandle y) throws Exception {
        Thread t1 = new Thread(() -> { for (long i = 0; i < ITER; i++) x.setOpaque(o, (long) x.getOpaque(o) + 1); });
        Thread t2 = new Thread(() -> { for (long i = 0; i < ITER; i++) y.setOpaque(o, (long) y.getOpaque(o) + 1); });
        long t0 = System.nanoTime();
        t1.start(); t2.start(); t1.join(); t2.join();
        return (System.nanoTime() - t0) / 1_000_000;
    }

    public static void main(String[] args) throws Exception {
        long[] adj = new long[7], apart = new long[7];
        for (int r = 0; r < 7; r++) {                       // 第 0 轮预热
            adj[r] = timeMs(new Adjacent(), ADJ_A, ADJ_B);
            apart[r] = timeMs(new Apart(), APART_A, APART_B);
        }
        long[] a = Arrays.copyOfRange(adj, 1, 7), b = Arrays.copyOfRange(apart, 1, 7);
        Arrays.sort(a); Arrays.sort(b);
        System.out.println("每个线程 " + ITER / 1_000_000 + "M 次自增（ms，6 轮，排序后）：");
        System.out.println("  相邻(同一缓存行)  " + Arrays.toString(a) + "  中位数 " + (a[2] + a[3]) / 2);
        System.out.println("  相隔 128 字节以上 " + Arrays.toString(b) + "  中位数 " + (b[2] + b[3]) / 2);
    }
}
