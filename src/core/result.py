from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Callable, Generic

A = TypeVar('A')
B = TypeVar('B')
E = TypeVar('E')


@dataclass(frozen=True)
class Ok(Generic[A]):
    value: A

    def map(self, f: Callable[[A], B]) -> Ok[B]:
        return Ok(f(self.value))

    def bind(self, f: Callable[[A], Ok[B] | Err]) -> Ok[B] | Err:
        return f(self.value)

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def unwrap(self) -> A:
        return self.value

    def unwrap_or(self, default: A) -> A:
        return self.value


@dataclass(frozen=True)
class Err(Generic[E]):
    reason: E

    def map(self, f) -> Err[E]:
        return self

    def bind(self, f) -> Err[E]:
        return self

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def unwrap(self):
        raise ValueError(f"Called unwrap on Err: {self.reason}")

    def unwrap_or(self, default):
        return default


Result = Ok | Err


def sequence(results):
    values = []
    for r in results:
        if r.is_err():
            return r
        values.append(r.value)
    return Ok(values)


def filter_ok(results):
    return (r.value for r in results if r.is_ok())


def partition_results(results):
    oks, errs = [], []
    for r in results:
        (oks if r.is_ok() else errs).append(r.value if r.is_ok() else r.reason)
    return oks, errs
