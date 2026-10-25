import java.util.Arrays;
import java.util.NoSuchElementException;

/**
 * hc15 Part 3b：顺序统计结构（order-statistics structure）：任意 p 的百分位，p 在查询时才给。
 * 实现：树堆（treap）——按值有序的二叉搜索树 + 随机优先级的堆，期望高度 O(log n)。相同的值合并成一个结点（cnt），
 * 每个结点记子树里的元素总数 total，所以「第 r 小」是一次从根往下的二分。数组存结点（下标 0 = 空），不为每个元素 new 对象。
 */
public final class OrderStatistics {
    private long[] key = new long[16];
    private int[] cnt = new int[16], left = new int[16], right = new int[16], total = new int[16], prio = new int[16];
    private int nodes; // 已用结点数；下标从 1 开始
    private int root;
    private int seed = 0x2545F491;

    /**
     * 最近秩法（nearest-rank）：n 个数里 p% 分位是第 ceil(p × n / 100) 小的那个。
     * 要求 n ≥ 0 且 1 ≤ p ≤ 100，否则 IAE。n 很大时也不能溢出（不要先算 p × n）。
     */
    public static long rank(long n, int p) {
        if (n < 0) throw new IllegalArgumentException("n must be >= 0: " + n);
        if (p < 1 || p > 100) throw new IllegalArgumentException("p must be in 1..100: " + p);
        return n / 100 * p + ((n % 100) * p + 99) / 100;
    }

    /** O(log n) 期望。 */
    public void add(long price) {
        root = insert(root, price);
    }

    private int nextPriority() { // xorshift32，确定性
        seed ^= seed << 13;
        seed ^= seed >>> 17;
        seed ^= seed << 5;
        return seed;
    }

    private int newNode(long x) {
        if (++nodes == key.length) {
            int cap = key.length * 2;
            key = Arrays.copyOf(key, cap);
            cnt = Arrays.copyOf(cnt, cap);
            left = Arrays.copyOf(left, cap);
            right = Arrays.copyOf(right, cap);
            total = Arrays.copyOf(total, cap);
            prio = Arrays.copyOf(prio, cap);
        }
        key[nodes] = x;
        cnt[nodes] = total[nodes] = 1;
        prio[nodes] = nextPriority();
        return nodes;
    }

    private void pull(int t) {
        total[t] = cnt[t] + total[left[t]] + total[right[t]];
    }

    private int insert(int t, long x) {
        if (t == 0) return newNode(x);
        if (x == key[t]) {
            cnt[t]++;
        } else if (x < key[t]) {
            int c = insert(left[t], x); // 先算再存：insert 里可能换掉 left 数组（扩容），不能让旧数组引用先被求值
            left[t] = c;
            if (prio[left[t]] > prio[t]) { // 右旋
                int l = left[t];
                left[t] = right[l];
                right[l] = t;
                pull(t);
                pull(l);
                return l;
            }
        } else {
            int c = insert(right[t], x);
            right[t] = c;
            if (prio[right[t]] > prio[t]) { // 左旋
                int r = right[t];
                right[t] = left[r];
                left[r] = t;
                pull(t);
                pull(r);
                return r;
            }
        }
        pull(t);
        return t;
    }

    public int size() {
        return total[root];
    }

    /** 第 rank 小（1 起，重复的值各算一个）。rank 不在 1..size() → IAE。 */
    public long kth(long rank) {
        if (rank < 1 || rank > size()) throw new IllegalArgumentException("rank out of range: " + rank + " (size " + size() + ")");
        int t = root;
        long r = rank;
        while (true) {
            long l = total[left[t]];
            if (r <= l) t = left[t];
            else if (r <= l + cnt[t]) return key[t];
            else {
                r -= l + cnt[t];
                t = right[t];
            }
        }
    }

    /** 最近秩百分位。p 不在 1..100 → IAE（先检查）；没有数据 → NoSuchElementException。 */
    public long percentile(int p) {
        long r = rank(size(), p);
        if (size() == 0) throw new NoSuchElementException("no prices yet");
        return kth(r);
    }

    /** 小于等于 price 的元素个数。 */
    public long countAtMost(long price) {
        long c = 0;
        int t = root;
        while (t != 0) {
            if (price < key[t]) t = left[t];
            else {
                c += total[left[t]] + cnt[t];
                t = right[t];
            }
        }
        return c;
    }
}
