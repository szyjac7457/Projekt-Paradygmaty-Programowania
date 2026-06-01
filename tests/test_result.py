import pytest
from src.core.result import Ok, Err, filter_ok, partition_results


def double(x):
    return x * 2

def to_ok_double(x):
    return Ok(x * 2)

def to_err(_):
    return Err("forced error")


class TestOk:
    def test_is_ok(self):
        assert Ok(1).is_ok() is True

    def test_is_err(self):
        assert Ok(1).is_err() is False

    def test_unwrap(self):
        assert Ok(42).unwrap() == 42

    def test_unwrap_or(self):
        assert Ok(42).unwrap_or(0) == 42

    def test_map(self):
        assert Ok(3).map(double) == Ok(6)

    def test_map_preserves_type(self):
        assert Ok("hello").map(str.upper) == Ok("HELLO")

    def test_bind_ok(self):
        assert Ok(3).bind(to_ok_double) == Ok(6)

    def test_bind_to_err(self):
        assert Ok(3).bind(to_err) == Err("forced error")


class TestErr:
    def test_is_ok(self):
        assert Err("bad").is_ok() is False

    def test_is_err(self):
        assert Err("bad").is_err() is True

    def test_unwrap_raises(self):
        with pytest.raises(ValueError):
            Err("bad").unwrap()

    def test_unwrap_or(self):
        assert Err("bad").unwrap_or(99) == 99

    def test_map_passthrough(self):
        err = Err("oops")
        assert err.map(double) is err

    def test_bind_passthrough(self):
        err = Err("oops")
        assert err.bind(to_ok_double) is err


class TestMonadLaws:
    """
    Left identity:  Ok(a).bind(f)       == f(a)
    Right identity: m.bind(Ok)          == m
    Associativity:  m.bind(f).bind(g)   == m.bind(lambda x: f(x).bind(g))
    """

    def test_left_identity(self):
        a = 5
        f = to_ok_double
        assert Ok(a).bind(f) == f(a)

    def test_right_identity(self):
        m = Ok(7)
        assert m.bind(Ok) == m

    def test_associativity(self):
        m = Ok(3)
        f = to_ok_double
        g = lambda x: Ok(x + 1)
        lhs = m.bind(f).bind(g)
        rhs = m.bind(lambda x: f(x).bind(g))
        assert lhs == rhs

    def test_left_identity_err(self):
        err = Err("e")
        assert err.bind(to_ok_double) == err

    def test_right_identity_err(self):
        err = Err("e")
        assert err.bind(Ok) == err

    def test_associativity_err(self):
        err = Err("e")
        f = to_ok_double
        g = lambda x: Ok(x + 1)
        assert err.bind(f).bind(g) == err.bind(lambda x: f(x).bind(g))


class TestHelpers:
    def test_filter_ok_basic(self):
        results = [Ok(1), Err("x"), Ok(2), Err("y"), Ok(3)]
        assert list(filter_ok(results)) == [1, 2, 3]

    def test_filter_ok_all_err(self):
        assert list(filter_ok([Err("a"), Err("b")])) == []

    def test_filter_ok_is_lazy(self):
        results = (Ok(i) for i in range(5))
        gen = filter_ok(results)
        assert next(gen) == 0

    def test_partition_results(self):
        results = [Ok(1), Err("bad"), Ok(2), Err("worse")]
        oks, errs = partition_results(results)
        assert oks == [1, 2]
        assert errs == ["bad", "worse"]

    def test_partition_all_ok(self):
        oks, errs = partition_results([Ok(1), Ok(2)])
        assert oks == [1, 2]
        assert errs == []

    def test_partition_all_err(self):
        oks, errs = partition_results([Err("a"), Err("b")])
        assert oks == []
        assert errs == ["a", "b"]
