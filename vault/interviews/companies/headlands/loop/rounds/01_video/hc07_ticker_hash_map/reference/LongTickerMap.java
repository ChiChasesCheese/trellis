/**
 * Part 2：key 是已经打包好的 long（见 TickerCodec），value 是 long。开放寻址 + 线性探测，和 TickerMap 同一个思路，但：
 *
 *   * 没有 String、没有 hashCode()/equals() 虚调用 —— 比较就是 ==
 *   * 没有 Long 装箱 —— add() 在稳态下一个字节都不分配
 *   * key 和 value 放在同一个 long[]（交错布局）：slots[2i] = key，slots[2i+1] = value。
 *     一次探测读 key 的同时 value 已经在同一条缓存行 (cache line, 64 字节) 里了；分开两个数组则是两次缓存未命中
 *   * key 的 0 表示空格，-1 表示墓碑 —— 合法 key 都是正数，所以不需要额外的状态数组
 */
public final class LongTickerMap {
    private static final long EMPTY = 0L;
    private static final long TOMB = -1L;
    private static final int MIN_CAPACITY = 8;
    /** 2^64 / 黄金比例，奇数。Fibonacci hashing 的乘数。 */
    private static final long GOLDEN = 0x9E3779B97F4A7C15L;

    @FunctionalInterface
    public interface LongLongConsumer { void accept(long key, long value); }

    private long[] slots;   // 长度 = 2 * capacity
    private int size;
    private int tombs;
    private int mask;
    private int shift;      // 64 - log2(capacity)

    public LongTickerMap() { this(0); }

    public LongTickerMap(int expectedSize) {
        if (expectedSize < 0) throw new IllegalArgumentException("expectedSize < 0");
        long want = Math.max(MIN_CAPACITY, expectedSize * 2L); // 预留装载因子 1/2：放满 expectedSize 条恰好不 resize
        if (want > (1 << 29)) throw new IllegalArgumentException("expectedSize too large");
        allocate(Integer.highestOneBit((int) want - 1) << 1);
    }

    private void allocate(int capacity) {
        slots = new long[2 * capacity];
        mask = capacity - 1;
        shift = 64 - Integer.numberOfTrailingZeros(capacity);
        size = 0;
        tombs = 0;
    }

    private int home(long key) { return (int) ((key * GOLDEN) >>> shift); }

    private static void checkKey(long key) {
        if (key <= 0) throw new IllegalArgumentException("key must be > 0 (0 = empty marker, -1 = tombstone): " + key);
    }

    public int size() { return size; }
    public int capacity() { return slots.length / 2; }
    public int tombstones() { return tombs; }

    /** 返回 key 所在的格子编号，没有返回 -1。 */
    private int find(long key) {
        int i = home(key);
        while (true) {
            long k = slots[2 * i];
            if (k == key) return i;
            if (k == EMPTY) return -1;
            i = (i + 1) & mask;           // 墓碑 (-1) 既不等于 key 也不是空，自然继续往后
        }
    }

    public boolean containsKey(long key) {
        checkKey(key);
        return find(key) >= 0;
    }

    public long get(long key, long ifAbsent) {
        checkKey(key);
        int i = find(key);
        return i < 0 ? ifAbsent : slots[2 * i + 1];
    }

    /** 放入；返回 true 表示这是新 key，false 表示覆盖了旧值。 */
    public boolean put(long key, long value) {
        checkKey(key);
        int i = locateForInsert(key);
        if (i >= 0) { slots[2 * i + 1] = value; return false; }
        insertNew(key, value, ~i);
        return true;
    }

    /** value += delta（不存在当作 0）；返回新值。热路径：稳态不分配。 */
    public long add(long key, long delta) {
        checkKey(key);
        int i = locateForInsert(key);
        if (i >= 0) {
            long v = Math.addExact(slots[2 * i + 1], delta);
            slots[2 * i + 1] = v;
            return v;
        }
        insertNew(key, delta, ~i);
        return delta;
    }

    /**
     * 找 key：找到返回非负格子号；找不到返回 ~(应该插入的位置)（负数）。
     * 应该插入的位置 = 探测路上第一个墓碑，没有墓碑就是终点的空格。
     */
    private int locateForInsert(long key) {
        int i = home(key);
        int firstTomb = -1;
        while (true) {
            long k = slots[2 * i];
            if (k == key) return i;
            if (k == EMPTY) return ~(firstTomb >= 0 ? firstTomb : i);
            if (k == TOMB && firstTomb < 0) firstTomb = i;
            i = (i + 1) & mask;
        }
    }

    private void insertNew(long key, long value, int at) {
        if (slots[2 * at] == TOMB) {          // 复用墓碑
            tombs--;
        } else if ((size + tombs + 1) * 2 > capacity()) { // 占用空格会让「已用格子」超过一半
            rehash();
            at = home(key);
            while (slots[2 * at] != EMPTY) at = (at + 1) & mask;
        }
        slots[2 * at] = key;
        slots[2 * at + 1] = value;
        size++;
    }

    public boolean remove(long key) {
        checkKey(key);
        int i = find(key);
        if (i < 0) return false;
        slots[2 * i] = TOMB;
        slots[2 * i + 1] = 0;
        size--;
        tombs++;
        return true;
    }

    private void rehash() {
        long[] old = slots;
        long want = Math.max(MIN_CAPACITY, size * 4L); // 纯插入触发时 size == capacity/2，所以正好翻倍
        if (want > (1 << 29)) throw new IllegalStateException("map too large");
        allocate(Integer.highestOneBit((int) want - 1) << 1);
        for (int j = 0; j < old.length; j += 2) {
            long k = old[j];
            if (k <= 0) continue;           // 空格或墓碑
            int i = home(k);
            while (slots[2 * i] != EMPTY) i = (i + 1) & mask;
            slots[2 * i] = k;
            slots[2 * i + 1] = old[j + 1];
            size++;
        }
    }

    public void forEach(LongLongConsumer action) {
        for (int j = 0; j < slots.length; j += 2) {
            if (slots[j] > 0) action.accept(slots[j], slots[j + 1]);
        }
    }

    public int maxProbeLength() {
        int worst = 0;
        for (int i = 0; i < capacity(); i++) {
            long k = slots[2 * i];
            if (k > 0) worst = Math.max(worst, (i - home(k)) & mask);
        }
        return worst;
    }
}
