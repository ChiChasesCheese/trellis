import java.util.concurrent.StructuredTaskScope;

/** J11 例 2：ShutdownOnSuccess——「谁先返回用谁」（对冲请求 hedged request）。慢的那个会被中断。 */
public class J11Ex2 {
    static String query(String venue, long ms) throws InterruptedException {
        try {
            Thread.sleep(ms);
            return venue + " 先回";
        } catch (InterruptedException e) {
            System.out.println("  [" + venue + " 被取消(InterruptedException)]");
            throw e;
        }
    }

    public static void main(String[] args) throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
            scope.fork(() -> query("NYSE", 300));
            scope.fork(() -> query("NASDAQ", 80));
            scope.fork(() -> query("ARCA", 500));
            String first = scope.join().result();   // 第一个成功的结果；其余子任务立刻被中断
            System.out.println("拿到: " + first);
        }
        System.out.println("离开 try 块时，三个子线程一定都已结束");
    }
}
