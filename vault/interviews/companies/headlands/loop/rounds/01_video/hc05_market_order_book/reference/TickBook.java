import java.util.Arrays;

/**
 * Part 4：热路径版订单簿。价格是 long tick（有界价格带 1..maxTicks-1），不装箱；
 * 订单池 = 结构数组（struct-of-arrays）+ 侵入式双向链表，价位 = 数组下标，id → 槽位 = 开放寻址哈希表。
 * 稳态下 limit / cancel 不分配对象。
 */
// 为什么需要这一版：Part 2 的 OrderBook 每个订单是一个 Node 对象 + TreeMap/HashMap 的装箱 Long key + 每次调用的 Event 列表，
// 实测每个操作约 400 字节垃圾（见 REPORT）；垃圾多 → GC 停顿 → 尾延迟抖动。低延迟系统要的是「稳态零分配」：
//  * 价格是有界整数（tick），所以「价位」不需要树，直接用数组下标：head[side][tick]。找最优价靠位图 + 前导/尾随零指令。
//  * 订单放进预分配的数组（struct-of-arrays），用 int 下标代替对象引用；队列用侵入式双向链表（prev/next 也是 int 数组）。
//  * id → 槽位用开放寻址哈希表（long[] 键），不装箱。
//  * 成交通过回调 TradeSink 报告，不创建事件对象。
// 代价：价格带、同时挂单数是构造时固定的上限（有界内存），超过就拒绝——这正是低延迟系统的取舍。
public final class TickBook {
    public static final long NONE = -1;
    public static final long REJECTED = -1;
    public static final long FULL = -2;
    /** 单笔数量上限：保证 价位总量（≤ 2^22 张 × 2^40）不会溢出 long。 */
    public static final long MAX_QTY = 1L << 40;

    /** 成交回调：不产生事件对象。 */
    public interface TradeSink {
        void onTrade(long takerId, long makerId, long price, long qty);
    }

    private final int maxTicks;
    private final int capacity;

    // 订单池
    private final long[] oid;
    private final long[] oqty;
    private final int[] oprice;
    private final byte[] oside;
    private final int[] prev;
    private final int[] next; // 队列里的后继；空闲槽里是 free list 的后继
    private int freeHead;
    private int live;

    // id → 槽位（线性探测 + 回移删除；id > 0 所以 0 表示空）
    private final long[] keys;
    private final int[] vals;
    private final int mask;

    // 价格梯：[side][tick]
    private final int[][] head;
    private final int[][] tail;
    private final long[][] levelQty;
    private final long[][] bits; // 非空价位位图，用来在最优价被吃光后 O(maxTicks/64) 找下一档
    private int bestBid; // 0 = 无
    private int bestAsk; // maxTicks = 无

    public TickBook(int maxTicks, int capacity) {
        if (maxTicks < 2) throw new IllegalArgumentException("maxTicks < 2");
        if (capacity < 1 || capacity > (1 << 22)) throw new IllegalArgumentException("capacity out of range");
        this.maxTicks = maxTicks;
        this.capacity = capacity;
        oid = new long[capacity];
        oqty = new long[capacity];
        oprice = new int[capacity];
        oside = new byte[capacity];
        prev = new int[capacity];
        next = new int[capacity];
        for (int i = 0; i < capacity; i++) next[i] = i + 1 < capacity ? i + 1 : -1;
        freeHead = 0;
        int tbl = Integer.highestOneBit(Math.max(16, capacity * 2 - 1)) << 1;
        keys = new long[tbl];
        vals = new int[tbl];
        mask = tbl - 1;
        head = new int[2][maxTicks];
        tail = new int[2][maxTicks];
        levelQty = new long[2][maxTicks];
        bits = new long[2][(maxTicks + 63) >>> 6];
        Arrays.fill(head[0], -1);
        Arrays.fill(head[1], -1);
        Arrays.fill(tail[0], -1);
        Arrays.fill(tail[1], -1);
        bestBid = 0;
        bestAsk = maxTicks;
    }

    /**
     * 限价单：先吃对手盘（价格-时间优先，每笔成交回调 sink），剩余挂簿。
     * 返回挂簿的剩余量（0 = 全部成交）；非法返回 REJECTED（id ≤ 0、重复、价格不在 1..maxTicks-1、数量不在 1..MAX_QTY）；
     * 池满返回 FULL（不撮合）。
     */
    public long limit(long id, OrderBook.Side side, long price, long qty, TradeSink sink) {
        if (id <= 0 || price <= 0 || price >= maxTicks || qty <= 0 || qty > MAX_QTY) return REJECTED;
        if (find(id) >= 0) return REJECTED;
        if (freeHead < 0) return FULL;
        int p = (int) price;
        boolean buy = side == OrderBook.Side.BUY;
        int s = buy ? 0 : 1;
        int o = 1 - s;
        long left = qty;
        while (left > 0 && (buy ? bestAsk <= p : bestBid >= p)) {
            int bp = buy ? bestAsk : bestBid;
            int slot = head[o][bp];
            long fill = Math.min(left, oqty[slot]);
            sink.onTrade(id, oid[slot], bp, fill);
            left -= fill;
            oqty[slot] -= fill;
            levelQty[o][bp] -= fill;
            if (oqty[slot] == 0) unlink(slot);
        }
        if (left > 0) rest(id, s, p, left);
        return left;
    }

