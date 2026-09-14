import random

import pytest

C1 = "customer_id,name,order\nc1,Alice,2\nc2,Bob,1\nc3,Carol,3\n"
P1 = "customer_id,ref,order\nc2,p-200,1\nc1,p-100,2\nc9,p-900,3\n"
EX1_OUT = "customer_id,name,order,customer_id,ref,order\nc2,Bob,1,c2,p-200,1\nc1,Alice,2,c1,p-100,2\n"
EX2_OUT = EX1_OUT + "c3,Carol,3,,,\n"

C3 = 'email,name,order\na@x.com,Ann,1\nb@x.com,"Baker, Bo",2\n'
P3 = "email,charge,order\nb@x.com,ch_3,3\na@x.com,ch_2,2\na@x.com,ch_1,1\n"
EX3_OUT = (
    "email,name,order,email,charge,order\n"
    "a@x.com,Ann,1,a@x.com,ch_1,1\n"
    "a@x.com,Ann,1,a@x.com,ch_2,2\n"
    'b@x.com,"Baker, Bo",2,b@x.com,ch_3,3\n'
)


# ---------------------------------------------------------------- Part 1: inner join
@pytest.mark.part1
def test_example1_inner_join(impl):
    assert impl.join_dataset("customer_id", C1, P1, True) == EX1_OUT
    assert impl.join_dataset("customer_id", C1, P1) == EX1_OUT  # skip_unmatched defaults to True


@pytest.mark.part1
@pytest.mark.edge
def test_header_only_files_give_header_only_output(impl):
    hdr = "customer_id,name,order,customer_id,ref,order\n"
    assert impl.join_dataset("customer_id", "customer_id,name,order\n", P1, True) == hdr
    assert impl.join_dataset("customer_id", "customer_id,name,order\n", P1, False) == hdr
    assert impl.join_dataset("customer_id", "customer_id,name,order", "customer_id,ref,order", True) == hdr
    # no matches at all -> header only
    assert impl.join_dataset("customer_id", C1, "customer_id,ref,order\nzz,p-1,1\n", True) == hdr


@pytest.mark.part1
@pytest.mark.edge
def test_missing_join_column_raises(impl):
    with pytest.raises(ValueError, match="missing join column 'ref'"):
        impl.join_dataset("ref", C1, P1)  # only in the processor file
    with pytest.raises(ValueError, match="missing join column 'name'"):
        impl.join_dataset("name", C1, P1)  # only in the customer file
    with pytest.raises(ValueError, match="missing join column 'customer_id'"):
        impl.join_dataset("customer_id", "", P1)  # empty file has no columns
    with pytest.raises(ValueError, match="missing join column 'Customer_ID'"):
        impl.join_dataset("Customer_ID", C1, P1)  # header names are case-sensitive


@pytest.mark.part1
@pytest.mark.edge
def test_whitespace_around_headers_and_cells(impl):
    c = " customer_id , name , order \n c1 , Alice , 2 \n"
    p = "customer_id ,ref, order\n c1 ,p-100 ,1\n"
    assert impl.join_dataset("customer_id", c, p) == "customer_id,name,order,customer_id,ref,order\nc1,Alice,2,c1,p-100,1\n"


@pytest.mark.part1
@pytest.mark.edge
def test_blank_lines_short_and_long_rows(impl):
    c = "id,name,order\n\nc1,Alice\n   \nc2,Bob,1,EXTRA\n"
    p = "id,ref\nc1,r1\n\nc2,r2\n"
    assert impl.join_dataset("id", c, p) == "id,name,order,id,ref\nc1,Alice,,c1,r1\nc2,Bob,1,c2,r2\n"


@pytest.mark.part1
@pytest.mark.edge
def test_keys_are_case_sensitive_and_exact(impl):
    c = "id,order\nC1,1\nc1,2\n"
    p = "id,ref\nc1,low\n"
    assert impl.join_dataset("id", c, p) == "id,order,id,ref\nc1,2,c1,low\n"


@pytest.mark.part1
@pytest.mark.fmt
def test_order_sorted_numerically_not_as_strings(impl):
    c = "id,order\na,10\nb,2\nc,1\n"
    p = "id,v\na,A\nb,B\nc,C\n"
    assert impl.join_dataset("id", c, p) == "id,order,id,v\nc,1,c,C\nb,2,b,B\na,10,a,A\n"
    # negative and equal orders: ties by customer input position
    c = "id,order\nx,0\ny,-5\nz,0\n"
    p = "id,v\nx,X\ny,Y\nz,Z\n"
    assert impl.join_dataset("id", c, p) == "id,order,id,v\ny,-5,y,Y\nx,0,x,X\nz,0,z,Z\n"


@pytest.mark.part1
@pytest.mark.fmt
def test_order_column_missing_or_non_integer_falls_back_to_position(impl):
    # no order column anywhere: pure input order on both sides
    c = "id,name\nb,Bee\na,Ay\n"
    p = "id,v\na,A2\nb,B1\na,A1\n"
    assert impl.join_dataset("id", c, p) == "id,name,id,v\nb,Bee,b,B1\na,Ay,a,A2\na,Ay,a,A1\n"
    # non-integer order value -> that row uses its input position (row 1 -> key 1)
    c = "id,order\np,5\nq,abc\nr,0\n"
    p = "id,v\np,P\nq,Q\nr,R\n"
    assert impl.join_dataset("id", c, p) == "id,order,id,v\nr,0,r,R\nq,abc,q,Q\np,5,p,P\n"


