import static org.junit.jupiter.api.Assertions.*;

import java.lang.foreign.Arena;
import java.lang.foreign.MemorySegment;
import java.time.Duration;
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/** Part 3：变长消息（长度前缀 + 回绕）。ring 建在 Arena.ofShared() 分配的原生内存上。 */
class MessageRingTest {
    private final Arena arena = Arena.ofShared();

    @AfterEach void closeArena() { arena.close(); }

    private MemorySegment segment(int capacity) {
        return arena.allocate(MessageRing.segmentBytes(capacity), 128);
    }

    private static byte[] bytes(int len, int fill) {
        byte[] b = new byte[len];
        Arrays.fill(b, (byte) fill);
        return b;
    }

    // ---------- 初始化 / 连接 ----------

    @Test @Tag("part3")
    void initThenAttachSeesTheSameRing() {
        var seg = segment(64);
        var producer = MessageRing.init(seg, 64);
        var consumer = MessageRing.attach(seg);
        assertEquals(64, consumer.capacity());
        assertEquals(60, consumer.maxPayload());
        assertTrue(producer.offer("hello".getBytes()));
        assertArrayEquals("hello".getBytes(), consumer.poll());
        assertNull(consumer.poll());
    }

    @Test @Tag("part3") @Tag("edge")
    void attachRejectsGarbage() {
        assertThrows(IllegalStateException.class, () -> MessageRing.attach(segment(64)));            // 全零：没有 magic
        var seg = segment(64);
        MessageRing.init(seg, 64);
        assertThrows(IllegalStateException.class, () -> MessageRing.attach(seg.asSlice(0, 100)));     // 尺寸对不上
        var tiny = arena.allocate(8, 8);
        assertThrows(IllegalStateException.class, () -> MessageRing.attach(tiny));
    }

    @ParameterizedTest @Tag("part3") @Tag("edge")
    @ValueSource(ints = {0, 1, 8, 15, 17, 24, 100, -16, (1 << 30) + 1})
    void initRejectsBadCapacity(int bad) {
        var seg = segment(64);
        assertThrows(IllegalArgumentException.class, () -> MessageRing.init(seg, bad));
    }

    @Test @Tag("part3") @Tag("edge")
    void initRejectsTooSmallSegment() {
        assertThrows(IllegalArgumentException.class, () -> MessageRing.init(arena.allocate(MessageRing.HEADER_BYTES + 32, 8), 64));
    }

    @Test @Tag("part3")
    void headerLayoutConstants() {
        assertEquals(512, MessageRing.HEADER_BYTES);
        assertEquals(512 + 1024L, MessageRing.segmentBytes(1024));
    }

    // ---------- 基本收发 ----------

    @Test @Tag("part3")
    void fifoWithVariedLengthsIncludingEmptyAndBinary() {
        var ring = MessageRing.init(segment(256), 256);
        byte[][] msgs = {new byte[0], {0}, {(byte) 0xFF, 0, (byte) 0x80}, bytes(5, 7), bytes(100, 0xAB), bytes(4, 1), bytes(3, 2)};
        for (byte[] m : msgs) assertTrue(ring.offer(m));
        for (byte[] m : msgs) assertArrayEquals(m, ring.poll());
        assertNull(ring.poll());
    }

    @Test @Tag("part3") @Tag("edge")
    void offerDoesNotKeepReferenceToCallersArray() {
        var ring = MessageRing.init(segment(64), 64);
        byte[] m = {1, 2, 3};
        ring.offer(m);
        m[0] = 99;
        byte[] got = ring.poll();
        assertArrayEquals(new byte[] {1, 2, 3}, got);
        got[1] = 42;                                    // 改返回值也不能影响环里的数据（环里已经没有了，但不该崩）
        assertNull(ring.poll());
    }

    // ---------- 满 / 空 的规则：以记录总长（8 字节对齐）为准 ----------

    @Test @Tag("part3") @Tag("edge")
    void fullRuleUsesAlignedRecordSizes() {
        var ring = MessageRing.init(segment(64), 64);
        // len 12 → 4 + 12 = 16 字节；64 / 16 = 4 条
        for (int i = 0; i < 4; i++) assertTrue(ring.offer(bytes(12, i)), "record " + i);
        assertFalse(ring.offer(bytes(12, 9)));
        assertFalse(ring.offer(new byte[0]), "一个字节都不剩，连空消息也放不下");
        assertEquals(64, ring.bytesPending());
        assertArrayEquals(bytes(12, 0), ring.poll());
        assertTrue(ring.offer(bytes(12, 9)));           // 腾出 16 字节，正好放下，且发生回绕
        for (int i = 1; i < 4; i++) assertArrayEquals(bytes(12, i), ring.poll());
        assertArrayEquals(bytes(12, 9), ring.poll());
        assertNull(ring.poll());
    }

