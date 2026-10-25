import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.atomic.AtomicReference;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

class DeskTreeTest {
    // 样例：
    //   0 (1)
    //   ├── 1 (4) ── 3 (6), 4 (3)
    //   └── 2 (-9) ── 5 (7), 6 (1)
    private static final int[] SAMPLE_PARENT = {-1, 0, 0, 1, 1, 2, 2};
    private static final long[] SAMPLE_PNL = {1, 4, -9, 6, 3, 7, 1};

    private static DeskTree sample() { return DeskTree.ofParents(SAMPLE_PARENT, SAMPLE_PNL); }

    private static final long BOUND = DeskTree.MAX_ABS_PNL;

    private static void assertIae(String message, Runnable body) {
        var e = assertThrows(IllegalArgumentException.class, body::run);
        assertEquals(message, e.getMessage());
    }

    /** 在指定栈大小的线程里跑；Error / 异常原样抛回测试线程。 */
    private static <T> T onStack(long bytes, Callable<T> body) throws Throwable {
        var result = new AtomicReference<T>();
        var failure = new AtomicReference<Throwable>();
        var t = new Thread(null, () -> {
            try { result.set(body.call()); } catch (Throwable e) { failure.set(e); }
        }, "sized-stack", bytes);
        t.start();
        t.join();
        if (failure.get() != null) throw failure.get();
        return result.get();
    }

    private static final long SMALL_STACK = 512 * 1024;

    /** 大列表比较：失败信息只报大小和开头几项，不把 10^5 个数字刷满屏幕。 */
    private static void assertSameDesks(List<Integer> expected, List<Integer> actual) {
        assertTrue(expected.equals(actual), () -> "plan.desks differs: expected " + expected.size() + " desks starting "
                + expected.stream().limit(5).toList() + ", got " + actual.size() + " starting " + actual.stream().limit(5).toList());
    }

    // ---------- 随机树 + 慢速模型 ----------

    /** 标签被打乱的随机树；reach 越小树越深。返回 parent 数组（根为 -1）。 */
    private static int[] randomParents(Random rnd, int n, int reach) {
        int[] perm = IntStream.range(0, n).toArray();
        for (int i = n - 1; i > 0; i--) {
            int j = rnd.nextInt(i + 1);
            int t = perm[i]; perm[i] = perm[j]; perm[j] = t;
        }
        int[] parent = new int[n];
        parent[perm[0]] = -1;
        for (int i = 1; i < n; i++) parent[perm[i]] = perm[i - 1 - rnd.nextInt(Math.min(i, reach))];
        return parent;
    }

    private static long[] randomPnl(Random rnd, int n, int lo, int hi) {
        long[] pnl = new long[n];
        for (int i = 0; i < n; i++) pnl[i] = lo + rnd.nextInt(hi - lo + 1);
        return pnl;
    }

    private static int rootOf(int[] parent) {
        for (int i = 0; i < parent.length; i++) if (parent[i] == -1) return i;
        return -1;
    }

    private static List<Integer> childrenOf(int[] parent, int v) {
        var out = new ArrayList<Integer>();
        for (int i = 0; i < parent.length; i++) if (parent[i] == v) out.add(i);
        return out;
    }

    /** 慢速递归模型（只在小树上用）：{take, skip}。 */
    private static long[] model(int[] parent, long[] pnl, int v) {
        long take = pnl[v], skip = 0;
        for (int c : childrenOf(parent, v)) {
            long[] r = model(parent, pnl, c);
            take += r[1];
            skip += Math.max(r[0], r[1]);
        }
        return new long[] {take, skip};
    }

    private static void modelPlan(int[] parent, long[] pnl, int v, boolean parentChosen, boolean[] chosen) {
        long[] r = model(parent, pnl, v);
        chosen[v] = !parentChosen && r[0] > r[1];
        for (int c : childrenOf(parent, v)) modelPlan(parent, pnl, c, chosen[v], chosen);
    }

    private static List<Integer> modelDesks(int[] parent, long[] pnl) {
        boolean[] chosen = new boolean[parent.length];
        modelPlan(parent, pnl, rootOf(parent), false, chosen);
        return IntStream.range(0, parent.length).filter(i -> chosen[i]).boxed().toList();
    }

