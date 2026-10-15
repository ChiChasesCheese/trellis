import java.util.concurrent.atomic.AtomicInteger;

/**
 * J16 例 2：重排序（reordering）。经典 "store buffering" 实验：
 *   线程 1: x = 1; r1 = y;        线程 2: y = 1; r2 = x;
 * 按"一条一条按顺序执行"的直觉，r1 和 r2 不可能同时为 0（至少有一个线程后执行，应能看到另一个的写入）。
 * 现实：CPU 的 store buffer 让"写"晚于后面的"读"对别的核可见，于是 (0,0) 会出现。volatile 禁止这种重排。
 */
public class J16Ex2Reorder {
    static int x, y;                        // 普通
    static volatile int vx, vy;             // volatile
    static int r1, r2, vr1, vr2;
    static final AtomicInteger go = new AtomicInteger(-1);
    static final AtomicInteger done = new AtomicInteger();

    static long test(boolean useVolatile, int iterations) throws Exception {
        long zeros = 0;
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < iterations; i++) {
                while (go.get() < i) Thread.onSpinWait();
                if (useVolatile) { vx = 1; vr1 = vy; } else { x = 1; r1 = y; }
                done.incrementAndGet();
            }
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < iterations; i++) {
                while (go.get() < i) Thread.onSpinWait();
                if (useVolatile) { vy = 1; vr2 = vx; } else { y = 1; r2 = x; }
                done.incrementAndGet();
            }
        });
        t1.start(); t2.start();
        for (int i = 0; i < iterations; i++) {
            x = 0; y = 0; vx = 0; vy = 0; done.set(0);
            go.set(i);                                           // 放行两个线程
            while (done.get() < 2) Thread.onSpinWait();          // 等两个都做完
            if (useVolatile ? (vr1 == 0 && vr2 == 0) : (r1 == 0 && r2 == 0)) zeros++;
        }
        t1.join(); t2.join();
        go.set(-1);
        return zeros;
    }

    public static void main(String[] args) throws Exception {
        int n = 1_000_000;
        System.out.println("普通字段  ，" + n + " 次中 (r1,r2)=(0,0) 出现 " + test(false, n) + " 次");
        System.out.println("volatile  ，" + n + " 次中 (r1,r2)=(0,0) 出现 " + test(true, n) + " 次");
    }
}
