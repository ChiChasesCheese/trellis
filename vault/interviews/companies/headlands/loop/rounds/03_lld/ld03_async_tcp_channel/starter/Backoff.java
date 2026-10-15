import java.util.random.RandomGenerator;

/**
 * Part 4a：指数退避。next() 依次返回 initial, initial*m, initial*m^2 … 封顶 max，且乘法不能溢出。
 * 参数非法（initial <= 0、max < initial、multiplier < 1）抛 IllegalArgumentException。
 */
public final class Backoff {
    public Backoff(long initialMs, long maxMs, int multiplier) {
        throw new UnsupportedOperationException("TODO");
    }

    public long next() { throw new UnsupportedOperationException("TODO"); }

    /** 全抖动：在 [0, next()] 内均匀随机（含两端）。 */
    public long next(RandomGenerator rng) { throw new UnsupportedOperationException("TODO"); }

    public void reset() { throw new UnsupportedOperationException("TODO"); }
}
