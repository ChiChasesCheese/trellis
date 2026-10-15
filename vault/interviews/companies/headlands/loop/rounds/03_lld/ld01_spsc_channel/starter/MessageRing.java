import java.lang.foreign.MemorySegment;

/**
 * Part 3：变长消息的 SPSC 环形缓冲区，建在一块 MemorySegment 上（Part 4 会把同一个结构放进内存映射文件，让两个进程各开一份）。
 *
 * 布局（reconstructed，是本题自己的约定，见 problem.md「布局」一节，测试只通过公共 API 观察它，但 HEADER_BYTES / segmentBytes 是约定的一部分）：
 *     头部 HEADER_BYTES = 512 字节：magic、capacity、version；head 和 tail 各占一条 128 字节的缓存行；closed 标志；
 *     之后是 capacity 字节的数据区（2 的幂，>= 16）。
 *     记录 = [len:int32][payload][补零到 8 字节对齐]；放不下连续的一整条时先写一条 PAD 记录（len = -1）占满到末尾，再从开头写。
 *     head / tail 是只增不减的「字节计数」，空间 = capacity - (tail - head)。
 *
 * 契约：
 *   * init：清零头部、写 capacity / version，最后才用 release 写 magic；capacity 不合法或 segment 太小 → IllegalArgumentException。
 *   * attach：magic 不对 / 版本不对 / 尺寸对不上 → IllegalStateException。
 *   * offer：payload > maxPayload()（= capacity - 4）→ IllegalArgumentException（永远放不下）；暂时放不下 → false；finish() 之后 → IllegalStateException。
 *     需要 PAD 时，PAD 要**单独发布**（哪怕随后真记录没挤进去，offer 返回 false）——否则空环上 tail 恰好靠近末尾时会永远放不进去。
 *   * poll：没有消息返回 null（遇到 PAD 就越过它）；isDrained：生产者已 finish 且 head 追上了 tail。先读 closed 再读 tail。
 *   * 内存序：写完记录字节后 release 发布 tail；消费者 acquire 读 tail 后才读字节；读完 release 发布 head。
 *     数据区字节用普通读写即可。VarHandle 可用 MethodHandles.memorySegmentViewVarHandle(ValueLayout.JAVA_LONG)（坐标：segment, 字节偏移）。
 *   * cached index：生产者缓存 head，消费者缓存 tail。
 */
public final class MessageRing {
    public static final int HEADER_BYTES = 512;
    public static final int MIN_CAPACITY = 16;
    public static final int MAX_CAPACITY = 1 << 30;

    private MessageRing() {}

    /** 整块 segment 需要的字节数 = HEADER_BYTES + capacity；capacity 不合法 → IllegalArgumentException（让 SharedChannel.create 能在动文件之前先校验）。 */
    public static long segmentBytes(int capacity) { throw new UnsupportedOperationException("TODO"); }

    public static MessageRing init(MemorySegment seg, int capacity) { throw new UnsupportedOperationException("TODO"); }
    public static MessageRing attach(MemorySegment seg) { throw new UnsupportedOperationException("TODO"); }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int maxPayload() { throw new UnsupportedOperationException("TODO"); }

    // 生产者
    public boolean offer(byte[] msg) { throw new UnsupportedOperationException("TODO"); }
    public void finish() { throw new UnsupportedOperationException("TODO"); }

    // 消费者
    public byte[] poll() { throw new UnsupportedOperationException("TODO"); }
    public boolean isDrained() { throw new UnsupportedOperationException("TODO"); }

    /** 已发布但未消费的字节数（含 PAD），近似值，夹在 [0, capacity]。 */
    public long bytesPending() { throw new UnsupportedOperationException("TODO"); }
}
