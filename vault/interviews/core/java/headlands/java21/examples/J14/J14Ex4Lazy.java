import java.util.stream.*;

/** J14 例 4：流水线是「懒」的、逐元素向下推的——不是一层一层处理整个集合。看 peek 的输出顺序。 */
public class J14Ex4Lazy {
    public static void main(String[] args) {
        System.out.println("--- 没有终止操作：什么都不会执行");
        Stream.of(1, 2, 3, 4).peek(x -> System.out.println("peek " + x));   // 无输出

        System.out.println("--- 逐元素下推 + 短路(findFirst)");
        int first = Stream.of(1, 2, 3, 4, 5, 6)
                .peek(x -> System.out.println("  source " + x))
                .filter(x -> { System.out.println("  filter " + x); return x % 2 == 0; })
                .map(x -> { System.out.println("  map    " + x); return x * 10; })
                .findFirst().orElseThrow();
        System.out.println("结果 = " + first);   // 只处理到 2 就停了

        System.out.println("--- sorted 是屏障：必须先看完全部元素");
        Stream.of(3, 1, 2)
                .peek(x -> System.out.println("  before sort " + x))
                .sorted()
                .peek(x -> System.out.println("  after sort  " + x))
                .toList();
    }
}
