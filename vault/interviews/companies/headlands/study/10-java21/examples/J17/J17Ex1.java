import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.lang.foreign.ValueLayout;

/** J17 例 1（最简单）：Arena 管生命周期，MemorySegment 是一段带边界的内存。越界、关闭后访问都会抛异常——而不是 SIGSEGV 崩进程。 */
public class J17Ex1 {
    public static void main(String[] args) {
        MemorySegment seg;
        try (Arena arena = Arena.ofConfined()) {                 // 只允许创建它的线程访问；try-with-resources 结束时释放
            seg = arena.allocate(32, 8);                         // 32 字节，8 字节对齐；保证已清零
            System.out.println("byteSize = " + seg.byteSize() + ", 新分配的第一个 long = " + seg.get(ValueLayout.JAVA_LONG, 0));

            seg.set(ValueLayout.JAVA_LONG, 0, 18_950L);          // 偏移 0 处写一个 long
            seg.set(ValueLayout.JAVA_INT, 8, 100);               // 偏移 8 处写一个 int
            System.out.println("读回: px=" + seg.get(ValueLayout.JAVA_LONG, 0) + " qty=" + seg.get(ValueLayout.JAVA_INT, 8));

            // getAtIndex：按元素下标，不用手算字节偏移
            seg.setAtIndex(ValueLayout.JAVA_LONG, 2, 7L);        // 等价于偏移 16
            System.out.println("getAtIndex(2) = " + seg.getAtIndex(ValueLayout.JAVA_LONG, 2));

            try { seg.get(ValueLayout.JAVA_LONG, 28); }          // 28+8 > 32
            catch (IndexOutOfBoundsException e) { System.out.println("越界 -> IndexOutOfBoundsException"); }
        }
        try { seg.get(ValueLayout.JAVA_LONG, 0); }
        catch (IllegalStateException e) { System.out.println("arena 关闭后访问 -> IllegalStateException: " + e.getMessage()); }

        // 对照：另外三种 Arena
        //   Arena.ofShared()  多线程可访问，close() 需要线程同步（较慢）
        //   Arena.ofAuto()    由 GC 回收，不能手动 close
        //   Arena.global()    永不释放
        try (Arena shared = Arena.ofShared()) {
            MemorySegment s = shared.allocate(8, 8);
            Thread t = new Thread(() -> s.set(ValueLayout.JAVA_LONG, 0, 99L));
            t.start();
            try { t.join(); } catch (InterruptedException e) { }
            System.out.println("shared arena：另一线程写入 -> 主线程读到 " + s.get(ValueLayout.JAVA_LONG, 0));
        }
        try (Arena confined = Arena.ofConfined()) {
            MemorySegment s = confined.allocate(8, 8);
            Thread t = new Thread(() -> {
                try { s.get(ValueLayout.JAVA_LONG, 0); }
                catch (WrongThreadException e) { System.out.println("confined arena：别的线程访问 -> WrongThreadException"); }
            });
            t.start();
            try { t.join(); } catch (InterruptedException e) { }
        }
    }
}
