import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;

/**
 * Part 3：堆外版本。一个 Arena 分配一整块 MemorySegment，每个槽位是定长记录（建议 32 字节：gen int、next int、再接 Order 的 4 个字段）。
 *
 * 契约：
 *   * handle 规则同 GenPool（可以直接复用 GenPool.handle / indexOf / generationOf）；
 *   * allocate()：返回的记录必须已清零（上一个主人的数据不能漏出来）；池空返回 NONE；
 *   * put / get：handle 不是「当前有效」→ IllegalStateException；get 返回的 Order 是拷贝；
 *   * free：同 GenPool；close()：释放整块内存，可以重复调用；关闭后任何访问抛 IllegalStateException（Arena 自带的行为）；
 *   * 要用 Arena.ofShared()（允许别的线程访问，JUnit 的超时断言会换线程）；
 *   * 字段读写建议用 MemoryLayout + VarHandle（见 study/10-java21/J17_ffm_api.md §2.3），不要手算偏移。
 */
public final class OffHeapOrderPool implements AutoCloseable {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;

    public OffHeapOrderPool(int capacity) { throw new UnsupportedOperationException("TODO"); }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int available() { throw new UnsupportedOperationException("TODO"); }
    /** 整块内存的字节数（long）。 */
    public long byteSize() { throw new UnsupportedOperationException("TODO"); }
    /** 一个槽位占多少字节（含头）。 */
    public static long recordBytes() { throw new UnsupportedOperationException("TODO"); }

    public long allocate() { throw new UnsupportedOperationException("TODO"); }
    public FreeResult free(long handle) { throw new UnsupportedOperationException("TODO"); }
    public boolean isLive(long handle) { throw new UnsupportedOperationException("TODO"); }

    /** 热路径写法：直接写四个字段，不创建 Java 对象。 */
    public void put(long handle, long id, long px, int qty, int side) { throw new UnsupportedOperationException("TODO"); }
    public void put(long handle, Order order) { throw new UnsupportedOperationException("TODO"); }
    /** 零分配读：只读一个字段（handle 无效 → IllegalStateException）。 */
    public long px(long handle) { throw new UnsupportedOperationException("TODO"); }
    public int qty(long handle) { throw new UnsupportedOperationException("TODO"); }
    /** 拷贝出一个 Order（会 new 对象，不在热路径上用）。 */
    public Order get(long handle) { throw new UnsupportedOperationException("TODO"); }

    @Override
    public void close() { throw new UnsupportedOperationException("TODO"); }
}
