import java.util.List;

/** Headlands 电面 hc04 Part 2：带「修正快照」的事件流。题面见 ../problem.md。 */
public final class QueueEvents {
    private QueueEvents() {}

    public sealed interface Event permits Push, Pop, Query, Correct {}
    public record Push(long value) implements Event {}
    public record Pop() implements Event {}
    public record Query() implements Event {}
    /** 修正快照：丢弃此前的整段逻辑历史，队列内容变成 contents（队头在前）。提示：紧凑构造器里做防御性拷贝。 */
    public record Correct(List<Long> contents) implements Event {}

    public sealed interface Answer permits Value, Empty {}
    public record Value(QueueMean.Mean mean) implements Answer {}
    public record Empty() implements Answer {}

    /** 逐个应用事件，每个 Query 产出一个 Answer。队列为空时 Pop 抛 java.util.NoSuchElementException。提示：对 sealed Event 写模式匹配 switch。 */
    public static List<Answer> run(List<? extends Event> events) { throw new UnsupportedOperationException("TODO"); }

    /** 文本 → 事件。格式：push N | pop | mean | snapshot [N ...]；空行忽略；错误抛 IllegalArgumentException("line k: ...")。 */
    public static List<Event> parse(List<String> lines) { throw new UnsupportedOperationException("TODO"); }

    /** 渲染一个答案：整数 "7"，分数 "-7/2"，空队列 "empty"。 */
    public static String render(Answer a) { throw new UnsupportedOperationException("TODO"); }

    /** 整题：文本事件 → 文本答案。 */
    public static List<String> solve(List<String> lines) { return run(parse(lines)).stream().map(QueueEvents::render).toList(); }
}
