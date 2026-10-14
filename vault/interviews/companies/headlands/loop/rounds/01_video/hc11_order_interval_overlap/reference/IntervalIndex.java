import java.util.Arrays;
import java.util.Objects;

/**
 * hc11 Part 4：坐标很大（比如纳秒时间戳，高达 10^18）时的区间计数索引 = 坐标压缩 + 懒标记线段树。
 *
 * <p><b>坐标压缩（coordinate compression）</b>：活跃数只会在区间的端点处变化，所以只有「出现过的端点」重要。
 * 把端点排序去重成 c[0] < c[1] < … < c[m-1]，相邻两个端点之间的 [c[j], c[j+1]) 叫一个<b>基本段</b>（elementary segment），
 * 每个基本段内活跃数是常数。区间 [s, e) 恰好覆盖基本段 idx(s) .. idx(e)-1，其中 idx 是端点在 c 里的下标（二分查找）。
 * 于是一个值域 10^18 的问题变成了只有 m-1 ≤ 2n 个格子的问题。
 *
 * <p><b>线段树（segment tree）</b>支持「区间加 delta」和「区间求最大值」，都是 O(log m)。
 * 这里用<b>不下推的懒标记</b>（标记永久化）：每个结点记两个数——{@code add[node]}：整段还欠着的加数；
 * {@code mx[node]}：这段里的最大值（已经含 add[node] 和子树里所有的加数，但不含祖先的 add）。
 * 查询时一路把经过的结点的 add 累加上去，不需要把标记往下推。
 *
 * <p>计数用 int：同时活着的订单数不会超过 int（订单数本身受数组大小限制）。remove 只能撤销之前 add 过的区间。
 */
public final class IntervalIndex {
    private final long[] coords; // 排好序、去重后的端点
    private final int segs;      // 基本段个数 = coords.length - 1（至少 0）
    private final int size;      // 叶子数：>= segs 的最小 2 的幂
    private final int[] mx;
    private final int[] add;

    /** 端点集合（任意顺序、可重复）。之后 add / remove 的区间两端都必须在这个集合里。 */
    public IntervalIndex(long[] coordinates) {
        Objects.requireNonNull(coordinates, "coordinates");
        var sorted = coordinates.clone();
        Arrays.sort(sorted);
        int m = 0;
        for (int i = 0; i < sorted.length; i++) {
            if (i == 0 || sorted[i] != sorted[i - 1]) sorted[m++] = sorted[i];
        }
        this.coords = Arrays.copyOf(sorted, m);
        this.segs = Math.max(0, m - 1);
        int sz = 1;
        while (sz < Math.max(1, segs)) sz <<= 1;
        this.size = sz;
        this.mx = new int[2 * sz];
        this.add = new int[2 * sz];
    }

    /** 从一批区间建索引：把所有端点收集起来压缩，再逐个 add。 */
    public static IntervalIndex of(long[][] intervals) {
        var pts = new long[intervals.length * 2];
        for (int i = 0; i < intervals.length; i++) {
            if (intervals[i].length != 2) throw new IllegalArgumentException("interval must have 2 elements");
            pts[2 * i] = intervals[i][0];
            pts[2 * i + 1] = intervals[i][1];
        }
        var idx = new IntervalIndex(pts);
        for (long[] iv : intervals) idx.add(iv[0], iv[1]);
        return idx;
    }

    /** 用「压缩 + 线段树」算 Part 1 的答案；必须与扫描线版本一致（用于对拍）。 */
    public static int maxOverlap(long[][] intervals) {
        return of(intervals).max();
    }

    // ---------------------------------------------------------------- 更新

    /** 加入区间 [start, end)：两端都必须是已知端点，start <= end；start == end 什么都不做。 */
    public void add(long start, long end) {
        update(start, end, 1);
    }

    /** 撤销一个之前加入过的区间（调用方保证）。 */
    public void remove(long start, long end) {
        update(start, end, -1);
    }

    private void update(long start, long end, int delta) {
        if (end < start) throw new IllegalArgumentException("end < start: " + end + " < " + start);
        int lo = exactIndex(start);
        int hi = exactIndex(end);
        if (lo == hi) return; // 空区间
        rangeAdd(1, 0, size - 1, lo, hi - 1, delta);
    }

    private void rangeAdd(int node, int nl, int nr, int l, int r, int delta) {
        if (l <= nl && nr <= r) { // 整段被覆盖：只记在这个结点上，不往下推
            add[node] += delta;
            mx[node] += delta;
            return;
        }
        int mid = (nl + nr) >>> 1;
        if (l <= mid) rangeAdd(2 * node, nl, mid, l, r, delta);
        if (r > mid) rangeAdd(2 * node + 1, mid + 1, nr, l, r, delta);
        mx[node] = add[node] + Math.max(mx[2 * node], mx[2 * node + 1]);
    }

    // ---------------------------------------------------------------- 查询

    /** 全局最大重叠数。 */
    public int max() {
        return segs == 0 ? 0 : mx[1];
    }

    /** t 时刻活着几个（t 落在所有端点之外是 0）。 */
    public int liveAt(long t) {
        int j = floorIndex(t);
        if (j < 0 || j >= segs) return 0;
        return rangeMax(1, 0, size - 1, j, j);
    }

    /** 区间 [from, to) 内任意时刻的最大活跃数。to < from → IAE；to == from（空范围）→ 0。 */
    public int maxIn(long from, long to) {
        if (to < from) throw new IllegalArgumentException("to < from: " + to + " < " + from);
        if (to == from || segs == 0) return 0;
        int lo = Math.max(0, floorIndex(from)); // from 所在的基本段（from 在最左端点之前就从第 0 段开始）
        int hi = Math.min(segs - 1, lowerBound(to) - 1); // 最后一个起点 < to 的基本段
        if (lo > hi) return 0;
        return Math.max(0, rangeMax(1, 0, size - 1, lo, hi)); // 范围伸出端点之外的部分活跃数是 0
    }

    private int rangeMax(int node, int nl, int nr, int l, int r) {
        if (l <= nl && nr <= r) return mx[node];
        int mid = (nl + nr) >>> 1;
        int best = Integer.MIN_VALUE;
        if (l <= mid) best = Math.max(best, rangeMax(2 * node, nl, mid, l, r));
        if (r > mid) best = Math.max(best, rangeMax(2 * node + 1, mid + 1, nr, l, r));
        return best + add[node]; // 本结点还欠着的加数对整段都生效，没往下推，所以在这里补上
    }

    public int coordinateCount() {
        return coords.length;
    }

    public int segmentCount() {
        return segs;
    }

    // ---------------------------------------------------------------- 二分查找（只用比较，不做减法 → 不会溢出）

    /** x 必须是已知端点，返回它的下标。 */
    private int exactIndex(long x) {
        int i = Arrays.binarySearch(coords, x);
        if (i < 0) throw new IllegalArgumentException("unknown coordinate: " + x);
        return i;
    }

    /** 最大的 j 使 coords[j] <= x；x 比所有端点都小返回 -1。 */
    private int floorIndex(long x) {
        int i = Arrays.binarySearch(coords, x);
        return i >= 0 ? i : -i - 2;
    }

    /** 最小的 j 使 coords[j] >= x；都比 x 小返回 coords.length。 */
    private int lowerBound(long x) {
        int i = Arrays.binarySearch(coords, x);
        return i >= 0 ? i : -i - 1;
    }
}
