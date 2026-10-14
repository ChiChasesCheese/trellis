import java.util.concurrent.locks.*;
import java.util.concurrent.*;

/** J16 例 7：ReentrantLock + Condition 写一个有界缓冲；tryLock 带超时；以及"为什么在虚拟线程下优于 synchronized"（J10）。 */
public class J16Ex7Lock {
    static final class BoundedBuffer<T> {
        private final Object[] items;
        private int head, tail, count;
        private final ReentrantLock lock = new ReentrantLock();
        private final Condition notFull = lock.newCondition();
        private final Condition notEmpty = lock.newCondition();
        BoundedBuffer(int cap) { items = new Object[cap]; }

        void put(T x) throws InterruptedException {
            lock.lockInterruptibly();                      // 可被中断地等锁；synchronized 做不到
            try {
                while (count == items.length) notFull.await();     // 用 while 而不是 if：防"虚假唤醒"
                items[tail] = x; tail = (tail + 1) % items.length; count++;
                notEmpty.signal();
            } finally { lock.unlock(); }                   // 必须在 finally 里
        }
        @SuppressWarnings("unchecked")
        T take() throws InterruptedException {
            lock.lockInterruptibly();
            try {
                while (count == 0) notEmpty.await();
                T x = (T) items[head]; items[head] = null; head = (head + 1) % items.length; count--;
                notFull.signal();
                return x;
            } finally { lock.unlock(); }
        }
    }

    public static void main(String[] args) throws Exception {
        var buf = new BoundedBuffer<Integer>(4);
        long[] sum = {0};
        Thread cons = Thread.ofVirtual().start(() -> {
            try { for (int i = 0; i < 1000; i++) sum[0] += buf.take(); } catch (InterruptedException e) { }
        });
        Thread prod = Thread.ofVirtual().start(() -> {
            try { for (int i = 1; i <= 1000; i++) buf.put(i); } catch (InterruptedException e) { }
        });
        prod.join(); cons.join();
        System.out.println("有界缓冲(容量4)传 1..1000，和 = " + sum[0] + " (期望 500500)");

        // tryLock 带超时：拿不到就放弃，不会无限等 —— 避免死锁的常用手段
        ReentrantLock l = new ReentrantLock();
        l.lock();                                          // 主线程占着
        Thread other = Thread.ofPlatform().start(() -> {
            try {
                boolean got = l.tryLock(100, TimeUnit.MILLISECONDS);
                System.out.println("另一个线程 tryLock(100ms) = " + got + "（锁被主线程占着，放弃而不是死等）");
            } catch (InterruptedException e) { }
        });
        other.join();
        System.out.println("主线程 isHeldByCurrentThread = " + l.isHeldByCurrentThread() + ", holdCount = " + l.getHoldCount());
        l.unlock();
    }
}
