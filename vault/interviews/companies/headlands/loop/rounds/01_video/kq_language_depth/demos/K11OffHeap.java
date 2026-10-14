import java.lang.foreign.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

/** Off-heap: direct ByteBuffer limits, FFM Arena (preview in 21: --enable-preview), bounds & lifetime safety. */
public class K11OffHeap {
    public static void main(String[] a) {
        try { ByteBuffer.allocateDirect(64 * 1024 * 1024); }
        catch (OutOfMemoryError e) { System.out.println("allocateDirect(64MB) with MaxDirectMemorySize=16m -> " + e); }

        ByteBuffer bb = ByteBuffer.allocateDirect(4096).order(ByteOrder.nativeOrder());
        bb.putLong(0, 123456789L); System.out.println("direct buffer isDirect=" + bb.isDirect() + " readback=" + bb.getLong(0));

        MemorySegment leaked;
        try (Arena arena = Arena.ofConfined()) {
            MemorySegment seg = arena.allocate(8L * 1_000_000, 8);
            for (long i = 0; i < 1_000_000; i++) seg.setAtIndex(ValueLayout.JAVA_LONG, i, i * 2);
            long sum = 0; for (long i = 0; i < 1_000_000; i++) sum += seg.getAtIndex(ValueLayout.JAVA_LONG, i);
            System.out.println("1M longs off-heap, sum=" + sum + ", byteSize=" + seg.byteSize());
            try { seg.getAtIndex(ValueLayout.JAVA_LONG, 1_000_000); }
            catch (IndexOutOfBoundsException e) { System.out.println("out of bounds -> " + e.getClass().getSimpleName()); }
            leaked = seg;
        }
        try { leaked.get(ValueLayout.JAVA_LONG, 0); }
        catch (IllegalStateException e) { System.out.println("use after Arena.close() -> " + e.getClass().getSimpleName() + ": " + e.getMessage()); }

        // record layout: struct { int id; long price; int qty } with padding
        StructLayout ORDER = MemoryLayout.structLayout(
            ValueLayout.JAVA_INT.withName("id"), MemoryLayout.paddingLayout(4),
            ValueLayout.JAVA_LONG.withName("price"), ValueLayout.JAVA_INT.withName("qty"), MemoryLayout.paddingLayout(4));
        System.out.println("struct Order size=" + ORDER.byteSize() + " alignment=" + ORDER.byteAlignment());
    }
}
