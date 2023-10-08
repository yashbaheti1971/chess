"""
Board Class
"""

from itertools import product
from typing import Union, overload, Optional

import numpy as np
import numpy.typing as npt

from engine.constants import BOARD_SIZE, UNICODE_PIECES, UNICODE_SQUARE
from engine.types import Color, Piece, PieceType, Location

PieceLocation = tuple[Piece, Location]

class Board:
    """
    Board.board is an 8x8 matrix of squares.
    Values stored in a square are:
        0: Piece Color
        1: Piece Type
        2: Whether the piece has moved
        3: Whether the square is occupied
    """
    def __init__(self) -> None:
        self.board: npt.NDArray[np.int8] = np.full(
            shape=(BOARD_SIZE, BOARD_SIZE, 4), fill_value=0, dtype=np.int8
        )

    def place_piece(self, location: tuple[int, int], piece: tuple[Color, PieceType]) -> PieceLocation:
        if self.board[location[0], location[1], 3] != 0:
            raise ValueError(f"{location} already occupied.")
        self.board[location] = np.array([piece[0], piece[1], 0, 1], dtype=np.int8)
        return (Piece(*piece), Location(*location))

    def remove_piece(self, location: tuple[int, int]) -> None:
        self.board[location[0], location[1], 3] = 0  # Mark square as unoccupied

    def promote_piece(self, location: tuple[int, int], rank: PieceType) -> None:
        self.board[location[0], location[1], 1] = rank

    def move_piece(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.board[end] = self.board[start]
        self.board[start[0], start[1], 3] = 0  # Mark square as unoccupied
        self.board[end[0], end[1], 2] = 1  # Mark piece as moved

    def get_piece(self, loc: tuple[int, int]) -> Piece:
        if self.board[loc[0], loc[1], 3] == 0:
            raise ValueError(f"No piece at {(loc[0], loc[1])}")
        return Piece(
            Color(self.board[loc[0], loc[1], 0]),
            PieceType(self.board[loc[0], loc[1], 1])
        )

    def get_pieces(self, color: Optional[Color] = None) -> set[PieceLocation]:
        if not color:
            locations = np.argwhere(self.board[:, :, 3] == 1)
        else:
            locations = np.argwhere(
                (self.board[:, :, 0] == color.value) & (self.board[:, :, 3] == 1)
            )
        return {(self.get_piece(loc), Location(*loc)) for loc in locations}

    def clear(self) -> None:
        self.board.fill(0)

    @staticmethod
    def is_in_bounds(location: tuple[int, int]) -> bool:
        return 0 <= location[0] < BOARD_SIZE and 0 <= location[1] < BOARD_SIZE

    @overload
    def __getitem__(self, index: tuple[int, int]) -> npt.NDArray[np.int8]: ...
    @overload
    def __getitem__(
        self, index: tuple[Union[int, slice], Union[int, slice], int]
    ) -> npt.NDArray[np.int8]: ...
    def __getitem__(
        self,
        index: Union[tuple[int, int], tuple[Union[int, slice], Union[int, slice], int]]
    ) -> npt.NDArray[np.int8]:
        if 2 <= len(index) <= 3:
            return self.board.__getitem__((*index, Ellipsis))
        raise IndexError(f"Invalid index {index} for Board.")

    @overload
    def __setitem__(
        self, index: tuple[int, int], value: Union[npt.NDArray[np.int8], int]
    ) -> None: ...
    @overload
    def __setitem__(self, index: tuple[int, int, int], value: int) -> None: ...
    def __setitem__(
        self, index: tuple[int, ...], value: Union[npt.NDArray[np.int8], int]
    ) -> None:
        if 2 <= len(index) <= 3:
            self.board.__setitem__(index, value)
        else:
            raise IndexError(f"Invalid index {index} for Board.")

    def __str__(self) -> str:
        visual: str = ""
        for i, j in product(range(BOARD_SIZE), range(BOARD_SIZE)):
            if self.board[i, j, 3]:
                piece = self.get_piece((i, j))
                visual += f" {UNICODE_PIECES[piece.type][piece.color]} "
            else:
                square_color = Color.BLACK if (i % 2 == 0) ^ (j % 2 == 0) else Color.WHITE
                visual += f" {UNICODE_SQUARE[square_color]} "
            if j == BOARD_SIZE - 1:
                visual += "\n"
        return visual

    __repr__ = __str__
