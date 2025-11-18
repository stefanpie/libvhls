from typing import TypeVar

T_unwrap = TypeVar("T_unwrap")


def unwrap[T_unwrap](value: T_unwrap | None, message: str | None = None) -> T_unwrap:
    if value is None:
        if message is None:
            raise ValueError("Unwrapped a None value")
        else:
            raise ValueError(f"Unwrapped a None value:\n{message}")
    return value
