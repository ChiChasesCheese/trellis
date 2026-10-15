/**
 * Part 2：带「版本号」(generation) 的 handle。
 *
 * handle 是一个 long：高 32 位 = 版本号，低 32 位 = 槽位编号。
 *     handle = (long) generation << 32 | index
 *
 * 版本号的规则（reconstructed 的设计，目标是让「状态」和「版本」放进同一个 int，并发版可以用一次 CAS 完成状态切换）：
 *     gens[i] 偶数 = 槽位 i 空闲；奇数 = 槽位 i 在用。
 *     allocate：gens[i]++（偶 → 奇），handle 里带这个奇数；
 *     free    ：gens[i]++（奇 → 偶）。
 * 所以每次 分配+归还 版本号涨 2；handle 只有在「槽位版本号 == handle 里的版本号」时才有效。
 * 好处：
 *   * 用后释放（use-after-free）：旧 handle 的版本号比槽位当前的小 → 被识别出来；
 *   * ABA：槽位被归还后又分配给别人，下标相同但版本号不同 → 旧 handle 仍然被识别为陈旧；
 *   * 全零 handle（版本号 0 = 偶数）和 NONE (-1，下标 0xFFFFFFFF 不可能是合法下标) 永远不合法，漏初始化的 handle 立刻暴露；
 *   * 32 位版本号溢出回绕后奇偶性不变（2^32 是偶数），所以不需要特殊处理；
 *     代价：同一个槽位被分配 2^31 次之后，一个极老的 handle 才可能「撞上」——实际可忽略。
 */
public final class GenPool {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;
    private static final int END = -1;

    private final int[] gens;
    private final int[] next;
    private int head;
    private int available;

    public GenPool(int capacity) { this(capacity, 0); }

    /** initialGeneration 必须是偶数（所有槽位从「空闲」开始）；测试用它快速逼近 32 位回绕。 */
    public GenPool(int capacity, int initialGeneration) {
        if (capacity < 1 || capacity > MAX_CAPACITY) throw new IllegalArgumentException("capacity: " + capacity);
        if ((initialGeneration & 1) != 0) throw new IllegalArgumentException("initialGeneration must be even");
        gens = new int[capacity];
        next = new int[capacity];
        java.util.Arrays.fill(gens, initialGeneration);
        for (int i = 0; i < capacity - 1; i++) next[i] = i + 1;
        next[capacity - 1] = END;
        head = 0;
        available = capacity;
    }

    public static long handle(int index, int generation) {
        // index & 0xFFFFFFFFL：index 当 int 看可能是负的（符号扩展会把高 32 位全刷成 1），必须先当无符号数转成 long
        return ((long) generation << 32) | (index & 0xFFFFFFFFL);
    }
    public static int indexOf(long handle) { return (int) handle; }
    public static int generationOf(long handle) { return (int) (handle >>> 32); }

    public int capacity() { return gens.length; }
    public int available() { return available; }

    public long allocate() {
        int index = head;
        if (index == END) return NONE;
        head = next[index];
        int g = ++gens[index];            // 偶 → 奇
        available--;
        return handle(index, g);
    }

    public FreeResult free(long handle) {
        int index = indexOf(handle);
        int g = generationOf(handle);
        if (index < 0 || index >= gens.length || (g & 1) == 0) return FreeResult.INVALID;
        if (gens[index] != g) return FreeResult.DOUBLE_FREE;
        gens[index] = g + 1;              // 奇 → 偶
        next[index] = head;
        head = index;
        available++;
        return FreeResult.FREED;
    }

    public boolean isLive(long handle) {
        int index = indexOf(handle);
        int g = generationOf(handle);
        return index >= 0 && index < gens.length && (g & 1) == 1 && gens[index] == g;
    }
}
