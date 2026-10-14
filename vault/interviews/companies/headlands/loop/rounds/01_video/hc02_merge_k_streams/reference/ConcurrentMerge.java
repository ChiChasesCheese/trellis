import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * Headlands 电面 hc02 Part 3 + 4：多线程、非阻塞地合并多路数据流。题面见 ../problem.md，讲义见 study/30-articles。
 *
 * 结构：每个 source 一个生产者（虚拟线程）把元素放进自己的有界队列（backpressure：消费者慢，生产者就停在 put 上，内存有界）；
 * 合并器只做一件事——「每个还活着的 source 都有队首时，才能决定谁最小」。
 * 为什么不能先拿到的先出：source A 有 5，source B 还没数据；B 稍后可能给 1，现在输出 5 就错了。
 * 这就是 Pending 的含义：不是没有数据，而是还不能安全地决定。
 */
public final class ConcurrentMerge<T extends Comparable<? super T>> implements AutoCloseable {

    /** tryNext/next 的结果。sealed → switch 必须穷尽。 */
    public sealed interface Poll<T> permits Ready, Pending, Done {}
    public record Ready<T>(T value, int stream) implements Poll<T> {}
    public record Pending<T>() implements Poll<T> {}
    public record Done<T>() implements Poll<T> {}

    /** 某个 source 出错（hasNext/next 抛异常、乱序、null）。stream = -1 表示不属于某个具体 source。 */
    public static final class MergeException extends RuntimeException {
        private final int stream;

        public MergeException(int stream, Throwable cause) {
            super("stream " + stream + " failed: " + cause, cause);
            this.stream = stream;
        }

        public int stream() { return stream; }
    }

    /** 生产者 → 合并器的消息。End/Failed 是「终止标记」：保证合并器永远不会无限等一个已经死掉的生产者。 */
    private sealed interface Msg<T> permits Item, End, Failed {}
    private record Item<T>(T value) implements Msg<T> {}
    private record End<T>() implements Msg<T> {}
    private record Failed<T>(Throwable cause) implements Msg<T> {}

    // ------------------------------------------------------------------ 合并核心（Part 3 与 Part 4 共用）

    /** 只在消费者一侧使用，不是线程安全的。 */
    private static final class Combiner<T extends Comparable<? super T>> {
        private final List<? extends BlockingQueue<Msg<T>>> queues;
        private final List<Item<T>> heads;
        private final boolean[] finished;

        Combiner(List<? extends BlockingQueue<Msg<T>>> queues) {
            this.queues = queues;
            this.heads = new ArrayList<>(Collections.nCopies(queues.size(), null));
            this.finished = new boolean[queues.size()];
        }

        /** block=false 时用 poll()（立刻返回），true 时用 take()（可被中断）。 */
        Poll<T> poll(boolean block) throws InterruptedException {
            boolean pending = false;
            for (int i = 0; i < queues.size(); i++) {
                if (finished[i] || heads.get(i) != null) continue;
                Msg<T> m = block ? queues.get(i).take() : queues.get(i).poll();
                if (m == null) { pending = true; continue; } // 继续看别的流：这样别的流的失败也能被发现
                switch (m) {
                    case Item<T> item -> heads.set(i, item);
                    case End<T> _ -> finished[i] = true;
                    case Failed<T>(var cause) -> throw new MergeException(i, cause);
                }
            }
            if (pending) return new Pending<>();
            int best = -1;
            for (int i = 0; i < heads.size(); i++) {
                var h = heads.get(i);
                // 严格小于才替换：相等时保留编号小的 → 稳定
                if (h != null && (best < 0 || h.value().compareTo(heads.get(best).value()) < 0)) best = i;
            }
            if (best < 0) return new Done<>();
            var out = new Ready<>(heads.get(best).value(), best);
            heads.set(best, null);
            return out;
        }
    }

    /**
     * 生产者循环：把 src 的元素按序放进 q，最后放 End。出错直接抛（由调用者决定是转成 Failed 标记还是让 scope 取消）。
     * q.put 在队列满时阻塞——这就是 backpressure。
     */
    private static <T extends Comparable<? super T>> void produce(int idx, Iterator<? extends T> src, BlockingQueue<Msg<T>> q)
            throws InterruptedException {
        T prev = null;
        long pos = 0;
        while (src.hasNext()) {
            T v = Objects.requireNonNull(src.next(), "null element");
            if (prev != null && v.compareTo(prev) < 0) throw new MergeK.UnsortedInputException(idx, pos);
            q.put(new Item<>(v));
            prev = v;
            pos++;
        }
        q.put(new End<>());
    }

    // ------------------------------------------------------------------ Part 3：非阻塞合并器

    private final Combiner<T> combiner;
    private final List<Thread> producers = new ArrayList<>();
    private final AtomicBoolean closed = new AtomicBoolean();

