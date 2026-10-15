import java.util.Collection;

/**
 * Part 3：key 集合在构造时固定，之后只能改 value。value 放在一个长度正好是 universe 大小的 long[] 里，
 * 用 SymbolIndex 把 key 变成数组下标。热路径 = 一次哈希 + 一次数组比较 + 一次数组写，没有探测循环、没有墓碑、没有 resize。
 * 更进一步：行情订阅时就把代码解析成下标缓存起来（indexOf），之后每条消息直接 addAt(下标)，连哈希都省了。
 */
public final class FrozenTickerMap {
    private final SymbolIndex index;
    private final long[] values;

    /** universe：今天会出现的全部代码（String，要符合 TickerCodec 的格式，且不重复）。所有 value 初始为 0。 */
    public FrozenTickerMap(Collection<String> universe) {
        long[] keys = new long[universe.size()];
        int i = 0;
        for (String t : universe) keys[i++] = TickerCodec.pack(t);
        this.index = SymbolIndex.build(keys);
        this.values = new long[keys.length];
    }

    public int size() { return values.length; }

    /** key 的下标（0..size()-1），不在 universe 里返回 -1。 */
    public int indexOf(long key) { return key <= 0 ? -1 : index.indexOf(key); }

    public boolean containsKey(long key) { return indexOf(key) >= 0; }

    public long get(long key, long ifAbsent) {
        int i = indexOf(key);
        return i < 0 ? ifAbsent : values[i];
    }

    /** 不在 universe 里返回 false，什么也不做。 */
    public boolean put(long key, long value) {
        int i = indexOf(key);
        if (i < 0) return false;
        values[i] = value;
        return true;
    }

    /** value += delta，返回新值；key 不在 universe 里抛 IllegalArgumentException。溢出抛 ArithmeticException 且不改值。 */
    public long add(long key, long delta) {
        int i = indexOf(key);
        if (i < 0) throw new IllegalArgumentException("unknown ticker key: " + key);
        return addAt(i, delta);
    }

    public long addAt(int index, long delta) { return values[index] = Math.addExact(values[index], delta); }

    public long getAt(int index) { return values[index]; }

    public long keyAt(int i) { return index.keyAt(i); }
}
