import java.util.OptionalLong;
import java.util.function.ObjLongConsumer;

/**
 * Part 1：手写哈希表，key = String（股票代码），value = long。不许用 java.util.HashMap / Map 做存储。
 * 要求：开放寻址 + 线性探测；装载因子（占用 + 墓碑）不超过 3/4；删除用墓碑；resize 时清掉墓碑。
 * 题面见 ../problem.md，讲义见 study/30-articles/hc07_ticker_hash_map.md。
 *
 * 提示：用两个并行数组 String[] keys / long[] vals；capacity 取 2 的幂，这样 (i & mask) 代替 i % capacity；
 * 墓碑可以是一个特殊的 String 对象（用 == 比较）。
 */
public final class TickerMap {
    public TickerMap() { throw new UnsupportedOperationException("TODO"); }

    /** expectedSize：预计放多少条，预留够用的容量。 */
    public TickerMap(int expectedSize) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }

    /** 格子总数。 */
    public int capacity() { throw new UnsupportedOperationException("TODO"); }

    /** 墓碑格子数（诊断用）。 */
    public int tombstones() { throw new UnsupportedOperationException("TODO"); }

    /** key 为 null -> NullPointerException（下同）。 */
    public boolean containsKey(String key) { throw new UnsupportedOperationException("TODO"); }

    public OptionalLong get(String key) { throw new UnsupportedOperationException("TODO"); }

    /** 放入 key -> value；返回旧值（没有则 empty）。 */
    public OptionalLong put(String key, long value) { throw new UnsupportedOperationException("TODO"); }

    /** value += delta（不存在当作 0）；返回新值。溢出抛 ArithmeticException，且表保持原样。 */
    public long add(String key, long delta) { throw new UnsupportedOperationException("TODO"); }

    /** 删除；返回被删的值（没有则 empty）。 */
    public OptionalLong remove(String key) { throw new UnsupportedOperationException("TODO"); }

    public void forEach(ObjLongConsumer<String> action) { throw new UnsupportedOperationException("TODO"); }

    /** 诊断：所有活 key 里「离自己的家最远」的距离（0 = 都在家）。 */
    public int maxProbeLength() { throw new UnsupportedOperationException("TODO"); }
}
