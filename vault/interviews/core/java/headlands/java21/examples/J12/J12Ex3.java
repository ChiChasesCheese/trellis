import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Subtask;

/**
 * J12 例 3（贴近真实）：一次下单请求的上下文（traceId、account）用 ScopedValue 传到深层方法，
 * 并且自动被 StructuredTaskScope fork 出的子线程继承；而一个"野"虚拟线程拿不到。
 */
public class J12Ex3 {
    record RequestContext(String traceId, String account) {}
    static final ScopedValue<RequestContext> CTX = ScopedValue.newInstance();

    static void log(String msg) {
        // 深层工具方法：不需要任何参数就知道自己在为哪个请求打日志
        var c = CTX.isBound() ? CTX.get() : null;
        String who = c == null ? "<无上下文>" : c.traceId() + "/" + c.account();
        System.out.println("[" + who + "] " + msg);
    }

    static long fetchQuote() throws InterruptedException { Thread.sleep(30); log("取行情"); return 18_950; }
    static long fetchLimit() throws InterruptedException { Thread.sleep(10); log("取额度"); return 500; }

    static void handleOrder() throws Exception {
        log("开始处理订单 ");
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Subtask<Long> q = scope.fork(J12Ex3::fetchQuote);   // 子线程自动继承 CTX 绑定
            Subtask<Long> l = scope.fork(J12Ex3::fetchLimit);
            scope.join().throwIfFailed();
            log("行情=" + q.get() + " 额度=" + l.get() + " ");
        }
    }

    public static void main(String[] args) throws Exception {
        ScopedValue.where(CTX, new RequestContext("t-001", "ACC-7")).call(() -> {
            handleOrder();

            // 对照：普通的 Thread.ofVirtual().start 不继承 ScopedValue
            Thread t = Thread.ofVirtual().start(() -> log("(野线程) 我能看到上下文吗？ "));
            t.join();
            return null;
        });
        ScopedValue.where(CTX, new RequestContext("t-002", "ACC-9")).call(() -> { handleOrder(); return null; });
    }
}
