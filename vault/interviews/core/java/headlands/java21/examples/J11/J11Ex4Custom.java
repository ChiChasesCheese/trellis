import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.StructuredTaskScope.Subtask;

/** J11 例 4：自定义 scope 策略——收集全部成功结果，失败的忽略（"尽力而为"的多路取价）。重写 handleComplete。 */
public class J11Ex4Custom {
    static class CollectOk<T> extends StructuredTaskScope<T> {
        private final Queue<T> ok = new ConcurrentLinkedQueue<>();
        private final Queue<Throwable> failed = new ConcurrentLinkedQueue<>();

        @Override
        protected void handleComplete(Subtask<? extends T> st) {
            switch (st.state()) {
                case SUCCESS -> ok.add(st.get());
                case FAILED -> failed.add(st.exception());
                case UNAVAILABLE -> throw new IllegalStateException();
            }
        }

        @Override public CollectOk<T> join() throws InterruptedException { super.join(); return this; }
        List<T> results() { ensureOwnerAndJoined(); return new ArrayList<>(ok); }
        int failures() { ensureOwnerAndJoined(); return failed.size(); }
    }

    public static void main(String[] args) throws Exception {
        try (var scope = new CollectOk<Long>()) {
            for (int v = 0; v < 5; v++) {
                final int venue = v;
                scope.fork(() -> {
                    Thread.sleep(20L * (5 - venue));
                    if (venue == 3) throw new RuntimeException("venue 3 down");
                    return 18_950L + venue;
                });
            }
            scope.join();
            var prices = scope.results();
            Collections.sort(prices);
            System.out.println("成功 " + prices.size() + " 个: " + prices + "，失败 " + scope.failures() + " 个");
        }
    }
}
