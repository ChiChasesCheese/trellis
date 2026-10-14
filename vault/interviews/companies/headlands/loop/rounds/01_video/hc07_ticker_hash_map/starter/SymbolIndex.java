/**
 * Part 3：最小完美哈希。给定固定的 key 集合（n 个 > 0 且互不相同的 long），build 之后
 * indexOf(key) 把集合里的 key 一一映射到 0..n-1，集合外的 key 返回 -1。
 * 提示：hash-and-displace —— 把 key 分到 ~n/4 个桶，按桶大小从大到小，为每个桶找一个位移 d，
 * 使桶内所有 key 的 slot(h, d) 都落在空格子里；最后别忘了在 indexOf 里比较 keys[slot] == key。
 */
public final class SymbolIndex {
    private SymbolIndex() {}

    /** 有 key <= 0 或重复 key -> IllegalArgumentException。空集合合法。 */
    public static SymbolIndex build(long[] universe) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }

    /** key 的编号（0..size()-1）；不在集合里（包括 key <= 0）返回 -1。 */
    public int indexOf(long key) { throw new UnsupportedOperationException("TODO"); }

    /** indexOf 的反函数：keyAt(indexOf(k)) == k。 */
    public long keyAt(int index) { throw new UnsupportedOperationException("TODO"); }
}