    @Test @Tag("part3") @Tag("edge")
    void recordsPadToEightBytes() {
        var ring = MessageRing.init(segment(64), 64);
        for (int i = 0; i < 8; i++) assertTrue(ring.offer(bytes(0, 0)));     // 空消息占 8 字节
        assertFalse(ring.offer(bytes(0, 0)));
        for (int i = 0; i < 8; i++) assertEquals(0, ring.poll().length);
        for (int i = 0; i < 8; i++) assertTrue(ring.offer(bytes(4, 1)));     // 4 + 4 = 8，仍是 8
        assertFalse(ring.offer(bytes(4, 1)));
        for (int i = 0; i < 8; i++) ring.poll();
        for (int i = 0; i < 4; i++) assertTrue(ring.offer(bytes(5, 1)));     // 4 + 5 = 9 → 16
        assertFalse(ring.offer(bytes(0, 1)));
    }

    @Test @Tag("part3") @Tag("edge")
    void maxPayloadFitsAnEmptyRingAndOneMoreByteNever() {
        var ring = MessageRing.init(segment(64), 64);
        byte[] max = bytes(ring.maxPayload(), 0x5A);
        assertTrue(ring.offer(max));
        assertEquals(64, ring.bytesPending());
        assertArrayEquals(max, ring.poll());
        assertThrows(IllegalArgumentException.class, () -> ring.offer(bytes(ring.maxPayload() + 1, 1)));  // 永远放不下 ≠ 暂时满
    }

    // ---------- 回绕 ----------

    @Test @Tag("part3") @Tag("edge")
    void wrapAroundWritesPadThenRecordAtStart() {
        var ring = MessageRing.init(segment(64), 64);
        assertTrue(ring.offer(bytes(20, 1)));           // 24 字节
        assertTrue(ring.offer(bytes(20, 2)));           // 24 字节，tail = 48
        assertArrayEquals(bytes(20, 1), ring.poll());
        assertArrayEquals(bytes(20, 2), ring.poll());
        assertEquals(0, ring.bytesPending());
        assertTrue(ring.offer(bytes(20, 3)));           // 到末尾只剩 16 < 24：先 PAD 16 字节，再从开头写 24 字节
        assertEquals(16 + 24, ring.bytesPending());
        assertArrayEquals(bytes(20, 3), ring.poll());   // 消费者越过 PAD 读到真消息
        assertEquals(0, ring.bytesPending());
        assertNull(ring.poll());
    }

    @Test @Tag("part3") @Tag("edge")
    void padIsPublishedEvenIfTheRecordDoesNotFit() {
        var ring = MessageRing.init(segment(64), 64);
        assertTrue(ring.offer(bytes(20, 1)));
        assertTrue(ring.offer(bytes(20, 2)));           // tail = 48，消费者一条没读
        assertFalse(ring.offer(bytes(20, 3)));          // PAD 能放（16 字节空位），随后真记录放不下 → false
        assertEquals(48 + 16, ring.bytesPending());     // 但 PAD 已经发布
        assertArrayEquals(bytes(20, 1), ring.poll());
        assertTrue(ring.offer(bytes(20, 3)));           // 空出 24 字节，且已经在偏移 0，直接放下
        assertArrayEquals(bytes(20, 2), ring.poll());
        assertArrayEquals(bytes(20, 3), ring.poll());
        assertNull(ring.poll());
    }

    @Test @Tag("part3") @Tag("edge")
    void anEmptyRingAcceptsAMaxSizeMessageFromEveryPosition() {
        // 活性：不管 tail 停在哪（含「只剩 8 字节就到末尾」），空环上 offer → （消费者越过 PAD）→ offer 一定能放进最大的消息
        var rnd = new Random(0);
        var ring = MessageRing.init(segment(64), 64);
        byte[] max = bytes(ring.maxPayload(), 0x33);
        for (int round = 0; round < 500; round++) {
            int steps = rnd.nextInt(5);
            for (int i = 0; i < steps; i++) {
                byte[] m = bytes(rnd.nextInt(30), round);
                if (!ring.offer(m)) {                    // 先发布了 PAD，需要消费者越过它
                    assertNull(ring.poll());
                    assertTrue(ring.offer(m));
                }
                assertArrayEquals(m, ring.poll());
            }
            assertNull(ring.poll());
            boolean ok = ring.offer(max);
            if (!ok) {                                   // 先发布了 PAD；消费者越过它（poll 返回 null）之后必须放得下
                assertNull(ring.poll());
                ok = ring.offer(max);
            }
            assertTrue(ok, "round " + round + ": 空环 offer → poll → offer 仍放不下最大消息 → 会死锁");
            assertArrayEquals(max, ring.poll());
        }
    }

    @Test @Tag("part3")
    void randomOperationsKeepFifoAndNeverLoseAMessage() {
        var rnd = new Random(0);
        var ring = MessageRing.init(segment(256), 256);
        var model = new ArrayDeque<byte[]>();
        long accepted = 0, rejected = 0;
        for (int step = 0; step < 300_000; step++) {
            if (rnd.nextInt(100) < 52) {
                byte[] m = bytes(rnd.nextInt(ring.maxPayload() / 3), step);
                if (ring.offer(m)) { model.addLast(m); accepted++; } else rejected++;
            } else {
                byte[] got = ring.poll();
                if (model.isEmpty()) assertNull(got);
                else assertArrayEquals(model.pollFirst(), got, "step " + step);
            }
            assertTrue(ring.bytesPending() <= 256);
        }
        assertTrue(accepted > 10_000 && rejected > 100, "测试要真的覆盖到满和回绕：accepted=" + accepted + " rejected=" + rejected);
        while (!model.isEmpty()) assertArrayEquals(model.pollFirst(), ring.poll());
        assertNull(ring.poll());
    }

