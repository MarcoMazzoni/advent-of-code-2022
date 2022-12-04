from __future__ import annotations
import dataclasses
import enum
import time
import typing

SHAPE_SCORE_MAPPING: typing.Final[typing.Dict[str, int]] = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3,
}


@enum.unique
class FirstMoveEnum(enum.Enum):
    """
    A: rock
    B: paper
    C: scissors
    """
    A = 1
    B = 2
    C = 3

    @classmethod
    def from_string(cls, i: str) -> 'FirstMoveEnum':
        return FirstMoveEnum(SHAPE_SCORE_MAPPING[i])


@enum.unique
class SecondMoveEnum(enum.Enum):
    X = 1
    Y = 2
    Z = 3

    @classmethod
    def from_string(cls, i: str) -> 'SecondMoveEnum':
        return SecondMoveEnum(SHAPE_SCORE_MAPPING[i])


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


GAME_SCORE_MAPPING_FIRST_PLAYER: typing.Final[typing.Dict[str, GameResult]] = {
    'AX': GameResult.DRAW,
    'BX': GameResult.WIN,
    'CX': GameResult.LOSS,
    'AY': GameResult.LOSS,
    'BY': GameResult.DRAW,
    'CY': GameResult.WIN,
    'AZ': GameResult.WIN,
    'BZ': GameResult.LOSS,
    'CZ': GameResult.DRAW,
}

GAME_SCORE_MAPPING_SECOND_PLAYER: typing.Final[typing.Dict[str, GameResult]] = {
    k: GameResult.opposite_outcome(v) for k, v in GAME_SCORE_MAPPING_FIRST_PLAYER.items()
}


@dataclasses.dataclass
class Game:
    _first_move: FirstMoveEnum
    _second_move: SecondMoveEnum

    @classmethod
    def build_from_string(cls, o: str) -> 'Game':
        return Game(
            _first_move=FirstMoveEnum.from_string(o[0]),
            _second_move=SecondMoveEnum.from_string(o[1])
        )

    def to_string(self) -> str:
        return self._first_move.name + self._second_move.name

    def compute_score_player_1(self) -> int:
        return GAME_SCORE_MAPPING_FIRST_PLAYER[self.to_string()].value + self._first_move.value

    def compute_score_player_2(self) -> int:
        return GAME_SCORE_MAPPING_SECOND_PLAYER[self.to_string()].value + self._second_move.value


def get_score(s: str) -> int:
    res = 0
    for i, curr_char in enumerate(s):
        if curr_char == '\n':
            res += Game.build_from_string(s[(i - 3):i:2]).compute_score_player_2()

    return res


if __name__ == '__main__':
    with open("input.txt") as f:
       inp = f.read()
    start = time.time_ns()
    score = get_score(inp)
    print(f'Score computation took: {(time.time_ns() - start) // 1_000_000} ms')
    print('Result:', score)
