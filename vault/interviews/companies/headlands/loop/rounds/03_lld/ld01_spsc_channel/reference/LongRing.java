import java.util.NoSuchElementException;

/**
 * Part 1：环形缓冲区 (ring buffer) —— 单线程语义版。
 *
 * 数据结构：
 *   buf[capacity]   capacity 是 2 的幂
 *   head            下一个要读的位置的「计数」  （只增不减）
 *   tail            下一个要写的位置的「计数」  （只增不减）
 *   元素个数 = tail - head；  槽位下标 = 计数 & mask   （mask = capacity - 1）
 *
 * 为什么计数一直增长、不对 capacity 取模再存：
 *   如果 head、tail 都存 0..capacity-1 的下标，那么 head == tail 既可能是「空」也可能是「满」，只能多浪费一个槽位或者另存一个 size。
 *   计数自由增长时，空 ⇔ tail - head == 0，满 ⇔ tail - head == capacity，两者天然不同，且不浪费槽位。
 *   long 计数增长到 2^63 需要 29 万年（每纳秒一次），不用担心溢出。
 *
 * 为什么 capacity 要是 2 的幂：
 *   `count % capacity` 要做一次除法（几十个周期）；capacity = 2^k 时 `count & (capacity - 1)` 只取低 k 位，一个周期，结果相同（对非负数）。
 *
 * 非线程安全。线程安全版见 SpscLongRing。
 */
public final class LongRing implements LongQueue {
    public static final int MAX_CAPACITY = 1 << 30;

    private final long[] buf;
    private final int mask;
    private long head;
    private long tail;

    /** capacity 必须是 2 的幂且在 [1, MAX_CAPACITY]，否则 IllegalArgumentException。 */
    public LongRing(int capacity) {
        if (capacity < 1 || capacity > MAX_CAPACITY || Integer.bitCount(capacity) != 1)
            throw new IllegalArgumentException("capacity must be a power of two in [1, 2^30]: " + capacity);
        this.buf = new long[capacity];
        this.mask = capacity - 1;
    }

    @Override public int capacity() { return buf.length; }
    @Override public int size() { return (int) (tail - head); }
    @Override public boolean isEmpty() { return head == tail; }

    @Override
    public boolean offer(long value) {
        if (tail - head == buf.length) return false;
        buf[(int) (tail & mask)] = value;
        tail++;
        return true;
    }

    @Override
    public long poll() {
        if (head == tail) throw new NoSuchElementException("ring is empty");
        long v = buf[(int) (head & mask)];
        head++;
        return v;
    }
}
