import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.util.concurrent.atomic.LongAdder;

/**
 * Part 4：线程安全的池。空闲链表是一个无锁的 Treiber 栈：
 *
 *     head（一个 long）= 高 32 位 tag（计数器） | 低 32 位栈顶槽位编号（-1 = 空）
 *     next[i]          = 槽位 i 之下的那个槽位
 *
 *   push(i):  loop { h = head; next[i] = idx(h); CAS(head, h, pack(tag(h)+1, i)) }
 *   pop():    loop { h = head; i = idx(h); if (i == -1) 空; n = next[i]; CAS(head, h, pack(tag(h)+1, n)) }
 *
 * 为什么要 tag（ABA 问题）：线程 A 读到 head=X、next[X]=Y，被切走；线程 B 弹出 X、弹出 Y、再把 X 压回去，head 又是 X；
 * 线程 A 醒来 CAS(head, X → Y) 成功——可是 Y 此刻在 B 手里（正在使用），却被 A 装进了空闲链表，两个线程拿到同一块。
 * 每次成功的 push/pop 都让 tag + 1，head 的整个 64 位值就不会「回到原样」，A 的 CAS 失败、重读。
 *
 * handle 的版本号规则和 GenPool 一样（偶空闲 / 奇在用）。归还时用 CAS(gens[i], g, g+1) 做「在用 → 空闲」的状态切换：
 * 两个线程同时 free 同一个 handle，恰好一个 CAS 成功（FREED），另一个看到版本已变 → DOUBLE_FREE。
 *
 * 内存序：
 *   * head 的 CAS 是 volatile 语义（既是 acquire 又是 release）：push 前对 next[i] 的写，对 pop 到 i 的线程可见；
 *   * next[] 的读写用 opaque（不撕裂、不被编译器缓存，但不付 release/acquire 的代价）——读到旧值没关系，因为那样 head 的 tag 已经变了，CAS 会失败；
 *   * 要点：「读到过期数据没关系，只要最后用 CAS 校验」是 lock-free 算法最常用的思路。
 */
public final class ConcurrentPool {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;
    private static final int EMPTY = -1;

    private static final VarHandle HEAD;
    private static final VarHandle GENS = MethodHandles.arrayElementVarHandle(int[].class);
    private static final VarHandle NEXTS = MethodHandles.arrayElementVarHandle(int[].class);
    static {
        try {
            HEAD = MethodHandles.lookup().findVarHandle(ConcurrentPool.class, "head", long.class);
        } catch (ReflectiveOperationException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    private final int[] gens;
    private final int[] next;
    private final LongAdder inUse = new LongAdder();   // 多线程计数用 LongAdder：分散热点，不会让所有线程抢同一个缓存行（J16）
    @SuppressWarnings("unused")                         // 只通过 VarHandle 访问
    private volatile long head;

    public ConcurrentPool(int capacity) {
        if (capacity < 1 || capacity > MAX_CAPACITY) throw new IllegalArgumentException("capacity: " + capacity);
        gens = new int[capacity];
        next = new int[capacity];
        for (int i = 0; i < capacity - 1; i++) next[i] = i + 1;
        next[capacity - 1] = EMPTY;
        head = pack(0, 0);
    }

    private static long pack(int tag, int index) { return ((long) tag << 32) | (index & 0xFFFFFFFFL); }
    private static int tagOf(long h) { return (int) (h >>> 32); }
    private static int indexOf(long h) { return (int) h; }

    public int capacity() { return gens.length; }
    /** 并发进行中是近似值；所有线程静止后是精确值。 */
    public int available() { return gens.length - (int) inUse.sum(); }

    public long allocate() {
        while (true) {
            long h = (long) HEAD.getAcquire(this);
            int index = indexOf(h);
            if (index == EMPTY) return NONE;
            int below = (int) NEXTS.getOpaque(next, index);
            if (HEAD.compareAndSet(this, h, pack(tagOf(h) + 1, below))) {
                // 弹出成功 = 这个槽位现在只属于本线程，没人会同时改它的版本号（旧 handle 的 free 会因为版本不匹配而失败）
                int g = (int) GENS.get(gens, index) + 1;
                GENS.setRelease(gens, index, g);            // 偶 → 奇
                inUse.increment();
                return GenPool.handle(index, g);
            }
            Thread.onSpinWait();                            // CAS 失败说明有竞争；提示 CPU 这是自旋
        }
    }

    public FreeResult free(long handle) {
        int index = GenPool.indexOf(handle);
        int g = GenPool.generationOf(handle);
        if (index < 0 || index >= gens.length || (g & 1) == 0) return FreeResult.INVALID;
        // 关键：用 CAS 把版本号从 g 推进到 g+1。并发 free 同一个 handle 时，恰好一个线程能成功。
        if (!GENS.compareAndSet(gens, index, g, g + 1)) return FreeResult.DOUBLE_FREE;
        inUse.decrement();
        while (true) {
            long h = (long) HEAD.getAcquire(this);
            NEXTS.setOpaque(next, index, indexOf(h));
            if (HEAD.compareAndSet(this, h, pack(tagOf(h) + 1, index))) return FreeResult.FREED;
            Thread.onSpinWait();
        }
    }

    public boolean isLive(long handle) {
        int index = GenPool.indexOf(handle);
        int g = GenPool.generationOf(handle);
        return index >= 0 && index < gens.length && (g & 1) == 1 && (int) GENS.getAcquire(gens, index) == g;
    }
}
