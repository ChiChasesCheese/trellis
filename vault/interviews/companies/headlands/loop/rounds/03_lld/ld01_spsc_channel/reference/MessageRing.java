import static java.lang.foreign.ValueLayout.JAVA_BYTE;
import static java.lang.foreign.ValueLayout.JAVA_INT_UNALIGNED;
import static java.lang.foreign.ValueLayout.JAVA_LONG;

import java.lang.foreign.MemorySegment;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;

/**
 * Part 3：变长消息的 SPSC 环形缓冲区，建在一块 {@link MemorySegment} 上（堆外内存或内存映射文件都行）。
 * Part 4 的 SharedChannel 把同一个结构放进 mmap 的文件里，让两个进程各开一份。
 *
 * ── 内存布局（reconstructed，全部是本题自己的约定）──────────────────────────────
 *     偏移    0  magic     long   0x5350534352494E47 ("SPSCRING")，最后写入（release），attach 时用 acquire 读来确认「已初始化」
 *     偏移    8  capacity  int    数据区字节数，2 的幂，>= 16
 *     偏移   12  version   int    1
 *     偏移  128  head      long   消费者已消费到的字节计数（只有消费者写）
 *     偏移  256  tail      long   生产者已发布到的字节计数（只有生产者写）
 *     偏移  264  closed    long   生产者调用 finish() 后置 1
 *     偏移  512  数据区    capacity 字节
 *   head / tail 各占一条 128 字节的缓存行，防伪共享。
 *
 * ── 记录格式 ────────────────────────────────────────────────────────────────
 *     [len:int32][payload: len 字节][补零到 8 字节对齐]       记录总长 recordSize(len) = (4 + len + 7) & ~7
 *     [PAD = -1 :int32][不用的字节…]                          「跳到数据区末尾」标记（见下）
 *   记录总是从 8 的倍数偏移开始，所以 4 字节的长度字段永远不会跨越数据区末尾。
 *
 * ── 回绕 (wrap-around) ─────────────────────────────────────────────────────
 *   一条记录不能被切成两半（读的人想拿到连续的字节）。如果当前位置到数据区末尾放不下，生产者先写一条 PAD 记录占满剩余部分，
 *   再从数据区开头写真正的记录。消费者读到 PAD 就直接跳到开头。
 *   关键的活性 (liveness) 细节：PAD 要「单独发布」，哪怕随后真记录没挤进去。否则会出现死锁——
 *   队列已空（消费者没东西可读，不会前进），但 tail 恰好在末尾附近，pad + 记录 > capacity，永远写不进去。
 *   单独发布 PAD 后，消费者会越过它，下一次 offer 从偏移 0 开始，空队列里一定放得下（只要消息 <= maxPayload）。
 *   代价：offer 返回 false 时可能已经悄悄发布了一个 PAD（对消息序列没有影响）。
 *
 * ── 内存序 ─────────────────────────────────────────────────────────────────
 *   和 SpscLongRing 完全一样：写完记录字节后 TAIL.setRelease；消费者 TAIL.getAcquire 之后读字节；读完 HEAD.setRelease 归还空间。
 *   长度字段、payload 都是普通读写——因为它们被 tail 的 release / acquire 保护。
 *   跨进程时同样成立：两个进程映射的是同一批物理页，缓存一致性由硬件保证，release/acquire 约束的是各自 CPU 与编译器的重排。
 *
 * 线程 / 进程约定：一个 MessageRing 对象只做一种角色：生产者对象调 offer / finish，消费者对象调 poll / isDrained。
 * 同一个 segment 上可以 attach 出多个对象，但同一角色同一时刻只能有一个。
 */
public final class MessageRing {
    public static final int HEADER_BYTES = 512;
    public static final int MIN_CAPACITY = 16;
    public static final int MAX_CAPACITY = 1 << 30;

    private static final long MAGIC = 0x5350534352494E47L;
    private static final int VERSION = 1;
    private static final long OFF_MAGIC = 0, OFF_CAPACITY = 8, OFF_VERSION = 12, OFF_HEAD = 128, OFF_TAIL = 256, OFF_CLOSED = 264;
    private static final int PAD = -1;

    /** (MemorySegment, long 字节偏移) -> long；JDK 21 里 ValueLayout.varHandle() 没有偏移坐标，用这个。 */
    private static final VarHandle LONG = MethodHandles.memorySegmentViewVarHandle(JAVA_LONG);

    private final MemorySegment seg;
    private final int capacity;
    private final int mask;
    // 生产者角色的状态
    private long tail;
    private long cachedHead;
    private boolean finished;
    // 消费者角色的状态
    private long head;
    private long cachedTail;

    private MessageRing(MemorySegment seg, int capacity) {
        this.seg = seg;
        this.capacity = capacity;
        this.mask = capacity - 1;
        this.tail = (long) LONG.getAcquire(seg, OFF_TAIL);
        this.head = (long) LONG.getAcquire(seg, OFF_HEAD);
        this.cachedHead = head;
        this.cachedTail = tail;
    }

    public static long segmentBytes(int capacity) { return HEADER_BYTES + (long) capacity; }

    private static void checkCapacity(int capacity) {
        if (capacity < MIN_CAPACITY || capacity > MAX_CAPACITY || Integer.bitCount(capacity) != 1)
            throw new IllegalArgumentException("capacity must be a power of two in [16, 2^30]: " + capacity);
    }

