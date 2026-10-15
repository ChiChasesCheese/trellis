/**
 * Part 4：线程安全的池。空闲链表用无锁的 Treiber 栈：head 是一个 long，高 32 位 tag（每次成功的 push/pop 都 +1，防 ABA）、
 * 低 32 位栈顶槽位编号（-1 = 空），用 VarHandle.compareAndSet 更新。
 *
 * handle 规则同 GenPool（偶空闲 / 奇在用，可直接复用 GenPool.handle / indexOf / generationOf）。
 * free 必须用 CAS 把槽位版本号从 g 推进到 g+1，这样两个线程同时 free 同一个 handle 时恰好一个返回 FREED、另一个返回 DOUBLE_FREE。
 * available() 在并发进行中可以是近似值，所有线程静止后必须精确。
 */
public final class ConcurrentPool {
    public static final long NONE = -1L;
    public static final int MAX_CAPACITY = 1 << 28;

    public ConcurrentPool(int capacity) { throw new UnsupportedOperationException("TODO"); }

    public int capacity() { throw new UnsupportedOperationException("TODO"); }
    public int available() { throw new UnsupportedOperationException("TODO"); }

    public long allocate() { throw new UnsupportedOperationException("TODO"); }
    public FreeResult free(long handle) { throw new UnsupportedOperationException("TODO"); }
    public boolean isLive(long handle) { throw new UnsupportedOperationException("TODO"); }
}
