/**
 * Part 1：环形缓冲区 (ring buffer)，单线程语义。
 *
 * 要求：
 *   * 容量是 2 的幂（[1, MAX_CAPACITY]），否则构造器抛 IllegalArgumentException；用 `计数 & mask` 取下标，不要用 %。
 *   * head / tail 是只增不减的 long 计数：空 ⇔ head == tail，满 ⇔ tail - head == capacity。不要浪费槽位，不要另存 size。
 *   * offer 满了返回 false（不覆盖最旧的元素）；poll 空了抛 NoSuchElementException；每个 long 值都是合法消息（没有哨兵值）。
 */
public final class LongRing implements LongQueue {
    public static final int MAX_CAPACITY = 1 << 30;

    public LongRing(int capacity) { throw new UnsupportedOperationException("TODO"); }

    @Override public int capacity() { throw new UnsupportedOperationException("TODO"); }
    @Override public int size() { throw new UnsupportedOperationException("TODO"); }
    @Override public boolean isEmpty() { throw new UnsupportedOperationException("TODO"); }
    @Override public boolean offer(long value) { throw new UnsupportedOperationException("TODO"); }
    @Override public long poll() { throw new UnsupportedOperationException("TODO"); }
}
