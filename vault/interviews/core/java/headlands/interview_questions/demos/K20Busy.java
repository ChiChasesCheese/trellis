import java.util.*;
/** A deliberately busy JVM to point jcmd / jstat / jstack at. */
public class K20Busy {
    static volatile Object sink;
    static long fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
    public static void main(String[] a) throws Exception {
        Thread cpu = new Thread(() -> { while (true) sink = fib(32); }, "cpu-hog"); cpu.setDaemon(true); cpu.start();
        Thread gc = new Thread(() -> { List<byte[]> keep = new ArrayList<>(); Random r = new Random();
            while (true) { sink = new byte[4096]; if (r.nextInt(2000) == 0) { keep.add(new byte[100_000]); if (keep.size() > 200) keep.clear(); } } }, "alloc-churn");
        gc.setDaemon(true); gc.start();
        Object lock = new Object();
        Thread blocked = new Thread(() -> { synchronized (lock) { try { Thread.sleep(60_000); } catch (InterruptedException e) {} } }, "holds-lock");
        Thread waiter = new Thread(() -> { synchronized (lock) { } }, "waits-for-lock");
        blocked.setDaemon(true); waiter.setDaemon(true); blocked.start(); Thread.sleep(100); waiter.start();
        Thread.sleep(Long.parseLong(a.length > 0 ? a[0] : "20000"));
    }
}
