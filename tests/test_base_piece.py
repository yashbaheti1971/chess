"""
Base test case for all pieces.
"""
from typing import Generator, Optional, Any

import unittest

from engine import Game
from engine.types import (
    Move, PieceType, Location, Piece,
    BLACK, WHITE,  # Colors
    KING,  # PieceTypes
    PASSING,
)


class BaseTestPiece(unittest.TestCase):

    game: Game

    @classmethod
    def setUpClass(cls) -> None:
        cls.game = Game()

    def setUp(self) -> None:
        self.game.reset()
        self.game.board.place_piece((0, 4), (BLACK, KING))
        self.game.board.place_piece((7, 4), (WHITE, KING))

    def assert_generated_moves(
        self, expected: set[Move],
        calculated: Optional[Generator[Move, None, None]] = None,
        piece: Optional[tuple[Piece, Location]] = None
    ) -> None:
        if calculated:
            calculated_set = set(calculated)
        if piece:
            calculated_set = set(calculated or self.game.legal_moves(color=piece[0][0], piece=piece))
        if calculated_set:
            self.assertSetEqual(
                expected, calculated_set,
                msg=f"\nGenerated: {len(calculated_set)} Moves"
                    f"\nMissing {len(expected - calculated_set)} Moves"
                    f"\nExtra {len(calculated_set - expected)} Moves"
            )
        if not piece and not calculated:
            raise ValueError("Must provide either piece or calculated.")

    def moves(
        self,
        start: tuple[int, int],
        end: list[tuple[int, int]],
        **kwds: Any
    ) -> set[Move]:

        return {
            Move(
                Location(*start), Location(*dest),
                type=kwds.get("move_type", PASSING),
                target=kwds.get("target", None),
                castle_type=kwds.get("castle_type", None)
            )
            for dest in end
        }
