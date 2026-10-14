/** J10 例 1（最简单）：三种创建虚拟线程的方式，以及它和平台线程的区别。 */
public class J10Ex1 {
    public static void main(String[] args) throws Exception {
        Runnable job = () -> {
            Thread t = Thread.currentThread();
            System.out.println("  running in " + t + "  isVirtual=" + t.isVirtual() + "  daemon=" + t.isDaemon());
        };

        // 方式 1：Thread.ofVirtual().start(...)：创建并立刻启动
        System.out.println("方式 1 ofVirtual().start");
        Thread v1 = Thread.ofVirtual().name("v-1").start(job);
        v1.join();

        // 方式 2：Thread.startVirtualThread(...)：最短的写法，没有名字
        System.out.println("方式 2 startVirtualThread");
        Thread.startVirtualThread(job).join();

        // 方式 3：builder 先 unstarted，再手动 start
        System.out.println("方式 3 unstarted + start");
        Thread v3 = Thread.ofVirtual().name("v-", 0).unstarted(job); // 名字 v-0, v-1 ...
        v3.start();
        v3.join();

        // 对照：平台线程
        System.out.println("对照：平台线程");
        Thread p = Thread.ofPlatform().name("p-1").start(job);
        p.join();

        // 虚拟线程永远是守护线程；优先级固定为 NORM_PRIORITY；没有 ThreadGroup 的实际意义
        Thread v = Thread.ofVirtual().unstarted(() -> {});
        System.out.println("virtual isDaemon=" + v.isDaemon() + " priority=" + v.getPriority());
    }
}
