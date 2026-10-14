import java.lang.foreign.*;
import java.lang.invoke.VarHandle;
import java.lang.foreign.MemoryLayout.PathElement;

/**
 * J17 例 2：用 MemoryLayout 描述"结构体"，让 JDK 算偏移量；在堆外开一个 100 万条成交记录的池。
 *   struct Fill { long id; long px; int qty; /* 4 字节填充 *\/ }  = 24 字节
 */
public class J17Ex2 {
    static final StructLayout FILL = MemoryLayout.structLayout(
            ValueLayout.JAVA_LONG.withName("id"),
            ValueLayout.JAVA_LONG.withName("px"),
            ValueLayout.JAVA_INT.withName("qty"),
            MemoryLayout.paddingLayout(4)                      // 补到 8 的倍数，让下一条记录的 long 对齐
    ).withName("Fill");

    // JDK 21：varHandle 的坐标是 (MemorySegment segment, long index)；
    // JDK 22 起坐标变成 (MemorySegment segment, long baseOffset, long index) —— 这是预览期间发生的不兼容改动之一
    static final VarHandle PX = FILL.varHandle(PathElement.groupElement("px"));
    static final VarHandle QTY = FILL.varHandle(PathElement.groupElement("qty"));

    public static void main(String[] args) {
        System.out.println("FILL.byteSize = " + FILL.byteSize() + ", alignment = " + FILL.byteAlignment());
        System.out.println("offset(px) = " + FILL.byteOffset(PathElement.groupElement("px")) + ", offset(qty) = " + FILL.byteOffset(PathElement.groupElement("qty")));

        int n = 1_000_000;
        SequenceLayout POOL = MemoryLayout.sequenceLayout(n, FILL);
        VarHandle POOL_PX = POOL.varHandle(PathElement.sequenceElement(), PathElement.groupElement("px"));
        VarHandle POOL_QTY = POOL.varHandle(PathElement.sequenceElement(), PathElement.groupElement("qty"));
        VarHandle POOL_ID = POOL.varHandle(PathElement.sequenceElement(), PathElement.groupElement("id"));

        try (Arena arena = Arena.ofConfined()) {
            MemorySegment pool = arena.allocate(POOL);         // 24,000,000 字节，已清零，按 POOL 的对齐
            System.out.println("pool.byteSize = " + pool.byteSize());
            for (long i = 0; i < n; i++) {
                POOL_ID.set(pool, i, i);                       // (segment, index, value)
                POOL_PX.set(pool, i, 18_950L + (i % 100));
                POOL_QTY.set(pool, i, 100 + (int) (i % 7));
            }
            long notional = 0, qty = 0;
            for (long i = 0; i < n; i++) {
                long px = (long) POOL_PX.get(pool, i);
                int q = (int) POOL_QTY.get(pool, i);
                notional = Math.addExact(notional, px * q);
                qty += q;
            }
            System.out.println("n = " + n + ", qty = " + qty + ", notional = " + notional + ", VWAP = " + (double) notional / qty);
        }   // 离开 try：24MB 堆外内存立刻归还；不依赖 GC
    }
}
