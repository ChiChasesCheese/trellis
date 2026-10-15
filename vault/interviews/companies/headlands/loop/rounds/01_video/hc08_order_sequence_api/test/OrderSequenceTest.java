import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class OrderSequenceTest {

    private static List<String> lines(String block) { return block.lines().toList(); }

    /** 朴素模型（Part 1 的参考写法）：ArrayList 线性扫描，当作对拍的真值。 */
    private static final class Model {
        final List<long[]> list = new ArrayList<>(); // {id, qty}
        int find(long id) {
            for (int i = 0; i < list.size(); i++) if (list.get(i)[0] == id) return i;
            return -1;
        }
        void put(long id, long qty) { list.add(new long[] {id, qty}); }
        long delete(long id, long qty) {
            int i = find(id);
            long left = list.get(i)[1] - qty;
            if (left == 0) list.remove(i); else list.get(i)[1] = left;
            return left;
        }
        long count(long id) { return find(id) + 1; }
        long qty(long id) {
            int at = find(id);
            long s = 0;
            for (int i = 0; i <= at; i++) s += list.get(i)[1];
            return s;
        }
        long idAt(int k) { return list.get(k - 1)[0]; }
        List<OrderSequence.Entry> entries() { return list.stream().map(e -> new OrderSequence.Entry(e[0], e[1])).toList(); }
    }

    // ================= Part 1：语义 =================

    @Test @Tag("part1") @Tag("edge")
    void emptySequence() {
        var s = new OrderSequence();
        assertEquals(0, s.size());
        assertEquals(0, s.totalQty());
        assertEquals(List.of(), s.entries());
        assertThrows(NoSuchElementException.class, () -> s.countUpTo(1));
        assertThrows(NoSuchElementException.class, () -> s.qtyUpTo(1));
        assertThrows(IndexOutOfBoundsException.class, () -> s.idAt(1));
    }

    @Test @Tag("part1")
    void prefixQueriesFollowInsertionOrderNotIdOrder() {
        var s = new OrderSequence();
        s.put(10, 3);
        s.put(5, 4);
        s.put(7, 5);
        assertEquals(1, s.countUpTo(10));
        assertEquals(2, s.countUpTo(5));
        assertEquals(3, s.countUpTo(7));
        assertEquals(3, s.qtyUpTo(10));
        assertEquals(7, s.qtyUpTo(5));
        assertEquals(12, s.qtyUpTo(7));
        assertEquals(10, s.idAt(1));
        assertEquals(5, s.idAt(2));
        assertEquals(7, s.idAt(3));
        assertEquals(12, s.totalQty());
    }

    @Test @Tag("part1")
    void deleteRemovesAndReinsertGoesToTheEnd() {
        var s = new OrderSequence();
        s.put(1, 3);
        s.put(2, 4);
        s.put(3, 5);
        assertEquals(0, s.delete(2, 4)); // 整单删除 → 剩余 0
        assertEquals(2, s.size());
        assertEquals(2, s.countUpTo(3));
        assertEquals(8, s.qtyUpTo(3));
        assertEquals(3, s.idAt(2));
        assertThrows(NoSuchElementException.class, () -> s.countUpTo(2));
        s.put(2, 9); // 同一个 id 重新进来：排到最后
        assertEquals(3, s.countUpTo(2));
        assertEquals(17, s.qtyUpTo(2));
        assertEquals(List.of(new OrderSequence.Entry(1, 3), new OrderSequence.Entry(3, 5), new OrderSequence.Entry(2, 9)), s.entries());
    }

    @Test @Tag("part1") @Tag("edge")
    void invalidArgumentsLeaveStateUntouched() {
        var s = new OrderSequence();
        s.put(1, 5);
        assertThrows(IllegalArgumentException.class, () -> s.put(2, 0));
        assertThrows(IllegalArgumentException.class, () -> s.put(2, -1));
        assertThrows(IllegalArgumentException.class, () -> s.put(1, 3)); // id 已活跃
        assertThrows(IllegalArgumentException.class, () -> s.delete(1, 0));
        assertThrows(IllegalArgumentException.class, () -> s.delete(1, -2));
        assertThrows(IllegalArgumentException.class, () -> s.delete(1, 6)); // 超过剩余
        assertThrows(NoSuchElementException.class, () -> s.delete(99, 1));
        assertThrows(IndexOutOfBoundsException.class, () -> s.idAt(0));
        assertThrows(IndexOutOfBoundsException.class, () -> s.idAt(2));
        assertThrows(IndexOutOfBoundsException.class, () -> s.idAt(-3));
        assertEquals(List.of(new OrderSequence.Entry(1, 5)), s.entries());
        assertEquals(5, s.totalQty());
    }

    @Test @Tag("part1") @Tag("edge")
    void anyLongIsAValidId() {
        var s = new OrderSequence();
        for (long id : new long[] {0, -1, Long.MIN_VALUE, Long.MAX_VALUE}) s.put(id, 2);
        assertEquals(4, s.countUpTo(Long.MAX_VALUE));
        assertEquals(1, s.countUpTo(0)); // 0 是第一张
        assertEquals(Long.MIN_VALUE, s.idAt(3));
        assertEquals(0, s.delete(0, 2));
        assertEquals(3, s.countUpTo(Long.MAX_VALUE));
    }

    @Test @Tag("part1") @Tag("edge")
    void totalQuantityOverflowIsRejected() {
        var s = new OrderSequence();
        s.put(1, Long.MAX_VALUE - 10);
        assertThrows(ArithmeticException.class, () -> s.put(2, 11));
        assertEquals(1, s.size()); // 状态不变
        s.put(2, 10); // 正好到顶
        assertEquals(Long.MAX_VALUE, s.qtyUpTo(2));
        assertEquals(Long.MAX_VALUE, s.totalQty());
        assertEquals(0, s.delete(1, Long.MAX_VALUE - 10));
        s.put(3, 100); // 腾出空间后又可以放
        assertEquals(110, s.qtyUpTo(3));
    }

    @Test @Tag("part1") @Tag("fmt")
    void sampleScript() {
        var out = OrderSequence.replay(lines("""
                # 样例
                PUT 10 5
                PUT 20 3
                PUT 30 7
                COUNT 30
                QTY 20
                DELETE 20 3
                QTY 30
                AT 2

                DELETE 10 5
                put 20 4
                QTY 20
                DELETE 99 1
                DELETE 30 9
                PUT 30 1
                AT 3
                AT 2
                """));
        assertEquals(lines("""
                OK
                OK
                OK
                3
                8
                0
                12
                30
                0
                OK
                11
                ERR unknown id
                ERR quantity exceeds remaining
                ERR duplicate id
                ERR index out of range
                20
                """), out);
    }

    @ParameterizedTest @Tag("part1") @Tag("fmt")
    @ValueSource(strings = {"", "  ", "NOPE 1", "PUT 1", "PUT 1 2 3", "PUT a 2", "PUT 1 2.5", "DELETE 1", "COUNT", "COUNT 1 2",
            "QTY x", "AT", "AT 99999999999", "AT 1.5", "PUT 99999999999999999999 1"})
    void parseRejectsMalformedLines(String bad) {
        assertThrows(IllegalArgumentException.class, () -> OrderSequence.parse(bad));
    }

    @Test @Tag("part1") @Tag("fmt")
    void parseAndRenderEveryKind() {
        assertEquals(new OrderSequence.Put(1, 2), OrderSequence.parse(" put  1   2 "));
        assertEquals(new OrderSequence.Delete(1, 2), OrderSequence.parse("DELETE 1 2"));
        assertEquals(new OrderSequence.CountUpTo(-3), OrderSequence.parse("count -3"));
        assertEquals(new OrderSequence.QtyUpTo(4), OrderSequence.parse("QTY 4"));
        assertEquals(new OrderSequence.IdAt(5), OrderSequence.parse("At 5"));
        assertEquals("OK", OrderSequence.render(new OrderSequence.Ok()));
        assertEquals("-7", OrderSequence.render(new OrderSequence.Num(-7)));
        assertEquals("ERR boom", OrderSequence.render(new OrderSequence.Err("boom")));
        var ex = assertThrows(IllegalArgumentException.class, () -> OrderSequence.replay(List.of("PUT 1 1", "", "PUT x 1")));
        assertTrue(ex.getMessage().startsWith("line 3"), ex.getMessage());
    }

    @Test @Tag("part1")
    void entriesAreASequencedList() {
        var s = new OrderSequence();
        s.put(4, 1);
        s.put(2, 2);
        s.put(9, 3);
        assertEquals(4, s.entries().getFirst().id());
        assertEquals(9, s.entries().getLast().id());
        assertEquals(List.of(9L, 2L, 4L), s.entries().reversed().stream().map(OrderSequence.Entry::id).toList());
    }

    // ================= Part 2：亚线性查询 =================

    @Test @Tag("part2") @Tag("edge")
    void differentialAgainstNaiveModel() {
        var rnd = new Random(0);
        var s = new OrderSequence();
        var m = new Model();
        long nextId = 1;
        for (int step = 0; step < 40_000; step++) {
            int dice = rnd.nextInt(10);
            if (dice < 4 || m.list.isEmpty()) {
                long q = 1 + rnd.nextInt(1_000);
                s.put(nextId, q);
                m.put(nextId++, q);
            } else if (dice < 6) {
                long id = m.list.get(rnd.nextInt(m.list.size()))[0];
                long q = m.list.get(m.find(id))[1];
                assertEquals(m.delete(id, q), s.delete(id, q)); // Part 2 只做整单删除
            } else {
                long id = m.list.get(rnd.nextInt(m.list.size()))[0];
                assertEquals(m.count(id), s.countUpTo(id));
                assertEquals(m.qty(id), s.qtyUpTo(id));
                int k = 1 + rnd.nextInt(m.list.size());
                assertEquals(m.idAt(k), s.idAt(k));
            }
            assertEquals(m.list.size(), s.size());
            if (step % 5_000 == 0) assertEquals(m.entries(), s.entries());
        }
        assertEquals(m.entries(), s.entries());
    }

    @Test @Tag("part2")
    void idAtWalksEveryRankAfterManyHoles() {
        var s = new OrderSequence();
        var rnd = new Random(0);
        var live = new ArrayList<Long>();
        for (long id = 1; id <= 3_000; id++) {
            s.put(id, 1 + id % 7);
            live.add(id);
        }
        for (int i = 0; i < 2_000; i++) {
            long id = live.remove(rnd.nextInt(live.size()));
            s.delete(id, 1 + id % 7);
        }
        assertEquals(1_000, s.size());
        for (int k = 1; k <= live.size(); k++) {
            assertEquals(live.get(k - 1), s.idAt(k));
            assertEquals(k, s.countUpTo(live.get(k - 1)));
        }
    }

    /** Fenwick 的边界最容易在「大小不是 2 的幂」「只剩头 / 只剩尾」时出错：1..70 张逐个全查。 */
    @Test @Tag("part2") @Tag("edge")
    void everySmallSizeEveryPrefix() {
        for (int n = 1; n <= 70; n++) {
            var s = new OrderSequence();
            for (int i = 1; i <= n; i++) s.put(100 + i, i);
            for (int i = 1; i <= n; i++) {
                assertEquals(i, s.countUpTo(100 + i));
                assertEquals((long) i * (i + 1) / 2, s.qtyUpTo(100 + i));
                assertEquals(100 + i, s.idAt(i));
            }
            if (n >= 2) {
                s.delete(101, 1); // 删头
                s.delete(100 + n, n); // 删尾
                assertEquals(n - 2, s.size());
                if (n >= 3) {
                    assertEquals(1, s.countUpTo(102));
                    assertEquals(2, s.qtyUpTo(102));
                    assertEquals(102, s.idAt(1));
                }
            }
        }
    }

    @Test @Tag("part2") @Tag("perf")
    void halfAMillionOrdersAndQueriesInUnderTwoSeconds() {
        var rnd = new Random(0);
        int n = 500_000;
        var qtys = new long[n + 1];
        var alive = new boolean[n + 1];
        var s = new OrderSequence();
        var total = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            long acc = 0;
            for (int id = 1; id <= n; id++) {
                qtys[id] = 1 + rnd.nextInt(100);
                alive[id] = true;
                s.put(id, qtys[id]);
            }
            for (int i = 0; i < n; i++) {
                int id = 1 + rnd.nextInt(n);
                if (!alive[id]) continue;
                if (i % 5 == 0) {
                    s.delete(id, qtys[id]);
                    alive[id] = false;
                } else {
                    acc += s.countUpTo(id) + s.qtyUpTo(id) + s.idAt(1 + rnd.nextInt(s.size()));
                }
            }
            return acc;
        });
        assertTrue(total > 0);
        assertTrue(s.size() < n);
    }

    // ================= Part 3：部分删除 + 压缩 =================

    @Test @Tag("part3")
    void partialDeleteKeepsPositionAndCount() {
        var s = new OrderSequence();
        s.put(1, 10);
        s.put(2, 10);
        s.put(3, 10);
        assertEquals(6, s.delete(2, 4));
        assertEquals(3, s.countUpTo(3)); // 只是减量，订单还在
        assertEquals(26, s.qtyUpTo(3));
        assertEquals(16, s.qtyUpTo(2));
        assertEquals(26, s.totalQty());
        assertEquals(List.of(new OrderSequence.Entry(1, 10), new OrderSequence.Entry(2, 6), new OrderSequence.Entry(3, 10)), s.entries());
        assertEquals(0, s.delete(2, 6)); // 把剩余的都删掉 → 订单移除
        assertEquals(2, s.countUpTo(3));
        assertEquals(20, s.qtyUpTo(3));
        assertThrows(NoSuchElementException.class, () -> s.delete(2, 1));
        assertThrows(IllegalArgumentException.class, () -> s.delete(3, 11));
        assertEquals(3, s.idAt(2));
    }

    @Test @Tag("part3") @Tag("fmt")
    void partialDeleteSampleScript() {
        var out = OrderSequence.replay(lines("""
                PUT 1 10
                PUT 2 10
                PUT 3 10
                DELETE 2 4
                QTY 3
                COUNT 3
                DELETE 2 6
                COUNT 3
                AT 2
                """));
        assertEquals(lines("""
                OK
                OK
                OK
                6
                26
                3
                0
                2
                3
                """), out);
    }

    @Test @Tag("part3") @Tag("edge")
    void capacityIsAPowerOfTwoAndValidated() {
        assertEquals(16, new OrderSequence().capacity());
        assertEquals(8, new OrderSequence(5).capacity());
        assertEquals(8, new OrderSequence(8).capacity());
        assertEquals(1, new OrderSequence(1).capacity());
        assertThrows(IllegalArgumentException.class, () -> new OrderSequence(0));
        assertThrows(IllegalArgumentException.class, () -> new OrderSequence(-4));
    }

    @Test @Tag("part3")
    void fullIndexSpaceTriggersCompactionThatKeepsOrder() {
        var s = new OrderSequence(8);
        for (long id = 1; id <= 8; id++) s.put(id, id);
        for (long id = 1; id <= 8; id += 2) s.delete(id, id); // 删掉 1,3,5,7 → 4 个洞
        assertEquals(0, s.compactions());
        s.put(9, 9); // 下标 9 > 8：必须压缩
        assertEquals(1, s.compactions());
        assertEquals(8, s.capacity()); // 活跃 4 张，容量没必要涨
        assertEquals(List.of(2L, 4L, 6L, 8L, 9L), s.entries().stream().map(OrderSequence.Entry::id).toList());
        assertEquals(5, s.countUpTo(9));
        assertEquals(2 + 4 + 6 + 8 + 9, s.qtyUpTo(9));
        assertEquals(6, s.idAt(3));
        assertEquals(2, s.countUpTo(4));
    }

    @Test @Tag("part3")
    void compactionGrowsWhenEverythingIsAlive() {
        var s = new OrderSequence(8);
        for (long id = 1; id <= 9; id++) s.put(id, 1);
        assertEquals(1, s.compactions());
        assertEquals(16, s.capacity()); // 8 张活跃、没有洞：必须长
        assertEquals(9, s.countUpTo(9));
        for (long id = 10; id <= 300; id++) s.put(id, 1);
        assertEquals(300, s.size());
        assertEquals(300, s.countUpTo(300));
        assertEquals(150, s.idAt(150));
        assertTrue(s.capacity() >= 300 && s.capacity() <= 1024, "capacity " + s.capacity());
    }

    @Test @Tag("part3") @Tag("edge")
    void compactionShrinksBackAfterBurst() {
        var s = new OrderSequence(16);
        for (long id = 1; id <= 4_000; id++) s.put(id, 1);
        int big = s.capacity();
        assertTrue(big >= 4_000);
        for (long id = 1; id <= 3_990; id++) s.delete(id, 1);
        for (long id = 5_000; id < 5_000 + big; id++) { // 一直 put 直到触发压缩
            s.put(id, 1);
            s.delete(id, 1);
        }
        assertTrue(s.capacity() < big / 4, "capacity " + s.capacity() + " after shrink, was " + big);
        assertEquals(10, s.size());
        assertEquals(10, s.countUpTo(4_000));
        assertEquals(3_991, s.idAt(1));
    }

    @Test @Tag("part3") @Tag("edge")
    void differentialWithTinyCapacityAndPartialDeletes() {
        var rnd = new Random(0);
        var s = new OrderSequence(4);
        var m = new Model();
        long nextId = 1;
        for (int step = 0; step < 60_000; step++) {
            int dice = rnd.nextInt(10);
            if (dice < 4 || m.list.isEmpty()) {
                long q = 1 + rnd.nextInt(50);
                s.put(nextId, q);
                m.put(nextId++, q);
            } else if (dice < 8) {
                long id = m.list.get(rnd.nextInt(m.list.size()))[0];
                long have = m.list.get(m.find(id))[1];
                long q = rnd.nextBoolean() ? have : 1 + rnd.nextInt((int) have); // 一半整删，一半部分删
                assertEquals(m.delete(id, q), s.delete(id, q));
            } else {
                long id = m.list.get(rnd.nextInt(m.list.size()))[0];
                assertEquals(m.count(id), s.countUpTo(id));
                assertEquals(m.qty(id), s.qtyUpTo(id));
                int k = 1 + rnd.nextInt(m.list.size());
                assertEquals(m.idAt(k), s.idAt(k));
            }
            assertEquals(m.list.size(), s.size());
        }
        assertEquals(m.entries(), s.entries());
        assertTrue(s.compactions() > 10, "compactions " + s.compactions());
    }

    @Test @Tag("part3") @Tag("perf")
    void twoMillionPutDeleteCyclesStayInBoundedMemory() {
        var s = new OrderSequence();
        var window = new ArrayDeque<Long>();
        var rnd = new Random(0);
        int n = 2_000_000;
        var qtys = new long[n + 1];
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            for (int id = 1; id <= n; id++) {
                qtys[id] = 1 + rnd.nextInt(100);
                s.put(id, qtys[id]);
                window.addLast((long) id);
                if (window.size() > 1_000) {
                    long old = window.pollFirst(); // 永远删最老的：洞全堆在序列前面
                    s.delete(old, qtys[(int) old]);
                }
            }
        });
        assertEquals(1_000, s.size());
        assertTrue(s.capacity() <= 4_096, "capacity " + s.capacity()); // 内存跟活跃量走，不跟 200 万走
        assertTrue(s.compactions() > 100, "compactions " + s.compactions());
        assertEquals(1_000, s.countUpTo(window.getLast()));
        assertEquals(window.getFirst(), s.idAt(1));
    }
}
