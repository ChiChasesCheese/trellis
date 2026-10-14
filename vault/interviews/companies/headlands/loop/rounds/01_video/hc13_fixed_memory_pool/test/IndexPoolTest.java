import static org.junit.jupiter.api.Assertions.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class IndexPoolTest {

    @Test @Tag("part1")
    void allocatesAscendingThenReportsExhaustion() {
        var pool = new IndexPool(3);
        assertEquals(3, pool.capacity());
        assertEquals(0, pool.allocate());
        assertEquals(1, pool.allocate());
        assertEquals(2, pool.allocate());
        assertEquals(0, pool.available());
        assertEquals(IndexPool.NONE, pool.allocate());
        assertEquals(IndexPool.NONE, pool.allocate()); // 重复问也不坏
    }

    @Test @Tag("part1")
    void reusesMostRecentlyFreedFirst() {
        var pool = new IndexPool(4);
        for (int i = 0; i < 4; i++) pool.allocate();
        assertEquals(FreeResult.FREED, pool.free(1));
        assertEquals(FreeResult.FREED, pool.free(3));
        assertEquals(3, pool.allocate()); // LIFO：最后归还的最先出来
        assertEquals(1, pool.allocate());
        assertEquals(IndexPool.NONE, pool.allocate());
    }

    @Test @Tag("part1") @Tag("edge")
    void detectsDoubleFree() {
        var pool = new IndexPool(2);
        int a = pool.allocate();
        assertEquals(FreeResult.FREED, pool.free(a));
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(a));
        assertEquals(2, pool.available(), "重复归还不能让 available 超过 capacity");
        // 从没分配过的块也是「当前不在使用中」
        assertEquals(FreeResult.DOUBLE_FREE, pool.free(1));
        assertEquals(2, pool.available());
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(ints = {-1, -2, 4, 5, Integer.MAX_VALUE, Integer.MIN_VALUE})
    void detectsInvalidBlocks(int bad) {
        var pool = new IndexPool(4);
        for (int i = 0; i < 4; i++) pool.allocate();
        assertEquals(FreeResult.INVALID, pool.free(bad));
        assertEquals(0, pool.available());
        assertFalse(pool.isAllocated(bad));
    }

    @Test @Tag("part1") @Tag("edge")
    void doubleFreeDoesNotCorruptTheFreeList() {
        // 经典 bug：重复归还把同一块插进链表两次 → 之后同一块被分配给两个人
        var pool = new IndexPool(3);
        int a = pool.allocate(), b = pool.allocate(), c = pool.allocate();
        pool.free(b);
        pool.free(b);
        pool.free(b);
        var seen = new HashSet<Integer>();
        for (int i = 0; i < 5; i++) {
            int x = pool.allocate();
            if (x != IndexPool.NONE) assertTrue(seen.add(x), "同一块被分配了两次: " + x);
        }
        assertEquals(1, seen.size());
        assertTrue(seen.contains(b));
        assertNotEquals(a, c);
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(ints = {0, -1, Integer.MIN_VALUE, (1 << 28) + 1, Integer.MAX_VALUE})
    void rejectsBadCapacity(int cap) {
        assertThrows(IllegalArgumentException.class, () -> new IndexPool(cap));
    }

    @Test @Tag("part1") @Tag("edge")
    void capacityOne() {
        var pool = new IndexPool(1);
        assertEquals(0, pool.allocate());
        assertEquals(IndexPool.NONE, pool.allocate());
        assertEquals(FreeResult.FREED, pool.free(0));
        assertEquals(0, pool.allocate());
    }

    @Test @Tag("part1")
    void isAllocatedTracksState() {
        var pool = new IndexPool(2);
        assertFalse(pool.isAllocated(0));
        int a = pool.allocate();
        assertTrue(pool.isAllocated(a));
        pool.free(a);
        assertFalse(pool.isAllocated(a));
    }

    @Test @Tag("part1")
    void freeOrThrowMapsResultsToExceptions() {
        var pool = new IndexPool(2);
        int a = pool.allocate();
        assertDoesNotThrow(() -> pool.freeOrThrow(a));
        assertThrows(IllegalStateException.class, () -> pool.freeOrThrow(a));
        assertThrows(IllegalArgumentException.class, () -> pool.freeOrThrow(99));
    }

    @Test @Tag("part1") @Tag("edge")
    void staleIndexCannotBeToldApartFromTheNewOwner() {
        // 本测试「记录」Part 1 的局限，不是在要求实现去修它：
        // 下标本身没有身份，a 归还后块被 b 拿走，a 手里的旧下标再 free，就把 b 的块偷偷还掉了。
        // Part 2 的 handle 带版本号就是为了堵住这个洞（GenPoolTest.staleHandleOfReusedSlotIsRejected）。
        var pool = new IndexPool(1);
        int a = pool.allocate();
        pool.free(a);
        int b = pool.allocate();
        assertEquals(a, b);
        assertEquals(FreeResult.FREED, pool.free(a));
        assertFalse(pool.isAllocated(b));
    }

    @Test @Tag("part1")
    void everyBlockHandedOutExactlyOnceAfterChurn() {
        var rnd = new Random(0);
        var pool = new IndexPool(100);
        List<Integer> held = new ArrayList<>();
        for (int step = 0; step < 10_000; step++) {
            if (rnd.nextBoolean() && !held.isEmpty()) {
                int k = rnd.nextInt(held.size());
                assertEquals(FreeResult.FREED, pool.free(held.remove(k)));
            } else {
                int x = pool.allocate();
                if (x != IndexPool.NONE) held.add(x);
            }
        }
        for (int x : new ArrayList<>(held)) pool.free(x);
        var seen = new BitSet();
        for (int i = 0; i < 100; i++) {
            int x = pool.allocate();
            assertNotEquals(IndexPool.NONE, x);
            assertFalse(seen.get(x));
            seen.set(x);
        }
        assertEquals(IndexPool.NONE, pool.allocate());
    }

    /** 池几乎一直是满的，每步换掉随机一块：O(n) 扫描空位的写法在这里会慢几个数量级（空位平均在中间，每次扫 n/2）。 */
    @Test @Tag("part1") @Tag("perf")
    void nearFullChurnIsFast() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            int cap = 1 << 16;
            var rnd = new Random(0);
            var pool = new IndexPool(cap);
            int[] held = new int[cap];
            for (int i = 0; i < cap; i++) held[i] = pool.allocate();
            assertEquals(IndexPool.NONE, pool.allocate());
            for (int step = 0; step < 1_500_000; step++) {
                int k = rnd.nextInt(cap);
                assertEquals(FreeResult.FREED, pool.free(held[k]));
                int b = pool.allocate();
                assertNotEquals(IndexPool.NONE, b);
                held[k] = b;
            }
            assertEquals(0, pool.available());
            var seen = new BitSet(cap);
            for (int b : held) { assertFalse(seen.get(b)); seen.set(b); }
        });
    }

    @Test @Tag("part1") @Tag("perf")
    void randomOpsMatchModelAndAreFast() {
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            int cap = 1 << 16;
            var rnd = new Random(0);
            var pool = new IndexPool(cap);
            var live = new BitSet(cap);
            int[] stack = new int[cap];
            int n = 0;
            for (int step = 0; step < 3_000_000; step++) {
                if (n > 0 && (n == cap || rnd.nextInt(2) == 0)) {
                    int k = rnd.nextInt(n);
                    int b = stack[k];
                    stack[k] = stack[--n];
                    live.clear(b);
                    assertEquals(FreeResult.FREED, pool.free(b));
                } else {
                    int b = pool.allocate();
                    assertNotEquals(IndexPool.NONE, b);
                    assertFalse(live.get(b));
                    live.set(b);
                    stack[n++] = b;
                }
            }
            assertEquals(cap - n, pool.available());
        });
    }
}
