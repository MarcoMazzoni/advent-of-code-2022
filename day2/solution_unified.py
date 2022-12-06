from __future__ import annotations

import abc
import dataclasses
import enum
import time
import typing
from abc import ABC

SHAPE_SCORE_MAPPING: typing.Final[typing.Dict[str, int]] = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3,
}


@enum.unique
class MoveEnum(enum.Enum):
    """
    A: rock
    B: paper
    C: scissors
    """
    A = 1
    B = 2
    C = 3

    @classmethod
    def from_string(cls, i: str) -> 'MoveEnum':
        return MoveEnum(SHAPE_SCORE_MAPPING[i])

    def get_move_that_looses_against_this(self) -> MoveEnum:
        if self == self.A:
            return self.C
        if self == self.B:
            return self.A
        if self == self.C:
            return self.B

    def get_move_that_wins_against_this(self) -> MoveEnum:
        if self == self.A:
            return self.B
        if self == self.B:
            return self.C
        if self == self.C:
            return self.A


MOVE_ENUM_TO_SOLUTION_1: typing.Dict[str, str] = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}


@enum.unique
class GameResult(enum.Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def opposite_outcome(cls, o: GameResult) -> GameResult:
        if o == GameResult.LOSS:
            return GameResult.WIN
        elif o == GameResult.WIN:
            return GameResult.LOSS
        elif o == GameResult.DRAW:
            return GameResult.DRAW
        else:
            raise ValueError(f'There is no opposite value of {o}')


GAME_SCORE_MAPPING_SECOND_PLAYER_SOLUTION_1: typing.Final[typing.Dict[str, GameResult]] = {
    'AX': GameResult.DRAW,
    'BX': GameResult.LOSS,
    'CX': GameResult.WIN,
    'AY': GameResult.WIN,
    'BY': GameResult.DRAW,
    'CY': GameResult.LOSS,
    'AZ': GameResult.LOSS,
    'BZ': GameResult.WIN,
    'CZ': GameResult.DRAW,
}

GAME_SCORE_MAPPING_SECOND_PLAYER_SOLUTION_2: typing.Final[typing.Dict[str, GameResult]] = {
    'X': GameResult.LOSS,
    'Y': GameResult.DRAW,
    'Z': GameResult.WIN,
}


@dataclasses.dataclass
class Game(ABC):
    @classmethod
    @abc.abstractmethod
    def build_from_string(cls, o: str) -> Game: ...

    @property
    @abc.abstractmethod
    def second_move(self) -> MoveEnum: ...

    @abc.abstractmethod
    def to_string(self) -> str: ...

    @abc.abstractmethod
    def compute_score_player_2(self) -> int: ...


@dataclasses.dataclass
class GameSolution2(Game):
    _first_move: MoveEnum
    _outcome: GameResult

    @classmethod
    def build_from_string(cls, o: str) -> Game:
        return GameSolution2(
            _first_move=MoveEnum.from_string(o[0]),
            _outcome=GAME_SCORE_MAPPING_SECOND_PLAYER_SOLUTION_2[o[1]]
        )

    @property
    def second_move(self) -> MoveEnum:
        if self._outcome == GameResult.DRAW:
            return self._first_move
        elif self._outcome == GameResult.LOSS:
            return self._first_move.get_move_that_looses_against_this()
        else:
            return self._first_move.get_move_that_wins_against_this()

    def to_string(self) -> str:
        return self._first_move.name + self._outcome.name

    def compute_score_player_2(self) -> int:
        return self._outcome.value + self.second_move.value


@dataclasses.dataclass
class GameSolution1(Game):
    _first_move: MoveEnum
    _second_move: MoveEnum

    @classmethod
    def build_from_string(cls, o: str) -> 'Game':
        return GameSolution1(
            _first_move=MoveEnum.from_string(o[0]),
            _second_move=MoveEnum.from_string(o[1])
        )

    @property
    def second_move(self) -> MoveEnum:
        return self._second_move

    def to_string(self) -> str:
        return self._first_move.name + MOVE_ENUM_TO_SOLUTION_1[self.second_move.name]

    def compute_score_player_2(self) -> int:
        return GAME_SCORE_MAPPING_SECOND_PLAYER_SOLUTION_1[self.to_string()].value + self.second_move.value


def get_score_solution_1(s: str) -> int:
    res = sum(map(lambda a: GameSolution1.build_from_string(a[:len(s):2]).compute_score_player_2(), s.splitlines()))
    return res


def get_score_solution_2(s: str) -> int:
    res = sum(map(lambda a: GameSolution2.build_from_string(a[:len(s):2]).compute_score_player_2(), s.splitlines()))
    return res


if __name__ == '__main__':
    with open("input.txt") as f:
       inp = f.read()
    score = get_score_solution_1(inp)
    print('Result solution 1:', get_score_solution_1(inp))
    print('Result solution 2:', get_score_solution_2(inp))
