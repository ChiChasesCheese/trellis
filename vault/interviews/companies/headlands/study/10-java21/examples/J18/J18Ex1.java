import java.util.*;

/** J18 例 1（最简单）：Comparator 组合子；reversed() 位置的陷阱；nullsFirst；compare 减法 bug。 */
public class J18Ex1 {
    record Person(String name, Integer age, String city) {}

    public static void main(String[] args) {
        List<Person> ps = new ArrayList<>(List.of(
                new Person("Bob", 30, "NY"), new Person("alice", 25, "SF"),
                new Person("Carol", 30, "NY"), new Person("dave", null, "LA"), new Person("Eve", 25, "NY")));

        // 1. 单键升序
        System.out.println("按 name(忽略大小写): " + names(sorted(ps, Comparator.comparing(Person::name, String.CASE_INSENSITIVE_ORDER))));

        // 2. 多键：年龄降序，再按名字升序。reversed() 只作用于"它前面整个链"
        Comparator<Person> byAgeDescThenName = Comparator.comparing(Person::age, Comparator.nullsLast(Comparator.<Integer>naturalOrder()))
                .reversed()
                .thenComparing(Person::name, String.CASE_INSENSITIVE_ORDER);
        System.out.println("年龄降序再 name（nullsLast 被 reversed 翻成 null 在最前）: " + names(sorted(ps, byAgeDescThenName)));

        // 3. 陷阱：把 reversed() 放在最后，会把 thenComparing 也一起反转
        Comparator<Person> wrong = Comparator.comparing(Person::city)
                .thenComparing(Person::name, String.CASE_INSENSITIVE_ORDER)
                .reversed();
        Comparator<Person> right = Comparator.comparing(Person::city).reversed()
                .thenComparing(Person::name, String.CASE_INSENSITIVE_ORDER);
        System.out.println("city 降序、name 升序（正确）: " + names(sorted(ps, right)));
        System.out.println("reversed 放最后（两个键都反了）: " + names(sorted(ps, wrong)));

        // 4. null 处理：comparing(keyExtractor, keyComparator)，keyComparator 用 nullsFirst/nullsLast 包一层
        Comparator<Person> nullAgeFirst = Comparator.comparing(Person::age, Comparator.nullsFirst(Comparator.naturalOrder()));
        System.out.println("age 升序，null 在最前: " + names(sorted(ps, nullAgeFirst)));
        try { sorted(ps, Comparator.comparing(Person::age)); }
        catch (NullPointerException e) { System.out.println("comparing(Person::age) 遇到 null -> NPE"); }

        // 5. 排序是稳定的（stable）：相等元素保持原来相对顺序（List.sort / Stream.sorted 对对象是稳定的）
        System.out.println("按 city 排序（稳定，同城保持原顺序）: " + names(sorted(ps, Comparator.comparing(Person::city))));

        // 6. 经典 bug：用减法比较
        int a = Integer.MAX_VALUE, b = -1;
        System.out.println("(a - b) = " + (a - b) + ", Integer.compare = " + Integer.compare(a, b));
    }

    static List<Person> sorted(List<Person> in, Comparator<Person> c) { var l = new ArrayList<>(in); l.sort(c); return l; }
    static List<String> names(List<Person> l) { return l.stream().map(Person::name).toList(); }
}
