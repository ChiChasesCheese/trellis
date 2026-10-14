import java.util.concurrent.*;

/** J12 旧写法：用 ThreadLocal 传「当前请求的用户」。三个痛点一次展示：泄漏、不继承、随处可改。 */
public class J12Old {
    static final ThreadLocal<String> USER = new ThreadLocal<>();

    static void handle(String user, boolean cleanup) {
        USER.set(user);
        try {
            System.out.println(Thread.currentThread().getName() + " 处理 " + user + "，USER=" + USER.get());
        } finally {
            if (cleanup) USER.remove(); // 痛点 1：必须手工清理；忘了就泄漏
        }
    }

    public static void main(String[] args) throws Exception {
        // 痛点 1：线程池复用线程，上一个请求的值留在线程里，下一个请求「看见了别人的用户」
        ExecutorService pool = Executors.newSingleThreadExecutor();
        pool.submit(() -> handle("alice", false)).get();               // 忘了 remove
        pool.submit(() -> System.out.println("下一个请求(未 set)读到 USER=" + USER.get())).get();
        pool.shutdown();

        // 痛点 2：新开的线程拿不到父线程的值
        USER.set("bob");
        Thread t = new Thread(() -> System.out.println("子线程读到 USER=" + USER.get()));
        t.start(); t.join();

        // 痛点 3：任何拿到引用的代码都能 set 改掉它，读代码的人无法知道谁在什么时候改了
        USER.set("mallory");
        System.out.println("主线程现在 USER=" + USER.get());
    }
}
