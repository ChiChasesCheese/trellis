/**
 * Part 1：定长内存池，块用 int 编号 0..capacity-1 表示，空闲链表（free list）藏在一个 int[] 里。
 *
 * 数据结构：
 *   next[i]  == 下一个空闲块的编号   （块 i 空闲时；链表末尾是 NONE = -1）
 *   next[i]  == ALLOCATED = -2        （块 i 正在使用时）
 *   head     == 第一个空闲块的编号     （没有空闲块时是 NONE）
 *
 * 初始时 next[i] = i+1，所以 allocate() 依次给出 0,1,2,...；free(b) 把 b 插在链表头，所以「最后归还的最先被再分配」（LIFO）。
 * 这个顺序是本题的约定（reconstructed）：它对 CPU 缓存最友好——刚用过的块大概率还在缓存里。
 *
 * 为什么不另开一个 boolean[] inUse：一个 int 同时承担「链表指针」和「是否在用」两件事，
 * 因为空闲的块不需要保存别的数据，在用的块不需要链表指针，两个状态互斥。省内存，也少一次缓存未命中。
 *
 * 所有操作 O(1)；非线程安全。
 */
public final class IndexPool {
    public static final int NONE = -1;
    public static final int MAX_CAPACITY = 1 << 28;
    private static final int ALLOCATED = -2;

    private final int[] next;
    private int head;
    private int available;

    public IndexPool(int capacity) {
        if (capacity < 1 || capacity > MAX_CAPACITY) throw new IllegalArgumentException("capacity: " + capacity);
        next = new int[capacity];
        for (int i = 0; i < capacity - 1; i++) next[i] = i + 1;
        next[capacity - 1] = NONE;
        head = 0;
        available = capacity;
    }

    public int capacity() { return next.length; }
    public int available() { return available; }

    /** 取一个空闲块；池空返回 NONE（不抛异常：池满是正常状态，不是错误）。 */
    public int allocate() {
        int block = head;
        if (block == NONE) return NONE;
        head = next[block];
        next[block] = ALLOCATED;
        available--;
        return block;
    }

    /** 归还。下标越界 → INVALID；当前不在使用中 → DOUBLE_FREE。 */
    public FreeResult free(int block) {
        if (block < 0 || block >= next.length) return FreeResult.INVALID;
        if (next[block] != ALLOCATED) return FreeResult.DOUBLE_FREE;
        next[block] = head;
        head = block;
        available++;
        return FreeResult.FREED;
    }

    public boolean isAllocated(int block) {
        return block >= 0 && block < next.length && next[block] == ALLOCATED;
    }

    /** 归还，失败就抛：重复归还 → IllegalStateException，编号非法 → IllegalArgumentException。 */
    public void freeOrThrow(int block) {
        // J05 switch 表达式：每个分支都产生一个值，漏写分支编译器报错（穷尽性检查）
        RuntimeException failure = switch (free(block)) {
            case FREED -> null;
            case DOUBLE_FREE -> new IllegalStateException("block not allocated (double free?): " + block);
            case INVALID -> new IllegalArgumentException("block out of range: " + block);
        };
        if (failure != null) throw failure;
    }
}
