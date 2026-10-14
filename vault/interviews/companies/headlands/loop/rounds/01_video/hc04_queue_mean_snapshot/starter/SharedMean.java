import java.util.Optional;

/**
 * Headlands 电面 hc04 Part 4：单写者、多读者的队列均值。题面见 ../problem.md。
 * 写者线程调用 push/pop；任意线程调用 read()/mean()，且必须拿到「某一时刻」的一致快照。
 */
public final class SharedMean {

    public record Stat(long seq, int size, QueueMean.I128 sum) {
        /** 该快照的精确均值；空队列返回 Optional.empty()。 */
        public Optional<QueueMean.Mean> mean() { throw new UnsupportedOperationException("TODO"); }
    }

    /** 第一个调用 push/pop 的线程成为唯一写者；别的线程再写 → IllegalStateException。 */
    public void push(long x) { throw new UnsupportedOperationException("TODO"); }

    public long pop() { throw new UnsupportedOperationException("TODO"); }

    /** 任意线程可调；seq 从 0 开始，每次修改 +1。提示：不可变 Stat + VarHandle 的 setRelease/getAcquire。 */
    public Stat read() { throw new UnsupportedOperationException("TODO"); }

    public Optional<QueueMean.Mean> mean() { return read().mean(); }
}
