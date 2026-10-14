import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.List;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicIntegerArray;
import java.util.concurrent.atomic.AtomicLong;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class ConcurrentPoolTest {

    // ---------- 单线程语义：和 GenPool 一致 ----------

    @Test @Tag("part4")
    void sequentialSemanticsMatchGenPool() {
        var pool = new ConcurrentPool(3);
        long a = pool.allocate(), b = pool.allocate(), c = pool.allocate();
        assertEquals(GenPool.handle(0, 1), a);
        assertEquals(GenPool.handle(1, 1), b);
        assertEquals(GenPool.handle(2, 1), c);
        assertEquals(ConcurrentPool.NONE, pool.allocate());
        assertEquals(0, pool.available());
        assertEquals(FreeResult.FREED, pool.free(b));
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(b));
        assertFalse(pool.isLive(b));
        long b2 = pool.allocate();                          // LIFO：马上拿到刚还的槽位
        assertEquals(1, GenPool.indexOf(b2));
        assertEquals(3, GenPool.generationOf(b2));
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(b));       // 旧 handle 不能动新主人
        assertTrue(pool.isLive(b2));
        assertEquals(FreeResult.INVALID, pool.free(0L));
        assertEquals(FreeResult.INVALID, pool.free(ConcurrentPool.NONE));
        assertEquals(FreeResult.INVALID, pool.free(GenPool.handle(3, 1)));
        assertEquals(FreeResult.INVALID, pool.free(GenPool.handle(1, 4)));
        assertEquals(0, pool.available());
    }

    @Test @Tag("part4") @Tag("edge")
    void capacityOneAndBadCapacity() {
        var pool = new ConcurrentPool(1);
        long a = pool.allocate();
        assertEquals(ConcurrentPool.NONE, pool.allocate());
        assertEquals(FreeResult.FREED, pool.free(a));
        assertNotEquals(ConcurrentPool.NONE, pool.allocate());
        assertThrows(IllegalArgumentException.class, () -> new ConcurrentPool(0));
        assertThrows(IllegalArgumentException.class, () -> new ConcurrentPool((1 << 28) + 1));
    }

    // ---------- 并发不变量 ----------

    /** 小池 + 多线程反复 分配/使用/归还：任何时刻同一个槽位至多一个主人；结束后一块不丢。 */
    @RepeatedTest(20) @Tag("part4") @Tag("conc")
    void exclusiveOwnershipUnderContention() throws Exception {
        final int capacity = 3, threads = 8, iterations = 20_000;
        var pool = new ConcurrentPool(capacity);
        var owner = new AtomicIntegerArray(capacity);       // 0 = 无人持有
        var violations = new AtomicInteger();
        var start = new CountDownLatch(1);
        var workers = new ArrayList<Thread>();
        for (int t = 1; t <= threads; t++) {
            final int me = t;
            var th = new Thread(() -> {
                await(start);
                for (int i = 0; i < iterations; i++) {
                    long h = pool.allocate();
                    if (h == ConcurrentPool.NONE) { Thread.onSpinWait(); continue; }
                    int idx = GenPool.indexOf(h);
                    if (!owner.compareAndSet(idx, 0, me)) violations.incrementAndGet();   // 别人已经持有 = 同一块发给了两个人
                    if (!pool.isLive(h)) violations.incrementAndGet();
                    if (!owner.compareAndSet(idx, me, 0)) violations.incrementAndGet();
                    if (pool.free(h) != FreeResult.FREED) violations.incrementAndGet();
                }
            });
            workers.add(th);
            th.start();
        }
        start.countDown();
        for (var th : workers) th.join();
        assertEquals(0, violations.get());
        assertAllSlotsRecoverable(pool, capacity);
    }

    /** 两个线程同时 free 同一个 handle：恰好一个 FREED。重复很多轮增加相撞的机会。 */
    @RepeatedTest(20) @Tag("part4") @Tag("conc")
    void racingDoubleFreeHasExactlyOneWinner() throws Exception {
        final int n = 2_000;
        var pool = new ConcurrentPool(n);
        long[] hs = new long[n];
        for (int i = 0; i < n; i++) hs[i] = pool.allocate();
        var wins = new AtomicInteger();
        var doubles = new AtomicInteger();
        var invalid = new AtomicInteger();
        var start = new CountDownLatch(1);
        var workers = new ArrayList<Thread>();
        for (int t = 0; t < 3; t++) {
            var th = new Thread(() -> {
                await(start);
                for (long h : hs) {
                    switch (pool.free(h)) {
                        case FREED -> wins.incrementAndGet();
                        case DOUBLE_FREE -> doubles.incrementAndGet();
                        case INVALID -> invalid.incrementAndGet();
                    }
                }
            });
            workers.add(th);
            th.start();
        }
        start.countDown();
        for (var th : workers) th.join();
        assertEquals(n, wins.get(), "每个 handle 恰好成功归还一次");
        assertEquals(2 * n, doubles.get());
        assertEquals(0, invalid.get());
        assertEquals(n, pool.available());
        assertAllSlotsRecoverable(pool, n);                 // 没有哪个槽位被压进空闲链表两次
    }

    /** 分配和归还发生在不同线程：生产者分配、消费者归还。总数守恒、无重复。 */
    @RepeatedTest(20) @Tag("part4") @Tag("conc")
    void allocateInOneThreadFreeInAnother() throws Exception {
        final int capacity = 64, producers = 3, consumers = 3, perProducer = 20_000;
        var pool = new ConcurrentPool(capacity);
        var handoff = new ConcurrentLinkedQueue<Long>();
        var produced = new AtomicLong();
        var freed = new AtomicLong();
        var badFrees = new AtomicInteger();
        var start = new CountDownLatch(1);
        var workers = new ArrayList<Thread>();
        long total = (long) producers * perProducer;
        for (int p = 0; p < producers; p++) {
            workers.add(new Thread(() -> {
                await(start);
                int done = 0;
                while (done < perProducer) {
                    long h = pool.allocate();
                    if (h == ConcurrentPool.NONE) { Thread.onSpinWait(); continue; }
                    handoff.add(h);
                    done++;
                    produced.incrementAndGet();
                }
            }));
        }
        for (int c = 0; c < consumers; c++) {
            workers.add(new Thread(() -> {
                await(start);
                while (freed.get() < total) {
                    Long h = handoff.poll();
                    if (h == null) { Thread.onSpinWait(); continue; }
                    if (pool.free(h) != FreeResult.FREED) badFrees.incrementAndGet();
                    freed.incrementAndGet();
                }
            }));
        }
        workers.forEach(Thread::start);
        start.countDown();
        for (var th : workers) th.join();
        assertEquals(total, produced.get());
        assertEquals(total, freed.get());
        assertEquals(0, badFrees.get());
        assertAllSlotsRecoverable(pool, capacity);
    }

    /** 大量虚拟线程（J10）：每个只做短小的 分配/归还，不阻塞。 */
    @Test @Tag("part4") @Tag("conc")
    void manyVirtualThreads() throws Exception {
        final int capacity = 16, tasks = 2_000, iterations = 200;
        var pool = new ConcurrentPool(capacity);
        var owner = new AtomicIntegerArray(capacity);
        var violations = new AtomicInteger();
        try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<?>> fs = new ArrayList<>();
            for (int t = 1; t <= tasks; t++) {
                final int me = t;
                fs.add(exec.submit(() -> {
                    for (int i = 0; i < iterations; i++) {
                        long h = pool.allocate();
                        if (h == ConcurrentPool.NONE) continue;
                        int idx = GenPool.indexOf(h);
                        if (!owner.compareAndSet(idx, 0, me)) violations.incrementAndGet();
                        owner.set(idx, 0);
                        if (pool.free(h) != FreeResult.FREED) violations.incrementAndGet();
                    }
                }));
            }
            for (var f : fs) f.get();
        }
        assertEquals(0, violations.get());
        assertAllSlotsRecoverable(pool, capacity);
    }

    @Test @Tag("part4") @Tag("perf") @Tag("conc")
    void fourThreadsHammeringOnePool() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var pool = new ConcurrentPool(1024);
            var bad = new AtomicInteger();
            var start = new CountDownLatch(1);
            var workers = new ArrayList<Thread>();
            for (int t = 0; t < 4; t++) {
                var th = new Thread(() -> {
                    await(start);
                    long[] mine = new long[16];
                    for (int i = 0; i < 50_000; i++) {
                        int k = 0;
                        for (; k < mine.length; k++) {
                            long h = pool.allocate();
                            if (h == ConcurrentPool.NONE) break;
                            mine[k] = h;
                        }
                        for (int j = 0; j < k; j++) if (pool.free(mine[j]) != FreeResult.FREED) bad.incrementAndGet();
                    }
                });
                workers.add(th);
                th.start();
            }
            start.countDown();
            for (var th : workers) th.join();
            assertEquals(0, bad.get());
            assertEquals(1024, pool.available());
        });
    }

    // ---------- 工具 ----------

    private static void await(CountDownLatch gate) {
        try { gate.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }

    /** 池静止后：恰好能分配出 capacity 个互不相同的槽位，再多就是 NONE；归还后 available 回到 capacity。 */
    private static void assertAllSlotsRecoverable(ConcurrentPool pool, int capacity) {
        assertEquals(capacity, pool.available());
        var seen = new BitSet();
        long[] hs = new long[capacity];
        for (int i = 0; i < capacity; i++) {
            hs[i] = pool.allocate();
            assertNotEquals(ConcurrentPool.NONE, hs[i], "丢了槽位：只分配出 " + i + " 个");
            int idx = GenPool.indexOf(hs[i]);
            assertFalse(seen.get(idx), "槽位被发了两次: " + idx);
            seen.set(idx);
        }
        assertEquals(ConcurrentPool.NONE, pool.allocate());
        assertEquals(0, pool.available());
        for (long h : hs) assertEquals(FreeResult.FREED, pool.free(h));
        assertEquals(capacity, pool.available());
    }
}
