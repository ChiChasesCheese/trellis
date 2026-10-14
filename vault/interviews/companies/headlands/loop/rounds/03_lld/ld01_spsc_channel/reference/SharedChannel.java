import java.io.IOException;
import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.nio.channels.FileChannel;
import java.nio.channels.FileChannel.MapMode;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

/**
 * Part 4：两个进程之间的有界共享内存消息通道 —— MessageRing 放进一个内存映射文件 (memory-mapped file)。
 *
 *   进程 A（生产者）                    进程 B（消费者）
 *   SharedChannel.create(file, cap)     SharedChannel.open(file)
 *        │ mmap                               │ mmap
 *        └────────────►  同一批物理页  ◄───────┘
 *
 * 为什么 mmap 能共享：操作系统把文件的页缓存 (page cache) 同时映射进两个进程的地址空间（MAP_SHARED），
 * 两边读写的是同一块物理内存，不经过 read/write 系统调用，也不拷贝。这是最快的进程间通信方式之一。
 * 文件本身不是重点——也可以用 /dev/shm 或 shm_open；用文件是因为它跨平台、测试好清理，并且「进程崩了数据还在」。
 *
 * 使用顺序：生产者 create() 完成之后，消费者才能 open()（create 里 magic 是最后写的，open 会检查）。
 * 同一个对象只扮演一个角色：send / finish（生产者）或 receive / isDrained（消费者）。
 *
 * FFM 的用法：FileChannel.map(mode, offset, size, Arena) 返回 MemorySegment（JDK 21 预览 API）。
 * 用 Arena.ofShared()：JUnit 超时断言之类可能换线程；close() 时整块取消映射。
 */
public final class SharedChannel implements AutoCloseable {
    private final Arena arena;
    private final MessageRing ring;

    private SharedChannel(Arena arena, MessageRing ring) {
        this.arena = arena;
        this.ring = ring;
    }

    /** 新建（或覆盖）文件，大小 = MessageRing.segmentBytes(capacity)，初始化头部。 */
    public static SharedChannel create(Path file, int capacity) throws IOException {
        long size = MessageRing.segmentBytes(capacity);       // 先校验 capacity，再动文件
        Arena arena = Arena.ofShared();
        try (FileChannel ch = FileChannel.open(file, StandardOpenOption.CREATE, StandardOpenOption.READ,
                StandardOpenOption.WRITE, StandardOpenOption.TRUNCATE_EXISTING)) {
            MemorySegment seg = ch.map(MapMode.READ_WRITE, 0, size, arena);     // 文件被扩展到 size，新增部分全零
            return new SharedChannel(arena, MessageRing.init(seg, capacity));
        } catch (IOException | RuntimeException e) {
            arena.close();
            throw e;
        }                                                       // FileChannel 关了，映射仍然有效（直到 arena.close）
    }

    /** 打开已有的通道文件。不是合法的通道文件 → IllegalStateException；读不到 → IOException。 */
    public static SharedChannel open(Path file) throws IOException {
        Arena arena = Arena.ofShared();
        try (FileChannel ch = FileChannel.open(file, StandardOpenOption.READ, StandardOpenOption.WRITE)) {
            long size = ch.size();
            if (size < MessageRing.HEADER_BYTES) throw new IllegalStateException("file too small to be a channel: " + size);
            MemorySegment seg = ch.map(MapMode.READ_WRITE, 0, size, arena);
            return new SharedChannel(arena, MessageRing.attach(seg));
        } catch (IOException | RuntimeException e) {
            arena.close();
            throw e;
        }
    }

    public int capacity() { return ring.capacity(); }
    public int maxPayload() { return ring.maxPayload(); }

    /** 生产者：false = 通道满。 */
    public boolean send(byte[] msg) { return ring.offer(msg); }
    /** 生产者：不会再有消息。 */
    public void finish() { ring.finish(); }

    /** 消费者：null = 暂时没有（不等于结束）。 */
    public byte[] receive() { return ring.poll(); }
    /** 消费者：生产者已 finish 且全部读完。 */
    public boolean isDrained() { return ring.isDrained(); }

    /** 取消映射。幂等。关闭后任何访问抛 IllegalStateException。文件留在磁盘上（对端可能还在用，或之后想重新 open）。 */
    @Override
    public void close() {
        if (arena.scope().isAlive()) arena.close();
    }
}
