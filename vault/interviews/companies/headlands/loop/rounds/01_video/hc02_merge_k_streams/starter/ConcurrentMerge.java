import java.util.Iterator;
import java.util.List;

/**
 * Headlands 电面 hc02 Part 3 + 4：多线程、非阻塞地合并多路数据流。题面见 ../problem.md。
 * 每个 source 一个生产者（虚拟线程）→ 每条流一个有界队列 → 合并器。
 */
public final class ConcurrentMerge<T extends Comparable<? super T>> implements AutoCloseable {

    /** tryNext/next 的结果。Pending = 还有活着的流没给出队首，暂时无法安全输出。 */
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

    // 提示：生产者 → 合并器的消息用一个 sealed 类型（Item / End / Failed），终止标记保证合并器不会永远等一个已死的生产者。

    /** 启动 sources.size() 个生产者线程。capacity = 每条流的队列容量（≥ 1，否则 IllegalArgumentException）。 */
    public static <T extends Comparable<? super T>> ConcurrentMerge<T> start(List<? extends Iterator<? extends T>> sources, int capacity) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 非阻塞：立刻返回。出错抛 MergeException（并自动 close）；close 之后调用抛 IllegalStateException。 */
    public Poll<T> tryNext() { throw new UnsupportedOperationException("TODO"); }

    /** 阻塞直到 Ready 或 Done（不会返回 Pending）。可被中断。 */
    public Poll<T> next() throws InterruptedException { throw new UnsupportedOperationException("TODO"); }

    /** 幂等。中断所有生产者并等它们退出（有上限，不能因为某个 source 不响应中断而永远卡住）。 */
    @Override public void close() { throw new UnsupportedOperationException("TODO"); }

    /**
     * Part 4：一次性合并，返回全部结果。生产者和合并任务都放进一个 StructuredTaskScope.ShutdownOnFailure：
     * 任何一个失败 → 其余被中断 → 抛 MergeException（带上失败的流编号）。
     */
    public static <T extends Comparable<? super T>> List<T> mergeAll(List<? extends Iterator<? extends T>> sources, int capacity)
            throws InterruptedException {
        throw new UnsupportedOperationException("TODO");
    }
}