    /** 2^n 枚举：最大独立集（相邻 = 父子）。 */
    private static long bruteRobber(int[] parent, long[] pnl) {
        int n = parent.length;
        long best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            long sum = 0;
            for (int v = 0; v < n && ok; v++) {
                if ((mask >> v & 1) == 0) continue;
                sum += pnl[v];
                if (parent[v] >= 0 && (mask >> parent[v] & 1) == 1) ok = false;
            }
            if (ok) best = Math.max(best, sum);
        }
        return best;
    }

    private static List<Integer> chainToRoot(int[] parent, int v) {
        var out = new ArrayList<Integer>();
        for (int x = v; x >= 0; x = parent[x]) out.add(x);
        return out;
    }

    /** 所有点对的路径和（经过最近公共祖先）里的最大值。 */
    private static long brutePath(int[] parent, long[] pnl) {
        int n = parent.length;
        long best = Long.MIN_VALUE;
        for (int u = 0; u < n; u++) {
            var up = chainToRoot(parent, u);
            for (int v = u; v < n; v++) {
                var vp = chainToRoot(parent, v);
                int lca = -1;
                for (int x : up) if (vp.contains(x)) { lca = x; break; }
                long sum = 0;
                for (int x : up) { sum += pnl[x]; if (x == lca) break; }
                for (int x : vp) { if (x == lca) break; sum += pnl[x]; }
                best = Math.max(best, sum);
            }
        }
        return best;
    }

    private static long bruteDown(int[] parent, long[] pnl) {
        long best = Long.MIN_VALUE;
        for (int d = 0; d < parent.length; d++) {
            long sum = 0;
            for (int x : chainToRoot(parent, d)) {
                sum += pnl[x];
                best = Math.max(best, sum);
            }
        }
        return best;
    }

    private static DeskTree.Subtree bruteSubtree(int[] parent, long[] pnl) {
        int n = parent.length;
        long[] sum = new long[n];
        for (int d = 0; d < n; d++) for (int x : chainToRoot(parent, d)) sum[x] += pnl[d];
        int best = 0;
        for (int v = 1; v < n; v++) if (sum[v] > sum[best]) best = v;
        return new DeskTree.Subtree(best, sum[best]);
    }

    private static int[][] edgesOf(int[] parent) {
        var out = new ArrayList<int[]>();
        for (int i = 0; i < parent.length; i++) if (parent[i] >= 0) out.add(new int[] {i, parent[i]});
        return out.toArray(new int[0][]);
    }

    // ================= Part 1：建树 + 最大总 PnL =================

    @Test @Tag("part1")
    void sampleTree() {
        var t = sample();
        assertEquals(7, t.size());
        assertEquals(0, t.root());
        assertEquals(18, t.maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void emptyTreeIsValid() {
        var t = DeskTree.ofParents(new int[0], new long[0]);
        assertEquals(0, t.size());
        assertEquals(-1, t.root());
        assertEquals(0, t.maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void singleDesk() {
        assertEquals(7, DeskTree.ofParents(new int[] {-1}, new long[] {7}).maxPnl());
        assertEquals(0, DeskTree.ofParents(new int[] {-1}, new long[] {-7}).maxPnl());
        assertEquals(0, DeskTree.ofParents(new int[] {-1}, new long[] {0}).maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void allNegativeChoosesNothing() {
        var t = DeskTree.ofParents(new int[] {-1, 0, 1, 1}, new long[] {-1, -2, -3, -4});
        assertEquals(0, t.maxPnl());
    }

    @Test @Tag("part1")
    void parentAndChildCannotBothBeChosen() {
        assertEquals(4, DeskTree.ofParents(new int[] {-1, 0}, new long[] {3, 4}).maxPnl());
        assertEquals(3, DeskTree.ofParents(new int[] {-1, 0}, new long[] {3, -4}).maxPnl());
        // 链 5-1-5：两头 10 好过中间 1
        assertEquals(10, DeskTree.ofParents(new int[] {-1, 0, 1}, new long[] {5, 1, 5}).maxPnl());
        // 链 3-5-3：中间 5 比两头 6 差
        assertEquals(6, DeskTree.ofParents(new int[] {-1, 0, 1}, new long[] {3, 5, 3}).maxPnl());
    }

    @Test @Tag("part1")
    void siblingsMayBothBeChosen() {
        // 根 10，三个孩子各 4：全选孩子 12 > 根 10
        assertEquals(12, DeskTree.ofParents(new int[] {-1, 0, 0, 0}, new long[] {10, 4, 4, 4}).maxPnl());
        assertEquals(13, DeskTree.ofParents(new int[] {-1, 0, 0, 0}, new long[] {13, 4, 4, 4}).maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void parentIndexMayBeLargerThanChildIndex() {
        // 根是 2；0、1 是它的孩子
        assertEquals(11, DeskTree.ofParents(new int[] {2, 2, -1}, new long[] {5, 6, 1}).maxPnl());
        // 根是 3 的反向链：3 → 2 → 1 → 0
        assertEquals(8, DeskTree.ofParents(new int[] {1, 2, 3, -1}, new long[] {4, 1, 4, 1}).maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void rootIsNotAlwaysTheFirstDesk() {
        var t = DeskTree.ofParents(new int[] {1, -1, 1}, new long[] {1, 1, 1});
        assertEquals(1, t.root());
        assertEquals(2, t.maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void invalidInputs() {
        assertThrows(NullPointerException.class, () -> DeskTree.ofParents(null, new long[0]));
        assertThrows(NullPointerException.class, () -> DeskTree.ofParents(new int[0], null));
        assertIae("length mismatch", () -> DeskTree.ofParents(new int[] {-1, 0}, new long[] {1}));
        assertIae("invalid pnl", () -> DeskTree.ofParents(new int[] {-1}, new long[] {BOUND + 1}));
        assertIae("invalid pnl", () -> DeskTree.ofParents(new int[] {-1}, new long[] {-BOUND - 1}));
        assertIae("invalid parent", () -> DeskTree.ofParents(new int[] {-1, 5}, new long[] {1, 1}));
        assertIae("invalid parent", () -> DeskTree.ofParents(new int[] {-1, -2}, new long[] {1, 1}));
        assertIae("invalid parent", () -> DeskTree.ofParents(new int[] {-1, 1}, new long[] {1, 1}));
        assertIae("invalid root", () -> DeskTree.ofParents(new int[] {1, 0}, new long[] {1, 1}));
        assertIae("invalid root", () -> DeskTree.ofParents(new int[] {-1, -1}, new long[] {1, 1}));
        assertIae("cycle", () -> DeskTree.ofParents(new int[] {-1, 2, 1}, new long[] {1, 1, 1}));
        assertIae("cycle", () -> DeskTree.ofParents(new int[] {-1, 2, 3, 1, 0}, new long[] {1, 1, 1, 1, 1}));
    }

    @Test @Tag("part1") @Tag("edge")
    void errorsAreCheckedInTheDocumentedOrder() {
        // 长度不等 先于 pnl 越界；pnl 越界 先于 parent 非法；parent 非法 先于 根的个数；根的个数 先于 环
        assertIae("length mismatch", () -> DeskTree.ofParents(new int[] {-1, 9}, new long[] {BOUND + 1}));
        assertIae("invalid pnl", () -> DeskTree.ofParents(new int[] {-1, 9}, new long[] {1, BOUND + 1}));
        assertIae("invalid parent", () -> DeskTree.ofParents(new int[] {-1, -1, 9}, new long[] {1, 1, 1}));
        assertIae("invalid root", () -> DeskTree.ofParents(new int[] {-1, -1, 1}, new long[] {1, 1, 1}));
        assertIae("too many desks",
                () -> DeskTree.ofParents(new int[DeskTree.MAX_DESKS + 1], new long[DeskTree.MAX_DESKS + 1]));
    }

    @Test @Tag("part1") @Tag("edge")
    void pnlBoundsAreInclusiveAndMinValueIsRejected() {
        assertEquals(BOUND, DeskTree.ofParents(new int[] {-1}, new long[] {BOUND}).maxPnl());
        assertEquals(0, DeskTree.ofParents(new int[] {-1}, new long[] {-BOUND}).maxPnl());
        // Math.abs(Long.MIN_VALUE) 仍是负数：用 abs 做检查会放过它
        assertIae("invalid pnl", () -> DeskTree.ofParents(new int[] {-1}, new long[] {Long.MIN_VALUE}));
        assertIae("invalid pnl", () -> DeskTree.ofParents(new int[] {-1}, new long[] {Long.MAX_VALUE}));
    }

    @Test @Tag("part1") @Tag("edge")
    void inputArraysAreCopied() {
        int[] parent = {-1, 0, 0};
        long[] pnl = {1, 5, 5};
        var t = DeskTree.ofParents(parent, pnl);
        pnl[1] = -100;
        parent[1] = 2;
        assertEquals(10, t.maxPnl());
        assertEquals(10, t.maxPnl());
    }

    @Test @Tag("part1") @Tag("edge")
    void noOverflowAtTheLimits() {
        // 星形：根 + 999_999 个叶子，全是上限 PnL；选全部叶子 = 999_999 × 10^12
        int n = DeskTree.MAX_DESKS;
        int[] parent = new int[n];
        parent[0] = -1;
        long[] pnl = new long[n];
        Arrays.fill(pnl, BOUND);
        var t = DeskTree.ofParents(parent, pnl);
        assertEquals(999_999L * BOUND, t.maxPnl());
        assertEquals((long) n * BOUND, t.bestSubtree().total());
        assertEquals(3 * BOUND, t.maxPathSum());
        assertEquals(2 * BOUND, t.maxDownPath());
    }

    @Test @Tag("part1")
    void matchesBruteForceOnRandomSmallTrees() {
        var rnd = new Random(1);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(13);
            int[] parent = randomParents(rnd, n, 1 + rnd.nextInt(n));
            long[] pnl = randomPnl(rnd, n, -6, 10);
            assertEquals(bruteRobber(parent, pnl), DeskTree.ofParents(parent, pnl).maxPnl(),
                    "parent=" + Arrays.toString(parent) + " pnl=" + Arrays.toString(pnl));
        }
    }

    // ================= Part 2：方案 + 边列表 =================

    @Test @Tag("part2")
    void samplePlan() {
        var plan = sample().plan();
        assertEquals(18, plan.total());
        assertEquals(List.of(0, 3, 4, 5, 6), plan.desks());
        assertEquals(new DeskTree.Plan(18, List.of(0, 3, 4, 5, 6)), plan);
    }

    @Test @Tag("part2") @Tag("edge")
    void emptyAndNegativePlans() {
        assertEquals(new DeskTree.Plan(0, List.of()), DeskTree.ofParents(new int[0], new long[0]).plan());
        assertEquals(new DeskTree.Plan(0, List.of()),
                DeskTree.ofParents(new int[] {-1, 0, 0}, new long[] {-1, -2, -3}).plan());
        assertEquals(new DeskTree.Plan(0, List.of()),
                DeskTree.ofParents(new int[] {-1, 0, 0}, new long[] {0, 0, 0}).plan());
    }

    @Test @Tag("part2") @Tag("edge")
    void tiesGoToSkippingTheDesk() {
        // 5 与 5：选根和选孩子一样好 → 不选根，选孩子
        assertEquals(new DeskTree.Plan(5, List.of(1)), DeskTree.ofParents(new int[] {-1, 0}, new long[] {5, 5}).plan());
        // 根 6，两个孩子 3+3：不选根
        assertEquals(new DeskTree.Plan(6, List.of(1, 2)),
                DeskTree.ofParents(new int[] {-1, 0, 0}, new long[] {6, 3, 3}).plan());
        // 链 3-5-3，6 对 5：选两头
        assertEquals(new DeskTree.Plan(6, List.of(0, 2)),
                DeskTree.ofParents(new int[] {-1, 0, 1}, new long[] {3, 5, 3}).plan());
        // 链 2-0-2：两头 4 比中间 0 好；链 1-5-1-5：选 1 和 3
        assertEquals(new DeskTree.Plan(10, List.of(1, 3)),
                DeskTree.ofParents(new int[] {-1, 0, 1, 2}, new long[] {1, 5, 1, 5}).plan());
    }

    @Test @Tag("part2") @Tag("edge")
    void zeroPnlDeskIsNeverChosen() {
        assertEquals(new DeskTree.Plan(4, List.of(1)), DeskTree.ofParents(new int[] {-1, 0, 1}, new long[] {0, 4, 0}).plan());
    }

    @Test @Tag("part2")
    void planIsValidAndMatchesTheTieRuleOnRandomTrees() {
        var rnd = new Random(2);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(30);
            int[] parent = randomParents(rnd, n, 1 + rnd.nextInt(n));
            long[] pnl = randomPnl(rnd, n, -3, 6);
            var tree = DeskTree.ofParents(parent, pnl);
            var plan = tree.plan();
            assertEquals(tree.maxPnl(), plan.total());
            assertEquals(modelDesks(parent, pnl), plan.desks(), "parent=" + Arrays.toString(parent) + " pnl=" + Arrays.toString(pnl));
            long sum = 0;
            for (int v : plan.desks()) {
                sum += pnl[v];
                assertTrue(parent[v] < 0 || !plan.desks().contains(parent[v]), "adjacent desks chosen");
            }
            assertEquals(plan.total(), sum);
        }
    }

    @Test @Tag("part2") @Tag("edge")
    void planIsImmutable() {
        var plan = sample().plan();
        assertThrows(UnsupportedOperationException.class, () -> plan.desks().add(1));
        var mutable = new ArrayList<>(List.of(1, 2));
        var copy = new DeskTree.Plan(3, mutable);
        mutable.clear();
        assertEquals(List.of(1, 2), copy.desks());
    }

    @Test @Tag("part2")
    void edgeListGivesTheSameTree() {
        int[][] edges = {{3, 1}, {0, 2}, {1, 0}, {4, 1}, {2, 5}, {6, 2}};
        var t = DeskTree.ofEdges(7, edges, SAMPLE_PNL, 0);
        assertEquals(0, t.root());
        assertEquals(18, t.maxPnl());
        assertEquals(sample().plan(), t.plan());
        assertEquals(sample().bestSubtree(), t.bestSubtree());
    }

    @Test @Tag("part2")
    void edgeListWithAnotherRoot() {
        // 同一棵无向树以 6 为根：6 - 2 - {0 - 1 - {3, 4}, 5}
        int[][] edges = {{0, 1}, {0, 2}, {1, 3}, {1, 4}, {2, 5}, {2, 6}};
        var t = DeskTree.ofEdges(7, edges, SAMPLE_PNL, 6);
        assertEquals(6, t.root());
        assertEquals(18, t.maxPnl());
        assertEquals(13, t.maxPathSum());
    }

    @Test @Tag("part2") @Tag("edge")
    void edgeListTrivialSizes() {
        var empty = DeskTree.ofEdges(0, new int[0][], new long[0], 0);
        assertEquals(0, empty.size());
        assertEquals(-1, empty.root());
        assertEquals(new DeskTree.Plan(0, List.of()), empty.plan());
        assertEquals(0, DeskTree.ofEdges(0, new int[0][], new long[0], 99).maxPnl());
        var one = DeskTree.ofEdges(1, new int[0][], new long[] {9}, 0);
        assertEquals(new DeskTree.Plan(9, List.of(0)), one.plan());
        var two = DeskTree.ofEdges(2, new int[][] {{1, 0}}, new long[] {5, 5}, 1);
        assertEquals(new DeskTree.Plan(5, List.of(0)), two.plan());
    }

    @Test @Tag("part2") @Tag("edge")
    void edgeListErrors() {
        long[] three = {1, 2, 3};
        assertThrows(NullPointerException.class, () -> DeskTree.ofEdges(3, null, three, 0));
        assertThrows(NullPointerException.class, () -> DeskTree.ofEdges(3, new int[0][], null, 0));
        assertIae("length mismatch", () -> DeskTree.ofEdges(2, new int[][] {{0, 1}}, three, 0));
        assertIae("length mismatch", () -> DeskTree.ofEdges(-1, new int[0][], new long[0], 0));
        assertIae("invalid pnl", () -> DeskTree.ofEdges(1, new int[0][], new long[] {BOUND + 1}, 0));
        assertIae("invalid root", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 2}}, three, 3));
        assertIae("invalid root", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 2}}, three, -1));
        assertIae("invalid edge", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 3}}, three, 0));
        assertIae("invalid edge", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 1}}, three, 0));
        assertIae("invalid edge", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1}}, three, 0));
        assertIae("invalid edge", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 2, 0}}, three, 0));
        assertIae("invalid edge", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, null}, three, 0));
        assertIae("invalid edge", () -> DeskTree.ofEdges(3, new int[][] {{0, -1}, {1, 2}}, three, 0));
        assertIae("not a tree", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}}, three, 0));
        assertIae("not a tree", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 2}, {2, 0}}, three, 0));
        assertIae("not a tree", () -> DeskTree.ofEdges(3, new int[][] {{0, 1}, {1, 0}}, three, 0));
        assertIae("not a tree", () -> DeskTree.ofEdges(4, new int[][] {{0, 1}, {1, 0}, {2, 3}}, new long[4], 0));
        assertIae("invalid edge", () -> DeskTree.ofEdges(0, new int[][] {{0, 1}}, new long[0], 0));
    }

    @Test @Tag("part2")
    void edgeListMatchesParentsOnRandomTrees() {
        var rnd = new Random(3);
        for (int round = 0; round < 200; round++) {
            int n = 1 + rnd.nextInt(40);
            int[] parent = randomParents(rnd, n, 1 + rnd.nextInt(n));
            long[] pnl = randomPnl(rnd, n, -5, 9);
            int[][] edges = edgesOf(parent);
            for (int i = edges.length - 1; i > 0; i--) {   // 乱序、随机方向
                int j = rnd.nextInt(i + 1);
                var t = edges[i]; edges[i] = edges[j]; edges[j] = t;
            }
            for (var e : edges) if (rnd.nextBoolean()) { int t = e[0]; e[0] = e[1]; e[1] = t; }
            var viaParents = DeskTree.ofParents(parent, pnl);
            var viaEdges = DeskTree.ofEdges(n, edges, pnl, viaParents.root());
            assertEquals(viaParents.plan(), viaEdges.plan());
            assertEquals(viaParents.maxPathSum(), viaEdges.maxPathSum());
            assertEquals(viaParents.bestSubtree(), viaEdges.bestSubtree());
            // 换一个根：最大独立集和最大路径和是无向树的性质，和选谁当根无关
            int other = rnd.nextInt(n);
            var rerooted = DeskTree.ofEdges(n, edges, pnl, other);
            assertEquals(other, rerooted.root());
            assertEquals(viaParents.maxPnl(), rerooted.maxPnl());
            assertEquals(viaParents.maxPathSum(), rerooted.maxPathSum());
            assertEquals(viaParents.plan().total(), rerooted.plan().total());
        }
    }

    // ================= Part 3：路径与子树 =================

    @Test @Tag("part3")
    void sampleSummaries() {
        var t = sample();
        assertEquals(11, t.maxDownPath());       // 0 → 1 → 3
        assertEquals(13, t.maxPathSum());        // 3 → 1 → 4
        assertEquals(new DeskTree.Subtree(0, 13), t.bestSubtree());   // 根 13 与 1 号 13 平局，取编号小的
    }

    @Test @Tag("part3") @Tag("edge")
    void singleDeskPaths() {
        var t = DeskTree.ofParents(new int[] {-1}, new long[] {-4});
        assertEquals(-4, t.maxDownPath());
        assertEquals(-4, t.maxPathSum());
        assertEquals(new DeskTree.Subtree(0, -4), t.bestSubtree());
    }

    @Test @Tag("part3") @Tag("edge")
    void allNegativePathIsTheLeastBadSingleDesk() {
        var t = DeskTree.ofParents(new int[] {-1, 0, 1}, new long[] {-5, -3, -8});
        assertEquals(-3, t.maxDownPath());
        assertEquals(-3, t.maxPathSum());
        assertEquals(new DeskTree.Subtree(2, -8), t.bestSubtree());
    }

    @Test @Tag("part3") @Tag("edge")
    void bendThroughANegativeDeskCanStillWin() {
        // 6 - (-1) - 7：拐弯路径 12 比任何单边都好
        var t = DeskTree.ofParents(new int[] {-1, 0, 0}, new long[] {-1, 6, 7});
        assertEquals(12, t.maxPathSum());
        assertEquals(7, t.maxDownPath());
        // 拐点太负：-10 + 6 + 7 = 3 < 单走 7
        var u = DeskTree.ofParents(new int[] {-1, 0, 0}, new long[] {-10, 6, 7});
        assertEquals(7, u.maxPathSum());
        assertEquals(7, u.maxDownPath());
    }

    @Test @Tag("part3") @Tag("edge")
    void bendUsesTheTwoBestBranchesOnly() {
        var t = DeskTree.ofParents(new int[] {-1, 0, 0, 0, 0}, new long[] {1, 5, 9, 7, -2});
        assertEquals(17, t.maxPathSum());     // 9 + 1 + 7
        assertEquals(10, t.maxDownPath());    // 1 + 9
    }

    @Test @Tag("part3") @Tag("edge")
    void bestSubtreeTieGoesToTheSmallestId() {
        var t = DeskTree.ofParents(new int[] {-1, 0, 0}, new long[] {-20, 5, 5});
        assertEquals(new DeskTree.Subtree(1, 5), t.bestSubtree());
        var u = DeskTree.ofParents(new int[] {3, 3, 3, -1}, new long[] {2, 2, 2, -6});
        assertEquals(new DeskTree.Subtree(0, 2), u.bestSubtree());
        // 根 4 带一个 0 的叶子：根的子树总和 4，叶子 0，取根
        var v = DeskTree.ofParents(new int[] {-1, 0}, new long[] {4, 0});
        assertEquals(new DeskTree.Subtree(0, 4), v.bestSubtree());
    }

    @Test @Tag("part3") @Tag("edge")
    void emptyTreeHasNoPath() {
        var t = DeskTree.ofParents(new int[0], new long[0]);
        for (Runnable r : List.<Runnable>of(t::maxDownPath, t::maxPathSum, t::bestSubtree)) {
            var e = assertThrows(NoSuchElementException.class, r::run);
            assertEquals("empty tree", e.getMessage());
        }
    }

    @Test @Tag("part3")
    void pathsAndSubtreesMatchBruteForceOnRandomSmallTrees() {
        var rnd = new Random(4);
        for (int round = 0; round < 400; round++) {
            int n = 1 + rnd.nextInt(25);
            int[] parent = randomParents(rnd, n, 1 + rnd.nextInt(n));
            long[] pnl = randomPnl(rnd, n, -9, 9);
            var t = DeskTree.ofParents(parent, pnl);
            String ctx = "parent=" + Arrays.toString(parent) + " pnl=" + Arrays.toString(pnl);
            assertEquals(bruteDown(parent, pnl), t.maxDownPath(), ctx);
            assertEquals(brutePath(parent, pnl), t.maxPathSum(), ctx);
            assertEquals(bruteSubtree(parent, pnl), t.bestSubtree(), ctx);
        }
    }

    // ================= Part 4：深度与规模 =================

    private static final int DEEP = 100_000;

    private static int[] chain(int n, boolean rootFirst) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = rootFirst ? i - 1 : (i == n - 1 ? -1 : i + 1);
        return parent;
    }

    private static long[] ones(int n) {
        long[] pnl = new long[n];
        Arrays.fill(pnl, 1);
        return pnl;
    }

    @Test @Tag("part4") @Tag("edge")
    void deepChainDoesNotNeedDeepStack() throws Throwable {
        // 链 0 → 1 → … → 99999，全是 1：选奇数编号（平局规则：根 L 为偶数个台时不选）
        onStack(SMALL_STACK, () -> {
            var t = DeskTree.ofParents(chain(DEEP, true), ones(DEEP));
            assertEquals(50_000, t.maxPnl());
            var plan = t.plan();
            assertEquals(50_000, plan.total());
            assertSameDesks(IntStream.range(0, DEEP / 2).map(i -> 2 * i + 1).boxed().toList(), plan.desks());
            assertEquals(DEEP, t.maxDownPath());
            assertEquals(DEEP, t.maxPathSum());
            assertEquals(new DeskTree.Subtree(0, DEEP), t.bestSubtree());
            return null;
        });
    }

    @Test @Tag("part4") @Tag("edge")
    void deepChainWithTheRootLast() throws Throwable {
        // 链 99999 → 99998 → … → 0，根是编号最大的台：编号顺序和层次顺序相反
        onStack(SMALL_STACK, () -> {
            var t = DeskTree.ofParents(chain(DEEP, false), ones(DEEP));
            assertEquals(DEEP - 1, t.root());
            assertEquals(50_000, t.maxPnl());
            var plan = t.plan();
            assertSameDesks(IntStream.range(0, DEEP / 2).map(i -> 2 * i).boxed().toList(), plan.desks());
            assertEquals(DEEP, t.maxPathSum());
            assertEquals(new DeskTree.Subtree(DEEP - 1, DEEP), t.bestSubtree());
            return null;
        });
    }

    @Test @Tag("part4") @Tag("edge")
    void deepChainFromAnEdgeList() throws Throwable {
        onStack(SMALL_STACK, () -> {
            int[][] edges = new int[DEEP - 1][];
            for (int i = 0; i < DEEP - 1; i++) edges[i] = new int[] {i + 1, i};
            var t = DeskTree.ofEdges(DEEP, edges, ones(DEEP), DEEP - 1);
            assertEquals(50_000, t.maxPnl());
            assertEquals(DEEP, t.maxPathSum());
            assertEquals(new DeskTree.Subtree(DEEP - 1, DEEP), t.bestSubtree());
            return null;
        });
    }

    @Test @Tag("part4") @Tag("edge")
    void deepChainWithAlternatingSigns() throws Throwable {
        // +3 -1 +3 -1 …：只选 +3 的台（互不相邻）= 150000；整条链 = 100000，去掉末尾的 -1 = 100001
        onStack(SMALL_STACK, () -> {
            long[] pnl = new long[DEEP];
            for (int i = 0; i < DEEP; i++) pnl[i] = i % 2 == 0 ? 3 : -1;
            var t = DeskTree.ofParents(chain(DEEP, true), pnl);
            assertEquals(150_000, t.maxPnl());
            assertEquals(100_001, t.maxDownPath());
            assertEquals(100_001, t.maxPathSum());
            assertEquals(new DeskTree.Subtree(0, 100_000), t.bestSubtree());
            return null;
        });
    }

    @Test @Tag("part4")
    void textbookRecursionAgreesOnSmallTrees() {
        assertEquals(18, sample().maxPnlRecursive());
        assertEquals(0, DeskTree.ofParents(new int[0], new long[0]).maxPnlRecursive());
        var rnd = new Random(5);
        for (int round = 0; round < 200; round++) {
            int n = 1 + rnd.nextInt(60);
            var t = DeskTree.ofParents(randomParents(rnd, n, 1 + rnd.nextInt(n)), randomPnl(rnd, n, -8, 12));
            assertEquals(t.maxPnl(), t.maxPnlRecursive());
        }
    }

    @Test @Tag("part4") @Tag("edge")
    void textbookRecursionOverflowsTheStackOnADeepChain() throws Throwable {
        // 同一棵 10^5 层的链：迭代版在 512 KiB 的栈上没事，递归版 StackOverflowError。
        var t = DeskTree.ofParents(chain(DEEP, true), ones(DEEP));
        assertEquals(50_000, onStack(SMALL_STACK, t::maxPnl));
        assertThrows(StackOverflowError.class, () -> onStack(SMALL_STACK, t::maxPnlRecursive));
        // 浅一点的链（100 层）递归版没问题：问题只在深度。
        var shallow = DeskTree.ofParents(chain(100, true), ones(100));
        assertEquals(50, onStack(SMALL_STACK, shallow::maxPnlRecursive));
    }

    @Test @Tag("part4") @Tag("edge")
    void veryWideTree() {
        int n = DEEP;
        int[] parent = new int[n];
        parent[0] = -1;
        long[] pnl = new long[n];
        pnl[0] = 150_000;
        for (int i = 1; i < n; i++) pnl[i] = 2;
        var t = DeskTree.ofParents(parent, pnl);
        assertEquals(2L * (n - 1), t.maxPnl());           // 199_998 > 150_000
        assertEquals(150_000 + 4, t.maxPathSum());        // 2 + 150000 + 2
        assertEquals(150_000 + 2, t.maxDownPath());
        assertEquals(new DeskTree.Subtree(0, 150_000 + 2L * (n - 1)), t.bestSubtree());
        var plan = t.plan();
        assertEquals(2L * (n - 1), plan.total());
        assertSameDesks(IntStream.range(1, n).boxed().toList(), plan.desks());
    }

    @Test @Tag("part4") @Tag("perf")
    void millionDesksUnderTwoSeconds() {
        var rnd = new Random(6);
        int n = 1_000_000;
        int[] parent = randomParents(rnd, n, 4);   // reach 小 → 很深的随机树
        long[] pnl = randomPnl(rnd, n, -1000, 1000);
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            var t = DeskTree.ofParents(parent, pnl);
            long a = t.maxPnl();
            var plan = t.plan();
            assertEquals(a, plan.total());
            assertTrue(t.maxPathSum() >= t.maxDownPath());
            assertDoesNotThrow(t::bestSubtree);
        });
    }

    @Test @Tag("part4") @Tag("perf")
    void millionDeskChainOnASmallStack() {
        int n = 1_000_000;
        assertTimeoutPreemptively(Duration.ofSeconds(2), () -> {
            long total = onStack(SMALL_STACK, () -> {
                var t = DeskTree.ofParents(chain(n, true), ones(n));
                assertEquals(500_000, t.plan().total());
                assertEquals(n, t.maxPathSum());
                return t.maxPnl();
            });
            assertEquals(500_000, total);
        });
    }

    @Test @Tag("part4") @Tag("edge")
    void differentTreesDifferentAnswers() {
        // 防止实现把结果缓存在静态字段里：连着建两棵不同的树
        var a = DeskTree.ofParents(new int[] {-1, 0}, new long[] {5, 1});
        var b = DeskTree.ofParents(new int[] {-1, 0}, new long[] {1, 5});
        assertEquals(5, a.maxPnl());
        assertEquals(5, b.maxPnl());
        assertNotEquals(a.plan(), b.plan());
    }
}
