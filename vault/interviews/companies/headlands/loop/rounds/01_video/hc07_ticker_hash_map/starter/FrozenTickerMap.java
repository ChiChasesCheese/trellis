import java.util.Collection;

/**
 * Part 3：key 集合在构造时固定，之后只能改 value；value 放在长度正好 n 的 long[] 里，用 SymbolIndex 把 key 变下标。
 * 热路径零分配、没有探测循环。所有 value 初始为 0。
 */
public final class FrozenTickerMap {
    /** universe：今天会出现的全部代码（要符合 TickerCodec 的格式，且不重复，否则 IllegalArgumentException）。 */
    public FrozenTickerMap(Collection<String> universe) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }

    /** key 的下标，不在 universe 里（包括 key <= 0）返回 -1。 */
    public int indexOf(long key) { throw new UnsupportedOperationException("TODO"); }

    public boolean containsKey(long key) { throw new UnsupportedOperationException("TODO"); }

    public long get(long key, long ifAbsent) { throw new UnsupportedOperationException("TODO"); }

    /** 不在 universe 里返回 false。 */
    public boolean put(long key, long value) { throw new UnsupportedOperationException("TODO"); }

    /** value += delta，返回新值；不在 universe 里 -> IllegalArgumentException；溢出 -> ArithmeticException 且不改值。 */
    public long add(long key, long delta) { throw new UnsupportedOperationException("TODO"); }

    /** 已经解析好下标之后的快速路径。 */
    public long addAt(int index, long delta) { throw new UnsupportedOperationException("TODO"); }

    public long getAt(int index) { throw new UnsupportedOperationException("TODO"); }

    public long keyAt(int index) { throw new UnsupportedOperationException("TODO"); }
}
