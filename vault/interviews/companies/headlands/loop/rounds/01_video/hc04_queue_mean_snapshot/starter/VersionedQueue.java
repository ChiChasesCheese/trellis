import java.util.List;

/**
 * Headlands 电面 hc04 Part 3：持久化（persistent）队列，每个版本 O(1) 取均值。
 * 版本号是 int；EMPTY 是空队列；任何操作都返回新版本号，旧版本永远不变。题面见 ../problem.md。
 */
public final class VersionedQueue {
    public static final int EMPTY = 0;

    /** 在 version 之后 push x，返回新版本号。未知版本抛 IllegalArgumentException。 */
    public int push(int version, long x) { throw new UnsupportedOperationException("TODO"); }

    /** 弹出 version 的队头，返回新版本号。空版本抛 NoSuchElementException。 */
    public int pop(int version) { throw new UnsupportedOperationException("TODO"); }

    /** 修正快照：新开一条独立的历史，内容恰好是 contents（队头在前）。 */
    public int correct(List<Long> contents) { throw new UnsupportedOperationException("TODO"); }

    public int size(int version) { throw new UnsupportedOperationException("TODO"); }

    /** 精确均值；空版本抛 NoSuchElementException。 */
    public QueueMean.Mean mean(int version) { throw new UnsupportedOperationException("TODO"); }

    /** 队列内容（队头在前），O(size)，测试用。 */
    public List<Long> contents(int version) { throw new UnsupportedOperationException("TODO"); }
}
