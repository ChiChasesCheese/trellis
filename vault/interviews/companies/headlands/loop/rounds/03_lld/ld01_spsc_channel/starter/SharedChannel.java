import java.io.IOException;
import java.nio.file.Path;

/**
 * Part 4：两个进程之间的有界共享内存消息通道 = MessageRing 放进一个内存映射文件。
 *
 *   * create(file, capacity)：新建 / 覆盖文件，大小 = MessageRing.segmentBytes(capacity)，用 FileChannel.map(READ_WRITE, 0, size, arena)
 *     映射成 MemorySegment（Arena.ofShared()），再 MessageRing.init。capacity 不合法 → IllegalArgumentException（且不要动文件）。
 *   * open(file)：映射已有文件并 MessageRing.attach。文件不存在 → IOException（NoSuchFileException）；
 *     太小 / 不是通道文件 → IllegalStateException。
 *   * send / finish 是生产者角色，receive / isDrained 是消费者角色。
 *   * close()：取消映射（arena.close()），幂等，不删文件；之后任何访问抛 IllegalStateException。
 *
 * 跨进程测试会启动子 JVM（见 test/SpscChild.java），所以 create 必须在子进程 open 之前完成（magic 最后写）。
 */
public final class SharedChannel implements AutoCloseable {
    private SharedChannel() {}

    public static SharedChannel create(Path file, int capacity) throws IOException { throw new UnsupportedOperationException("TODO"); }
    public static SharedChannel open(Path file) throws IOException { throw new UnsupportedOperationException("TODO"); }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int maxPayload() { throw new UnsupportedOperationException("TODO"); }

    public boolean send(byte[] msg) { throw new UnsupportedOperationException("TODO"); }
    public void finish() { throw new UnsupportedOperationException("TODO"); }

    public byte[] receive() { throw new UnsupportedOperationException("TODO"); }
    public boolean isDrained() { throw new UnsupportedOperationException("TODO"); }

    @Override
    public void close() { throw new UnsupportedOperationException("TODO"); }
}