    /** 在一块（必须 8 字节对齐的）segment 上建一个全新的环：清零头部，写入 capacity，最后才写 magic。 */
    public static MessageRing init(MemorySegment seg, int capacity) {
        checkCapacity(capacity);
        if (seg.byteSize() < segmentBytes(capacity))
            throw new IllegalArgumentException("segment too small: " + seg.byteSize() + " < " + segmentBytes(capacity));
        seg.asSlice(0, HEADER_BYTES).fill((byte) 0);
        seg.set(JAVA_INT_UNALIGNED, OFF_CAPACITY, capacity);
        seg.set(JAVA_INT_UNALIGNED, OFF_VERSION, VERSION);
        LONG.setRelease(seg, OFF_MAGIC, MAGIC);           // 最后写：看到 magic 的人一定看到上面的 capacity
        return new MessageRing(seg, capacity);
    }

    /** 连接到已有的环（比如另一个进程建好的）。没有 magic / 版本不对 / 尺寸对不上 → IllegalStateException。 */
    public static MessageRing attach(MemorySegment seg) {
        if (seg.byteSize() < HEADER_BYTES || (long) LONG.getAcquire(seg, OFF_MAGIC) != MAGIC)
            throw new IllegalStateException("not an initialised SPSC ring");
        int version = seg.get(JAVA_INT_UNALIGNED, OFF_VERSION);
        int capacity = seg.get(JAVA_INT_UNALIGNED, OFF_CAPACITY);
        if (version != VERSION) throw new IllegalStateException("unsupported version " + version);
        if (capacity < MIN_CAPACITY || capacity > MAX_CAPACITY || Integer.bitCount(capacity) != 1
                || seg.byteSize() < segmentBytes(capacity))
            throw new IllegalStateException("corrupt header: capacity=" + capacity + ", segment=" + seg.byteSize());
        return new MessageRing(seg, capacity);
    }

    public int capacity() { return capacity; }
    /** 单条消息 payload 的上限：一条记录要能整个放进空环里。 */
    public int maxPayload() { return capacity - 4; }

    static int recordSize(int len) { return (4 + len + 7) & ~7; }

    // ───────────────────────── 生产者 ─────────────────────────

    /**
     * 追加一条消息。返回 false = 现在放不下（满）。payload 超过 maxPayload() 永远放不下 → IllegalArgumentException。
     * finish() 之后调用 → IllegalStateException。
     */
    public boolean offer(byte[] msg) {
        int len = msg.length;
        if (len > maxPayload()) throw new IllegalArgumentException("message too large: " + len + " > " + maxPayload());
        if (finished) throw new IllegalStateException("producer already finished");
        int rec = recordSize(len);
        long t = tail;
        int idx = (int) (t & mask);
        int toEnd = capacity - idx;
        if (rec > toEnd) {                                // 放不下连续的一整条：先单独发布一条 PAD，占满剩余部分
            if (!hasRoom(t, toEnd)) return false;
            seg.set(JAVA_INT_UNALIGNED, HEADER_BYTES + idx, PAD);
            t += toEnd;
            tail = t;
            LONG.setRelease(seg, OFF_TAIL, t);
            idx = 0;
        }
        if (!hasRoom(t, rec)) return false;
        long at = HEADER_BYTES + idx;
        MemorySegment.copy(msg, 0, seg, JAVA_BYTE, at + 4, len);        // payload
        seg.set(JAVA_INT_UNALIGNED, at, len);                           // 长度前缀
        tail = t + rec;
        LONG.setRelease(seg, OFF_TAIL, t + rec);                        // 发布
        return true;
    }

    /** 还有 need 字节空间吗？先用缓存的 head 判断，不够再读真正的 head（cached index）。 */
    private boolean hasRoom(long t, int need) {
        if (capacity - (t - cachedHead) >= need) return true;
        cachedHead = (long) LONG.getAcquire(seg, OFF_HEAD);
        return capacity - (t - cachedHead) >= need;
    }

    /** 告诉消费者「不会再有消息了」。幂等。 */
    public void finish() {
        finished = true;
        LONG.setRelease(seg, OFF_CLOSED, 1L);             // 在最后一次 tail 发布之后
    }

    // ───────────────────────── 消费者 ─────────────────────────

    /** 取走下一条消息；暂时没有（空）返回 null。注意 null 不等于结束：结束用 isDrained()。 */
    public byte[] poll() {
        long h = head;
        while (true) {
            if (h == cachedTail) {
                cachedTail = (long) LONG.getAcquire(seg, OFF_TAIL);
                if (h == cachedTail) return null;
            }
            int idx = (int) (h & mask);
            long at = HEADER_BYTES + idx;
            int len = seg.get(JAVA_INT_UNALIGNED, at);
            if (len == PAD) {                              // 跳到数据区开头
                h += capacity - idx;
                head = h;
                LONG.setRelease(seg, OFF_HEAD, h);
                continue;
            }
            byte[] out = new byte[len];
            MemorySegment.copy(seg, JAVA_BYTE, at + 4, out, 0, len);
            h += recordSize(len);
            head = h;
            LONG.setRelease(seg, OFF_HEAD, h);             // 读完才归还
            return out;
        }
    }

    /**
     * 生产者已 finish() 且所有已发布的内容都被消费者读完（包括末尾可能残留的 PAD）。
     * 顺序很重要：先读 closed，再读 tail——生产者是「先发布最后一次 tail，再置 closed」，
     * 看到 closed 就保证看到了最终的 tail。反过来读会漏掉最后几条消息。
     */
    public boolean isDrained() {
        if ((long) LONG.getAcquire(seg, OFF_CLOSED) == 0L) return false;
        return head == (long) LONG.getAcquire(seg, OFF_TAIL);
    }

    /** 已发布但未消费的字节数（含 PAD）。任何角色可调，近似值。 */
    public long bytesPending() {
        long h = (long) LONG.getAcquire(seg, OFF_HEAD);
        long t = (long) LONG.getAcquire(seg, OFF_TAIL);
        return Math.clamp(t - h, 0, capacity);
    }
}
