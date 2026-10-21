/** J16 旧写法（Java 5~8）：一把大锁（synchronized）保护一个计数器。正确，但所有线程排队；而且"锁里面做什么"全靠自觉。 */
public class J16Old {
    static class Counter {
        private long n;
        synchronized void inc() { n++; }
        synchronized long get() { return n; }
    }

    public static void main(String[] args) throws Exception {
        Counter c = new Counter();
        int threads = 8, per = 2_000_000;
        Thread[] ts = new Thread[threads];
        long t0 = System.nanoTime();
        for (int i = 0; i < threads; i++) { ts[i] = new Thread(() -> { for (int k = 0; k < per; k++) c.inc(); }); ts[i].start(); }
        for (Thread t : ts) t.join();
        System.out.println("synchronized 计数器: " + c.get() + " (期望 " + (long) threads * per + "), " + (System.nanoTime() - t0) / 1_000_000 + " ms");
    }
}
