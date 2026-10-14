import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.PriorityQueue;
import java.util.Spliterator;
import java.util.Spliterators;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

/**
 * Headlands 电面 hc02 Part 1 + 2：把 k 个各自有序的序列合并成一个有序序列。题面见 ../problem.md，讲义见 study/30-articles。
 *
 * 核心想法（为什么用堆）：每个序列只有「当前最小的未用元素」（队首）有资格成为下一个输出，
 * 所以全局最小值一定在 k 个队首之中。把 k 个队首放进一个最小堆，每次弹出堆顶就是答案，
 * 然后把弹出元素所在序列的下一个元素补进堆。每输出一个元素花 O(log k)，总共 O(N log k)（N = 元素总数）。
 */
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

    // ------------------------------------------------------------------ Part 1

    /**
     * Part 1：合并 k 个 List。相等元素按「序列编号小的在前」输出（稳定）。
     * 任何一个序列不是升序 → UnsortedInputException；出现 null 元素 → NullPointerException。
     */
    public static <T extends Comparable<? super T>> List<T> merge(List<? extends List<? extends T>> lists) {
        long total = 0;
        for (var l : lists) total += l.size();
        // 预留容量：避免 ArrayList 反复扩容拷贝。上限防止 int 溢出。
        var out = new ArrayList<T>((int) Math.min(total, Integer.MAX_VALUE - 8));
        var its = new ArrayList<Iterator<? extends T>>(lists.size());
        for (var l : lists) its.add(l.iterator());
        var merged = mergeIterators(its);
        while (merged.hasNext()) out.add(merged.next());
        return out;
    }

    /**
     * Part 1（性能版）：long[] 版本，不装箱，自己写数组堆。
     * 为什么：PriorityQueue<Head<Long>> 每个元素一个对象 + 一次装箱，堆里是指针，比较时要追指针（cache miss）；
     * 这里堆里只放 int 序列号，数据都在原数组里，顺序读取对 CPU 缓存友好。
     */
    public static long[] mergeLongs(long[][] arrays) {
        int k = arrays.length;
        long total = 0;
        for (long[] a : arrays) total += a.length;
        if (total > Integer.MAX_VALUE - 8) throw new IllegalArgumentException("too many elements: " + total);
        long[] out = new long[(int) total];
        int[] pos = new int[k];    // pos[s] = 序列 s 下一个要读的下标
        int[] heap = new int[k];   // 堆里放序列号 s，按 (arrays[s][pos[s]], s) 排序
        int n = 0;
        for (int s = 0; s < k; s++) if (arrays[s].length > 0) heap[n++] = s;
        for (int i = n / 2 - 1; i >= 0; i--) siftDown(arrays, pos, heap, n, i); // 自底向上建堆 O(k)
        int o = 0;
        while (n > 0) {
            int s = heap[0];
            long v = arrays[s][pos[s]];
            out[o++] = v;
            if (++pos[s] < arrays[s].length) {
                if (arrays[s][pos[s]] < v) throw new UnsortedInputException(s, pos[s]); // 不能写 a - b < 0：会溢出
            } else {
                heap[0] = heap[--n]; // 序列用完：把堆尾搬到堆顶
            }
            siftDown(arrays, pos, heap, n, 0);
        }
        return out;
    }

    private static boolean less(long[][] arrays, int[] pos, int a, int b) {
        long va = arrays[a][pos[a]], vb = arrays[b][pos[b]];
        return va < vb || (va == vb && a < b); // 相等看序列号 → 稳定
    }

    private static void siftDown(long[][] arrays, int[] pos, int[] heap, int n, int i) {
        int s = heap[i];
        while (true) {
            int child = 2 * i + 1;
            if (child >= n) break;
            if (child + 1 < n && less(arrays, pos, heap[child + 1], heap[child])) child++;
            if (!less(arrays, pos, heap[child], s)) break;
            heap[i] = heap[child];
            i = child;
        }
        heap[i] = s;
    }

    // ------------------------------------------------------------------ Part 2

    /** 堆里的一项：某个序列当前的队首。 */
    private static final class Head<T> {
        final int stream;
        final Iterator<? extends T> source;
        T value;
        long position; // value 在本序列里的下标

        Head(int stream, Iterator<? extends T> source) {
            this.stream = stream;
            this.source = source;
        }
    }

    /**
     * Part 2：惰性合并。构造时不碰任何 source；第一次 hasNext/next 才每个 source 取一个队首；
     * 之后每输出一个元素，它所在 source 的「下一个元素」要等到下一次调用才去取（延迟补位）。
     * 为什么延迟：source 可能很慢（网络）、甚至无限；刚输出完 x 就去等 x 后面的元素会白白阻塞。
     */
    public static <T extends Comparable<? super T>> Iterator<T> mergeIterators(List<? extends Iterator<? extends T>> sources) {
        var snapshot = List.copyOf(sources);
        return new Iterator<>() {
            private final PriorityQueue<Head<T>> heap = new PriorityQueue<>(
                    Math.max(1, snapshot.size()),
                    Comparator.<Head<T>, T>comparing(h -> h.value).thenComparingInt(h -> h.stream));
            private boolean started;
            private Head<T> lastEmitted; // 刚输出过、还没补位的那个序列

            private void prime() {
                if (!started) {
                    started = true;
                    for (int i = 0; i < snapshot.size(); i++) {
                        var h = new Head<T>(i, snapshot.get(i));
                        if (advance(h, null)) heap.add(h);
                    }
                }
                if (lastEmitted != null) {
                    var h = lastEmitted;
                    lastEmitted = null;
                    if (advance(h, h.value)) heap.add(h);
                }
            }

            /** 取 h 的下一个元素；有则返回 true。prev 用来检查升序（相等允许）。 */
            private boolean advance(Head<T> h, T prev) {
                if (!h.source.hasNext()) return false;
                T next = Objects.requireNonNull(h.source.next(), "null element in stream " + h.stream);
                if (prev != null) {
                    if (next.compareTo(prev) < 0) throw new UnsortedInputException(h.stream, h.position + 1);
                    h.position++;
                }
                h.value = next;
                return true;
            }

            @Override public boolean hasNext() {
                prime();
                return !heap.isEmpty();
            }

            @Override public T next() {
                prime();
                Head<T> h = heap.poll();
                if (h == null) throw new NoSuchElementException();
                lastEmitted = h;
                return h.value;
            }
        };
    }

    /** Part 2：Stream 版。返回的 Stream 也是惰性的；关闭它会关闭所有输入 Stream。 */
    public static <T extends Comparable<? super T>> Stream<T> mergeStreams(List<? extends Stream<? extends T>> streams) {
        var snapshot = List.copyOf(streams);
        var iterators = new ArrayList<Iterator<? extends T>>(snapshot.size());
        for (var s : snapshot) iterators.add(s.iterator());
        var it = mergeIterators(iterators);
        return StreamSupport.stream(Spliterators.spliteratorUnknownSize(it, Spliterator.ORDERED), false)
                .onClose(() -> snapshot.forEach(Stream::close));
    }
}
