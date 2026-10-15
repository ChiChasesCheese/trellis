import static java.lang.foreign.MemoryLayout.PathElement.groupElement;
import static java.lang.foreign.MemoryLayout.PathElement.sequenceElement;
import static java.lang.foreign.ValueLayout.JAVA_INT;
import static java.lang.foreign.ValueLayout.JAVA_LONG;

import java.lang.foreign.Arena;
import java.lang.foreign.MemoryLayout;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.SequenceLayout;
import java.lang.foreign.StructLayout;
import java.lang.invoke.VarHandle;

/**
 * Part 3：堆外 (off-heap) 版本。一个 Arena 分配一整块 MemorySegment，每个槽位是 32 字节的定长记录：
 *
 *     偏移  0  gen   int   版本号（偶数空闲 / 奇数在用，同 GenPool）
 *     偏移  4  next  int   空闲链表的下一个槽位（只在空闲时有意义）
 *     偏移  8  id    long  ┐
 *     偏移 16  px    long  │ Order 的四个字段（只在使用时有意义）
 *     偏移 24  qty   int   │
 *     偏移 28  side  int   ┘
 *
 * 为什么放堆外：这 capacity 个订单对 GC「不存在」——不管池多大，GC 扫描的工作量不变；布局连续（每 64 字节一条缓存行正好 2 个槽位）。
 * 为什么把 gen / next 也放进槽位：空闲链表和版本号跟着数据走，一次分配、没有任何堆上的 per-slot 对象，也没有第二个数组。
 * 只有 head / available 两个标量放在 Java 字段里。
 *
 * 字段访问用 MemoryLayout 生成的 VarHandle，而不是手算偏移：改字段只改布局声明，不会有魔法数字。
 * 非线程安全（和 GenPool 一样）；Arena.ofShared() 只是允许「在别的线程里使用」（例如 JUnit 的超时断言会换线程），不是说它并发安全。
 */
public final class OffHeapOrderPool implements AutoCloseable {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;
    private static final int END = -1;

    private static final StructLayout SLOT = MemoryLayout.structLayout(
            JAVA_INT.withName("gen"),
            JAVA_INT.withName("next"),
            JAVA_LONG.withName("id"),
            JAVA_LONG.withName("px"),
            JAVA_INT.withName("qty"),
            JAVA_INT.withName("side"));
    /** 布局里的元素个数用 MAX_CAPACITY：它只是描述，不分配内存；这样 VarHandle 可以是 static final，JIT 能内联。 */
    private static final SequenceLayout SLOTS = MemoryLayout.sequenceLayout(MAX_CAPACITY, SLOT);
    // 每个 VarHandle 的坐标是 (MemorySegment, long 槽位下标)
    private static final VarHandle GEN = SLOTS.varHandle(sequenceElement(), groupElement("gen"));
    private static final VarHandle NEXT = SLOTS.varHandle(sequenceElement(), groupElement("next"));
    private static final VarHandle ID = SLOTS.varHandle(sequenceElement(), groupElement("id"));
    private static final VarHandle PX = SLOTS.varHandle(sequenceElement(), groupElement("px"));
    private static final VarHandle QTY = SLOTS.varHandle(sequenceElement(), groupElement("qty"));
    private static final VarHandle SIDE = SLOTS.varHandle(sequenceElement(), groupElement("side"));

    private final Arena arena;
    private final MemorySegment seg;
    private final int capacity;
    private int head;
    private int available;

    public OffHeapOrderPool(int capacity) {
        if (capacity < 1 || capacity > MAX_CAPACITY) throw new IllegalArgumentException("capacity: " + capacity);
        this.capacity = capacity;
        this.arena = Arena.ofShared();
        this.seg = arena.allocate(SLOT.byteSize() * capacity, 64);   // 保证已清零，gen 全为 0 = 全部空闲
        for (int i = 0; i < capacity; i++) NEXT.set(seg, (long) i, i + 1 < capacity ? i + 1 : END);
        this.head = 0;
        this.available = capacity;
    }

    public int capacity() { return capacity; }
    public int available() { return available; }
    /** 整块内存的字节数；是 long——capacity * 32 可以超过 2^31（ByteBuffer 做不到）。 */
    public long byteSize() { return seg.byteSize(); }
    public static long recordBytes() { return SLOT.byteSize(); }

    public long allocate() {
        int index = head;
        if (index == END) return NONE;
        head = (int) NEXT.get(seg, (long) index);
        int g = (int) GEN.get(seg, (long) index) + 1;
        GEN.set(seg, (long) index, g);
        // 清零载荷：上一个使用者的数据不能漏给下一个（C 的 malloc 不清零是一类经典的信息泄漏）
        ID.set(seg, (long) index, 0L);
        PX.set(seg, (long) index, 0L);
        QTY.set(seg, (long) index, 0);
        SIDE.set(seg, (long) index, 0);
        available--;
        return GenPool.handle(index, g);
    }

    public FreeResult free(long handle) {
        int index = GenPool.indexOf(handle);
        int g = GenPool.generationOf(handle);
        if (index < 0 || index >= capacity || (g & 1) == 0) return FreeResult.INVALID;
        if ((int) GEN.get(seg, (long) index) != g) return FreeResult.DOUBLE_FREE;
        GEN.set(seg, (long) index, g + 1);
        NEXT.set(seg, (long) index, head);
        head = index;
        available++;
        return FreeResult.FREED;
    }

    public boolean isLive(long handle) {
        int index = GenPool.indexOf(handle);
        int g = GenPool.generationOf(handle);
        return index >= 0 && index < capacity && (g & 1) == 1 && (int) GEN.get(seg, (long) index) == g;
    }

    private int liveIndex(long handle) {
        if (!isLive(handle)) throw new IllegalStateException("stale or invalid handle: " + Long.toHexString(handle));
        return GenPool.indexOf(handle);
    }

    /**
     * 热路径写法：直接写四个字段，不创建任何 Java 对象。API 设计要点——只给「必须 new 一个 Order」的接口，
     * 调用方就没法写出零分配的热循环（逃逸分析不保证每次都能消掉那个 new）。
     */
    public void put(long handle, long id, long px, int qty, int side) {
        long i = liveIndex(handle);
        ID.set(seg, i, id);
        PX.set(seg, i, px);
        QTY.set(seg, i, qty);
        SIDE.set(seg, i, side);
    }

    public void put(long handle, Order order) {
        // J04 record 模式：一步把 Order 拆成四个变量；比 order.id(), order.px()... 少写四次访问器
        switch (order) {
            case Order(long id, long px, int qty, int side) -> put(handle, id, px, qty, side);
        }
    }

    /** 零分配读：只读一个字段。 */
    public long px(long handle) { return (long) PX.get(seg, liveIndex(handle)); }
    public int qty(long handle) { return (int) QTY.get(seg, liveIndex(handle)); }

    /** 方便但每次调用都 new 一个 Order（拷贝）；不在热路径上用。 */
    public Order get(long handle) {
        long i = liveIndex(handle);
        return new Order((long) ID.get(seg, i), (long) PX.get(seg, i), (int) QTY.get(seg, i), (int) SIDE.get(seg, i));
    }

    /** 幂等：重复 close 不抛（Arena.close 第二次会抛，所以先判断）。 */
    @Override
    public void close() {
        if (arena.scope().isAlive()) arena.close();
    }
}
