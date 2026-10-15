import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Part 2 的前半：SpscLongRing 在单线程下和 LongRing 行为完全一致（用例在 LongQueueContract 里）。多线程见 SpscLongRingTest。 */
@Tag("part2")
class SpscLongRingSequentialTest extends LongQueueContract {
    @Override LongQueue make(int capacity) { return new SpscLongRing(capacity); }

    @Test
    void maxCapacityConstant() {
        assertEquals(1 << 30, SpscLongRing.MAX_CAPACITY);
    }
}
