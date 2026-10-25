import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.stream.IntStream;

/**
 * 交易台层级树（hc16）。台（desk）编号 0..n-1，每个台有一个整数 PnL（tick 的整数倍，可为负）。
 * 参考实现：建树时一次 BFS 得到「自顶向下」的顺序，所有查询按这个顺序的逆序（孩子先于父亲）做 DP，全程无递归，
 * 栈深 O(1)；唯一的递归版本 {@link #maxPnlRecursive()} 只用来演示 10^5 层链会栈溢出。
 */
public final class DeskTree {
    /** |pnl| 上限：保证任何子树和 / 路径和 / 选择和 ≤ 10^6 × 10^12 = 10^18 < Long.MAX_VALUE，因此所有查询不会溢出。 */
    public static final long MAX_ABS_PNL = 1_000_000_000_000L;
    public static final int MAX_DESKS = 1_000_000;

    /** 一个选择方案：total = 所选台的 PnL 之和；desks 升序。 */
    public record Plan(long total, List<Integer> desks) {
        public Plan {
            desks = List.copyOf(desks);
        }
    }

    /** 子树汇总：以 root 为根的子树的 PnL 总和。 */
    public record Subtree(int root, long total) {}

    private final int n;
    private final int root;          // 空树为 -1
    private final long[] pnl;
    private final int[] parent;
    private final int[] order;       // BFS 顺序：父亲一定在孩子前面
    private final int[] childStart;  // CSR：v 的孩子是 childList[childStart[v] .. childStart[v+1])
    private final int[] childList;

    private DeskTree(int[] parent, long[] pnl, int root) {
        this.n = parent.length;
        this.parent = parent;
        this.pnl = pnl;
        this.root = root;
        this.childStart = new int[n + 1];
        for (int v = 0; v < n; v++) {
            if (parent[v] >= 0) childStart[parent[v] + 1]++;
        }
        for (int v = 0; v < n; v++) childStart[v + 1] += childStart[v];
        this.childList = new int[Math.max(0, n - 1)];
        var fill = Arrays.copyOf(childStart, n);
        for (int v = 0; v < n; v++) {
            if (parent[v] >= 0) childList[fill[parent[v]]++] = v;
        }
        this.order = new int[n];
        if (n > 0) {
            int head = 0, tail = 0;
            order[tail++] = root;
            while (head < tail) {
                int v = order[head++];
                for (int i = childStart[v]; i < childStart[v + 1]; i++) order[tail++] = childList[i];
            }
            if (tail != n) throw new IllegalArgumentException("cycle");
        }
    }

    private static void checkPnl(int n, long[] pnl) {
        if (n > MAX_DESKS) throw new IllegalArgumentException("too many desks");
        for (long p : pnl) {
            if (p > MAX_ABS_PNL || p < -MAX_ABS_PNL) throw new IllegalArgumentException("invalid pnl");
        }
    }

    /** parent[i] = i 的上级台，-1 表示根；n = 0 是合法的空树。parent 里的下标不要求小于 i。 */
    public static DeskTree ofParents(int[] parent, long[] pnl) {
        Objects.requireNonNull(parent);
        Objects.requireNonNull(pnl);
        int n = parent.length;
        if (pnl.length != n) throw new IllegalArgumentException("length mismatch");
        checkPnl(n, pnl);
        int root = -1, roots = 0;
        for (int i = 0; i < n; i++) {
            int p = parent[i];
            if (p == -1) {
                roots++;
                root = i;
            } else if (p < 0 || p >= n || p == i) {
                throw new IllegalArgumentException("invalid parent");
            }
        }
        if (n > 0 && roots != 1) throw new IllegalArgumentException("invalid root");
        return new DeskTree(parent.clone(), pnl.clone(), root);
    }

    /** edges[i] = {a, b}：无向边；以 root 为根定向。n = 0 时 root 被忽略。 */
    public static DeskTree ofEdges(int n, int[][] edges, long[] pnl, int root) {
        Objects.requireNonNull(edges);
        Objects.requireNonNull(pnl);
        if (n < 0 || pnl.length != n) throw new IllegalArgumentException("length mismatch");
        checkPnl(n, pnl);
        if (n > 0 && (root < 0 || root >= n)) throw new IllegalArgumentException("invalid root");
        for (var e : edges) {
            if (e == null || e.length != 2 || e[0] < 0 || e[0] >= n || e[1] < 0 || e[1] >= n || e[0] == e[1]) {
                throw new IllegalArgumentException("invalid edge");
            }
        }
        if (edges.length != Math.max(0, n - 1)) throw new IllegalArgumentException("not a tree");
        if (n == 0) return new DeskTree(new int[0], pnl.clone(), -1);
        int[] start = new int[n + 1];
        for (var e : edges) {
            start[e[0] + 1]++;
            start[e[1] + 1]++;
        }
        for (int v = 0; v < n; v++) start[v + 1] += start[v];
        int[] adj = new int[2 * edges.length];
        int[] fill = Arrays.copyOf(start, n);
        for (var e : edges) {
            adj[fill[e[0]]++] = e[1];
            adj[fill[e[1]]++] = e[0];
        }
        int[] parent = new int[n];
        Arrays.fill(parent, -2);
        parent[root] = -1;
        int[] queue = new int[n];
        int head = 0, tail = 0;
        queue[tail++] = root;
        while (head < tail) {
            int v = queue[head++];
            for (int i = start[v]; i < start[v + 1]; i++) {
                int w = adj[i];
                if (parent[w] == -2) {
                    parent[w] = v;
                    queue[tail++] = w;
                }
            }
        }
        if (tail != n) throw new IllegalArgumentException("not a tree");
        return new DeskTree(parent, pnl.clone(), root);
    }

