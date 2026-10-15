import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;

/**
 * Part 4：堆外 (off-heap) 的定长哈希表，用 FFM API（Foreign Function & Memory，Java 21 里是预览特性）。
 *
 * 为什么要堆外：
 *   * 内存由我们自己控制：一次分配一整块，按 64 字节（一条缓存行）对齐，4 个 16 字节的槽位 [key:8][value:8] 正好一行
 *   * GC 完全看不见它：不管表有多大，GC 扫描/整理的工作量都不变（低延迟系统避免 GC 抖动的常见手段）
 *   * 可以换成共享内存 / 内存映射文件，进程重启后数据还在 —— 本题不做
 * 代价：要手动 close()；没有自动扩容（这里选择固定容量，超过就报错）；每次访问有边界检查（JIT 能消掉大部分）。
 */
public final class OffHeapTickerMap implements AutoCloseable {
    private static final long SLOT_BYTES = 16;
    private static final long GOLDEN = 0x9E3779B97F4A7C15L;

    private final Arena arena;
    private final MemorySegment seg;
    private final int capacity;
    private final int mask;
    private final int shift;
    private final int maxEntries;
    private int size;

    /** 最多放 maxEntries 个不同的 key；槽位数 = 不小于 2*maxEntries 的 2 的幂（装载因子 <= 0.5）。 */
    public OffHeapTickerMap(int maxEntries) {
        if (maxEntries < 1 || maxEntries > (1 << 28)) throw new IllegalArgumentException("maxEntries: " + maxEntries);
        this.maxEntries = maxEntries;
        this.capacity = Math.max(8, Integer.highestOneBit(maxEntries * 2 - 1) << 1);
        this.mask = capacity - 1;
        this.shift = 64 - Integer.numberOfTrailingZeros(capacity);
        // ofShared：允许别的线程使用（JUnit 的超时断言会换线程）；ofConfined 只允许创建它的线程访问，略快
        this.arena = Arena.ofShared();
        this.seg = arena.allocate(capacity * SLOT_BYTES, 64);   // 分配出来的内存保证已清零，所以 key == 0 就是空格
    }

    private int home(long key) { return (int) ((key * GOLDEN) >>> shift); }

    private long keyAt(int slot) { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES); }
    private long valueAt(int slot) { return seg.get(ValueLayout.JAVA_LONG, slot * SLOT_BYTES + 8); }

    private static void checkKey(long key) {
        if (key <= 0) throw new IllegalArgumentException("key must be > 0: " + key);
    }

    public int size() { return size; }
    public int capacity() { return capacity; }
    public int maxEntries() { return maxEntries; }

    public long get(long key, long ifAbsent) {
        checkKey(key);
        int i = home(key);
        while (true) {
            long k = keyAt(i);
            if (k == key) return valueAt(i);
            if (k == 0) return ifAbsent;
            i = (i + 1) & mask;
        }
    }

    public boolean containsKey(long key) {
        checkKey(key);
        int i = home(key);
        while (true) {
            long k = keyAt(i);
            if (k == key) return true;
            if (k == 0) return false;
            i = (i + 1) & mask;
        }
    }

    /** 新 key 且已满 -> IllegalStateException("full")。返回 true = 新 key。 */
    public boolean put(long key, long value) {
        checkKey(key);
        int i = home(key);
        while (true) {
            long k = keyAt(i);
            if (k == key) { seg.set(ValueLayout.JAVA_LONG, i * SLOT_BYTES + 8, value); return false; }
            if (k == 0) break;
            i = (i + 1) & mask;
        }
        if (size == maxEntries) throw new IllegalStateException("full: " + maxEntries + " entries");
        seg.set(ValueLayout.JAVA_LONG, i * SLOT_BYTES, key);
        seg.set(ValueLayout.JAVA_LONG, i * SLOT_BYTES + 8, value);
        size++;
        return true;
    }

    /** value += delta，返回新值；满了且是新 key -> IllegalStateException。 */
    public long add(long key, long delta) {
        checkKey(key);
        int i = home(key);
        while (true) {
            long k = keyAt(i);
            if (k == key) {
                long v = Math.addExact(valueAt(i), delta);
                seg.set(ValueLayout.JAVA_LONG, i * SLOT_BYTES + 8, v);
                return v;
            }
            if (k == 0) break;
            i = (i + 1) & mask;
        }
        if (size == maxEntries) throw new IllegalStateException("full: " + maxEntries + " entries");
        seg.set(ValueLayout.JAVA_LONG, i * SLOT_BYTES, key);
        seg.set(ValueLayout.JAVA_LONG, i * SLOT_BYTES + 8, delta);
        size++;
        return delta;
    }

    /** 释放堆外内存。之后任何访问都会抛 IllegalStateException。可以重复调用（FFM 自己的第二次 close 会抛异常，所以这里先判断）。 */
    @Override
    public void close() {
        if (arena.scope().isAlive()) arena.close();
    }
}