    public boolean cancel(long id) {
        int slot = find(id);
        if (slot < 0) return false;
        unlink(slot);
        return true;
    }

    public long bestBid() { return bestBid == 0 ? NONE : bestBid; }
    public long bestAsk() { return bestAsk == maxTicks ? NONE : bestAsk; }
    public int liveOrders() { return live; }

    public long qtyAt(OrderBook.Side side, long price) {
        if (price <= 0 || price >= maxTicks) return 0;
        return levelQty[side == OrderBook.Side.BUY ? 0 : 1][(int) price];
    }

    // ---------- 内部 ----------

    private void rest(long id, int s, int p, long qty) {
        int slot = freeHead;
        freeHead = next[slot];
        live++;
        oid[slot] = id;
        oqty[slot] = qty;
        oprice[slot] = p;
        oside[slot] = (byte) s;
        int t = tail[s][p];
        prev[slot] = t;
        next[slot] = -1;
        if (t >= 0) {
            next[t] = slot;
        } else {
            head[s][p] = slot;
            bits[s][p >>> 6] |= 1L << (p & 63);
            if (s == 0) { if (p > bestBid) bestBid = p; } else { if (p < bestAsk) bestAsk = p; }
        }
        tail[s][p] = slot;
        levelQty[s][p] += qty;
        put(id, slot);
    }

    /** 把槽位从队列摘下、归还池、清 id 表；价位空了就更新位图与最优价。 */
    private void unlink(int slot) {
        int s = oside[slot];
        int p = oprice[slot];
        int pr = prev[slot];
        int nx = next[slot];
        if (pr >= 0) next[pr] = nx; else head[s][p] = nx;
        if (nx >= 0) prev[nx] = pr; else tail[s][p] = pr;
        levelQty[s][p] -= oqty[slot];
        if (head[s][p] < 0) {
            bits[s][p >>> 6] &= ~(1L << (p & 63));
            if (s == 0 && p == bestBid) {
                int n = p > 0 ? atOrBelow(bits[0], p - 1) : -1;
                bestBid = n < 0 ? 0 : n;
            } else if (s == 1 && p == bestAsk) {
                int n = p + 1 < maxTicks ? atOrAbove(bits[1], p + 1) : -1;
                bestAsk = n < 0 ? maxTicks : n;
            }
        }
        removeKey(oid[slot]);
        next[slot] = freeHead;
        freeHead = slot;
        live--;
    }

    // 位图：第 p 位 = 1 表示价位 p 非空。找「≥ from 的第一个非空价位」：先屏蔽 from 之前的位，
    // 再按 64 位一个字扫描，字里用 numberOfTrailingZeros 一条指令定位。最坏扫 maxTicks/64 个字，而不是 maxTicks 个价位。
    private static int atOrAbove(long[] b, int from) {
        int w = from >>> 6;
        long word = b[w] & (-1L << (from & 63));
        while (true) {
            if (word != 0) return (w << 6) + Long.numberOfTrailingZeros(word);
            if (++w >= b.length) return -1;
            word = b[w];
        }
    }

    private static int atOrBelow(long[] b, int from) {
        int w = from >>> 6;
        long word = b[w] & (-1L >>> (63 - (from & 63)));
        while (true) {
            if (word != 0) return (w << 6) + 63 - Long.numberOfLeadingZeros(word);
            if (--w < 0) return -1;
            word = b[w];
        }
    }

    // 哈希函数：乘一个大奇数（黄金比例常数）把相邻的 id 打散，再把高 32 位折叠进低位；
    // 否则连续 id 会连续落进相邻槽位，线性探测会形成长长的「聚簇」。
    private int hash(long k) {
        long h = k * 0x9E3779B97F4A7C15L;
        return (int) (h ^ (h >>> 32)) & mask;
    }

    private int find(long id) {
        int i = hash(id);
        while (keys[i] != 0) {
            if (keys[i] == id) return vals[i];
            i = (i + 1) & mask;
        }
        return -1;
    }

    private void put(long id, int slot) {
        int i = hash(id);
        while (keys[i] != 0) i = (i + 1) & mask;
        keys[i] = id;
        vals[i] = slot;
    }

    /**
     * 线性探测的回移删除（backward shift）：不留墓碑，探测链不会越来越长。
     * 直接把槽位清零会"切断"后面那些原本因冲突而溢出到后面的 key 的探测链，使 find 找不到它们；
     * 所以要把后面能往前挪的元素挪回空洞。判断：元素 j 的理想位置 k 若不在 (i, j] 的环形区间里，挪到 i 之后仍然在它的探测链上。
     */
    private void removeKey(long id) {
        int i = hash(id);
        while (keys[i] != id) i = (i + 1) & mask;
        int j = i;
        while (true) {
            j = (j + 1) & mask;
            if (keys[j] == 0) break;
            int k = hash(keys[j]);
            if (((j - k) & mask) >= ((j - i) & mask)) {
                keys[i] = keys[j];
                vals[i] = vals[j];
                i = j;
            }
        }
        keys[i] = 0;
    }
}
