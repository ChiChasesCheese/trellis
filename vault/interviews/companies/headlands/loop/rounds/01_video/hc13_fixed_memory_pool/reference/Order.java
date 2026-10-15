/** Part 3 的定长记录：8 + 8 + 4 + 4 = 24 字节有效载荷（池里每个槽位另有 8 字节头，共 32 字节）。 */
public record Order(long id, long px, int qty, int side) {
    public static final Order ZERO = new Order(0, 0, 0, 0);
}
