from typing import List, TypeVar, Union, Dict, Callable, Tuple, Any, NewType
from numpy.typing import NDArray
from tensorflow import Tensor


V = TypeVar("V")
Matrix = NDArray[V]
Vector = NDArray[V]


def check_vector(v: NDArray) -> None:
    assert v.ndim == 1, "Input must be a 1D array"


def check_matrix(v: NDArray) -> None:
    assert v.ndim == 2, "Input must be a 2D array"