    // ---------- finish / drained ----------

    @Test @Tag("part3")
    void drainedMeansFinishedAndEmpty() {
        var seg = segment(64);
        var producer = MessageRing.init(seg, 64);
        var consumer = MessageRing.attach(seg);
        assertFalse(consumer.isDrained(), "空但生产者还没说结束 ≠ drained");
        producer.offer(bytes(3, 1));
        producer.offer(bytes(3, 2));
        producer.finish();
        producer.finish();                               // 幂等
        assertFalse(consumer.isDrained(), "还有两条没读");
        assertNotNull(consumer.poll());
        assertFalse(consumer.isDrained());
        assertNotNull(consumer.poll());
        assertTrue(consumer.isDrained());
        assertNull(consumer.poll());
        assertTrue(consumer.isDrained());
        assertThrows(IllegalStateException.class, () -> producer.offer(bytes(1, 1)));
    }

    @Test @Tag("part3") @Tag("edge")
    void trailingPadIsConsumedBeforeDrained() {
        var seg = segment(64);
        var producer = MessageRing.init(seg, 64);
        var consumer = MessageRing.attach(seg);
        producer.offer(bytes(20, 1));
        producer.offer(bytes(20, 2));
        assertFalse(producer.offer(bytes(20, 3)));       // 留下一条孤零零的 PAD
        producer.finish();
        assertNotNull(consumer.poll());
        assertNotNull(consumer.poll());
        assertFalse(consumer.isDrained(), "末尾还有一条 PAD 没越过");
        assertNull(consumer.poll());                     // poll 越过 PAD，返回 null（没有消息）
        assertTrue(consumer.isDrained());
    }

    // ---------- 并发 ----------

    @RepeatedTest(20) @Tag("part3") @Tag("conc")
    void producerAndConsumerThreadsExchangeInOrderExactlyOnce() throws Exception {
        final int n = 20_000;
        var seg = segment(256);                          // 小环：每几条消息就回绕一次
        var producer = MessageRing.init(seg, 256);
        var consumer = MessageRing.attach(seg);
        var start = new CountDownLatch(1);
        var abort = new AtomicBoolean();
        var error = new AtomicReference<String>();
        var p = new Thread(() -> {
            await(start);
            for (long i = 0; i < n; i++) {
                byte[] m = Msgs.make(i);
                while (!producer.offer(m)) { if (abort.get()) return; Thread.onSpinWait(); }
            }
            producer.finish();
        });
        var c = new Thread(() -> {
            await(start);
            long expect = 0;
            while (!consumer.isDrained()) {
                byte[] m = consumer.poll();
                if (m == null) { if (abort.get()) return; Thread.onSpinWait(); continue; }
                String err = Msgs.check(m, expect);
                if (err != null) { error.set(err); abort.set(true); return; }
                expect++;
            }
            if (expect != n) error.compareAndSet(null, "received " + expect + " of " + n);
        });
        p.setDaemon(true); c.setDaemon(true);
        p.start(); c.start();
        start.countDown();
        p.join(10_000); c.join(10_000);
        boolean stalled = p.isAlive() || c.isAlive();
        abort.set(true);
        assertFalse(stalled, "ring stalled");
        assertNull(error.get());
    }

    @Test @Tag("part3") @Tag("perf")
    void twoMillionMessagesSingleThread() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var ring = MessageRing.init(segment(1 << 12), 1 << 12);
            byte[] m = bytes(24, 7);
            long total = 0;
            for (int i = 0; i < 2_000_000; i++) {
                assertTrue(ring.offer(m));
                total += ring.poll().length;
            }
            assertEquals(48_000_000L, total);
        });
    }

    @Test @Tag("part3") @Tag("perf") @Tag("conc")
    void twoMillionMessagesBetweenThreads() {
        assertTimeoutPreemptively(Duration.ofSeconds(3), () -> {
            var seg = segment(1 << 16);
            var producer = MessageRing.init(seg, 1 << 16);
            var consumer = MessageRing.attach(seg);
            final int n = 2_000_000;
            var error = new AtomicReference<String>();
            var p = new Thread(() -> {
                for (long i = 0; i < n; i++) {
                    byte[] m = Msgs.make(i);
                    while (!producer.offer(m)) Thread.onSpinWait();
                }
                producer.finish();
            });
            p.start();
            long expect = 0;
            while (!consumer.isDrained()) {
                byte[] m = consumer.poll();
                if (m == null) { Thread.onSpinWait(); continue; }
                String err = Msgs.check(m, expect);
                if (err != null) { error.set(err); break; }
                expect++;
            }
            p.join();
            assertNull(error.get());
            assertEquals(n, expect);
        });
    }

    private static void await(CountDownLatch gate) {
        try { gate.await(); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
    }
}
