import java.util.concurrent.*;

/** J11 旧写法：ExecutorService + Future。一个子任务失败后，另一个还在白白跑——没人替你取消。 */
public class J11Old {
    static String slowOk() throws Exception {
        Thread.sleep(1500);
        System.out.println("  [slowOk 跑完了——白干了，因为 fastFail 早就失败了]");
        return "ok";
    }
    static String fastFail() throws Exception {
        Thread.sleep(100);
        throw new IllegalStateException("risk service down");
    }

    public static void main(String[] args) throws Exception {
        ExecutorService pool = Executors.newFixedThreadPool(2);
        Future<String> a = pool.submit(J11Old::slowOk);
        Future<String> b = pool.submit(J11Old::fastFail);
        try {
            // 痛点：你得「按某种顺序」get。先 get(a) 会傻等 1.5s，才轮到发现 b 早就失败了
            System.out.println(a.get());
            System.out.println(b.get());
        } catch (ExecutionException e) {
            System.out.println("main 终于发现失败: " + e.getCause());
        } finally {
            // 痛点：如果忘了 shutdown，或者异常路径漏了 cancel，线程就泄漏
            pool.shutdown();
        }
    }
}
