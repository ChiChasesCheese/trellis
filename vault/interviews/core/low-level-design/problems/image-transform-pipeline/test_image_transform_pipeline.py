"""图像变换流水线的 pytest 套件：`-k part1` 选第 1 关，依此类推。"""

import importlib
import os
import random

import pytest

impl = importlib.import_module(os.environ.get("IMPL", "solution"))


def img(rows):
    return impl.Image(rows)


def rows(image):
    return [list(r) for r in image.pixels]


def run(steps, image):
    return rows(impl.Pipeline(steps).apply(image))


A = [[1, 2, 3], [4, 5, 6]]   # 2 行 3 列


# ---- 第 1 关：图像与步骤 ----------------------------------------------------------


def test_part1_image_validation():
    assert img(A).height == 2 and img(A).width == 3
    for bad in ([], [[]], [[1, 2], [3]], [[256]], [[-1]], [[1.5]], [[True]], [["a"]]):
        with pytest.raises(ValueError):
            img(bad)


def test_part1_image_is_a_value_and_cannot_be_mutated():
    a, b = img(A), img([[1, 2, 3], [4, 5, 6]])
    assert a == b and hash(a) == hash(b)
    source = [[1, 2], [3, 4]]
    image = img(source)
    source[0][0] = 99                     # 改调用方自己的列表，不影响图像
    assert rows(image) == [[1, 2], [3, 4]]
    with pytest.raises(TypeError):
        image.pixels[0][0] = 5            # type: ignore[index]


def test_part1_flip():
    assert run([impl.Flip(True)], img(A)) == [[3, 2, 1], [6, 5, 4]]
    assert run([impl.Flip(False)], img(A)) == [[4, 5, 6], [1, 2, 3]]


def test_part1_rotate_clockwise_and_modulo():
    assert run([impl.Rotate(1)], img(A)) == [[4, 1], [5, 2], [6, 3]]
    assert run([impl.Rotate(2)], img(A)) == [[6, 5, 4], [3, 2, 1]]
    assert run([impl.Rotate(3)], img(A)) == [[3, 6], [2, 5], [1, 4]]
    for turns in (0, 4, -4, 8):
        assert run([impl.Rotate(turns)], img(A)) == A
    assert run([impl.Rotate(5)], img(A)) == run([impl.Rotate(1)], img(A))
    assert run([impl.Rotate(-1)], img(A)) == run([impl.Rotate(3)], img(A))


