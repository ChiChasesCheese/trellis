import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Subtask;

/** J11 例 1（最简单）：ShutdownOnFailure——两个子任务都成功才算成功。 */
public class J11Ex1 {
    static String fetchQuote() throws InterruptedException { Thread.sleep(100); return "AAPL 189.50"; }
    static int fetchLimit() throws InterruptedException { Thread.sleep(50); return 10_000; }

    public static void main(String[] args) throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Subtask<String> quote = scope.fork(J11Ex1::fetchQuote);   // fork：开一个虚拟线程跑子任务
            Subtask<Integer> limit = scope.fork(J11Ex1::fetchLimit);

            scope.join()            // 等所有子任务结束（或有一个失败而被取消）
                 .throwIfFailed();  // 有失败就在这里抛 ExecutionException

            // 只有 join 之后才能 get；join 之前 get 会抛 IllegalStateException
            System.out.println("quote = " + quote.get() + ", limit = " + limit.get());
        }
    }
}
