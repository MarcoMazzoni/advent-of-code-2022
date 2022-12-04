from __future__ import annotations
import dataclasses
import enum
import time
import typing

SHAPE_SCORE_MAPPING: typing.Final[typing.Dict[str, int]] = {
    'A': 1,
    'B': 2,
    'C': 3
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


GAME_SCORE_MAPPING_SECOND_PLAYER: typing.Final[typing.Dict[str, GameResult]] = {
    'X': GameResult.LOSS,
    'Y': GameResult.DRAW,
    'Z': GameResult.WIN,
}

GAME_SCORE_MAPPING_FIRST_PLAYER: typing.Final[typing.Dict[str, GameResult]] = {
    k: GameResult.opposite_outcome(v) for k, v in GAME_SCORE_MAPPING_SECOND_PLAYER.items()
}


@dataclasses.dataclass
class Game:
    _first_move: MoveEnum
    _outcome: GameResult

    @classmethod
    def build_from_string(cls, o: str) -> 'Game':
        return Game(
            _first_move=MoveEnum.from_string(o[0]),
            _outcome=GAME_SCORE_MAPPING_SECOND_PLAYER[o[1]]
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
