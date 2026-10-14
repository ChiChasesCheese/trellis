import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 1：LongRing 的单线程语义（用例在 LongQueueContract 里）。 */
@Tag("part1")
class LongRingTest extends LongQueueContract {
    @Override LongQueue make(int capacity) { return new LongRing(capacity); }

    @Test
    void maxCapacityConstant() {
        assertEquals(1 << 30, LongRing.MAX_CAPACITY);
    }
}