def test_part1_crop():
    big = img([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    assert run([impl.Crop(1, 1, 2, 2)], big) == [[6, 7], [10, 11]]
    assert run([impl.Crop(0, 0, 3, 4)], big) == rows(big)


def test_part1_brighten_clamps_both_ways_and_invert():
    image = img([[0, 100, 250]])
    assert run([impl.Brighten(10)], image) == [[10, 110, 255]]
    assert run([impl.Brighten(-120)], image) == [[0, 0, 130]]
    assert run([impl.Invert()], image) == [[255, 155, 5]]


def test_part1_steps_apply_left_to_right_and_input_is_untouched():
    image = img(A)
    result = impl.Pipeline([impl.Flip(True), impl.Rotate(1)]).apply(image)
    assert rows(result) == [[6, 3], [5, 2], [4, 1]]
    assert rows(image) == A
    assert impl.Pipeline([]).apply(image) == image


def test_part1_step_parameters_are_validated_at_construction():
    for bad in (lambda: impl.Crop(-1, 0, 1, 1), lambda: impl.Crop(0, -1, 1, 1),
                lambda: impl.Crop(0, 0, 0, 1), lambda: impl.Crop(0, 0, 1, 0)):
        with pytest.raises(ValueError):
            bad()


def test_part1_step_failure_names_the_step_and_its_index():
    p = impl.Pipeline([impl.Flip(True), impl.Crop(0, 0, 3, 1), impl.Invert()])
    with pytest.raises(impl.StepError) as info:
        p.apply(img(A))
    assert info.value.index == 1 and info.value.step == impl.Crop(0, 0, 3, 1)
    assert isinstance(info.value, impl.PipelineError)
    with pytest.raises(impl.StepError):
        impl.Pipeline([impl.Crop(1, 1, 1, 3)]).apply(img(A))   # 列超出


# ---- 第 2 关：缩放、组合、尺寸推演 -------------------------------------------------------


def test_part2_resize_nearest_neighbour_up_and_down():
    assert run([impl.Resize(4, 4)], img([[1, 2], [3, 4]])) == [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]]
    assert run([impl.Resize(1, 2)], img([[1, 2, 3, 4]])) == [[1, 3]]
    assert run([impl.Resize(2, 3)], img(A)) == A
    assert run([impl.Resize(3, 2)], img([[1], [2]])) == [[1, 1], [1, 1], [2, 2]]


def test_part2_resize_target_is_validated():
    for h, w in ((0, 3), (3, 0), (-1, 1)):
        with pytest.raises(ValueError):
            impl.Resize(h, w)


def test_part2_order_of_steps_matters():
    image = img([[1, 2, 3, 4], [5, 6, 7, 8]])
    crop_then_resize = run([impl.Crop(0, 0, 2, 2), impl.Resize(2, 4)], image)
    resize_then_crop = run([impl.Resize(2, 8), impl.Crop(0, 0, 2, 2)], image)
    assert crop_then_resize == [[1, 1, 2, 2], [5, 5, 6, 6]]
    assert resize_then_crop == [[1, 1], [5, 5]]
    assert run([impl.Rotate(1), impl.Crop(0, 0, 1, 2)], image) == [[5, 1]]
    assert impl.Pipeline([impl.Rotate(1), impl.Crop(0, 0, 4, 1)]).output_size(2, 4) == (4, 1)
    with pytest.raises(impl.StepError):
        impl.Pipeline([impl.Crop(0, 0, 4, 1), impl.Rotate(1)]).output_size(2, 4)


def test_part2_then_and_add_build_new_pipelines():
    base = impl.Pipeline([impl.Flip(True)])
    longer = base.then(impl.Invert())
    assert len(base) == 1 and len(longer) == 2
    combined = base + impl.Pipeline([impl.Rotate(1), impl.Invert()])
    assert combined.steps == (impl.Flip(True), impl.Rotate(1), impl.Invert())
    assert rows(combined.apply(img(A))) == run([impl.Flip(True), impl.Rotate(1), impl.Invert()], img(A))
    assert impl.Pipeline([impl.Flip(True)]) == base
    assert hash(impl.Pipeline([impl.Flip(True)])) == hash(base)


def test_part2_output_size_agrees_with_apply():
    steps = [impl.Rotate(1), impl.Crop(0, 1, 2, 1), impl.Resize(5, 7), impl.Flip(False), impl.Brighten(9)]
    p = impl.Pipeline(steps)
    out = p.apply(img(A))
    assert p.output_size(2, 3) == (out.height, out.width) == (5, 7)
    assert impl.Pipeline().output_size(4, 5) == (4, 5)


def test_part2_output_size_never_touches_pixels_and_reports_the_failing_step():
    p = impl.Pipeline([impl.Resize(10**6, 10**6), impl.Crop(0, 0, 10**6, 10**6 + 1)])
    with pytest.raises(impl.StepError) as info:
        p.output_size(2, 2)
    assert info.value.index == 1
    assert impl.Pipeline([impl.Resize(10**6, 10**6)]).output_size(2, 2) == (10**6, 10**6)


# ---- 第 3 关：前缀缓存 ------------------------------------------------------------------

S1, S2, S3, S4 = impl.Flip(True), impl.Invert(), impl.Brighten(10), impl.Rotate(1)


def test_part3_second_run_is_served_from_cache_and_matches_apply():
    runner = impl.CachedRunner(10)
    p = impl.Pipeline([S1, S2, S3])
    first = runner.run(p, img(A))
    assert runner.steps_executed == 3
    again = runner.run(p, img(A))
    assert runner.steps_executed == 3
    assert first == again == p.apply(img(A))


def test_part3_a_shared_prefix_is_not_recomputed():
    runner = impl.CachedRunner(10)
    runner.run(impl.Pipeline([S1, S2, S3]), img(A))
    out = runner.run(impl.Pipeline([S1, S2, S4]), img(A))
    assert runner.steps_executed == 4                  # 只多算了 S4
    assert out == impl.Pipeline([S1, S2, S4]).apply(img(A))
    runner.run(impl.Pipeline([S1]), img(A))            # 前缀本身也被缓存了
    assert runner.steps_executed == 4


def test_part3_cache_is_keyed_by_the_image_value():
    runner = impl.CachedRunner(10)
    p = impl.Pipeline([S1, S2])
    runner.run(p, img(A))
    runner.run(p, img([[1, 2, 3], [4, 5, 6]]))         # 内容相同的另一个对象：命中
    assert runner.steps_executed == 2
    runner.run(p, img([[9, 9, 9], [9, 9, 9]]))         # 内容不同：重算
    assert runner.steps_executed == 4


def test_part3_invalid_pipeline_is_rejected_before_any_work():
    runner = impl.CachedRunner(10)
    runner.run(impl.Pipeline([S1]), img(A))
    bad = impl.Pipeline([S1, S2, impl.Crop(0, 0, 9, 9)])
    with pytest.raises(impl.StepError) as info:
        runner.run(bad, img(A))
    assert info.value.index == 2
    assert runner.steps_executed == 1 and runner.cache_size() == 1


def test_part3_lru_eviction_keeps_the_most_recently_used_prefixes():
    runner = impl.CachedRunner(2)
    runner.run(impl.Pipeline([S1, S2, S3]), img(A))
    assert runner.cache_size() == 2 and runner.steps_executed == 3     # 缓存里是 [S1,S2] 和 [S1,S2,S3]
    runner.run(impl.Pipeline([S1, S2, S4]), img(A))                    # 命中 [S1,S2]，只算 S4
    assert runner.steps_executed == 4
    runner.run(impl.Pipeline([S1, S2, S3]), img(A))                    # [S1,S2,S3] 刚被淘汰
    assert runner.steps_executed == 5
    runner.run(impl.Pipeline([S1]), img(A))                            # [S1] 早就被淘汰
    assert runner.steps_executed == 6
    assert runner.cache_size() == 2


def test_part3_a_hit_refreshes_recency():
    runner = impl.CachedRunner(2)
    runner.run(impl.Pipeline([S1]), img(A))
    runner.run(impl.Pipeline([S2]), img(A))
    runner.run(impl.Pipeline([S1]), img(A))        # 刷新 [S1]
    runner.run(impl.Pipeline([S3]), img(A))        # 淘汰最久没用的 [S2]
    before = runner.steps_executed
    runner.run(impl.Pipeline([S1]), img(A))
    assert runner.steps_executed == before
    runner.run(impl.Pipeline([S2]), img(A))
    assert runner.steps_executed == before + 1


def test_part3_empty_pipeline_and_bad_capacity():
    runner = impl.CachedRunner(3)
    assert runner.run(impl.Pipeline(), img(A)) == img(A)
    assert runner.steps_executed == 0 and runner.cache_size() == 0
    with pytest.raises(ValueError):
        impl.CachedRunner(0)


# ---- 第 4 关：化简 ----------------------------------------------------------------------


def simplified(steps):
    return impl.Pipeline(steps).simplified().steps


def test_part4_cancelling_and_merging_pairs():
    assert simplified([impl.Flip(True), impl.Flip(True)]) == ()
    assert simplified([impl.Flip(True), impl.Flip(False)]) == (impl.Flip(True), impl.Flip(False))
    assert simplified([impl.Invert(), impl.Invert(), impl.Invert()]) == (impl.Invert(),)
    assert simplified([impl.Rotate(1), impl.Rotate(2)]) == (impl.Rotate(3),)
    assert simplified([impl.Rotate(1), impl.Rotate(3)]) == ()
    assert simplified([impl.Rotate(4)]) == ()
    assert simplified([impl.Brighten(0)]) == ()


def test_part4_merging_cascades_to_earlier_steps():
    assert simplified([impl.Flip(True), impl.Rotate(1), impl.Rotate(3), impl.Flip(True)]) == ()
    assert simplified([impl.Invert(), impl.Brighten(5), impl.Brighten(-5), impl.Invert()]) == (
        impl.Invert(), impl.Brighten(5), impl.Brighten(-5), impl.Invert())    # 一正一负不合并


def test_part4_same_sign_brighten_merges_but_mixed_sign_does_not():
    assert simplified([impl.Brighten(30), impl.Brighten(40)]) == (impl.Brighten(70),)
    assert simplified([impl.Brighten(-30), impl.Brighten(-40)]) == (impl.Brighten(-70),)
    mixed = [impl.Brighten(200), impl.Brighten(-100)]
    assert simplified(mixed) == tuple(mixed)
    assert impl.Pipeline(mixed).apply(img([[100]])) == img([[155]])       # 先截到 255 再减，不是 200


def test_part4_simplified_is_equivalent_and_idempotent_on_random_pipelines():
    rng = random.Random(7)
    pool = [impl.Flip(True), impl.Flip(False), impl.Rotate(1), impl.Rotate(2), impl.Rotate(3), impl.Invert(),
            impl.Brighten(200), impl.Brighten(-100), impl.Brighten(30), impl.Brighten(-30), impl.Brighten(0),
            impl.Resize(3, 4), impl.Resize(5, 2)]
    for _ in range(300):
        image = img([[rng.randrange(256) for _ in range(5)] for _ in range(4)])
        p = impl.Pipeline([rng.choice(pool) for _ in range(rng.randrange(0, 9))])
        s = p.simplified()
        assert len(s) <= len(p)
        assert s.apply(image) == p.apply(image)
        assert s.simplified() == s


def test_part4_simplified_leaves_the_original_alone():
    p = impl.Pipeline([impl.Flip(True), impl.Flip(True), impl.Invert()])
    s = p.simplified()
    assert len(p) == 3 and s.steps == (impl.Invert(),)
