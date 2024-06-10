"""
Contains util to deal with parametrized tuple operations, some of those are
probably significantly slower than the normal implementation and should be
inlined as needed, just using them for prototyping as they improve readability
and require less typing while still doing defensive programming checks.

Also note that becaus tuples are immutable data structures it might be better
to use lists if we want to modify them often and don't iterate over them often.
"""

from typing import Optional, TypeVar

T = TypeVar("T", int, float)


def tuple_op_check(*tuples: tuple[T, ...]) -> None:
    assert len(tuples) > 0

    length_of_first: int = len(tuples[0])
    assert isinstance(tuples[0], tuple)

    for tuple_ in tuples[1:]:
        assert isinstance(tuple_, tuple)
        assert len(tuple_) == length_of_first


def tuple_sum(*tuples: tuple[T, ...]) -> tuple[T]:
    return tuple(sum(elements) for elements in zip(*tuples))


def tuple_sub(x: tuple, y: tuple) -> tuple:
    tuple_op_check(x, y)
    return tuple(xp - yp for xp, yp in zip(x, y))


def tuple_prod(*tuples: tuple[T, ...]) -> tuple[T, ...]:
    tuple_op_check(*tuples)
    # result = (1, 1, 1, ...)
    result = tuple(1 for _ in range(len(tuples[0])))
    for tuple_ in tuples:
        # result * tuples[i] -> (result[0] * tuples[i][0], ...)
        result = tuple(res * tp for res, tp in zip(result, tuple_))
    return result


def tuple_scale(tuple_: tuple[T], scaling_factor: T) -> tuple[T]:
    return tuple(tp * scaling_factor for tp in tuple_)


def tuple_div(x: tuple[float], y: tuple[float]) -> tuple[float]:
    tuple_op_check(x, y)
    return tuple(xp / yp for xp, yp in zip(x, y))


def tuple_div_safe(x: tuple[float], y: tuple[float]) -> Optional[tuple[float]]:
    try:
        tuple_div(x, y)
    except ZeroDivisionError:
        return None


def tuple_leq(x: tuple, y: tuple) -> bool:
    tuple_op_check(x, y)
    return all(xp <= yp for (xp, yp) in zip(x, y))


def tuple_less(x: tuple, y: tuple) -> bool:
    tuple_op_check(x, y)
    return all(xp < yp for (xp, yp) in zip(x, y))


def tuple_geq(x: tuple[T, ...], y: tuple[T, ...]) -> bool:
    tuple_op_check(x, y)
    return all(xp >= yp for (xp, yp) in zip(x, y))


def tuple_greater(x: tuple[T, ...], y: tuple[T, ...]) -> bool:
    tuple_op_check(x, y)
    return all(xp > yp for (xp, yp) in zip(x, y))


def tuple_eq(x: tuple[T, ...], y: tuple[T, ...]) -> bool:
    tuple_op_check(x, y)
    return all(xp == yp for (xp, yp) in zip(x, y))


def tuple_neq(x: tuple[T, ...], y: tuple[T, ...]) -> bool:
    tuple_op_check(x, y)
    return any(xp != yp for (xp, yp) in zip(x, y))
