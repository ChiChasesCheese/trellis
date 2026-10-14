import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.util.NoSuchElementException;

/*
 * 字段布局：为了避免伪共享（false sharing），让「生产者写的字段」和「消费者写的字段」落在不同的缓存行。
 * Java 没有 C 的 alignas，常用技巧是借助继承：JVM 总是把父类的字段排在子类字段前面，且不会跨类重排，
 * 所以在两组热字段之间插一个「只有填充字段」的类，就能把它们推开 128 字节（Apple M 系列的缓存行是 128 字节，x86 是 64）。
 *
 *   RingBase    : buf, mask             只读，两个线程都要读
 *   PadA        : 15 个 long (120 B)    填充
 *   ProducerFields: tail, cachedHead    只有生产者线程写
 *   PadB        : 15 个 long            填充
 *   ConsumerFields: head, cachedTail    只有消费者线程写
 *   PadC        : 15 个 long            填充（挡住后面可能分配在相邻内存里的别的对象）
 *
 * 填充字段从来没被读写过，JIT 会不会把它们优化掉？不会：对象布局在类加载时就定了，JIT 只优化代码，不会改字段布局。
 * （JDK 内部用 @jdk.internal.vm.annotation.Contended 做同一件事；用户代码要加 -XX:-RestrictContended，所以这里用继承技巧。）
 */
abstract class RingBase {
    final long[] buf;
    final int mask;
    RingBase(int capacity) { this.buf = new long[capacity]; this.mask = capacity - 1; }
}
abstract class PadA extends RingBase {
    long a01, a02, a03, a04, a05, a06, a07, a08, a09, a10, a11, a12, a13, a14, a15;
    PadA(int capacity) { super(capacity); }
}
abstract class ProducerFields extends PadA {
    long tail;          // 只有生产者写；消费者通过 acquire 读
    long cachedHead;    // 生产者对 head 的「旧快照」
    ProducerFields(int capacity) { super(capacity); }
}
abstract class PadB extends ProducerFields {
    long b01, b02, b03, b04, b05, b06, b07, b08, b09, b10, b11, b12, b13, b14, b15;
    PadB(int capacity) { super(capacity); }
}
abstract class ConsumerFields extends PadB {
    long head;          // 只有消费者写；生产者通过 acquire 读
    long cachedTail;    // 消费者对 tail 的「旧快照」
    ConsumerFields(int capacity) { super(capacity); }
}
abstract class PadC extends ConsumerFields {
    long c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14, c15;
    PadC(int capacity) { super(capacity); }
}

/**
 * Part 2：线程安全的 SPSC（single-producer single-consumer，单生产者单消费者）环形缓冲区。
 *
 * 线程约定（违反了就没有任何保证）：
 *   * 恰好一个线程调用 offer / isFull（生产者）；
 *   * 恰好一个线程调用 poll / isEmpty（消费者）；
 *   * size() 任何线程都可以调，结果是近似值。
 *
 * 为什么不需要锁，也不需要 CAS：tail 只有生产者写，head 只有消费者写，每个变量只有一个写者，没有「两个人同时改」的情况。
 * 需要的只是「可见性 + 顺序」，用 release / acquire 就够了：
 *
 *   生产者：  buf[i] = v;                       // ① 先写数据
 *            TAIL.setRelease(tail + 1);         // ② 再发布 tail（release：①不会被重排到②之后）
 *   消费者：  t = TAIL.getAcquire();            // ③ 读 tail（acquire：④不会被重排到③之前）
 *            v = buf[h];                        // ④ 读数据；只要③读到了②写的值，④就一定看到①写的数据
 *            HEAD.setRelease(h + 1);            // ⑤ 归还槽位：生产者 acquire 读到新 head 后才会覆盖这个槽，⑤保证④先读完
 *
 * 缓存对方的下标（cached index）：
 *   生产者每次 offer 都要知道「满了没」，原本得读一次 head（消费者在写它，那条缓存行总在消费者核心里，读它要跨核通信）。
 *   办法：自己保存一份旧的 head（cachedHead）。只有旧值看起来满了才去读真正的 head。因为 head 只增不减，旧值只会让我们「低估空位」，
 *   绝不会高估——所以用旧值判断「有空位」永远是安全的。消费者对 tail 同理。
 *   效果：在队列不是几乎满 / 几乎空的稳态下，每个线程每批只触碰一次对方的缓存行，而不是每条消息一次。
 */
public final class SpscLongRing extends PadC implements LongQueue {
    public static final int MAX_CAPACITY = 1 << 30;

    private static final VarHandle HEAD;
    private static final VarHandle TAIL;
    static {
        try {
            var l = MethodHandles.lookup();
            HEAD = l.findVarHandle(ConsumerFields.class, "head", long.class);
            TAIL = l.findVarHandle(ProducerFields.class, "tail", long.class);
        } catch (ReflectiveOperationException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    public SpscLongRing(int capacity) {
        super(checkCapacity(capacity));
    }

    private static int checkCapacity(int capacity) {
        if (capacity < 1 || capacity > MAX_CAPACITY || Integer.bitCount(capacity) != 1)
            throw new IllegalArgumentException("capacity must be a power of two in [1, 2^30]: " + capacity);
        return capacity;
    }

    @Override public int capacity() { return buf.length; }

    /** 近似值：先读 head 再读 tail（tail 只增，所以差不会为负），再夹到 [0, capacity]。任何线程可调。 */
    @Override
    public int size() {
        long h = (long) HEAD.getAcquire(this);
        long t = (long) TAIL.getAcquire(this);
        return (int) Math.clamp(t - h, 0, buf.length);   // J15 Math.clamp (Java 21)
    }

    /** 仅消费者线程。 */
    @Override
    public boolean isEmpty() {
        return head == (long) TAIL.getAcquire(this);
    }

    /** 仅生产者线程。 */
    @Override
    public boolean isFull() {
        return tail - (long) HEAD.getAcquire(this) == buf.length;
    }

    /** 仅生产者线程。 */
    @Override
    public boolean offer(long value) {
        long t = tail;                                  // 自己独占写，普通读即可
        if (t - cachedHead == buf.length) {             // 按旧快照看是满的 → 才去读真正的 head
            cachedHead = (long) HEAD.getAcquire(this);
            if (t - cachedHead == buf.length) return false;
        }
        buf[(int) (t & mask)] = value;                  // ① 数据
        TAIL.setRelease(this, t + 1);                   // ② 发布
        return true;
    }

    /** 仅消费者线程。 */
    @Override
    public long poll() {
        long h = head;
        if (h == cachedTail) {                          // 按旧快照看是空的 → 才去读真正的 tail
            cachedTail = (long) TAIL.getAcquire(this);
            if (h == cachedTail) throw new NoSuchElementException("ring is empty");
        }
        long v = buf[(int) (h & mask)];                 // ④
        HEAD.setRelease(this, h + 1);                   // ⑤
        return v;
    }
}
