import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.ArrayDeque;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

/**
 * 定长 long 队列的单线程契约。LongRing（Part 1）和 SpscLongRing（Part 2，在单线程下）必须满足同一套规则，
 * 所以这些用例写在抽象基类里，由 LongRingTest（tag part1）和 SpscLongRingSequentialTest（tag part2）各跑一遍。
 */
abstract class LongQueueContract {
    abstract LongQueue make(int capacity);

    @Test
    void fifoOrder() {
        LongQueue q = make(8);
        for (long i = 1; i <= 5; i++) assertTrue(q.offer(i * 10));
        assertEquals(5, q.size());
        for (long i = 1; i <= 5; i++) assertEquals(i * 10, q.poll());
        assertTrue(q.isEmpty());
        assertEquals(0, q.size());
    }

    @Test @Tag("edge")
    void fullAndEmptyRules() {
        LongQueue q = make(4);
        assertTrue(q.isEmpty());
        assertFalse(q.isFull());
        for (int i = 0; i < 4; i++) assertTrue(q.offer(i));
        assertTrue(q.isFull());
        assertFalse(q.isEmpty());
        assertFalse(q.offer(99), "满了必须拒绝，不能覆盖最旧的元素");
        assertEquals(4, q.size());
        assertEquals(0, q.poll());                    // 腾出一个位置
        assertFalse(q.isFull());
        assertTrue(q.offer(4));                       // 回绕到数组开头
        assertTrue(q.isFull());
        for (int i = 1; i <= 4; i++) assertEquals(i, q.poll());
        assertTrue(q.isEmpty());
    }

    @Test @Tag("edge")
    void pollOnEmptyThrows() {
        LongQueue q = make(2);
        assertThrows(NoSuchElementException.class, q::poll);
        q.offer(1);
        q.poll();
        assertThrows(NoSuchElementException.class, q::poll);
    }

    @Test @Tag("edge")
    void capacityOneWorks() {
        LongQueue q = make(1);
        assertEquals(1, q.capacity());
        for (int round = 0; round < 10; round++) {
            assertTrue(q.offer(round));
            assertFalse(q.offer(-1));
            assertEquals(round, q.poll());
        }
    }

    @Test @Tag("edge")
    void everyLongIsAValidMessage() {
        // 没有哨兵值：Long.MIN_VALUE、-1、0、Long.MAX_VALUE 都能原样进出
        LongQueue q = make(4);
        long[] vs = {Long.MIN_VALUE, -1, 0, Long.MAX_VALUE};
        for (long v : vs) q.offer(v);
        for (long v : vs) assertEquals(v, q.poll());
    }

    @Test @Tag("edge")
    void countersKeepWorkingAfterManyWraps() {
        LongQueue q = make(4);
        long next = 0, expect = 0;
        for (int i = 0; i < 1_000_000; i++) {         // 远超 capacity 倍，也远超 2^16：计数一直在涨
            q.offer(next++);
            q.offer(next++);
            assertEquals(expect++, q.poll());
            assertEquals(expect++, q.poll());
        }
        assertTrue(q.isEmpty());
    }

    @ParameterizedTest @Tag("edge")
    @ValueSource(ints = {0, -1, -8, 3, 6, 12, 1000, (1 << 30) + 1, Integer.MAX_VALUE, Integer.MIN_VALUE})
    void rejectsNonPowerOfTwoCapacity(int bad) {
        assertThrows(IllegalArgumentException.class, () -> make(bad));
    }

    @Test
    void randomOpsMatchArrayDeque() {
        var rnd = new Random(0);
        LongQueue q = make(16);
        var model = new ArrayDeque<Long>();
        for (int step = 0; step < 200_000; step++) {
            if (rnd.nextInt(100) < 55) {
                long v = rnd.nextLong();
                boolean ok = q.offer(v);
                assertEquals(model.size() < 16, ok);
                if (ok) model.addLast(v);
            } else if (model.isEmpty()) {
                assertThrows(NoSuchElementException.class, q::poll);
            } else {
                assertEquals(model.pollFirst(), q.poll());
            }
            assertEquals(model.size(), q.size());
        }
    }

    @Test @Tag("perf")
    void twentyMillionOpsSingleThread() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            LongQueue q = make(1024);
            long sum = 0;
            for (int i = 0; i < 10_000_000; i++) {
                q.offer(i);
                sum += q.poll();
            }
            assertEquals(49_999_995_000_000L, sum);
        });
    }
}
