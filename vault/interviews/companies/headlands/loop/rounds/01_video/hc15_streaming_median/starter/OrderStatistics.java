/**
 * hc15 Part 3b（starter）：顺序统计结构：任意 p 的百分位，p 在查询时才给。
 *
 * <p>提示：按值有序的平衡二叉搜索树，每个结点多存「子树里的元素总数」，第 r 小就是一次从根往下的二分。
 * Java 标准库没有这个结构（TreeMap 不能按名次取）；面试里可以自己写树堆（treap，随机优先级的 BST，期望高度 O(log n)），
 * 相同的值合并成一个带计数的结点，用数组存结点。（坑：数组扩容后，`left[t] = insert(left[t], x)` 会把结果写进扩容前的旧数组——先把返回值存进局部变量。）
 */
public final class OrderStatistics {
    // 在这里加你的字段

    /**
     * 最近秩法（nearest-rank）：n 个数里 p% 分位是第 ceil(p × n / 100) 小的那个。n ≥ 0 且 1 ≤ p ≤ 100，否则 IAE。
     * 已给出（n 很大时也不溢出：先拆开 n / 100 和 n % 100，不要先算 p × n）。
     */
    public static long rank(long n, int p) {
        if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
        if (p < 1 || p > 100) throw new IllegalArgumentException("p must be in 1..100: " + p);
        return n / 100 * p + ((n % 100) * p + 99) / 100;
    }

    /** 期望 O(log n)。 */
    public void add(long price) {
        throw new UnsupportedOperationException("TODO");
    }

    public int size() {
        throw new UnsupportedOperationException("TODO");
    }

    /** 第 rank 小（1 起，重复的值各算一个）。rank 不在 1..size() → IAE。 */
    public long kth(long rank) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 最近秩百分位。p 不在 1..100 → IAE（先检查）；没有数据 → NoSuchElementException。 */
    public long percentile(int p) {
        throw new UnsupportedOperationException("TODO");
    }

    /** 小于等于 price 的元素个数。 */
    public long countAtMost(long price) {
        throw new UnsupportedOperationException("TODO");
    }
}
