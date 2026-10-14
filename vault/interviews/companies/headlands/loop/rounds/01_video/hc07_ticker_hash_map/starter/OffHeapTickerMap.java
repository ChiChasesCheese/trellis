/**
 * Part 4：堆外定长哈希表（FFM API：Arena + MemorySegment，Java 21 预览特性，已经用 --enable-preview 编译）。
 * 每个槽位 16 字节 [key:8][value:8]，整块内存 64 字节对齐；key == 0 表示空格（分配出来的内存已清零）。
 * 固定容量：槽位数 = 不小于 2*maxEntries 的 2 的幂；放满后再插入新 key -> IllegalStateException；已有 key 仍可更新。
 * 没有 remove、没有 resize。close() 之后任何访问 -> IllegalStateException；close() 可重复调用。
 * 提示：Arena.ofShared()（测试会换线程访问）；arena.allocate(bytes, 64)；seg.get/set(ValueLayout.JAVA_LONG, offset)。
 */
public final class OffHeapTickerMap implements AutoCloseable {
    public OffHeapTickerMap(int maxEntries) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }
    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int maxEntries() { throw new UnsupportedOperationException("TODO"); }

    /** 所有访问方法：key <= 0 -> IllegalArgumentException。 */
    public boolean containsKey(long key) { throw new UnsupportedOperationException("TODO"); }

    public long get(long key, long ifAbsent) { throw new UnsupportedOperationException("TODO"); }

    /** 返回 true = 新 key。 */
    public boolean put(long key, long value) { throw new UnsupportedOperationException("TODO"); }

    /** value += delta，返回新值；溢出 ArithmeticException。 */
    public long add(long key, long delta) { throw new UnsupportedOperationException("TODO"); }

    @Override
    public void close() { throw new UnsupportedOperationException("TODO"); }
}