@pytest.mark.part1
def test_drop_duplicate_key_variant(impl):
    assert impl.join_dataset("customer_id", C1, P1, True, drop_duplicate_key=True) == (
        "customer_id,name,order,ref,order\nc2,Bob,1,p-200,1\nc1,Alice,2,p-100,2\n")


# ---------------------------------------------------------------- Part 2: left join
@pytest.mark.part2
def test_example2_left_join(impl):
    assert impl.join_dataset("customer_id", C1, P1, False) == EX2_OUT


@pytest.mark.part2
def test_example4_header_only_processor_left_join(impl):
    assert impl.join_dataset("id", "id,name,order\n1,Ann,1\n", "id,ref,order\n", False) == "id,name,order,id,ref,order\n1,Ann,1,,,\n"


@pytest.mark.part2
@pytest.mark.edge
def test_left_join_unmatched_rows_get_exactly_one_empty_cell_per_processor_column(impl):
    c = "id,order\nu1,1\n"
    for p_hdr in ("id", "id,a", "id,a,b,c,d"):
        out = impl.join_dataset("id", c, p_hdr + "\n", False)
        assert out == f"id,order,{p_hdr}\nu1,1," + "," * (p_hdr.count(",")) + "\n"
    # unmatched rows keep their place in the customer-order sort among matched rows
    c = "id,order\nm,3\nn,1\no,2\n"
    p = "id,v\nm,M\no,O\n"
    assert impl.join_dataset("id", c, p, False) == "id,order,id,v\nn,1,,\no,2,o,O\nm,3,m,M\n"


# ---------------------------------------------------------------- Part 3: one-to-many
@pytest.mark.part3
def test_example3_one_to_many_with_quoted_comma(impl):
    assert impl.join_dataset("email", C3, P3, True) == EX3_OUT


@pytest.mark.part3
@pytest.mark.edge
def test_duplicate_keys_on_both_sides_join_independently(impl):
    c = "id,name,order\nk,first,2\nk,second,1\n"
    p = "id,v,order\nk,V2,2\nk,V1,1\n"
    assert impl.join_dataset("id", c, p) == (
        "id,name,order,id,v,order\n"
        "k,second,1,k,V1,1\nk,second,1,k,V2,2\n"
        "k,first,2,k,V1,1\nk,first,2,k,V2,2\n")


@pytest.mark.part3
@pytest.mark.fmt
def test_quotes_and_commas_round_trip(impl):
    c = 'id,note\n1,"He said ""hi"", twice"\n'
    p = 'id,ref\n1,"a,b"\n'
    assert impl.join_dataset("id", c, p) == 'id,note,id,ref\n1,"He said ""hi"", twice",1,"a,b"\n'
    # a quoted value without special characters is written back unquoted
    assert impl.join_dataset("id", 'id,n\n1,"plain"\n', "id,r\n1,x\n") == "id,n,id,r\n1,plain,1,x\n"


@pytest.mark.part3
@pytest.mark.edge
def test_processor_order_ties_and_fallback_within_a_match_group(impl):
    c = "id\nk\n"
    p = "id,order\nk,5\nk,5\nk,zz\nk,-1\n"
    # -1, then the two 5s in input order, then 'zz' (non-integer -> position 2)... positions: 0,1,2,3
    # keys: (5,0) (5,1) (2,2) (-1,3) -> sorted: -1, zz, 5, 5
    assert impl.join_dataset("id", c, p) == "id,id,order\nk,k,-1\nk,k,zz\nk,k,5\nk,k,5\n"


# ---------------------------------------------------------------- io / perf
@pytest.mark.part2
@pytest.mark.io
def test_stdin_stdout_exact_and_error_path(run_script):
    r = run_script("JOIN customer_id false\n" + C1 + "---\n" + P1)
    assert r.returncode == 0, r.stderr
    assert r.stdout == EX2_OUT
    r = run_script("JOIN email true\n" + C3 + "---\n" + P3)
    assert r.stdout == EX3_OUT
    r = run_script("JOIN nope true\n" + C1 + "---\n" + P1)
    assert r.returncode == 1
    assert r.stdout == ""
    assert "missing join column 'nope'" in r.stderr
    assert run_script("").stdout == ""


@pytest.mark.part3
@pytest.mark.perf
def test_perf_50k_x_50k_rows(run_script):
    rng = random.Random(0)
    n = 50_000
    keys = [f"cus_{i:06d}" for i in range(n)]
    c_lines = ["customer_id,name,email,order"]
    for i, k in enumerate(keys):
        c_lines.append(f"{k},Name {i},{k}@example.com,{rng.randrange(n)}")
    p_keys = keys[:]
    rng.shuffle(p_keys)
    p_lines = ["customer_id,legacy_ref,amount,order"]
    for i, k in enumerate(p_keys):
        p_lines.append(f'{k},"ref,{i}",{rng.randrange(100000)},{rng.randrange(n)}')
    stdin = "JOIN customer_id true\n" + "\n".join(c_lines) + "\n---\n" + "\n".join(p_lines) + "\n"
    r = run_script(stdin, timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.count("\n") == n + 1  # every customer matched exactly once, plus the header
    assert r.seconds < 2.0, f"too slow: {r.seconds:.2f}s"
    assert r.max_rss_mb < 256, f"too much memory: {r.max_rss_mb:.0f}MB"
