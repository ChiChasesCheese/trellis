import java.util.Arrays;

/**
 * Part 3：最小完美哈希 (minimal perfect hash)。
 *
 * 场景：开盘前就知道今天会出现的全部代码（比如 8000 个），盘中只会查这些代码。
 * 既然 key 集合固定，我们可以花一点启动时间「找一个对这批 key 完全没有冲突的哈希函数」：
 *   完美 (perfect)：任意两个 key 的结果不同（零冲突，所以查询是确定的 O(1)，没有探测循环）
 *   最小 (minimal)：n 个 key 恰好映射到 0..n-1，value 可以放进一个长度正好 n 的紧凑数组
 *
 * 算法：hash-and-displace（CHD 的简化版）
 *   1. 把 key 按 bucket(h) 分到 r ≈ n/4 个桶里（每桶平均 4 个 key）
 *   2. 按桶大小从大到小处理：对一个桶，找一个「位移」d，使得桶里每个 key 的 slot(h, d) 都落在没被占用、且互不相同的格子里
 *   3. 只有 1 个 key 的桶最后处理，直接给它下一个空格子，位移里存 ~slot（负数表示「直接指定」）
 *   查询：h = hash(key); d = disp[bucket(h)]; slot = d<0 ? ~d : slot(h,d); 然后校验 keys[slot] == key
 *   （校验必须有：完美哈希只保证「集合内的 key」不冲突；集合外的 key 也会被映射到某个格子，必须靠比较识别出来。）
 */
public final class SymbolIndex {
    private static final int MAX_SEEDS = 64;
    private static final int MAX_DISPLACEMENT = 1 << 22;
    private static final long WEYL = 0x9E3779B9L;  // 32 位黄金比例奇数：d*WEYL 在 2^32 上均匀撒点

    private final long[] keys;   // keys[slot] = 分到这个格子的 key
    private final int[] disp;    // 每个桶的位移
    private final int seed;
    private final int n;

    private SymbolIndex(long[] keys, int[] disp, int seed) {
        this.keys = keys;
        this.disp = disp;
        this.seed = seed;
        this.n = keys.length;
    }

    /** universe：全部 key（必须 > 0 且互不相同）。 */
    public static SymbolIndex build(long[] universe) {
        for (long k : universe) if (k <= 0) throw new IllegalArgumentException("key must be > 0: " + k);
        long[] sorted = universe.clone();
        Arrays.sort(sorted);
        for (int i = 1; i < sorted.length; i++)
            if (sorted[i] == sorted[i - 1]) throw new IllegalArgumentException("duplicate key: " + sorted[i]);
        if (sorted.length == 0) return new SymbolIndex(new long[0], new int[0], 0);
        for (int seed = 0; seed < MAX_SEEDS; seed++) {
            SymbolIndex built = tryBuild(universe, seed);
            if (built != null) return built;
        }
        throw new IllegalStateException("no perfect hash found in " + MAX_SEEDS + " seeds");
    }

    // splitmix64 的终结函数：双射、雪崩性好。key 稍有不同（比如只差一个字母）输出就完全不同。
    private static long mix(long z) {
        z = (z ^ (z >>> 30)) * 0xBF58476D1CE4E5B9L;
        z = (z ^ (z >>> 27)) * 0x94D049BB133111EBL;
        return z ^ (z >>> 31);
    }

    private static long hash(long key, int seed) { return mix(key ^ (seed * 0x9E3779B97F4A7C15L)); }

    /** 乘法移位把 32 位无符号数缩到 [0, range)，不用除法（Lemire 的 fastrange）。 */
    private static int bucket(long h, int r) { return (int) (((h >>> 32) * r) >>> 32); }

    private static int slot(long h, int d, int m) {
        long x = ((h & 0xFFFFFFFFL) + d * WEYL) & 0xFFFFFFFFL;
        return (int) ((x * m) >>> 32);
    }

    private static SymbolIndex tryBuild(long[] universe, int seed) {
        int n = universe.length;
        int r = Math.max(1, (n + 3) / 4);
        long[] h = new long[n];
        int[] count = new int[r + 1];
        for (int i = 0; i < n; i++) {
            h[i] = hash(universe[i], seed);
            count[bucket(h[i], r) + 1]++;
        }
        // 计数排序：start[b]..start[b+1] 是桶 b 的成员在 members[] 里的区间
        int[] start = new int[r + 1];
        for (int b = 0; b < r; b++) start[b + 1] = start[b] + count[b + 1];
        int[] fill = Arrays.copyOf(start, r);
        int[] members = new int[n];
        for (int i = 0; i < n; i++) members[fill[bucket(h[i], r)]++] = i;
        // 桶按大小从大到小处理：大桶最难放，趁表还空的时候先放
        long[] order = new long[r];
        for (int b = 0; b < r; b++) order[b] = ((long) (start[b + 1] - start[b]) << 32) | b;
        Arrays.sort(order);

        long[] slotKeys = new long[n];
        boolean[] used = new boolean[n];
        int[] disp = new int[r];
        int[] tmp = new int[n];
        int cursor = 0;                              // 单元素桶用：下一个可能空着的格子
        for (int idx = r - 1; idx >= 0; idx--) {
            int b = (int) (order[idx] & 0xFFFFFFFFL);
            int from = start[b], to = start[b + 1], size = to - from;
            if (size == 0) continue;
            if (size == 1) {
                while (used[cursor]) cursor++;
                used[cursor] = true;
                slotKeys[cursor] = universe[members[from]];
                disp[b] = ~cursor;
                continue;
            }
            boolean placed = false;
            for (int d = 0; d < MAX_DISPLACEMENT && !placed; d++) {
                int ok = 0;
                for (int p = from; p < to; p++) {
                    int s = slot(h[members[p]], d, n);
                    if (used[s]) break;
                    used[s] = true;                   // 先占着，这样桶内两个 key 撞同一格也能发现
                    tmp[ok++] = s;
                }
                if (ok == size) {
                    for (int p = 0; p < size; p++) slotKeys[tmp[p]] = universe[members[from + p]];
                    disp[b] = d;
                    placed = true;
                } else {
                    for (int p = 0; p < ok; p++) used[tmp[p]] = false; // 回滚，换下一个 d
                }
            }
            if (!placed) return null;                 // 这个 seed 不行，换种子重来
        }
        return new SymbolIndex(slotKeys, disp, seed);
    }

    public int size() { return n; }

    /** key 在 0..size()-1 里的编号；不在集合里返回 -1。 */
    public int indexOf(long key) {
        if (n == 0) return -1;
        long h = hash(key, seed);
        int d = disp[bucket(h, disp.length)];
        int s = d < 0 ? ~d : slot(h, d, n);
        return keys[s] == key ? s : -1;
    }

    /** indexOf 的反函数。 */
    public long keyAt(int index) { return keys[index]; }
}
