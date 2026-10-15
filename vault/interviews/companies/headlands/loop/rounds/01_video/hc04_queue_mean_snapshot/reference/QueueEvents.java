import java.util.ArrayList;
import java.util.List;

/** Headlands 电面 hc04 Part 2：带「修正快照」的事件流。题面见 ../problem.md。 */
public final class QueueEvents {
    private QueueEvents() {}

    public sealed interface Event permits Push, Pop, Query, Correct {}
    public record Push(long value) implements Event {}
    public record Pop() implements Event {}
    public record Query() implements Event {}
    /** 修正快照：丢弃此前的整段逻辑历史，队列内容变成 contents（队头在前）。 */
    public record Correct(List<Long> contents) implements Event {
        public Correct { contents = List.copyOf(contents); } // 防御性拷贝；null 元素直接 NPE
    }

    public sealed interface Answer permits Value, Empty {}
    public record Value(QueueMean.Mean mean) implements Answer {}
    public record Empty() implements Answer {}

    /** 逐个应用事件，每个 Query 产出一个 Answer。队列为空时 Pop 抛 java.util.NoSuchElementException。 */
    public static List<Answer> run(List<? extends Event> events) {
        var q = new QueueMean();
        var out = new ArrayList<Answer>();
        for (Event e : events) {
            switch (e) {
                case Push(var v) -> q.push(v);
                case Pop _ -> q.pop();
                case Query _ -> out.add(q.isEmpty() ? new Empty() : new Value(q.mean()));
                case Correct(var contents) -> {
                    q = new QueueMean();
                    for (long v : contents) q.push(v);
                }
            }
        }
        return out;
    }

    /** 文本 → 事件。格式：push N | pop | mean | snapshot [N ...]；空行忽略；错误抛 IllegalArgumentException("line k: ...")。 */
    public static List<Event> parse(List<String> lines) {
        var events = new ArrayList<Event>();
        int lineNo = 0;
        for (String raw : lines) {
            lineNo++;
            String line = raw.strip();
            if (line.isEmpty()) continue;
            String[] t = line.split("\\s+");
            try {
                events.add(switch (t[0]) {
                    case "push" -> {
                        if (t.length != 2) throw new IllegalArgumentException("push takes exactly one integer");
                        yield new Push(Long.parseLong(t[1]));
                    }
                    case "pop" -> {
                        if (t.length != 1) throw new IllegalArgumentException("pop takes no argument");
                        yield new Pop();
                    }
                    case "mean" -> {
                        if (t.length != 1) throw new IllegalArgumentException("mean takes no argument");
                        yield new Query();
                    }
                    case "snapshot" -> {
                        var contents = new ArrayList<Long>();
                        for (int i = 1; i < t.length; i++) contents.add(Long.parseLong(t[i]));
                        yield new Correct(contents);
                    }
                    default -> throw new IllegalArgumentException("unknown command '" + t[0] + "'");
                });
            } catch (IllegalArgumentException ex) { // NumberFormatException 也是它的子类
                throw new IllegalArgumentException("line " + lineNo + ": " + ex.getMessage(), ex);
            }
        }
        return events;
    }

    /** 渲染一个答案：整数 "7"，分数 "-7/2"，空队列 "empty"。 */
    public static String render(Answer a) {
        return switch (a) {
            case Value(QueueMean.Mean(var n, var d)) when d == 1 -> n.toString();
            case Value(QueueMean.Mean(var n, var d)) -> n + "/" + d;
            case Empty _ -> "empty";
        };
    }

    /** 整题：文本事件 → 文本答案。 */
    public static List<String> solve(List<String> lines) {
        return run(parse(lines)).stream().map(QueueEvents::render).toList();
    }
}
