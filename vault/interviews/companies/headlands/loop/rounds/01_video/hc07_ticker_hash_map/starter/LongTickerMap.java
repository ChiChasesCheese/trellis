/**
 * Part 2：key 是 TickerCodec 打包出来的 long（> 0），value 是 long。开放寻址 + 线性探测 + 墓碑，装载因子 <= 3/4。
 * 约束：不装箱、不创建 String；稳态下 add/get 零分配。
 * 提示：把 key 和 value 放在同一个 long[]（slots[2i] = key, slots[2i+1] = value）；0 = 空格，-1 = 墓碑；
 * 哈希用乘法（Fibonacci hashing）再取高位 —— 不要用 key & mask（打包后的 key 低位全是补的 0！）。
 */
public final class LongTickerMap {
    @FunctionalInterface
    public interface LongLongConsumer { void accept(long key, long value); }

    public LongTickerMap() { throw new UnsupportedOperationException("TODO"); }

    public LongTickerMap(int expectedSize) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }
    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int tombstones() { throw new UnsupportedOperationException("TODO"); }

    /** 所有方法：key <= 0 -> IllegalArgumentException。 */
    public boolean containsKey(long key) { throw new UnsupportedOperationException("TODO"); }

    public long get(long key, long ifAbsent) { throw new UnsupportedOperationException("TODO"); }

    /** 返回 true = 新 key，false = 覆盖了旧值。 */
    public boolean put(long key, long value) { throw new UnsupportedOperationException("TODO"); }

    /** value += delta（不存在当作 0），返回新值；溢出 ArithmeticException 且不改值。 */
    public long add(long key, long delta) { throw new UnsupportedOperationException("TODO"); }

    public boolean remove(long key) { throw new UnsupportedOperationException("TODO"); }

    public void forEach(LongLongConsumer action) { throw new UnsupportedOperationException("TODO"); }

    public int maxProbeLength() { throw new UnsupportedOperationException("TODO"); }
}
