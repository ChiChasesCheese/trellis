import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class GenPoolTest {

    @Test @Tag("part2")
    void handlePackingRoundTrips() {
        long h = GenPool.handle(5, 7);
        assertEquals(5, GenPool.indexOf(h));
        assertEquals(7, GenPool.generationOf(h));
        assertEquals((7L << 32) | 5L, h);
        // 版本号是负数（高位为 1）、下标是 int 最大值：符号扩展是最常见的打包 bug
        long h2 = GenPool.handle(Integer.MAX_VALUE, -1);
        assertEquals(Integer.MAX_VALUE, GenPool.indexOf(h2));
        assertEquals(-1, GenPool.generationOf(h2));
        long h3 = GenPool.handle(0, Integer.MIN_VALUE);
        assertEquals(0, GenPool.indexOf(h3));
        assertEquals(Integer.MIN_VALUE, GenPool.generationOf(h3));
    }

    @Test @Tag("part2")
    void firstHandlesAreGenerationOneAscendingIndex() {
        var pool = new GenPool(3);
        assertEquals(GenPool.handle(0, 1), pool.allocate());
        assertEquals(GenPool.handle(1, 1), pool.allocate());
        assertEquals(GenPool.handle(2, 1), pool.allocate());
        assertEquals(GenPool.NONE, pool.allocate());
        assertEquals(0, pool.available());
    }

    @Test @Tag("part2")
    void freeThenAllocateBumpsGenerationByTwo() {
        var pool = new GenPool(1);
        long a = pool.allocate();
        assertEquals(FreeResult.FREED, pool.free(a));
        long b = pool.allocate();
        assertEquals(GenPool.indexOf(a), GenPool.indexOf(b));
        assertEquals(GenPool.generationOf(a) + 2, GenPool.generationOf(b));
        assertNotEquals(a, b);
    }

    @Test @Tag("part2") @Tag("edge")
    void useAfterFreeIsDetected() {
        var pool = new GenPool(2);
        long a = pool.allocate();
        assertTrue(pool.isLive(a));
        pool.free(a);
        assertFalse(pool.isLive(a));
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(a));
        assertEquals(2, pool.available());
    }

    @Test @Tag("part2") @Tag("edge")
    void staleHandleOfReusedSlotIsRejected() {
        // IndexPool.staleIndexCannotBeToldApartFromTheNewOwner 的对照：同一个场景，这里旧 handle 不能再动新主人的块
        var pool = new GenPool(1);
        long a = pool.allocate();
        pool.free(a);
        long b = pool.allocate();
        assertEquals(GenPool.indexOf(a), GenPool.indexOf(b));
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(a));
        assertTrue(pool.isLive(b));
        assertFalse(pool.isLive(a));
        assertEquals(FreeResult.FREED, pool.free(b));
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(longs = {0L, -1L, 1L, 0x0000_0002_0000_0000L, 0x0000_0001_0000_0003L, 0x0000_0001_FFFF_FFFFL,
            0x0000_0001_8000_0000L, Long.MIN_VALUE, Long.MAX_VALUE})
    void invalidHandles(long bad) {
        // 全零、NONE、版本号为偶数（从没发过）、下标越界（含「低 32 位当 int 是负数」）
        var pool = new GenPool(3);
        pool.allocate();
        assertEquals(FreeResult.INVALID, pool.free(bad));
        assertFalse(pool.isLive(bad));
        assertEquals(2, pool.available());
    }

    @Test @Tag("part2") @Tag("edge")
    void noneIsNeverAValidHandle() {
        var pool = new GenPool(1);
        assertEquals(FreeResult.INVALID, pool.free(GenPool.NONE));
        long a = pool.allocate();
        assertNotEquals(GenPool.NONE, a);
        assertFalse(pool.isLive(GenPool.NONE));
    }

    @Test @Tag("part2") @Tag("edge")
    void generationWrapsAroundCorrectly() {
        // 从 2^32-2 起步：分配得到 -1（0xFFFFFFFF，奇数），归还后回绕成 0（偶数 = 空闲），再分配得到 1
        var pool = new GenPool(1, -2);
        long a = pool.allocate();
        assertEquals(-1, GenPool.generationOf(a));
        assertTrue(pool.isLive(a));
        assertEquals(FreeResult.FREED, pool.free(a));
        long b = pool.allocate();
        assertEquals(1, GenPool.generationOf(b));
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(a));
        assertTrue(pool.isLive(b));
        assertThrows(IllegalArgumentException.class, () -> new GenPool(1, 1));
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(ints = {0, -1, (1 << 28) + 1})
    void rejectsBadCapacity(int cap) {
        assertThrows(IllegalArgumentException.class, () -> new GenPool(cap));
    }

    @Test @Tag("part2")
    void interleavedLifetimesStayIndependent() {
        var pool = new GenPool(4);
        List<Long> hs = new ArrayList<>();
        for (int i = 0; i < 4; i++) hs.add(pool.allocate());
        pool.free(hs.get(1));
        pool.free(hs.get(2));
        long x = pool.allocate();
        assertEquals(GenPool.indexOf(hs.get(2)), GenPool.indexOf(x)); // LIFO
        assertTrue(pool.isLive(hs.get(0)));
        assertFalse(pool.isLive(hs.get(1)));
        assertFalse(pool.isLive(hs.get(2)));
        assertTrue(pool.isLive(hs.get(3)));
        assertTrue(pool.isLive(x));
    }

    @Test @Tag("part2") @Tag("perf")
    void nearFullChurnIsFast() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            int cap = 1 << 16;
            var rnd = new Random(0);
            var pool = new GenPool(cap);
            long[] held = new long[cap];
            for (int i = 0; i < cap; i++) held[i] = pool.allocate();
            assertEquals(GenPool.NONE, pool.allocate());
            for (int step = 0; step < 1_500_000; step++) {
                int k = rnd.nextInt(cap);
                assertEquals(FreeResult.FREED, pool.free(held[k]));
                assertEquals(FreeResult.DOUBLE_FREE, pool.free(held[k]));
                long h = pool.allocate();
                assertNotEquals(GenPool.NONE, h);
                held[k] = h;
            }
            assertEquals(0, pool.available());
        });
    }

    @Test @Tag("part2") @Tag("perf")
    void randomOpsAgainstModelAreFast() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            int cap = 1 << 16;
            var rnd = new Random(0);
            var pool = new GenPool(cap);
            long[] held = new long[cap];
            int n = 0;
            long[] graveyard = new long[1024];
            int g = 0;
            for (int step = 0; step < 3_000_000; step++) {
                if (n > 0 && (n == cap || rnd.nextInt(2) == 0)) {
                    int k = rnd.nextInt(n);
                    long h = held[k];
                    held[k] = held[--n];
                    assertEquals(FreeResult.FREED, pool.free(h));
                    graveyard[g++ & 1023] = h;
                } else {
                    long h = pool.allocate();
                    assertNotEquals(GenPool.NONE, h);
                    held[n++] = h;
                }
                if ((step & 1023) == 0 && g > 0) {            // 时不时拿一个死 handle 试探：必须每次都被拒绝
                    long dead = graveyard[rnd.nextInt(Math.min(g, 1024))];
                    assertFalse(pool.isLive(dead));
                    assertEquals(FreeResult.DOUBLE_FREE, pool.free(dead));
                }
            }
            assertEquals(cap - n, pool.available());
        });
    }
}