    private ConcurrentMerge(List<? extends Iterator<? extends T>> sources, int capacity) {
        var queues = new ArrayList<BlockingQueue<Msg<T>>>();
        for (int i = 0; i < sources.size(); i++) queues.add(new ArrayBlockingQueue<>(capacity));
        this.combiner = new Combiner<>(queues);
        for (int i = 0; i < sources.size(); i++) {
            final int idx = i;
            final var src = sources.get(i);
            final var q = queues.get(i);
            // 虚拟线程：source 的 hasNext 可能阻塞在 I/O 上，虚拟线程阻塞时不占 OS 线程，开 k 个很便宜
            producers.add(Thread.ofVirtual().name("merge-producer-" + i).start(() -> {
                try {
                    produce(idx, src, q);
                } catch (InterruptedException _) {
                    // close() 叫我们走：不需要终止标记，没人在听了
                } catch (Throwable t) {
                    try {
                        q.put(new Failed<>(t)); // 一定要留下遗言，否则合并器会一直等这条流
                    } catch (InterruptedException _) { /* closing */ }
                }
            }));
        }
    }

    /** 启动 sources.size() 个生产者线程。capacity = 每条流的队列容量（≥ 1），也就是每条流最多提前读多少。 */
    public static <T extends Comparable<? super T>> ConcurrentMerge<T> start(List<? extends Iterator<? extends T>> sources, int capacity) {
        if (capacity < 1) throw new IllegalArgumentException("capacity must be >= 1: " + capacity);
        return new ConcurrentMerge<>(List.copyOf(sources), capacity);
    }

    /** 非阻塞：立刻返回。Pending = 还有活着的流没给出队首，暂时无法安全输出。出错抛 MergeException（并自动 close）。 */
    public Poll<T> tryNext() {
        if (closed.get()) throw new IllegalStateException("closed");
        try {
            return combiner.poll(false);
        } catch (MergeException e) {
            close();
            throw e;
        } catch (InterruptedException e) { // poll(false) 不会抛，但签名要求
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** 阻塞直到 Ready 或 Done（不会返回 Pending）。可被中断。 */
    public Poll<T> next() throws InterruptedException {
        if (closed.get()) throw new IllegalStateException("closed");
        try {
            return combiner.poll(true);
        } catch (MergeException e) {
            close();
            throw e;
        }
    }

    /** 幂等。中断所有生产者并等它们退出（最多 1 秒/个，source 不响应中断也不会让 close 永远卡住）。 */
    @Override public void close() {
        if (!closed.compareAndSet(false, true)) return;
        producers.forEach(Thread::interrupt);
        for (Thread t : producers) {
            try {
                t.join(Duration.ofSeconds(1));
            } catch (InterruptedException _) {
                Thread.currentThread().interrupt();
                return;
            }
        }
    }

    // ------------------------------------------------------------------ Part 4：StructuredTaskScope

    /**
     * 一次性合并，返回全部结果。所有生产者和合并任务都在同一个 StructuredTaskScope 里：
     * 任何一个失败 → scope 关闭 → 其余任务被中断 → 方法抛 MergeException。
     * 为什么比手写好：线程的生命周期被限制在 try 块里，离开 try 块时所有子线程一定已经结束，不会泄漏。
     */
    public static <T extends Comparable<? super T>> List<T> mergeAll(List<? extends Iterator<? extends T>> sources, int capacity)
            throws InterruptedException {
        if (capacity < 1) throw new IllegalArgumentException("capacity must be >= 1: " + capacity);
        var srcs = List.copyOf(sources);
        var queues = new ArrayList<BlockingQueue<Msg<T>>>();
        for (int i = 0; i < srcs.size(); i++) queues.add(new ArrayBlockingQueue<>(capacity));
        try (var scope = new StructuredTaskScope.ShutdownOnFailure("merge-all", Thread.ofVirtual().factory())) {
            for (int i = 0; i < srcs.size(); i++) {
                final int idx = i;
                scope.fork(() -> {
                    try {
                        produce(idx, srcs.get(idx), queues.get(idx));
                    } catch (InterruptedException e) {
                        throw e; // 被取消：原样往外抛
                    } catch (Exception e) {
                        throw new MergeException(idx, e); // 真正的失败：带上流编号，scope 会据此取消其他任务
                    }
                    return null;
                });
            }
            var merged = scope.fork(() -> {
                var combiner = new Combiner<T>(queues);
                var out = new ArrayList<T>();
                while (true) {
                    switch (combiner.poll(true)) {
                        case Ready<T>(var v, _) -> out.add(v);
                        case Done<T> _ -> { return out; }
                        case Pending<T> _ -> throw new AssertionError("blocking poll never returns Pending");
                    }
                }
            });
            scope.join();
            scope.throwIfFailed(e -> e instanceof MergeException me ? me : new MergeException(-1, e));
            return merged.get();
        }
    }
}