    public int size() { return n; }

    /** 根台的编号；空树返回 -1。 */
    public int root() { return root; }

    // ---------------- Part 1 ----------------

    /** 选一些台，任何一个台和它的直接上级不同时被选，最大总 PnL。什么都不选也允许（空树和全负的树答案是 0）。 */
    public long maxPnl() {
        long[] in = new long[n];
        long[] out = new long[n];
        return solveRobber(in, out);
    }

    /** in[v] / out[v]：v 的子树里，v 被选 / 不被选时的最大总 PnL；返回根的 max(in, out)，空树 0。 */
    private long solveRobber(long[] in, long[] out) {
        for (int v = 0; v < n; v++) in[v] = pnl[v];
        for (int i = n - 1; i >= 0; i--) {
            int v = order[i];
            int p = parent[v];
            if (p >= 0) {
                in[p] += out[v];
                out[p] += Math.max(in[v], out[v]);
            }
        }
        return n == 0 ? 0 : Math.max(in[root], out[root]);
    }

    // ---------------- Part 2 ----------------

    /**
     * 同 maxPnl，并返回选了哪些台。平局规则：v 被选当且仅当它的上级没被选，且 in[v] &gt; out[v]（严格更好）；
     * 相等就不选。desks 升序。
     */
    public Plan plan() {
        long[] in = new long[n];
        long[] out = new long[n];
        long total = solveRobber(in, out);
        boolean[] chosen = new boolean[n];
        for (int v : order) {
            int p = parent[v];
            chosen[v] = (p < 0 || !chosen[p]) && in[v] > out[v];
        }
        var desks = IntStream.range(0, n).filter(v -> chosen[v]).boxed().toList();
        return new Plan(total, desks);
    }

    // ---------------- Part 3 ----------------

    private void requireNonEmpty() {
        if (n == 0) throw new NoSuchElementException("empty tree");
    }

    /** 从某个台出发一路往下（每步到一个孩子）的非空路径的最大 PnL 和。 */
    public long maxDownPath() {
        requireNonEmpty();
        return paths()[0];
    }

    /** 树中任意一条非空简单路径（可以先上后下，在某个台拐弯）的最大 PnL 和。 */
    public long maxPathSum() {
        requireNonEmpty();
        return paths()[1];
    }

    /** {最大向下路径, 最大任意路径}。top1 / top2：孩子向下路径里最好的两条，负的当作 0（不要）。 */
    private long[] paths() {
        long[] top1 = new long[n];
        long[] top2 = new long[n];
        long bestDown = Long.MIN_VALUE, bestPath = Long.MIN_VALUE;
        for (int i = n - 1; i >= 0; i--) {
            int v = order[i];
            long down = pnl[v] + top1[v];
            bestDown = Math.max(bestDown, down);
            bestPath = Math.max(bestPath, pnl[v] + top1[v] + top2[v]);
            int p = parent[v];
            if (p >= 0 && down > 0) {
                if (down > top1[p]) {
                    top2[p] = top1[p];
                    top1[p] = down;
                } else if (down > top2[p]) {
                    top2[p] = down;
                }
            }
        }
        return new long[] {bestDown, bestPath};
    }

    /** 子树总 PnL 最大的那个台；平局取编号最小的。 */
    public Subtree bestSubtree() {
        requireNonEmpty();
        long[] sum = pnl.clone();
        for (int i = n - 1; i > 0; i--) {
            int v = order[i];
            sum[parent[v]] += sum[v];
        }
        int best = 0;
        for (int v = 1; v < n; v++) {
            if (sum[v] > sum[best]) best = v;
        }
        return new Subtree(best, sum[best]);
    }

    // ---------------- Part 4 ----------------

    /** 教科书递归版（和 maxPnl 同答案）；够深的链上会 StackOverflowError。只用来演示为什么要迭代。 */
    public long maxPnlRecursive() {
        if (n == 0) return 0;
        long[] r = solveRecursive(root);
        return Math.max(r[0], r[1]);
    }

    private long[] solveRecursive(int v) {
        long take = pnl[v], skip = 0;
        for (int i = childStart[v]; i < childStart[v + 1]; i++) {
            long[] c = solveRecursive(childList[i]);
            take += c[1];
            skip += Math.max(c[0], c[1]);
        }
        return new long[] {take, skip};
    }
}
