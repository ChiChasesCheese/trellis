import java.util.*;
import java.util.stream.*;

/** One program per Java era: what you can write today vs Java 8. Compile with --release 21. */
public class K14Versions {
    sealed interface Shape permits Circle, Rect {}
    record Circle(double r) implements Shape {}
    record Rect(double w, double h) implements Shape {}

    static double area(Shape s) {                         // 17 sealed + 21 pattern switch + record patterns
        return switch (s) {
            case Circle(var r) -> Math.PI * r * r;
            case Rect(var w, var h) when w == h -> w * w;
            case Rect(var w, var h) -> w * h;
        };
    }
    public static void main(String[] args) throws Exception {
        var list = List.of(3, 1, 2);                                          // 9: immutable factories; 10: var
        System.out.println(list.stream().sorted().toList());                  // 16: Stream.toList
        String json = """
            {"k": 1}
            """;                                                              // 15: text block
        System.out.print(json);
        Object o = "hi";
        if (o instanceof String s && s.length() == 2) System.out.println("instanceof pattern: " + s);   // 16
        System.out.println(area(new Rect(2, 3)) + " " + area(new Rect(2, 2)));
        var dq = new LinkedHashSet<>(List.of("a", "b", "c"));
        System.out.println(dq.reversed() + " first=" + dq.getFirst());       // 21: SequencedCollection
        String tee = Stream.of(1, 2, 3, 4).collect(Collectors.teeing(Collectors.counting(), Collectors.summingInt((Integer i) -> i), (Long c, Integer sum) -> c + "/" + sum));
        System.out.println("teeing count/sum: " + tee);  // 12
        try (var ex = java.util.concurrent.Executors.newVirtualThreadPerTaskExecutor()) {    // 21
            System.out.println("virtual: " + ex.submit(() -> Thread.currentThread().isVirtual()).get());
        }
        System.out.println(Runtime.version() + " | HttpClient (11): " + java.net.http.HttpClient.class.getSimpleName());
    }
}
