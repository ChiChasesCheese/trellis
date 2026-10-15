import java.util.random.RandomGenerator;

/**
 * Part 4a：指数退避。next() 依次返回 initial, initial*m, initial*m^2, … 封顶 max；reset() 回到 initial。
 * next(rng) 是「全抖动」（full jitter）：在 [0, 当前上限] 内均匀取值，避免大量客户端同时重连造成惊群。
 */
public final class Backoff {
    private final long initialMs;
    private final long maxMs;
    private final int multiplier;
    private long current;

    public Backoff(long initialMs, long maxMs, int multiplier) {
        if (initialMs <= 0) throw new IllegalArgumentException("initialMs must be > 0");
        if (maxMs < initialMs) throw new IllegalArgumentException("maxMs must be >= initialMs");
        if (multiplier < 1) throw new IllegalArgumentException("multiplier must be >= 1");
        this.initialMs = initialMs;
        this.maxMs = maxMs;
        this.multiplier = multiplier;
        this.current = initialMs;
    }

    /** 本次该等多久；然后把下一次的延迟乘以 multiplier（封顶，且不会溢出）。 */
    public long next() {
        long d = current;
        current = current > maxMs / multiplier ? maxMs : Math.min(maxMs, current * multiplier);
        return d;
    }

    /** 全抖动：在 [0, next()] 内均匀随机（含两端）。 */
    public long next(RandomGenerator rng) {
        long cap = next();
        return rng.nextLong(cap + 1);
    }

    public void reset() { current = initialMs; }
}
