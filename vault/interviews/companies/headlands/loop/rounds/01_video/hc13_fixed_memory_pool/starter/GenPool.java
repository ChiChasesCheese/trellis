/**
 * Part 2：带版本号 (generation) 的 handle，打包进一个 long：高 32 位 = 版本号，低 32 位 = 槽位编号。
 *
 * 版本号规则（见 problem.md）：偶数 = 槽位空闲，奇数 = 槽位在用；allocate 和 free 各把它 +1；初始全是 initialGeneration（偶数）。
 *   * 只有「槽位当前版本 == handle 里的版本」且版本是奇数，handle 才有效；
 *   * free：下标越界或版本为偶数 → INVALID；版本为奇数但和槽位当前版本不同 → DOUBLE_FREE；
 *   * NONE (-1) 和全零 handle 永远无效。
 */
public final class GenPool {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;

    public GenPool(int capacity) { this(capacity, 0); }

    /** initialGeneration 必须是偶数，否则 IllegalArgumentException。 */
    public GenPool(int capacity, int initialGeneration) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 打包。提示：index 当 int 可能是负的，先 & 0xFFFFFFFFL 再 | 进去，否则符号扩展会污染高 32 位。 */
    public static long handle(int index, int generation) { throw new UnsupportedOperationException("TODO"); }
    public static int indexOf(long handle) { throw new UnsupportedOperationException("TODO"); }
    public static int generationOf(long handle) { throw new UnsupportedOperationException("TODO"); }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int available() { throw new UnsupportedOperationException("TODO"); }

    public long allocate() { throw new UnsupportedOperationException("TODO"); }
    public FreeResult free(long handle) { throw new UnsupportedOperationException("TODO"); }
    public boolean isLive(long handle) { throw new UnsupportedOperationException("TODO"); }
}
