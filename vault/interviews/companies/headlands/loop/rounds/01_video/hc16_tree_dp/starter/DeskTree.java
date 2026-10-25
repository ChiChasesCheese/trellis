import java.util.List;

/**
 * 交易台层级树（hc16）。台编号 0..n-1，每个台有一个整数 PnL（可为负）。
 * 提示：建树时做一次 BFS 得到「父亲在孩子前面」的顺序，之后所有查询按这个顺序的逆序做 DP，不要递归（Part 4）。
 * parent 里的下标不保证小于 i，所以不能直接从 n-1 倒着扫。
 */
public final class DeskTree {
    /** |pnl| 上限：保证任何和都 ≤ 10^18，不会溢出 long。 */
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

    private DeskTree() {}

    /**
     * parent[i] = i 的上级台，-1 表示根；n = 0 是合法的空树。parent / pnl 为 null → NPE。
     * 检查顺序：长度不等 "length mismatch" → n &gt; MAX_DESKS "too many desks" → 某个 |pnl| &gt; MAX_ABS_PNL "invalid pnl" →
     * 某个 parent 越界或等于自己 "invalid parent" → 根的个数 ≠ 1（n &gt; 0）"invalid root" → 根到不了所有台（有环）"cycle"。
     * 全是 IllegalArgumentException。入参数组要拷贝（之后改入参不影响树）。
     */
    public static DeskTree ofParents(int[] parent, long[] pnl) { throw new UnsupportedOperationException("TODO"); }

    /**
     * edges[i] = {a, b}：无向边；以 root 为根定向（Part 2）。edges / pnl 为 null → NPE；n = 0 时 root 被忽略。
     * 检查顺序：pnl.length ≠ n（或 n &lt; 0）"length mismatch" → "too many desks" → "invalid pnl" → n &gt; 0 且 root 越界 "invalid root" →
     * 某条边不是两个端点 / 端点越界 / 自环 "invalid edge" → 边数 ≠ max(0, n-1) 或从 root 到不了所有台 "not a tree"。
     */
    public static DeskTree ofEdges(int n, int[][] edges, long[] pnl, int root) { throw new UnsupportedOperationException("TODO"); }

    public int size() { throw new UnsupportedOperationException("TODO"); }

    /** 根台的编号；空树返回 -1。 */
    public int root() { throw new UnsupportedOperationException("TODO"); }

    // ---------------- Part 1 ----------------

    /** 选一些台，任何一个台和它的直接上级不同时被选，最大总 PnL。什么都不选也允许（空树和全负的树答案是 0）。 */
    public long maxPnl() { throw new UnsupportedOperationException("TODO"); }

    // ---------------- Part 2 ----------------

    /**
     * 同 maxPnl，并返回选了哪些台。平局规则：v 被选当且仅当它的上级没被选，且「v 被选时子树最大总 PnL」严格大于「v 不被选时」；
     * 相等就不选。desks 升序。
     */
    public Plan plan() { throw new UnsupportedOperationException("TODO"); }

    // ---------------- Part 3（空树都抛 NoSuchElementException("empty tree")）----------------

    /** 从某个台出发一路往下（每步到一个孩子）的非空路径的最大 PnL 和。 */
    public long maxDownPath() { throw new UnsupportedOperationException("TODO"); }

    /** 树中任意一条非空简单路径（可以先上后下，在某个台拐弯）的最大 PnL 和。 */
    public long maxPathSum() { throw new UnsupportedOperationException("TODO"); }

    /** 子树总 PnL 最大的那个台；平局取编号最小的。 */
    public Subtree bestSubtree() { throw new UnsupportedOperationException("TODO"); }

    // ---------------- Part 4 ----------------

    /** 教科书递归版（和 maxPnl 同答案）；够深的链上会 StackOverflowError。其余所有方法必须在 10^5 层的链上不爆栈。 */
    public long maxPnlRecursive() { throw new UnsupportedOperationException("TODO"); }
}
