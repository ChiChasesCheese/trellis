import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 2：一个生产者线程 + 一个消费者线程。单线程语义见 LongRingTest（两个实现共用）。 */
class SpscLongRingTest {

    /** 生产者发 0..n-1，消费者必须按序恰好收到一次。返回 null = 正常，否则是出错描述。 */
    static String transfer(int capacity, long n) throws InterruptedException {
        var ring = new SpscLongRing(capacity);
        var start = new CountDownLatch(1);
        var abort = new AtomicBoolean();                // 出错或超时后让另一个线程别再空转
        var error = new AtomicLong(-1);                 // 第一个出错的序号
        var producer = new Thread(() -> {
            await(start);
            for (long i = 0; i < n; i++) {
                while (!ring.offer(i)) { if (abort.get()) return; Thread.onSpinWait(); }
            }
        });
        var consumer = new Thread(() -> {
            await(start);
            for (long expect = 0; expect < n; expect++) {
                while (ring.isEmpty()) { if (abort.get()) return; Thread.onSpinWait(); }
                long got = ring.poll();
                if (got != expect) { error.compareAndSet(-1, expect); abort.set(true); return; }
            }
        });
        producer.setDaemon(true);
        consumer.setDaemon(true);
        producer.start();
        consumer.start();
        start.countDown();
        producer.join(10_000);
        consumer.join(10_000);
        boolean stalled = producer.isAlive() || consumer.isAlive();
        abort.set(true);
        if (stalled) return "timeout (ring stalled)";
        return error.get() < 0 ? null : "first mismatch at seq " + error.get();
    }

    private static void await(CountDownLatch gate) {
        try { gate.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }

    @RepeatedTest(20) @Tag("part2") @Tag("conc")
    void inOrderExactlyOnceTinyRing() throws Exception {
        assertNull(transfer(2, 200_000), "capacity 2：几乎每条消息都在回绕、都在判满判空");
    }

    @RepeatedTest(20) @Tag("part2") @Tag("conc")
    void inOrderExactlyOnceMediumRing() throws Exception {
        assertNull(transfer(64, 300_000));
    }

    @Test @Tag("part2") @Tag("conc")
    void capacityOneRingBetweenThreads() throws Exception {
        assertNull(transfer(1, 100_000));
    }

    /** 可见性：每条消息自带校验——消费者读到的值必须等于生产者写入的那个值（不是旧一轮留下的值，也不是 0）。 */
    @RepeatedTest(20) @Tag("part2") @Tag("conc")
    void consumerNeverSeesStaleSlot() throws Exception {
        final int n = 200_000;
        var ring = new SpscLongRing(8);
        var start = new CountDownLatch(1);
        var bad = new AtomicLong();
        var producer = new Thread(() -> {
            await(start);
            for (long i = 1; i <= n; i++) {
                long v = i * 0x9E3779B97F4A7C15L;        // 一个与序号一一对应、看起来随机的值
                while (!ring.offer(v)) Thread.onSpinWait();
            }
        });
        var consumer = new Thread(() -> {
            await(start);
            for (long i = 1; i <= n; i++) {
                while (ring.isEmpty()) Thread.onSpinWait();
                if (ring.poll() != i * 0x9E3779B97F4A7C15L) bad.incrementAndGet();
            }
        });
        producer.start(); consumer.start();
        start.countDown();
        producer.join(); consumer.join();
        assertEquals(0, bad.get());
        assertTrue(ring.isEmpty());
    }

    @Test @Tag("part2") @Tag("edge")
    void sizeFromAnyThreadStaysWithinBounds() throws Exception {
        var ring = new SpscLongRing(16);
        var stop = new AtomicBoolean();
        var bad = new AtomicLong();
        var observer = new Thread(() -> {
            while (!stop.get()) { int s = ring.size(); if (s < 0 || s > 16) bad.incrementAndGet(); }
        });
        observer.start();
        var producer = new Thread(() -> {
            for (long i = 0; i < 300_000; i++) while (!ring.offer(i)) Thread.onSpinWait();
        });
        producer.start();
        for (long i = 0; i < 300_000; i++) { while (ring.isEmpty()) Thread.onSpinWait(); ring.poll(); }
        producer.join();
        stop.set(true);
        observer.join();
        assertEquals(0, bad.get());
    }

    @Test @Tag("part2") @Tag("perf") @Tag("conc")
    void tenMillionMessagesBetweenTwoThreads() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            assertNull(transfer(1 << 14, 10_000_000L));
        });
    }
}
