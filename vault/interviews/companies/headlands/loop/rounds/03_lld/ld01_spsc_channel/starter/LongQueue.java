/**
 * 定长 long 队列的最小接口（Part 1 的 LongRing 和 Part 2 的 SpscLongRing 都实现它，测试可以对两者复用同一套单线程用例）。
 *
 * poll() 在空队列上抛 NoSuchElementException，而不是返回一个「魔法值」：long 的每个取值都可能是合法消息，没有哪个值能当哨兵。
 * 想自旋等待的消费者写 `while (q.isEmpty()) Thread.onSpinWait(); q.poll();`——在 SPSC 里这是安全的：
 * 只有消费者会让队列变空，所以 isEmpty() 为 false 之后，直到消费者自己 poll，队列不会再变空。
 */
public interface LongQueue {
    int capacity();
    /** 当前元素个数。SpscLongRing 里在并发时是近似值（在 [0, capacity] 内）。 */
    int size();
    /** 满了返回 false（不抛异常）。 */
    boolean offer(long value);
    /** 空队列抛 NoSuchElementException。 */
    long poll();
    boolean isEmpty();

    // J18 接口 default 方法：所有实现共享的派生规则
    default boolean isFull() { return size() == capacity(); }
}
