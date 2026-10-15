import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * Headlands 电面 hc04 Part 3：持久化（persistent）队列，每个版本 O(1) 取均值。题面见 ../problem.md。
 *
 * 想法：所有 push 过的元素组成一棵树（子节点 = 在父版本后 push 的值）。一个版本 = (尾节点, 已弹出个数, 窗口和)。
 * 队列内容 = 从根到尾节点这条路径上、深度在 (headDepth, depth(tail)] 的那一段。
 *   push：新建一个子节点，O(1)。   pop：要知道队头值 = 路径上深度 headDepth+1 的祖先 → level ancestor。
 * level ancestor 用 skew-binary jump pointer（每个节点只多存一个 int），O(log n) 且不需要 n log n 的倍增表。
 * 全部放在原始类型数组里（SoA），没有每节点对象。
 */
public final class VersionedQueue {
    public static final int EMPTY = 0;

    // 节点（0 是根哨兵）
    private long[] val = new long[64];
    private int[] parent = new int[64];
    private int[] jump = new int[64];
    private int[] depth = new int[64];
    private int nodes = 1;

    // 版本（0 = 空队列）
    private int[] vTail = new int[64];
    private int[] vHeadDepth = new int[64];
    private long[] vHi = new long[64];
    private long[] vLo = new long[64];
    private int versions = 1;

    /** 在 version 之后 push x，返回新版本号；version 本身不变。 */
    public int push(int version, long x) {
        check(version);
        int node = newNode(vTail[version], x);
        var sum = new QueueMean.I128(vHi[version], vLo[version]).plus(x);
        return newVersion(node, vHeadDepth[version], sum);
    }

    /** 弹出 version 的队头，返回新版本号。空版本抛 NoSuchElementException。 */
    public int pop(int version) {
        check(version);
        if (size(version) == 0) throw new NoSuchElementException("pop on empty version " + version);
        int h = vHeadDepth[version] + 1;
        long front = val[levelAncestor(vTail[version], h)];
        var sum = new QueueMean.I128(vHi[version], vLo[version]).minus(front);
        return newVersion(vTail[version], h, sum);
    }

    /** 修正快照：新开一条独立的历史，内容恰好是 contents（队头在前）。 */
    public int correct(List<Long> contents) {
        int node = 0;
        var sum = QueueMean.I128.ZERO;
        for (long x : List.copyOf(contents)) {
            node = newNode(node, x);
            sum = sum.plus(x);
        }
        return newVersion(node, 0, sum);
    }

    public int size(int version) {
        check(version);
        return depth[vTail[version]] - vHeadDepth[version];
    }

    public QueueMean.Mean mean(int version) {
        int n = size(version);
        if (n == 0) throw new NoSuchElementException("mean of empty version " + version);
        return new QueueMean.Mean(new QueueMean.I128(vHi[version], vLo[version]).toBigInteger(), n);
    }

    /** 队列内容（队头在前），O(size)，测试与调试用。 */
    public List<Long> contents(int version) {
        int n = size(version);
        var out = new ArrayList<Long>(n);
        int node = vTail[version];
        for (int i = 0; i < n; i++) {
            out.add(val[node]);
            node = parent[node];
        }
        Collections.reverse(out);
        return out;
    }

    // ---------------------------------------------------------------- internals

    private void check(int version) {
        if (version < 0 || version >= versions) throw new IllegalArgumentException("unknown version " + version);
    }

    private int newNode(int p, long x) {
        if (nodes == val.length) {
            int cap = Math.multiplyExact(nodes, 2);
            val = Arrays.copyOf(val, cap);
            parent = Arrays.copyOf(parent, cap);
            jump = Arrays.copyOf(jump, cap);
            depth = Arrays.copyOf(depth, cap);
        }
        int n = nodes++;
        val[n] = x;
        parent[n] = p;
        depth[n] = depth[p] + 1;
        int j = jump[p];
        jump[n] = (depth[p] - depth[j] == depth[j] - depth[jump[j]]) ? jump[j] : p;
        return n;
    }

    private int newVersion(int tail, int headDepth, QueueMean.I128 sum) {
        if (versions == vTail.length) {
            int cap = Math.multiplyExact(versions, 2);
            vTail = Arrays.copyOf(vTail, cap);
            vHeadDepth = Arrays.copyOf(vHeadDepth, cap);
            vHi = Arrays.copyOf(vHi, cap);
            vLo = Arrays.copyOf(vLo, cap);
        }
        int v = versions++;
        vTail[v] = tail;
        vHeadDepth[v] = headDepth;
        vHi[v] = sum.hi();
        vLo[v] = sum.lo();
        return v;
    }

    private int levelAncestor(int v, int d) {
        while (depth[v] > d) v = depth[jump[v]] >= d ? jump[v] : parent[v];
        return v;
    }
}
