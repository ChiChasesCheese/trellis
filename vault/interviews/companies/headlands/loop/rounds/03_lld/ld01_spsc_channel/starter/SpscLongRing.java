/**
 * Part 2：线程安全的 SPSC（单生产者单消费者）环形缓冲区。接口和语义同 LongRing，加上：
 *
 *   * 线程约定：恰好一个线程调 offer / isFull（生产者），恰好一个线程调 poll / isEmpty（消费者），size() 任何线程可调（近似值，夹在 [0, capacity]）。
 *   * 不许用锁、不许用 CAS：tail 只有生产者写、head 只有消费者写。用 VarHandle 的 setRelease / getAcquire 发布和读取下标
 *     （先写数据再 release 发布 tail；消费者 acquire 读 tail 之后才读数据；读完数据再 release 归还 head）。
 *   * cached index：生产者缓存对方的 head，只有「按旧值看是满的」才去读真正的 head；消费者缓存 tail，同理。
 *   * 伪共享：生产者写的字段（tail、cachedHead）和消费者写的字段（head、cachedTail）要相隔至少一条缓存行（Apple M 系列 128 字节）。
 *     Java 常用的办法是继承链 + 填充 long（见讲义 ld01 §4.2），实测方法见讲义 §4.2。
 */
public final class SpscLongRing implements LongQueue {
    public static final int MAX_CAPACITY = 1 << 30;

    public SpscLongRing(int capacity) { throw new UnsupportedOperationException("TODO"); }

    @Override public int capacity() { throw new UnsupportedOperationException("TODO"); }
    @Override public int size() { throw new UnsupportedOperationException("TODO"); }
    @Override public boolean isEmpty() { throw new UnsupportedOperationException("TODO"); }
    @Override public boolean isFull() { throw new UnsupportedOperationException("TODO"); }
    @Override public boolean offer(long value) { throw new UnsupportedOperationException("TODO"); }
    @Override public long poll() { throw new UnsupportedOperationException("TODO"); }
}
