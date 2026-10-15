/**
 * Part 1：定长内存池，块用 int 编号 0..capacity-1 表示。
 *
 * 契约（详见 problem.md）：
 *   * allocate() 初始依次给出 0,1,2,...；池空返回 NONE（不抛异常）；
 *   * free(b)：越界 → INVALID；当前不在使用中 → DOUBLE_FREE；否则 FREED；之后「最后归还的最先被再分配」（LIFO）；
 *   * 所有操作 O(1)，不允许为了找空闲块而扫描数组；非线程安全。
 */
public final class IndexPool {
    public static final int NONE = -1;
    public static final int MAX_CAPACITY = 1 << 28;

    /** capacity 不在 [1, MAX_CAPACITY] → IllegalArgumentException。 */
    public IndexPool(int capacity) {
        throw new UnsupportedOperationException("TODO");
    }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int available() { throw new UnsupportedOperationException("TODO"); }

    public int allocate() { throw new UnsupportedOperationException("TODO"); }

    public FreeResult free(int block) { throw new UnsupportedOperationException("TODO"); }

    public boolean isAllocated(int block) { throw new UnsupportedOperationException("TODO"); }

    /** 归还，失败就抛：DOUBLE_FREE → IllegalStateException，INVALID → IllegalArgumentException。 */
    public void freeOrThrow(int block) { throw new UnsupportedOperationException("TODO"); }
}
