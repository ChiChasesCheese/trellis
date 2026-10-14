import java.util.Iterator;
import java.util.List;
import java.util.stream.Stream;

/** Headlands 电面 hc02 Part 1 + 2：把 k 个各自有序的序列合并成一个有序序列。题面见 ../problem.md，把每个 TODO 换成实现。 */
public final class MergeK {
    private MergeK() {}

    /** 某个输入序列不是升序（允许相等）。stream 是序列编号，position 是违规元素在该序列里的下标。 */
    public static final class UnsortedInputException extends RuntimeException {
        private final int stream;
        private final long position;

        public UnsortedInputException(int stream, long position) {
            super("stream " + stream + " is not sorted at position " + position);
            this.stream = stream;
            this.position = position;
        }

        public int stream() { return stream; }

        public long position() { return position; }
    }

    /**
     * Part 1：合并 k 个 List。相等元素按「序列编号小的在前」输出（稳定）。
     * 不是升序 → UnsortedInputException；null 元素 → NullPointerException。提示：最小堆里放「每个序列的队首」。
     */
    public static <T extends Comparable<? super T>> List<T> merge(List<? extends List<? extends T>> lists) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Part 1（性能版）：long[] 版本，不装箱。提示：堆里只放序列号 int，数据留在原数组里。 */
    public static long[] mergeLongs(long[][] arrays) { throw new UnsupportedOperationException("TODO"); }

    /**
     * Part 2：惰性合并。构造时不碰任何 source；每输出一个元素，它所在 source 的下一个元素推迟到下一次调用再取。
     * 同样稳定、同样检查升序（检查发生在读到那个元素的时候）。
     */
    public static <T extends Comparable<? super T>> Iterator<T> mergeIterators(List<? extends Iterator<? extends T>> sources) {
        throw new UnsupportedOperationException("TODO");
    }

    /** Part 2：Stream 版。返回的 Stream 也是惰性的；关闭它会关闭所有输入 Stream。 */
    public static <T extends Comparable<? super T>> Stream<T> mergeStreams(List<? extends Stream<? extends T>> streams) {
        throw new UnsupportedOperationException("TODO");
    }
}
