import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class OffHeapOrderPoolTest {

    @Test @Tag("part3")
    void putGetRoundTrip() {
        try (var pool = new OffHeapOrderPool(4)) {
            long h = pool.allocate();
            var o = new Order(123_456_789_012L, 18_950, 100, 1);
            pool.put(h, o);
            assertEquals(o, pool.get(h));
            pool.put(h, new Order(1, 2, 3, 4));
            assertEquals(new Order(1, 2, 3, 4), pool.get(h));
        }
    }

    @Test @Tag("part3")
    void fieldwiseAccessMatchesRecordAccess() {
        try (var pool = new OffHeapOrderPool(2)) {
            long h = pool.allocate();
            pool.put(h, 11L, 22L, 33, 1);
            assertEquals(new Order(11, 22, 33, 1), pool.get(h));
            assertEquals(22L, pool.px(h));
            assertEquals(33, pool.qty(h));
            pool.put(h, new Order(5, 6, 7, 0));
            assertEquals(6L, pool.px(h));
            assertEquals(7, pool.qty(h));
            pool.free(h);
            assertThrows(IllegalStateException.class, () -> pool.px(h));
            assertThrows(IllegalStateException.class, () -> pool.qty(h));
            assertThrows(IllegalStateException.class, () -> pool.put(h, 1L, 1L, 1, 1));
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void extremeValuesSurviveRoundTrip() {
        try (var pool = new OffHeapOrderPool(2)) {
            long h = pool.allocate();
            var o = new Order(Long.MIN_VALUE, Long.MAX_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE);
            pool.put(h, o);
            assertEquals(o, pool.get(h));
            var neg = new Order(-1, -1, -1, -1);
            pool.put(h, neg);
            assertEquals(neg, pool.get(h));
        }
    }

    @Test @Tag("part3")
    void neighbouringRecordsDoNotOverlap() {
        int n = 1000;
        try (var pool = new OffHeapOrderPool(n)) {
            long[] hs = new long[n];
            for (int i = 0; i < n; i++) {
                hs[i] = pool.allocate();
                pool.put(hs[i], new Order(i, -i, i * 3, i % 2));
            }
            for (int i = 0; i < n; i++) assertEquals(new Order(i, -i, i * 3, i % 2), pool.get(hs[i]), "slot " + i);
            assertEquals(OffHeapOrderPool.NONE, pool.allocate());
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void reusedRecordIsZeroed() {
        try (var pool = new OffHeapOrderPool(1)) {
            long a = pool.allocate();
            pool.put(a, new Order(7, 8, 9, 10));
            pool.free(a);
            long b = pool.allocate();
            assertEquals(Order.ZERO, pool.get(b), "上一个主人的数据不能漏给下一个");
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void staleAndInvalidHandlesAreRejected() {
        try (var pool = new OffHeapOrderPool(2)) {
            long a = pool.allocate();
            pool.put(a, new Order(1, 1, 1, 1));
            assertEquals(FreeResult.FREED, pool.free(a));
            assertEquals(FreeResult.DOUBLE_FREE, pool.free(a));
            assertThrows(IllegalStateException.class, () -> pool.get(a));
            assertThrows(IllegalStateException.class, () -> pool.put(a, Order.ZERO));
            long b = pool.allocate();                       // 同一槽位被重新分配
            pool.put(b, new Order(2, 2, 2, 2));
            assertThrows(IllegalStateException.class, () -> pool.get(a));      // 旧 handle 读不到新主人的数据
            assertEquals(FreeResult.DOUBLE_FREE, pool.free(a));
            assertEquals(new Order(2, 2, 2, 2), pool.get(b));
            for (long bad : new long[] {OffHeapOrderPool.NONE, 0L, 1L, 0x1_0000_0063L}) {
                assertEquals(FreeResult.INVALID, pool.free(bad));
                assertThrows(IllegalStateException.class, () -> pool.get(bad));
            }
        }
    }

    @Test @Tag("part3")
    void layoutIsOneContiguousSegment() {
        assertEquals(32, OffHeapOrderPool.recordBytes());
        try (var pool = new OffHeapOrderPool(1000)) {
            assertEquals(32_000L, pool.byteSize());
            assertEquals(1000, pool.capacity());
            assertEquals(1000, pool.available());
            pool.allocate();
            assertEquals(999, pool.available());
        }
    }

    @Test @Tag("part3") @Tag("edge")
    void closeIsIdempotentAndBlocksFurtherAccess() {
        var pool = new OffHeapOrderPool(2);
        long h = pool.allocate();
        pool.close();
        pool.close();                                       // 第二次不抛
        assertThrows(IllegalStateException.class, () -> pool.get(h));
        assertThrows(IllegalStateException.class, pool::allocate);
    }

    @Test @Tag("part3") @Tag("edge")
    void rejectsBadCapacity() {
        assertThrows(IllegalArgumentException.class, () -> new OffHeapOrderPool(0));
        assertThrows(IllegalArgumentException.class, () -> new OffHeapOrderPool(-5));
        assertThrows(IllegalArgumentException.class, () -> new OffHeapOrderPool((1 << 28) + 1));
        assertThrows(NullPointerException.class, () -> {
            try (var pool = new OffHeapOrderPool(1)) { pool.put(pool.allocate(), null); }
        });
    }

    @Test @Tag("part3")
    void usableFromAnotherThread() throws Exception {
        // Arena.ofShared：不在创建线程里也能访问（Arena.ofConfined 会抛 WrongThreadException）
        try (var pool = new OffHeapOrderPool(2)) {
            long h = pool.allocate();
            pool.put(h, new Order(9, 9, 9, 9));
            assertEquals(new Order(9, 9, 9, 9), CompletableFuture.supplyAsync(() -> pool.get(h)).get());
        }
    }

    @Test @Tag("part3") @Tag("perf")
    void millionRecordsChurn() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            int cap = 1_000_000;
            var rnd = new Random(0);
            try (var pool = new OffHeapOrderPool(cap)) {
                long[] hs = new long[cap];
                for (int i = 0; i < cap; i++) {
                    hs[i] = pool.allocate();
                    pool.put(hs[i], new Order(i, i * 2L, i & 0xFFFF, i & 1));
                }
                assertEquals(OffHeapOrderPool.NONE, pool.allocate());
                long sum = 0;
                for (int i = 0; i < cap; i++) sum += pool.get(hs[i]).px();
                assertEquals((long) cap * (cap - 1), sum);
                List<Long> freed = new ArrayList<>();
                for (int i = 0; i < 200_000; i++) {
                    int k = rnd.nextInt(cap);
                    if (hs[k] != 0 && pool.free(hs[k]) == FreeResult.FREED) { freed.add(hs[k]); hs[k] = 0; }
                }
                assertEquals(freed.size(), pool.available());
                for (long h : freed) assertFalse(pool.isLive(h));
            }
        });
    }
}
