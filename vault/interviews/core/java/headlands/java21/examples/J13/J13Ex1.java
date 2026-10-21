import java.util.*;
import java.util.stream.*;

/** J13 例 1（最简单）：未命名变量 _ 出现的位置（JDK 21 预览，JDK 22 转正）。 */
public class J13Ex1 {
    static class Res implements AutoCloseable { public void close() { System.out.println("  Res closed"); } }

    static int parseOrDefault(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException _) {          // 1. catch 参数
            return -1;
        }
    }

    public static void main(String[] args) {
        List<String> names = List.of("a", "b", "c");

        int n = 0;
        for (String _ : names) n++;                  // 2. 增强 for 的循环变量
        System.out.println("n = " + n);

        var map = new HashMap<String, Integer>();
        var _ = map.put("k", 1);                     // 3. 局部变量声明：明确表示"我故意不要返回值"
        map.computeIfAbsent("z", _ -> 0);            // 4. lambda 参数
        System.out.println("map = " + new TreeMap<>(map));

        try (var _ = new Res()) {                    // 5. try-with-resources：只要它的"开/关"，不用它本身
            System.out.println("  in try");
        }

        // 6. 多个 _ 同时出现是合法的，因为它们都不是真正的变量
        BiFunctionLike f = (_, _) -> 42;
        System.out.println("f = " + f.apply("x", "y") + ", parse(\"x\") = " + parseOrDefault("x") + ", parse(\"12\") = " + parseOrDefault("12"));

        long evens = IntStream.range(0, 10).filter(i -> i % 2 == 0).count();
        System.out.println("evens = " + evens);
    }

    interface BiFunctionLike { int apply(String a, String b); }
}
