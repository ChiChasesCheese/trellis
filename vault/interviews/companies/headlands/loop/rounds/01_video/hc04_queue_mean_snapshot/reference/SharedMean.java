import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.util.Optional;

/**
 * Headlands 电面 hc04 Part 4：单写者、多读者的队列均值。题面见 ../problem.md。
 *
 * 写者每次修改后把 (seq, size, sum) 打成一个不可变 Stat，用 release 语义发布；读者 acquire 读一次引用，
 * 拿到的永远是某个真实时刻的一致快照。读者不加锁、不阻塞写者，也不会读到「新 sum + 旧 size」的撕裂值。
 */
public final class SharedMean {

    public record Stat(long seq, int size, QueueMean.I128 sum) {
        /** 该快照的精确均值；空队列返回 Optional.empty()。 */
        public Optional<QueueMean.Mean> mean() {
            return size == 0 ? Optional.empty() : Optional.of(new QueueMean.Mean(sum.toBigInteger(), size));
        }
    }

    private static final VarHandle PUBLISHED;
    private static final VarHandle OWNER;
    static {
        try {
            var l = MethodHandles.lookup();
            PUBLISHED = l.findVarHandle(SharedMean.class, "published", Stat.class);
            OWNER = l.findVarHandle(SharedMean.class, "owner", Thread.class);
        } catch (ReflectiveOperationException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    private final QueueMean queue = new QueueMean(); // 只有写者线程碰
    private long seq;                                 // 只有写者线程碰
    @SuppressWarnings("unused") private Stat published = new Stat(0, 0, QueueMean.I128.ZERO); // 经 PUBLISHED 访问
    @SuppressWarnings("unused") private Thread owner;                                                  // 经 OWNER 访问

    public void push(long x) {
        claimWriter();
        queue.push(x);
        publish();
    }

    public long pop() {
        claimWriter();
        long x = queue.pop();
        publish();
        return x;
    }

    /** 任意线程可调。 */
    public Stat read() { return (Stat) PUBLISHED.getAcquire(this); }

    public Optional<QueueMean.Mean> mean() { return read().mean(); }

    private void publish() {
        PUBLISHED.setRelease(this, new Stat(++seq, queue.size(), queue.sum()));
    }

    /** 第一个写的线程成为唯一写者；别的线程再写 → IllegalStateException。 */
    private void claimWriter() {
        Thread me = Thread.currentThread();
        Thread cur = (Thread) OWNER.getAcquire(this);
        if (cur == me) return;
        if (cur != null || !OWNER.compareAndSet(this, null, me)) {
            throw new IllegalStateException("single-writer violated: owned by " + OWNER.getAcquire(this));
        }
    }
}
