import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.SequencedMap;
import java.util.SequencedSet;
import java.util.TreeMap;
import java.util.TreeSet;

/** J09 例 2（进阶）：LinkedHashSet / LinkedHashMap 的重排；TreeSet / TreeMap 的限制；entry 是只读快照；包装成不可变。 */
public class J09Ex2 {

    public static void main(String[] args) {
        // ---- LinkedHashSet：addFirst / addLast 对已存在的元素会「移动」它 ----
        SequencedSet<String> set = new LinkedHashSet<>(java.util.List.of("a", "b", "c"));
        set.addFirst("c");                                   // c 已存在 -> 移到最前
        set.addLast("a");                                    // a 已存在 -> 移到最后
        System.out.println(set + " first=" + set.getFirst() + " last=" + set.getLast());   // [c, b, a]
        System.out.println(set.reversed());                  // [a, b, c]

        // ---- LinkedHashMap：putFirst / putLast，以及老的 put 对已存在 key「不改顺序」----
        SequencedMap<String, Integer> m = new LinkedHashMap<>();
        m.put("x", 1); m.put("y", 2); m.put("z", 3);
        m.put("x", 10);                                      // 已存在：只改值，顺序不变
        System.out.println(m);                               // {x=10, y=2, z=3}
        m.putLast("x", 11);                                  // 现在把 x 挪到最后
        System.out.println(m);                               // {y=2, z=3, x=11}
        m.putFirst("w", 0);                                  // 新 key 放最前
        System.out.println(m + " first=" + m.firstEntry() + " last=" + m.lastEntry());
        System.out.println("poll: " + m.pollFirstEntry() + " then " + m.pollLastEntry() + " -> " + m);

        // sequencedKeySet / sequencedValues / sequencedEntrySet：Map 的三个视图也是有序的
        System.out.println(m.sequencedKeySet().getLast() + " " + m.sequencedValues().getFirst());

        // firstEntry() 返回的是「快照」，不能 setValue
        try {
            m.firstEntry().setValue(99);
        } catch (UnsupportedOperationException e) {
            System.out.println("firstEntry().setValue -> UnsupportedOperationException");
        }

        // ---- TreeSet / TreeMap：顺序由比较器决定，所以 addFirst / putFirst 不被支持 ----
        TreeSet<Integer> ts = new TreeSet<>(java.util.List.of(5, 1, 3));
        System.out.println(ts.getFirst() + " " + ts.getLast() + " " + ts.reversed());   // 1 5 [5, 3, 1]
        try {
            ts.addFirst(0);
        } catch (UnsupportedOperationException e) {
            System.out.println("TreeSet.addFirst -> UnsupportedOperationException");
        }
        TreeMap<Integer, String> tm = new TreeMap<>(Map.of(1, "one", 2, "two", 3, "three"));
        try {
            tm.putFirst(0, "zero");
        } catch (UnsupportedOperationException e) {
            System.out.println("TreeMap.putFirst -> UnsupportedOperationException");
        }
        System.out.println(tm.firstEntry() + " " + tm.pollLastEntry() + " " + tm.reversed());

        // ---- 包装成只读：保留「有序」这个类型 ----
        SequencedMap<String, Integer> ro = Collections.unmodifiableSequencedMap(m);
        System.out.println(ro.firstEntry());
        try {
            ro.putLast("q", 1);
        } catch (UnsupportedOperationException e) {
            System.out.println("unmodifiableSequencedMap.putLast -> UnsupportedOperationException");
        }
    }
}
